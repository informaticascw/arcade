#!/usr/bin/env python3

"""
Requirements:
    sudo apt-get update
    sudo apt-get install -y imagemagick

Usage:
    python3 update_metadata_for_all_games.py
    python3 update_metadata_for_all_games.py --install-deps
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
GAMES_DIR = ROOT_DIR / "games"
PLACEHOLDER_AUTHORS = ["Kees", "Annie"]
ANCHOR_TOKENS = ("game", "opdracht", "eindopdracht", "pygame")
IGNORED_TOKENS = {
    "en",
    "main",
    "master"
}
NAME_SEPARATORS = re.compile(r"\s*(?:&|,|/|\ben\b)\s*", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Update game metadata and capture screenshots for all games."
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install required system packages before processing games.",
    )
    parser.add_argument(
        "--match",
        help="Only process game directories whose name contains this text.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Only process the first N matching game directories.",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds to wait after starting each game before taking a screenshot.",
    )
    return parser.parse_args()


def install_dependencies() -> None:
    commands = [
        ["sudo", "apt-get", "update"],
        ["sudo", "apt-get", "install", "-y", "imagemagick"],
    ]

    for command in commands:
        subprocess.run(command, check=True)


def ensure_screenshot_command() -> str:
    screenshot_command = shutil.which("import")
    if screenshot_command:
        return screenshot_command

    print("Screenshot command 'import' ontbreekt, probeer imagemagick te installeren...", file=sys.stderr)
    install_dependencies()

    screenshot_command = shutil.which("import")
    if screenshot_command:
        return screenshot_command

    raise RuntimeError("Screenshot command 'import' is niet beschikbaar na installatie van imagemagick.")


def iter_game_dirs(match: str | None, limit: int | None) -> list[Path]:
    game_dirs: list[Path] = []

    for game_dir in sorted(GAMES_DIR.iterdir()):
        if not game_dir.is_dir():
            continue
        if not (game_dir / "main.py").exists():
            continue
        if not (game_dir / "metadata.json").exists():
            continue
        if match and match.lower() not in game_dir.name.lower():
            continue
        game_dirs.append(game_dir)

    if limit is not None:
        return game_dirs[:limit]
    return game_dirs


def derive_authors(directory_name: str) -> list[str]:
    tokens = [token for token in re.split(r"[-_]+", directory_name.lower()) if token]
    start_index = 0

    for index, token in enumerate(tokens):
        if token in ANCHOR_TOKENS:
            start_index = index + 1

    authors: list[str] = []
    for token in tokens[start_index:]:
        if token in IGNORED_TOKENS:
            continue
        if any(character.isdigit() for character in token):
            continue
        if len(token) <= 1:
            continue
        authors.append(token.title())

    return authors


def derive_authors_from_name(game_name: str) -> list[str]:
    parts = [part.strip() for part in NAME_SEPARATORS.split(game_name) if part.strip()]
    authors: list[str] = []

    for part in parts:
        if any(character.isdigit() for character in part):
            continue
        normalized = " ".join(word.capitalize() for word in part.split())
        if normalized:
            authors.append(normalized)

    return authors


def update_metadata(game_dir: Path) -> list[str]:
    metadata_path = game_dir / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    current_authors = metadata.get("authors", [])
    derived_authors = derive_authors(game_dir.name)
    fallback_authors = derive_authors_from_name(metadata.get("name", ""))

    authors = derived_authors
    if not authors:
        authors = fallback_authors
    elif len(authors) == 1 and len(fallback_authors) in {2, 3}:
        if authors[0].lower() not in {author.lower() for author in fallback_authors}:
            authors = fallback_authors

    if authors and current_authors == PLACEHOLDER_AUTHORS:
        metadata["authors"] = authors
    metadata.pop("instructionspage", None)

    metadata_path.write_text(
        json.dumps(metadata, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    return metadata.get("authors", [])


def screenshot_target(game_dir: Path) -> Path:
    default_path = game_dir / "screenshot.jpg"
    fallback_path = game_dir / "screenshot-autocaptured.jpg"

    if default_path.exists():
        return fallback_path
    return default_path


def stop_process(process: subprocess.Popen[bytes]) -> None:
    if process.poll() is not None:
        return

    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return

    deadline = time.time() + 5
    while time.time() < deadline:
        if process.poll() is not None:
            return
        time.sleep(0.1)

    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=5)


def capture_game(game_dir: Path, delay: float, screenshot_command: str) -> Path:
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        cwd=game_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

    target = screenshot_target(game_dir)

    try:
        time.sleep(delay)
        subprocess.run(
            [screenshot_command, "-window", "root", str(target)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    finally:
        stop_process(process)

    return target


def main() -> int:
    args = parse_args()

    if args.install_deps:
        install_dependencies()

    try:
        screenshot_command = ensure_screenshot_command()
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(str(error), file=sys.stderr)
        return 1

    if not os.environ.get("DISPLAY"):
        print("DISPLAY is not set, so screenshots cannot be captured.", file=sys.stderr)
        return 1

    game_dirs = iter_game_dirs(args.match, args.limit)
    if not game_dirs:
        print("No matching games found.")
        return 0

    for game_dir in game_dirs:
        authors = update_metadata(game_dir)
        screenshot_path = capture_game(game_dir, args.delay, screenshot_command)
        print(f"Processed {game_dir.name}: authors={authors}, screenshot={screenshot_path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())