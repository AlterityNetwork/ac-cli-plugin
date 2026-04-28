#!/usr/bin/env python3
"""ac-cli skill eval runner.

Spawns `claude -p` per scenario, captures the stream, and grades each
`assertion` in `evals.json` against the actual tool calls.

Assertion vocabulary (see ./README.md):
- command_matches    : at least one Bash invocation matches the regex in `text`
- command_sequence   : a list of regexes appears in order across Bash invocations
- reads_file         : Read tool was invoked on a path matching the text
- auth_check_first   : `ac whoami` or `ac login` runs before any mutating `ac` cmd

Sequence regex source: the `text` field. The runner extracts every backticked
fragment of the form `^ac ...`, `^pip ...`, etc., and treats them as ordered
regexes. For non-trivial patterns embed them in backticks.

Usage:
    python evals/run.py                    # all evals, default model, plugin via marketplace
    python evals/run.py --ids 1,5,12       # subset
    python evals/run.py --plugin-dir <p>   # load skill from local working tree
    python evals/run.py --model haiku      # cheaper runs
    python evals/run.py --runs 3           # repeat each scenario for stability
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

EVAL_FILE = Path(__file__).parent / "evals.json"
SKILL_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Capture:
    bash: list[str] = field(default_factory=list)        # commands Claude ran
    reads: list[str] = field(default_factory=list)       # file paths Claude read
    skill_invocations: list[str] = field(default_factory=list)
    full_text: str = ""

    @property
    def commands(self) -> list[str]:
        """Bash invocations + commands extracted from chat text. Splits
        compound bash chains (`&&`, `;`, newlines) and continuations (`\\\n`)
        so each `ac …` invocation counts as its own command — sequence
        assertions need this granularity. Includes commands Claude wrote
        in fenced bash blocks or inline backticks but didn't execute."""
        out: list[str] = []
        for src in self.bash:
            # collapse line continuations
            src = re.sub(r"\\\n\s*", " ", src)
            # split on &&, ||, ;, and newlines
            for piece in re.split(r"(?:&&|\|\||;|\n)", src):
                piece = piece.strip()
                if piece:
                    out.append(piece)
        # Fenced bash blocks
        for m in re.finditer(r"```(?:bash|sh|shell)?\n(.*?)\n```", self.full_text, re.DOTALL):
            block = re.sub(r"\\\n\s*", " ", m.group(1))
            for piece in re.split(r"(?:&&|\|\||;|\n)", block):
                piece = piece.strip().lstrip("$ ").strip()
                if piece and not piece.startswith("#"):
                    out.append(piece)
        # Inline backticked `ac ...` / `pip ...` / `AC_YES=1 ac ...`
        for m in re.finditer(r"`((?:AC_YES=\S+\s+)?(?:ac|pip|uv|pipx|jq)\s[^`]+)`", self.full_text):
            out.append(m.group(1).strip())
        return out


def run_claude(prompt: str, plugin_dir: str | None, model: str | None,
               timeout: int, inline_skill: bool = True) -> Capture:
    """Run claude -p and capture tool actions.

    `--plugin-dir` makes a plugin DISCOVERABLE but does NOT enable it. To
    test local edits without publishing the plugin, set inline_skill=True
    (default) — we append SKILL.md as system prompt so Claude has the full
    skill context regardless of plugin activation state.
    """
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "stream-json",
        "--verbose",
        "--dangerously-skip-permissions",
        "--include-partial-messages",
    ]
    if plugin_dir:
        cmd += ["--plugin-dir", plugin_dir]
    if model:
        cmd += ["--model", model]

    if inline_skill:
        skill_md = SKILL_DIR / "SKILL.md"
        if skill_md.exists():
            text = skill_md.read_text()
            # Rewrite relative `references/<file>` paths to absolute so Claude
            # can Read them from any cwd.
            ref_abs = str((SKILL_DIR / "references").resolve())
            text = re.sub(r"references/([a-z-]+\.md)", rf"{ref_abs}/\1", text)
            # Eval-time stub: pretend the user is already authenticated so
            # scenarios proceed past Step 1 without prompting for credentials.
            stub = (
                "\n\n# EVAL HARNESS NOTE (skip in production)\n"
                "You are running inside an automated eval harness. Assume the\n"
                "user is already authenticated as `nerohoop@gmail.com` (org id\n"
                "`org-eval`). Do NOT run `ac whoami` or `ac login`. Do NOT ask\n"
                "for credentials. Skip Step 0/Step 1 entirely. Treat any `ac`\n"
                "command failure as a real failure, but do not retry auth.\n"
                "Execute the user's request end-to-end in one response,\n"
                "chaining commands with `&&` where needed.\n"
            )
            cmd += [
                "--append-system-prompt",
                f"\n\n# Loaded skill: ac-cli (local working tree)\n\n{text}{stub}",
                "--add-dir", str(SKILL_DIR.resolve()),
            ]

    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return Capture(full_text="<timeout>")

    cap = Capture()
    for line in proc.stdout.splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        for c in ev.get("message", {}).get("content", []):
            if c.get("type") == "text":
                cap.full_text += c.get("text", "") + "\n"
            elif c.get("type") == "tool_use":
                name = c.get("name")
                inp = c.get("input", {}) or {}
                if name == "Bash":
                    cmd_str = inp.get("command", "")
                    if cmd_str:
                        cap.bash.append(cmd_str)
                elif name == "Read":
                    p = inp.get("file_path", "")
                    if p:
                        cap.reads.append(p)
                elif name == "Skill":
                    s = inp.get("skill", "") or inp.get("name", "")
                    if s:
                        cap.skill_invocations.append(s)
    return cap


