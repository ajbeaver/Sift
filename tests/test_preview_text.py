from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sift.preview.text import load_text_preview


class TextPreviewTests(unittest.TestCase):
    def test_text_preview_truncates_by_lines(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.txt"
            path.write_text("\n".join(f"line {index}" for index in range(10)))

            preview = load_text_preview(path, max_lines=3)

            self.assertEqual(preview.kind, "text")
            self.assertTrue(preview.truncated)
            self.assertIn("[truncated]", preview.body)

    def test_text_preview_rejects_binary_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "sample.bin"
            path.write_bytes(b"\x00\x01\x02")

            preview = load_text_preview(path)

            self.assertEqual(preview.kind, "binary")


if __name__ == "__main__":
    unittest.main()
