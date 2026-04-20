from __future__ import annotations

from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, Header, Input, ListView

from sift.controller import SiftController
from sift.state import AppState
from sift.ui.browser_pane import BrowserPane
from sift.ui.inspect_pane import InspectPane
from sift.ui.layout import APP_CSS
from sift.ui.preview_pane import PreviewScreen
from sift.ui.status_bar import StatusBar


class SiftApp(App[None]):
    CSS = APP_CSS
    TITLE = "sift"
    BINDINGS = [
        Binding("w,up", "move_up", "Up"),
        Binding("s,down", "move_down", "Down"),
        Binding("a,left", "go_parent", "Parent"),
        Binding("d,right,enter", "enter_selection", "Enter"),
        Binding("space", "toggle_preview", "Preview"),
        Binding("o", "open_selected", "Open"),
        Binding("g", "quick_look", "Quick Look"),
        Binding("/", "focus_filter", "Filter"),
        Binding("escape", "close_transient", "Close"),
        Binding("q", "close_or_quit", "Close/Quit"),
    ]

    def __init__(self, start_path: Path | None = None) -> None:
        super().__init__()
        self.state = AppState(current_path=(start_path or Path.cwd()).resolve())
        self.controller = SiftController(self.state)

    def compose(self) -> ComposeResult:
        yield Header(id="chrome", show_clock=False)
        yield Input(placeholder="Filter current directory", id="filter")
        yield BrowserPane(id="browser")
        yield InspectPane(id="inspect")
        yield StatusBar(id="status")
        yield Footer()

    def on_mount(self) -> None:
        self.controller.initialize()
        self._sync_view()
        self._focus_browser()

    def action_move_down(self) -> None:
        self.controller.move_selection(1)
        self._sync_view()

    def action_move_up(self) -> None:
        self.controller.move_selection(-1)
        self._sync_view()

    def action_go_parent(self) -> None:
        self.controller.go_parent()
        self._sync_view()
        self._focus_browser()

    def action_enter_selection(self) -> None:
        selected_before = self.state.selected_entry
        self.controller.enter_selection()
        self._sync_view()
        if selected_before and not selected_before.is_dir and self.state.preview_visible and self.state.preview:
            self._show_preview_screen()

    def action_toggle_preview(self) -> None:
        self.controller.toggle_preview()
        self._sync_view()
        if self.state.preview_visible and self.state.preview:
            self._show_preview_screen()

    def action_open_selected(self) -> None:
        self.controller.open_selected()
        self._sync_view()

    def action_quick_look(self) -> None:
        self.controller.quick_look_selected()
        self._sync_view()

    def action_focus_filter(self) -> None:
        filter_input = self.query_one("#filter", Input)
        filter_input.add_class("visible")
        filter_input.focus()

    def action_close_transient(self) -> None:
        filter_input = self.query_one("#filter", Input)
        if filter_input.has_focus:
            filter_input.value = ""
            filter_input.remove_class("visible")
            self.controller.clear_filter()
            self._focus_browser()
            self._sync_view()
            return
        if len(self.screen_stack) > 1:
            self.state.preview_visible = False
            self.pop_screen()
            self._sync_view()
            self._focus_browser()

    def action_close_or_quit(self) -> None:
        if self._has_transient_ui():
            self.action_close_transient()
            return
        self.exit()

    @on(Input.Changed, "#filter")
    def on_filter_change(self, event: Input.Changed) -> None:
        self.controller.set_filter(event.value)
        self._sync_view()

    @on(ListView.Highlighted, "#browser")
    def on_browser_highlighted(self, event: ListView.Highlighted) -> None:
        if event.item is None:
            return
        browser = event.control
        if browser.index is None or browser.index < 0:
            return
        if browser.index == self.state.selected_index:
            return
        self.state.selected_index = browser.index
        self.controller.refresh_selection(load_preview_content=False)
        self._sync_detail_panes()

    def _sync_view(self) -> None:
        browser = self.query_one(BrowserPane)
        browser.sync_entries(self.state.entries)
        browser.sync_selection(self.state.selected_index)
        self._sync_detail_panes()

    def _sync_detail_panes(self) -> None:
        inspect = self.query_one(InspectPane)
        status = self.query_one(StatusBar)
        inspect.show_metadata(self.state.inspect)
        status.set_message(f"{self.state.current_path} | {self.state.status_message}")

    def _has_transient_ui(self) -> bool:
        filter_input = self.query_one("#filter", Input)
        return filter_input.has_focus or len(self.screen_stack) > 1

    def _show_preview_screen(self) -> None:
        if len(self.screen_stack) > 1 or self.state.preview is None:
            return
        self.push_screen(PreviewScreen(self.state.preview), self._on_preview_closed)

    def _on_preview_closed(self, _result: None) -> None:
        if self.state.preview_visible:
            self.state.preview_visible = False
            self._sync_view()
        self._focus_browser()

    def _focus_browser(self) -> None:
        self.query_one(BrowserPane).focus()


def main(start_path: Path | None = None) -> None:
    app = SiftApp(start_path=start_path)
    app.run()
