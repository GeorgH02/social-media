import unittest
from ml import classify_text


class TestMLService(unittest.TestCase):
    def test_classify_text_with_positive_sentiment(self):
        result = classify_text("I love this! It's amazing!")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertIn("label", result[0][0])
        self.assertIn("score", result[0][0])

    def test_classify_text_with_negative_sentiment(self):
        result = classify_text("This is terrible and awful.")
        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_classify_text_with_empty_string(self):
        result = classify_text("")
        self.assertIn("error", result)

    def test_classify_text_returns_consistent_format(self):
        result = classify_text("This is a test.")
        self.assertIsInstance(result, (list, dict))
        if isinstance(result, list):
            self.assertGreater(len(result), 0)
            self.assertIsInstance(result[0], list)


if __name__ == "__main__":
    unittest.main()
