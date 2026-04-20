from __future__ import annotations

from textual.widgets import Static

from sift.models import Metadata


class InspectPane(Static):
    def show_metadata(self, metadata: Metadata | None) -> None:
        if metadata is None:
            self.update("No selection")
            return

        lines = [
            f"Path: {metadata.path}",
            f"Type: {metadata.kind}",
            f"Size: {metadata.size if metadata.size is not None else '-'}",
            f"Modified: {metadata.modified_at.isoformat(sep=' ', timespec='seconds') if metadata.modified_at else '-'}",
            f"Permissions: {metadata.permissions}",
            f"Preview: {metadata.preview_kind}",
        ]
        if metadata.symlink_target:
            lines.append(f"Target: {metadata.symlink_target}")
        if metadata.error:
            lines.append(f"Error: {metadata.error}")
        self.update("\n".join(lines))
