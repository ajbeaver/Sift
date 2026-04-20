from __future__ import annotations

import mimetypes
from pathlib import Path

TEXT_EXTENSIONS = {
    ".c",
    ".cfg",
    ".conf",
    ".cpp",
    ".css",
    ".go",
    ".h",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

QUICKLOOK_EXTENSIONS = {
    ".aiff",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".m4a",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".tiff",
    ".wav",
}

STRUCTURED_PREVIEW_EXTENSIONS = {
    ".csv": "csv",
    ".json": "json",
    ".log": "log",
    ".md": "markdown",
}


def is_hidden_name(name: str) -> bool:
    return name.startswith(".")


def is_probably_binary(data: bytes) -> bool:
    if not data:
        return False
    if b"\x00" in data:
        return True
    text_bytes = sum(byte < 9 or 13 < byte < 32 for byte in data)
    return (text_bytes / len(data)) > 0.30


def classify_path(path: Path, *, is_dir: bool = False) -> str:
    if is_dir:
        return "directory"

    suffix = path.suffix.lower()
    if suffix in STRUCTURED_PREVIEW_EXTENSIONS:
        return STRUCTURED_PREVIEW_EXTENSIONS[suffix]
    if suffix in QUICKLOOK_EXTENSIONS:
        return "quicklook"
    if suffix in TEXT_EXTENSIONS:
        return "text"

    mime_type, _ = mimetypes.guess_type(path.name)
    if mime_type:
        if mime_type.startswith("text/"):
            return "text"
        if mime_type.startswith(("image/", "audio/", "video/")):
            return "quicklook"
        if mime_type == "application/pdf":
            return "quicklook"

    return "binary"
