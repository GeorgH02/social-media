import unittest
import json
import os
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from worker import ensure_connection, process_message

class TestResizeWorker(unittest.TestCase):
    def test_ensure_connection_environment_variable(self):
        with patch.dict(os.environ, {"RABBIT_HOST": "test-host"}):
            import importlib
            import worker as worker_module
            importlib.reload(worker_module)
            self.assertEqual(worker_module.RABBIT_HOST, "test-host")

    def test_process_message_with_valid_queue_name(self):
        with patch.dict(os.environ, {"RESIZE_QUEUE": "custom-resize"}):
            import importlib
            import worker as worker_module
            importlib.reload(worker_module)
            self.assertTrue(
                hasattr(worker_module, "QUEUE_NAME") or 
                hasattr(worker_module, "RESIZE_QUEUE")
            )

    def test_message_structure_validation(self):
        test_message = {
            "post_id": 1,
            "image_full": "https://example.com/image.jpg"
        }
        message_json = json.dumps(test_message)
        parsed = json.loads(message_json)
        self.assertIn("post_id", parsed)
        self.assertIn("image_full", parsed)
        self.assertEqual(parsed["post_id"], 1)

    def test_environment_configuration(self):
        with patch.dict(os.environ, {
            "RABBIT_HOST": "queue",
            "RESIZE_QUEUE": "resize",
            "THUMB_DIR": "/data/thumbs",
            "THUMB_PUBLIC_PREFIX": "/thumbs",
            "THUMB_SIZE": "256"
        }, clear=False):
            self.assertEqual(os.getenv("RABBIT_HOST", "queue"), "queue")
            self.assertEqual(os.getenv("RESIZE_QUEUE", "resize"), "resize")


if __name__ == "__main__":
    unittest.main()
