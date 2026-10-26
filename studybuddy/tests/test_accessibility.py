import re
import unittest
from pathlib import Path


class FrontendAccessibilitySmokeTests(unittest.TestCase):
    html = (Path(__file__).parents[1] / "frontend" / "index.html").read_text(encoding="utf-8")

    def test_page_has_language_and_main_regions(self):
        self.assertRegex(self.html, r"<html[^>]+lang=")
        self.assertIn('id="pg"', self.html)

    def test_interactive_labels_exist(self):
        self.assertGreaterEqual(len(re.findall(r"aria-label=", self.html)), 5)


if __name__ == "__main__":
    unittest.main()
