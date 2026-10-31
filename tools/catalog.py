#!/usr/bin/env python3
"""Search the completed-project catalogue using only Python's standard library."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "catalog" / "projects.json"


def load_projects() -> list[dict]:
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read {CATALOG}: {exc}") from exc
    if not isinstance(data, list):
        raise SystemExit("catalog/projects.json must contain a JSON array")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Search completed IoT and embedded projects")
    parser.add_argument("--list", action="store_true", help="list all completed projects")
    parser.add_argument("--board", help="filter by board family, e.g. ESP32")
    parser.add_argument("--difficulty", choices=["beginner", "intermediate", "advanced"])
    parser.add_argument("--category", help="filter by category")
    parser.add_argument("--name", help="filter by project name")
    parser.add_argument("--language", help="filter by programming language, e.g. C++")
    parser.add_argument("--tag", help="filter by exact tag")
    parser.add_argument("--search", help="search names, tags, technologies, categories and boards")
    args = parser.parse_args()

    projects = load_projects()
    needle = (args.search or "").casefold()
    matched = []
    for project in projects:
        haystack = " ".join([
            str(project.get("name", "")),
            " ".join(project.get("tags", [])),
            " ".join(project.get("technologies", [])),
            " ".join(project.get("category", [])),
            str(project.get("board_family", "")),
        ]).casefold()
        if args.board and args.board.casefold() != str(project.get("board_family", "")).casefold():
            continue
        if args.difficulty and args.difficulty != project.get("difficulty"):
            continue
        if args.category and args.category.casefold() not in [str(x).casefold() for x in project.get("category", [])]:
            continue
        if args.name and args.name.casefold() not in str(project.get("name", "")).casefold():
            continue
        if args.language and args.language.casefold() not in [str(x).casefold() for x in project.get("languages", [])]:
            continue
        if args.tag and args.tag.casefold() not in [str(x).casefold() for x in project.get("tags", [])]:
            continue
        if needle and needle not in haystack:
            continue
        matched.append(project)

    if not matched:
        print("No completed projects match those filters.")
        return 0

    for item in matched:
        print(f"{item.get('name', 'Untitled')} [{item.get('id', 'no-id')}]")
        print(f"  Board: {item.get('board_family')} / {item.get('board_model')}")
        print(f"  Difficulty: {item.get('difficulty')} | Status: {item.get('status')}")
        print(f"  Category: {', '.join(item.get('category', []))}")
        print(f"  Guide: {item.get('path')}")
        print()
    print(f"{len(matched)} completed project(s) found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
