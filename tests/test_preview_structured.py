from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sift.preview.structured import load_structured_preview


class StructuredPreviewTests(unittest.TestCase):
    def test_json_preview_pretty_prints_small_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.json"
            path.write_text('{"b": 1, "a": 2}')

            preview = load_structured_preview(path, "json")

            self.assertEqual(preview.kind, "structured_text")
            self.assertIn('"a": 2', preview.body)
            self.assertIn('"b": 1', preview.body)

    def test_csv_preview_renders_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "data.csv"
            path.write_text("name,role\nalice,dev\nbob,ops\n")

            preview = load_structured_preview(path, "csv")

            self.assertEqual(preview.kind, "structured_text")
            self.assertIn("name", preview.body)
            self.assertIn("alice", preview.body)


if __name__ == "__main__":
    unittest.main()
