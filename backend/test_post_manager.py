import sys
import sqlite3
import subprocess
import unittest
import os
from pathlib import Path

# Use DATABASE_URL if set (from CI), otherwise use default
DB_PATH = Path(os.getenv("DATABASE_URL", "sqlite:///social-media-database.db").replace("sqlite:///", ""))


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
