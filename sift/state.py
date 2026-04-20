from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from sift.models import Entry, Metadata, PreviewResult


@dataclass
class AppState:
    current_path: Path
    entries: list[Entry] = field(default_factory=list)
    selected_index: int = 0
    filter_text: str = ""
    inspect: Metadata | None = None
    preview: PreviewResult | None = None
    preview_visible: bool = False
    status_message: str = ""

    @property
    def selected_entry(self) -> Entry | None:
        if not self.entries:
            return None
        index = max(0, min(self.selected_index, len(self.entries) - 1))
        return self.entries[index]

    def clamp_selection(self) -> None:
        if not self.entries:
            self.selected_index = 0
            return
        self.selected_index = max(0, min(self.selected_index, len(self.entries) - 1))