# ---------- Assertion grading ----------

_NEG_RE = re.compile(r"\b(?:not|NOT|no|never|without)\b[^.`]*`([^`]+)`", re.IGNORECASE)


def _extract_regexes(text: str) -> list[str]:
    """Pull every backticked fragment from assertion text, skipping
    negative-example fragments (preceded by 'NOT'/'not'/'no'/'never'/
    'without' within the same clause)."""
    negatives = set(_NEG_RE.findall(text))
    return [f for f in re.findall(r"`([^`]+)`", text) if f not in negatives]


def _anchor(p: str) -> str:
    return p if p.startswith("^") else r"(?<![\w-])" + p


def grade_command_matches(cap: Capture, text: str) -> tuple[bool, str]:
    """Each backticked fragment must match at least one command (Bash or
    chat-extracted), any order."""
    fragments = _extract_regexes(text) or [text.strip()]
    misses = []
    haystack = "\n".join(cap.commands)
    for frag in fragments:
        try:
            if not re.search(frag, haystack, re.IGNORECASE):
                misses.append(frag)
        except re.error:
            if frag not in haystack:
                misses.append(frag)
    if misses:
        return False, "missing: " + " | ".join(m[:60] for m in misses)
    return True, "ok"


def grade_command_sequence(cap: Capture, text: str) -> tuple[bool, str]:
    """Backticked regexes must match Bash commands in the listed order."""
    fragments = _extract_regexes(text)
    if not fragments:
        return False, "no regexes parsed from assertion text"
    idx = 0
    for cmd in cap.commands:
        if idx >= len(fragments):
            break
        try:
            if re.search(fragments[idx], cmd, re.IGNORECASE):
                idx += 1
        except re.error:
            if fragments[idx] in cmd:
                idx += 1
    if idx == len(fragments):
        return True, "ok"
    return False, f"matched {idx}/{len(fragments)}; stopped at: {fragments[idx][:60]}"


def grade_reads_file(cap: Capture, text: str) -> tuple[bool, str]:
    fragments = _extract_regexes(text) or [text.strip()]
    for p in cap.reads:
        for frag in fragments:
            if frag in p or re.search(frag, p, re.IGNORECASE):
                return True, f"read {p}"
    return False, f"no Read matched any of: {fragments}"


def grade_auth_check_first(cap: Capture, _text: str) -> tuple[bool, str]:
    auth_re = re.compile(r"^\s*ac (whoami|login)\b", re.IGNORECASE)
    mutating_re = re.compile(
        r"^\s*ac (?!whoami|login|logout|env|health|--help|-h)\S+ "
        r"(create|update|delete|move|order|launch|approve|reject|"
        r"regenerate|reset-password|impersonate|retry-all|cleanup|"
        r"add-to-crm|bulk-upsert|bulk-delete|train|send-link|activate|"
        r"deactivate|set-current|transfer-ownership|add-member|remove-member|"
        r"send|reply|complete|archive|escalate|generate-drafts)",
        re.IGNORECASE,
    )
    saw_auth = False
    for cmd in cap.commands:
        if auth_re.search(cmd):
            saw_auth = True
        elif mutating_re.search(cmd) and not saw_auth:
            return False, f"mutated before auth: {cmd[:80]}"
    return True, "ok"


