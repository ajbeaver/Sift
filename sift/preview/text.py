from __future__ import annotations

from pathlib import Path

from sift.fs.classify import is_probably_binary
from sift.models import PreviewResult

DEFAULT_MAX_BYTES = 64 * 1024
DEFAULT_MAX_LINES = 200


def load_text_preview(
    path: Path,
    *,
    max_bytes: int = DEFAULT_MAX_BYTES,
    max_lines: int = DEFAULT_MAX_LINES,
) -> PreviewResult:
    try:
        with path.open("rb") as handle:
            raw = handle.read(max_bytes + 1)
    except OSError as exc:
        return PreviewResult(
            kind="error",
            title=path.name,
            body=f"Unable to read file.\n{exc}",
            error=str(exc),
        )

    if is_probably_binary(raw):
        return PreviewResult(
            kind="binary",
            title=path.name,
            body="Binary file. Use Quick Look or open the file externally.",
        )

    truncated = len(raw) > max_bytes
    if truncated:
        raw = raw[:max_bytes]

    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    if len(lines) > max_lines:
        truncated = True
        lines = lines[:max_lines]

    body = "\n".join(lines)
    if truncated:
        body = f"{body}\n\n[truncated]"

    return PreviewResult(kind="text", title=path.name, body=body, truncated=truncated)
