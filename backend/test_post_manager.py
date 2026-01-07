import sys
import sqlite3
import subprocess
import unittest
from pathlib import Path

DB_PATH = Path("social-media-database.db")


class TestPostManagerScript(unittest.TestCase):
    def setUp(self):
        if DB_PATH.exists():
            try:
                DB_PATH.unlink()
            except PermissionError:
                pass

    def test_script_runs_and_prints_latest(self):
        result = subprocess.run(
            [sys.executable, "class_manager.py"],
            capture_output=True,
            text=True
        )

        print("\n--- STDOUT ---\n" + result.stdout)
        if result.stderr:
            print("\n--- STDERR ---\n" + result.stderr)

        self.assertEqual(result.returncode, 0, msg=result.stderr)

        out = result.stdout
        self.assertIn("Latest Post:", out)
        self.assertRegex(out, r"(?m)^User:\s+.+$")
        self.assertRegex(out, r"(?m)^Text:\s+.+$")
        self.assertRegex(out, r"(?m)^Image:\s+https?://\S+$")

        self.assertTrue(DB_PATH.exists())
        with sqlite3.connect(DB_PATH) as conn:
            pass
