from __future__ import annotations

import subprocess
from pathlib import Path

from sift.models import PlatformActionResult


def quick_look(path: Path) -> PlatformActionResult:
    return _launch(["qlmanage", "-p", str(path)], success_message=f"Opened Quick Look for {path.name}.")


def open_with_default_app(path: Path) -> PlatformActionResult:
    return _launch(["open", str(path)], success_message=f"Opened {path.name}.")


def _launch(command: list[str], *, success_message: str) -> PlatformActionResult:
    try:
        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError as exc:
        return PlatformActionResult(success=False, message=str(exc))
    return PlatformActionResult(success=True, message=success_message)
