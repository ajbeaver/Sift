from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sift.fs.scanner import scan_directory


class ScannerTests(unittest.TestCase):
    def test_scan_directory_groups_directories_before_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "z-file.txt").write_text("x")
            (root / "a-dir").mkdir()
            (root / ".hidden").write_text("x")

            entries = scan_directory(root)

            self.assertEqual([entry.name for entry in entries], ["a-dir", ".hidden", "z-file.txt"])
            self.assertTrue(entries[1].is_hidden)

    def test_scan_directory_applies_case_insensitive_filter(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "README.md").write_text("x")
            (root / "notes.txt").write_text("x")

            entries = scan_directory(root, "read")

            self.assertEqual([entry.name for entry in entries], ["README.md"])


if __name__ == "__main__":
    unittest.main()
