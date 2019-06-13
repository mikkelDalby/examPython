import unittest
from findinhtml import make_markdown

class TestFindinhtml(unittest.TestCase):
    def test_make_markdown(self):
        self.assertEqual("# Test\n", make_markdown("<h1>Test</h1>"))
        self.assertEqual("## Test\n", make_markdown("<h2>Test</h2>"))
        self.assertEqual("Test\n", make_markdown("<p>Test</p>"))