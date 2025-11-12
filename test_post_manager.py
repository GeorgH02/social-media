import os
import sys
import sqlite3
import subprocess
import unittest
from pathlib import Path

DB_PATH = Path("social-media-database.db")

class TestPostManagerScript(unittest.TestCase):
    def setUp(self):
        if DB_PATH.exists():
            DB_PATH.unlink()

    def test_script_runs_and_prints_latest(self):
        result = subprocess.run(
            [sys.executable, "post_manager.py"],
            capture_output=True,
            text=True
        )

        print("\n--- STDOUT ---\n" + result.stdout)
        if result.stderr:
            print("\n--- STDERR ---\n" + result.stderr)

        self.assertEqual(result.returncode, 0, msg=result.stderr)

        out = result.stdout
        self.assertIn("Latest Post:", out)
        self.assertIn("User: jessica184", out)
        self.assertIn("Text: Cute dog alert", out)
        self.assertIn("Image: https://example.com/dog.jpg", out)


        self.assertTrue(DB_PATH.exists())
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM post;")
            count = cur.fetchone()[0]
            self.assertEqual(count, 3)

if __name__ == "__main__":
    unittest.main()
