from __future__ import annotations

import unittest

from sift.__main__ import build_parser


class CliTests(unittest.TestCase):
    def test_help_includes_path_argument(self) -> None:
        parser = build_parser()
        help_text = parser.format_help()

        self.assertIn("usage: sift", help_text)
        self.assertIn("[path]", help_text)
        self.assertIn("Directory to open on launch", help_text)


if __name__ == "__main__":
    unittest.main()
