from __future__ import annotations

import csv
import json
from pathlib import Path

from sift.models import PreviewResult
from sift.preview.text import DEFAULT_MAX_BYTES, load_text_preview

CSV_MAX_ROWS = 20
CSV_MAX_COLUMNS = 6
CSV_MAX_WIDTH = 24
JSON_PARSE_LIMIT = 32 * 1024


def load_structured_preview(path: Path, kind: str) -> PreviewResult:
    if kind == "json":
        return load_json_preview(path)
    if kind == "csv":
        return load_csv_preview(path)
    return _wrap_text_preview(load_text_preview(path))


def load_json_preview(path: Path) -> PreviewResult:
    try:
        if path.stat().st_size > JSON_PARSE_LIMIT:
            return _wrap_text_preview(load_text_preview(path))
        text = path.read_text(encoding="utf-8")
        data = json.loads(text)
        body = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=True)
        if len(body.encode("utf-8")) > DEFAULT_MAX_BYTES:
            preview = load_text_preview(path)
            return _wrap_text_preview(preview)
        return PreviewResult(kind="structured_text", title=path.name, body=body)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return _wrap_text_preview(load_text_preview(path))


def load_csv_preview(path: Path) -> PreviewResult:
    rows: list[list[str]] = []
    truncated = False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.reader(handle)
            for index, row in enumerate(reader):
                if index >= CSV_MAX_ROWS:
                    truncated = True
                    break
                rows.append([_clip(cell) for cell in row[:CSV_MAX_COLUMNS]])
                if len(row) > CSV_MAX_COLUMNS:
                    rows[-1].append("...")
    except (OSError, UnicodeDecodeError):
        return _wrap_text_preview(load_text_preview(path))

    if not rows:
        return PreviewResult(kind="structured_text", title=path.name, body="[empty csv]")

    widths = [max(len(row[column]) if column < len(row) else 0 for row in rows) for column in range(max(len(row) for row in rows))]
    rendered = []
    for row in rows:
        padded = []
        for index, width in enumerate(widths):
            value = row[index] if index < len(row) else ""
            padded.append(value.ljust(width))
        rendered.append(" | ".join(padded).rstrip())

    body = "\n".join(rendered)
    if truncated:
        body = f"{body}\n\n[truncated]"
    return PreviewResult(kind="structured_text", title=path.name, body=body, truncated=truncated)


def _clip(value: str) -> str:
    value = value.replace("\n", " ").strip()
    if len(value) <= CSV_MAX_WIDTH:
        return value
    return f"{value[: CSV_MAX_WIDTH - 3]}..."


def _wrap_text_preview(preview: PreviewResult) -> PreviewResult:
    if preview.kind == "error":
        return preview
    return PreviewResult(
        kind="structured_text",
        title=preview.title,
        body=preview.body,
        truncated=preview.truncated,
        error=preview.error,
    )
