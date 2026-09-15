"""Regression checks for authentication in Copilot settings evaluations."""
import subprocess
import unittest
from unittest.mock import patch

import run


class SettingsAuthTests(unittest.TestCase):
    def test_settings_writes_require_prior_auth(self):
        for command in (
            'ac settings targeting set --profiles-file /tmp/icps.json --json',
            'ac settings framework set --content-file /tmp/framework.md',
            'ac settings framework publish',
        ):
            with self.subTest(command=command):
                self.assertFalse(run.grade_auth_check_first(run.Capture(bash=[command]), '')[0])
                self.assertFalse(run.grade_auth_check_first(run.Capture(bash=[command, 'ac whoami']), '')[0])
                self.assertTrue(run.grade_auth_check_first(run.Capture(bash=['ac whoami && ' + command]), '')[0])

    def test_proposed_auth_does_not_count_as_executed_auth(self):
        cap = run.Capture(bash=['ac settings targeting set --profiles-file /tmp/icps.json'],
                          full_text='First run `ac whoami`.')
        self.assertFalse(run.grade_auth_check_first(cap, '')[0])

    def test_read_only_settings_do_not_require_auth_assertion(self):
        self.assertTrue(run.grade_auth_check_first(run.Capture(bash=['ac settings targeting get']), '')[0])

    @patch.object(run.subprocess, 'run')
    def test_auth_eval_harness_permits_whoami(self, execute):
        execute.return_value = subprocess.CompletedProcess([], 0, stdout='', stderr='')
        run.run_claude('Replace targeting profiles', None, None, 10, require_auth_check=True)
        args = execute.call_args.args[0]
        prompt = args[args.index('--append-system-prompt') + 1]
        self.assertIn('Run `ac whoami` before any mutation', prompt)
        self.assertNotIn('Do NOT run `ac whoami`', prompt)


if __name__ == '__main__':
    unittest.main()
