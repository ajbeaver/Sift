from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Literal

EntryKind = Literal["directory", "file", "symlink", "other"]
PreviewKind = Literal[
    "none",
    "directory",
    "text",
    "structured_text",
    "quicklook",
    "binary",
    "error",
]


@dataclass(frozen=True)
class Entry:
    path: Path
    name: str
    kind: EntryKind
    is_hidden: bool

    @property
    def is_dir(self) -> bool:
        return self.kind == "directory"

    @property
    def is_file(self) -> bool:
        return self.kind == "file"

    @property
    def is_symlink(self) -> bool:
        return self.kind == "symlink"


@dataclass(frozen=True)
class Metadata:
    path: Path
    kind: EntryKind
    size: int | None
    modified_at: datetime | None
    permissions: str
    symlink_target: str | None
    preview_kind: str
    error: str | None = None


@dataclass(frozen=True)
class PreviewResult:
    kind: PreviewKind
    title: str
    body: str
    truncated: bool = False
    error: str | None = None


@dataclass(frozen=True)
class PlatformActionResult:
    success: bool
    message: str
