from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container, VerticalScroll
from textual.screen import ModalScreen
from textual.widgets import Static

from sift.models import PreviewResult


class PreviewPane(Static):
    DEFAULT_CSS = """
    PreviewPane {
        width: 100%;
        height: auto;
    }
    """

    def show_preview(self, preview: PreviewResult | None) -> None:
        if preview is None:
            self.update("No preview")
            return
        title = preview.title or "Preview"
        self.update(f"{title}\n\n{preview.body}")


class PreviewScreen(ModalScreen[None]):
    BINDINGS = [
        Binding("up", "scroll_up", "Up", show=False),
        Binding("down", "scroll_down", "Down", show=False),
        Binding("pageup", "page_up", "Page Up", show=False),
        Binding("pagedown", "page_down", "Page Down", show=False),
        Binding("home", "scroll_home", "Home", show=False),
        Binding("end", "scroll_end", "End", show=False),
        Binding("q,escape", "close_preview", "Close"),
    ]

    def __init__(self, preview: PreviewResult) -> None:
        super().__init__()
        self._preview = preview

    def compose(self) -> ComposeResult:
        with Container(id="preview-modal"):
            with VerticalScroll(id="preview-scroll"):
                yield PreviewPane(self._render_text(), id="preview-body")

    def on_mount(self) -> None:
        self.query_one("#preview-scroll", VerticalScroll).focus()

    def action_close_preview(self) -> None:
        self.dismiss(None)

    def action_scroll_up(self) -> None:
        self._scroll_by(-3)

    def action_scroll_down(self) -> None:
        self._scroll_by(3)

    def action_page_up(self) -> None:
        self._scroll_by(-20)

    def action_page_down(self) -> None:
        self._scroll_by(20)

    def action_scroll_home(self) -> None:
        self.query_one("#preview-scroll", VerticalScroll).scroll_home(animate=False)

    def action_scroll_end(self) -> None:
        self.query_one("#preview-scroll", VerticalScroll).scroll_end(animate=False)

    def _render_text(self) -> str:
        title = self._preview.title or "Preview"
        return f"{title}\n\n{self._preview.body}"

    def _scroll_by(self, delta: int) -> None:
        self.query_one("#preview-scroll", VerticalScroll).scroll_relative(y=delta, animate=False)
