from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from sift.controller import SiftController
from sift.models import PlatformActionResult
from sift.state import AppState


def _success_action(path: Path) -> PlatformActionResult:
    return PlatformActionResult(success=True, message=f"ok:{path.name}")


class ControllerTests(unittest.TestCase):
    def test_enter_selection_descends_into_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            child = root / "src"
            child.mkdir()

            state = AppState(current_path=root)
            controller = SiftController(state, open_action=_success_action, quicklook_action=_success_action)
            controller.initialize()

            controller.enter_selection()

            self.assertEqual(state.current_path, child)
            self.assertFalse(state.preview_visible)

    def test_toggle_preview_loads_preview_for_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "README.txt"
            path.write_text("hello")

            state = AppState(current_path=root)
            controller = SiftController(state, open_action=_success_action, quicklook_action=_success_action)
            controller.initialize()

            controller.toggle_preview()

            self.assertTrue(state.preview_visible)
            self.assertEqual(state.preview.kind, "text")

    def test_open_selected_uses_injected_platform_action(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "README.txt"
            path.write_text("hello")

            state = AppState(current_path=root)
            controller = SiftController(state, open_action=_success_action, quicklook_action=_success_action)
            controller.initialize()

            result = controller.open_selected()

            self.assertTrue(result.success)
            self.assertEqual(result.message, "ok:README.txt")


if __name__ == "__main__":
    unittest.main()
