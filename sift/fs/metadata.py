from __future__ import annotations

import stat
from datetime import datetime
from pathlib import Path

from sift.fs.classify import classify_path
from sift.models import Metadata


def load_metadata(path: Path) -> Metadata:
    try:
        stat_result = path.lstat()
    except OSError as exc:
        return Metadata(
            path=path,
            kind="other",
            size=None,
            modified_at=None,
            permissions="??????????",
            symlink_target=None,
            preview_kind="error",
            error=str(exc),
        )

    mode = stat_result.st_mode
    if stat.S_ISDIR(mode):
        kind = "directory"
    elif stat.S_ISREG(mode):
        kind = "file"
    elif stat.S_ISLNK(mode):
        kind = "symlink"
    else:
        kind = "other"

    symlink_target = None
    if kind == "symlink":
        try:
            symlink_target = str(path.resolve(strict=False))
        except OSError:
            symlink_target = None

    size = stat_result.st_size if kind != "directory" else None
    modified_at = datetime.fromtimestamp(stat_result.st_mtime)
    preview_kind = classify_path(path, is_dir=(kind == "directory"))

    return Metadata(
        path=path,
        kind=kind,
        size=size,
        modified_at=modified_at,
        permissions=stat.filemode(mode),
        symlink_target=symlink_target,
        preview_kind=preview_kind,
        error=None,
    )
