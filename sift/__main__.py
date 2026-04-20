from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sift",
        description="Terminal-native read-only file workspace for browsing and previewing files.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Directory to open on launch. Defaults to the current working directory.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        from sift.app import main as run_app
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise SystemExit(
                "Missing dependency: textual. Install project dependencies before running `python3 -m sift`."
            ) from exc
        raise
    run_app(Path(args.path).expanduser())


if __name__ == "__main__":
    main()
