from __future__ import annotations

from pathlib import Path

from sift.fs.classify import classify_path
from sift.models import PreviewResult
from sift.preview.structured import load_structured_preview
from sift.preview.text import load_text_preview


def load_preview(path: Path) -> PreviewResult:
    if path.is_dir():
        return PreviewResult(
            kind="directory",
            title=path.name or str(path),
            body="Directory selected.\nPress Enter to browse into it.",
        )

    preview_kind = classify_path(path)
    if preview_kind in {"json", "csv", "markdown", "log"}:
        return load_structured_preview(path, preview_kind)
    if preview_kind == "text":
        return load_text_preview(path)
    if preview_kind == "quicklook":
        return PreviewResult(
            kind="quicklook",
            title=path.name,
            body="Quick Look available.\nPress Space to preview in-terminal if supported, or use the Quick Look action.",
        )
    return PreviewResult(
        kind="binary",
        title=path.name,
        body="No inline preview for this file type. Use Quick Look or open the file externally.",
    )
