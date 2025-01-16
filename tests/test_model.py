
import unittest
from src.ai.model import process_image

class TestModel(unittest.TestCase):
    def test_process_image(self):
        result = process_image("tests/sample.jpg")
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