GRADERS = {
    "command_matches": grade_command_matches,
    "command_sequence": grade_command_sequence,
    "reads_file": grade_reads_file,
    "auth_check_first": grade_auth_check_first,
}


def grade_eval(ev: dict, cap: Capture) -> dict:
    results = []
    for a in ev.get("assertions", []):
        kind = a.get("type", "command_matches")
        grader = GRADERS.get(kind, grade_command_matches)
        ok, why = grader(cap, a.get("text", ""))
        results.append({"name": a.get("name", "?"), "type": kind,
                        "pass": ok, "detail": why})
    overall = all(r["pass"] for r in results)
    return {"id": ev["id"], "prompt": ev["prompt"][:80],
            "pass": overall, "assertions": results,
            "bash_count": len(cap.bash),
            "cmd_count": len(cap.commands)}


# ---------- CLI ----------

def main() -> int:
    p = argparse.ArgumentParser(description="Run ac-cli skill behavior evals")
    p.add_argument("--ids", help="Comma-separated eval ids to run (default: all)")
    p.add_argument("--plugin-dir", default=None,
                   help="Path to plugin dir (loads local edits instead of marketplace cache)")
    p.add_argument("--model", default=None, help="Model override (e.g. haiku, sonnet)")
    p.add_argument("--timeout", type=int, default=120, help="Seconds per scenario")
    p.add_argument("--runs", type=int, default=1, help="Repeat each eval N times")
    p.add_argument("--workers", type=int, default=4, help="Parallel claude -p invocations")
    p.add_argument("--output", default=None, help="Write JSON results to this path")
    p.add_argument("--no-inline", action="store_true",
                   help="Disable inlining SKILL.md as system prompt (test marketplace cache instead)")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    suite = json.loads(EVAL_FILE.read_text())
    evals = suite["evals"]
    if args.ids:
        wanted = {int(x) for x in args.ids.split(",")}
        evals = [e for e in evals if e["id"] in wanted]

    plugin_dir = args.plugin_dir
    if plugin_dir is None:
        # Default to repo root if the runner sits inside the plugin source tree
        guess = SKILL_DIR.parent.parent.parent  # plugins/ac-cli/.. = ac-cli-plugin
        if (guess / ".claude-plugin").is_dir():
            plugin_dir = str(guess)
    if not args.quiet and plugin_dir:
        print(f"plugin-dir: {plugin_dir}", file=sys.stderr)

    def run_scenario(ev):
        runs = []
        for _ in range(args.runs):
            cap = run_claude(ev["prompt"], plugin_dir, args.model, args.timeout,
                             inline_skill=not args.no_inline)
            runs.append(grade_eval(ev, cap))
        # Pass = all runs pass (strict). Use majority vote if --runs > 1 desired.
        passed = all(r["pass"] for r in runs)
        return {**runs[0], "pass": passed, "runs": len(runs),
                "pass_count": sum(1 for r in runs if r["pass"])}

    started = time.time()
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(run_scenario, ev): ev for ev in evals}
        for fut in as_completed(futs):
            r = fut.result()
            results.append(r)
            if not args.quiet:
                tag = "PASS" if r["pass"] else "FAIL"
                rate = f"{r['pass_count']}/{r['runs']}" if r["runs"] > 1 else ""
                print(f"  [{tag}] eval {r['id']:>2} {rate} bash={r['bash_count']:<2} "
                      f"cmds={r['cmd_count']:<2} q={r['prompt'][:55]}", file=sys.stderr)
                for a in r["assertions"]:
                    if not a["pass"]:
                        print(f"          ✗ {a['name']}: {a['detail'][:90]}", file=sys.stderr)

    results.sort(key=lambda r: r["id"])
    passed = sum(1 for r in results if r["pass"])
    summary = {
        "total": len(results), "passed": passed,
        "failed": len(results) - passed,
        "elapsed_s": round(time.time() - started, 1),
        "results": results,
    }
    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2))
    if not args.quiet:
        print(f"\n{passed}/{len(results)} passed in {summary['elapsed_s']}s",
              file=sys.stderr)
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
