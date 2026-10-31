#!/usr/bin/env python3
"""Basic consistency checks for the completed-project catalogue."""
from __future__ import annotations
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {"id", "name", "path", "board_family", "difficulty", "status", "category", "languages", "technologies", "tags", "built_date"}
VALID_STATUS = {"built-and-verified", "built-with-limitations", "archived"}
VALID_DIFFICULTY = {"beginner", "intermediate", "advanced"}


def main() -> int:
    errors: list[str] = []
    try:
        projects = json.loads((ROOT / "catalog/projects.json").read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: cannot load projects.json: {exc}")
        return 1
    if not isinstance(projects, list):
        print("FAIL: projects.json must be a list")
        return 1

    ids: set[str] = set()
    for index, project in enumerate(projects, start=1):
        missing = REQUIRED - set(project)
        if missing:
            errors.append(f"entry {index}: missing fields {sorted(missing)}")
        pid = project.get("id")
        if pid in ids:
            errors.append(f"duplicate project id: {pid}")
        ids.add(pid)
        if project.get("status") not in VALID_STATUS:
            errors.append(f"{pid}: invalid/non-completed catalogue status {project.get('status')!r}")
        if project.get("difficulty") not in VALID_DIFFICULTY:
            errors.append(f"{pid}: invalid difficulty {project.get('difficulty')!r}")
        guide = project.get("path", "")
        if not (ROOT / guide).is_file():
            errors.append(f"{pid}: guide does not exist: {guide}")
        folder = (ROOT / guide).parent if guide else ROOT
        metadata_path = folder / "metadata.json"
        if not metadata_path.is_file():
            errors.append(f"{pid}: metadata.json is missing beside guide")
        else:
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                if metadata.get("id") != pid:
                    errors.append(f"{pid}: metadata id does not match catalogue id")
                if metadata.get("status") != project.get("status"):
                    errors.append(f"{pid}: metadata status does not match catalogue status")
            except Exception as exc:
                errors.append(f"{pid}: invalid metadata.json: {exc}")

    csv_path = ROOT / "catalog/PROJECT_INDEX.csv"
    try:
        with csv_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        csv_ids = {row.get("id") for row in rows}
        if csv_ids != ids:
            errors.append(f"CSV ids {sorted(csv_ids)} do not match JSON ids {sorted(ids)}")
    except Exception as exc:
        errors.append(f"cannot validate CSV index: {exc}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {len(projects)} completed project(s); JSON, project guides, metadata and CSV index are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
