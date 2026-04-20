from __future__ import annotations

import os
from pathlib import Path

from sift.fs.classify import is_hidden_name
from sift.models import Entry, EntryKind


def _entry_kind(dir_entry: os.DirEntry[str]) -> EntryKind:
    if dir_entry.is_dir(follow_symlinks=False):
        return "directory"
    if dir_entry.is_file(follow_symlinks=False):
        return "file"
    if dir_entry.is_symlink():
        return "symlink"
    return "other"


def scan_directory(path: Path, filter_text: str = "") -> list[Entry]:
    needle = filter_text.strip().lower()
    entries: list[Entry] = []

    with os.scandir(path) as iterator:
        for dir_entry in iterator:
            name = dir_entry.name
            if needle and needle not in name.lower():
                continue
            kind = _entry_kind(dir_entry)
            entries.append(
                Entry(
                    path=Path(dir_entry.path),
                    name=name,
                    kind=kind,
                    is_hidden=is_hidden_name(name),
                )
            )

    entries.sort(key=lambda entry: (not entry.is_dir, entry.name.lower()))
    return entries
