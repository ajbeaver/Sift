from __future__ import annotations

from textual.widgets import Label, ListItem, ListView

from sift.models import Entry


class BrowserPane(ListView):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entry_signature: tuple[tuple[str, str, bool], ...] = ()

    def sync_entries(self, entries: list[Entry]) -> bool:
        signature = tuple((str(entry.path), entry.kind, entry.is_hidden) for entry in entries)
        if signature == self._entry_signature:
            return False

        self.clear()
        for entry in entries:
            marker = "[D]" if entry.is_dir else "[F]"
            label = f"{marker} {entry.name}{'/' if entry.is_dir else ''}"
            if entry.is_hidden:
                label = f"[dim]{label}[/dim]"
            self.append(ListItem(Label(label, markup=True)))
        self._entry_signature = signature
        return True

    def sync_selection(self, selected_index: int) -> None:
        if not self._entry_signature:
            return
        if self.index != selected_index:
            self.index = selected_index
