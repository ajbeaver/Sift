from __future__ import annotations

from pathlib import Path
from typing import Callable

from sift.fs.classify import classify_path
from sift.fs.metadata import load_metadata
from sift.fs.scanner import scan_directory
from sift.models import PlatformActionResult, PreviewResult
from sift.platform.macos import open_with_default_app, quick_look
from sift.preview.loader import load_preview
from sift.state import AppState

PlatformAction = Callable[[Path], PlatformActionResult]


class SiftController:
    def __init__(
        self,
        state: AppState,
        *,
        open_action: PlatformAction = open_with_default_app,
        quicklook_action: PlatformAction = quick_look,
    ) -> None:
        self.state = state
        self._open_action = open_action
        self._quicklook_action = quicklook_action

    def initialize(self) -> None:
        self.refresh_entries()

    def refresh_entries(self) -> None:
        try:
            self.state.entries = scan_directory(self.state.current_path, self.state.filter_text)
            self.state.clamp_selection()
            if not self.state.entries:
                self.state.inspect = None
                self.state.preview = PreviewResult(kind="none", title="", body="No entries.")
                self.state.status_message = "No entries."
                return
            self.refresh_selection(load_preview_content=self.state.preview_visible)
            self.state.status_message = f"{len(self.state.entries)} entries"
        except OSError as exc:
            self.state.entries = []
            self.state.inspect = None
            self.state.preview = PreviewResult(kind="error", title="Directory error", body=str(exc), error=str(exc))
            self.state.status_message = str(exc)

    def move_selection(self, delta: int) -> None:
        if not self.state.entries:
            return
        self.state.selected_index += delta
        self.state.clamp_selection()
        self.refresh_selection(load_preview_content=self.state.preview_visible)

    def set_filter(self, value: str) -> None:
        self.state.filter_text = value
        self.state.selected_index = 0
        self.refresh_entries()

    def clear_filter(self) -> None:
        self.set_filter("")

    def refresh_selection(self, *, load_preview_content: bool) -> None:
        entry = self.state.selected_entry
        if entry is None:
            self.state.inspect = None
            self.state.preview = PreviewResult(kind="none", title="", body="No selection.")
            return
        self.state.inspect = load_metadata(entry.path)
        if load_preview_content:
            self.state.preview = load_preview(entry.path)
        else:
            preview_kind = classify_path(entry.path, is_dir=entry.is_dir)
            self.state.preview = PreviewResult(
                kind="none",
                title=entry.name,
                body=f"Preview available: {preview_kind}",
            )

    def enter_selection(self) -> None:
        entry = self.state.selected_entry
        if entry is None:
            return
        if entry.is_dir:
            self.state.current_path = entry.path
            self.state.selected_index = 0
            self.state.preview_visible = False
            self.refresh_entries()
            return
        self.state.preview_visible = True
        self.state.preview = load_preview(entry.path)

    def go_parent(self) -> None:
        parent = self.state.current_path.parent
        if parent == self.state.current_path:
            self.state.status_message = "Already at filesystem root."
            return
        self.state.current_path = parent
        self.state.selected_index = 0
        self.state.preview_visible = False
        self.refresh_entries()

    def toggle_preview(self) -> None:
        entry = self.state.selected_entry
        if entry is None:
            return
        self.state.preview_visible = not self.state.preview_visible
        if self.state.preview_visible:
            self.state.preview = load_preview(entry.path)
        else:
            self.state.preview = PreviewResult(kind="none", title=entry.name, body="Preview closed.")

    def open_selected(self) -> PlatformActionResult:
        entry = self.state.selected_entry
        if entry is None:
            result = PlatformActionResult(success=False, message="No selection.")
            self.state.status_message = result.message
            return result
        if entry.is_dir:
            self.enter_selection()
            result = PlatformActionResult(success=True, message=f"Entered {entry.name}/")
            self.state.status_message = result.message
            return result
        result = self._open_action(entry.path)
        self.state.status_message = result.message
        return result

    def quick_look_selected(self) -> PlatformActionResult:
        entry = self.state.selected_entry
        if entry is None:
            result = PlatformActionResult(success=False, message="No selection.")
            self.state.status_message = result.message
            return result
        result = self._quicklook_action(entry.path)
        self.state.status_message = result.message
        return result
