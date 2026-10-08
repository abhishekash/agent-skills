#!/usr/bin/env python3
"""Validate SKILL.md files: frontmatter present, required keys, name == dir, sane lengths.

Zero dependencies (intentionally — runs anywhere). Exit 1 with a report on failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_KEYS = {"name", "description"}
DESCRIPTION_RANGE = (40, 600)  # too short to route on / too long to stay in context


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("must start with a '---' frontmatter block")
    meta: dict[str, str] = {}
    i = 1
    while i < len(lines) and lines[i].strip() != "---":
        if lines[i].strip() and ":" in lines[i]:
            key, _, value = lines[i].partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
        i += 1
    if i >= len(lines):
        raise ValueError("unterminated frontmatter block")
    return meta


def validate(skill_md: Path) -> list[str]:
    errors: list[str] = []
    try:
        meta = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except ValueError as e:
        return [f"{skill_md}: {e}"]

    missing = REQUIRED_KEYS - meta.keys()
    if missing:
        errors.append(f"{skill_md}: missing frontmatter keys: {sorted(missing)}")

    name = meta.get("name", "")
    if name != skill_md.parent.name:
        errors.append(f"{skill_md}: name {name!r} != directory {skill_md.parent.name!r}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", name):
        errors.append(f"{skill_md}: name {name!r} should be kebab-case")

    desc = meta.get("description", "")
    lo, hi = DESCRIPTION_RANGE
    if not (lo <= len(desc) <= hi):
        errors.append(f"{skill_md}: description is {len(desc)} chars (want {lo}–{hi})")
    if "use when" not in desc.lower():
        errors.append(f"{skill_md}: description should say when to use it ('…Use when …')")
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "skills")
    skill_files = sorted(root.glob("*/SKILL.md"))
    if not skill_files:
        print(f"no skills found under {root}", file=sys.stderr)
        return 1
    all_errors: list[str] = []
    for f in skill_files:
        all_errors.extend(validate(f))
    if all_errors:
        print("\n".join(all_errors), file=sys.stderr)
        return 1
    print(f"ok: {len(skill_files)} skills valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
