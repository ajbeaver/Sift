from __future__ import annotations

from textual.widgets import Static


class StatusBar(Static):
    def set_message(self, message: str) -> None:
        self.update(message)
