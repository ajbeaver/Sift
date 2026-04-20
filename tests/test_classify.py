from __future__ import annotations

import unittest
from pathlib import Path

from sift.fs.classify import classify_path, is_probably_binary


class ClassifyTests(unittest.TestCase):
    def test_classify_path_handles_text_quicklook_and_binary(self) -> None:
        self.assertEqual(classify_path(Path("README.md")), "markdown")
        self.assertEqual(classify_path(Path("photo.jpg")), "quicklook")
        self.assertEqual(classify_path(Path("archive.bin")), "binary")

    def test_binary_detection_uses_null_bytes(self) -> None:
        self.assertTrue(is_probably_binary(b"abc\x00def"))
        self.assertFalse(is_probably_binary(b"hello\nworld\n"))


if __name__ == "__main__":
    unittest.main()
