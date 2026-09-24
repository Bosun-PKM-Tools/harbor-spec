"""
tests/validate_fixtures.py
──────────────────────────
Validates gold-standard acid-test notes under tests/fixtures/canonical/
against Draft 2020-12 realm schemas (via archetype + universal envelope refs).

Usage
  python tests/validate_fixtures.py
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML is required (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError:
    print("FAIL: jsonschema/referencing required (pip install jsonschema)", file=sys.stderr)
    sys.exit(2)

_REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SCHEMAS_DIR = _REPO_ROOT / "schemas"
_CANONICAL_DIR = pathlib.Path(__file__).resolve().parent / "fixtures" / "canonical"

_UUIDV7_URN = re.compile(
    r"^urn:uuid:[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)

# filename stem -> (realm schema key, expected $pkm.realm)
_CANONICAL_FIXTURES = (
    ("02-yeoman-person.md", "02-yeoman", "yeoman"),
    ("03-trice-task.md", "03-trice", "trice"),
    ("04-logbook-day.md", "04-logbook", "logbook"),
    ("05-quartermaster-receipt.md", "05-quartermaster", "quartermaster"),
    ("17-supercargo-tool.md", "17-supercargo", "supercargo"),
)

_ARCHETYPE_SCHEMAS = (
    "v1/archetypes/catalog-dossier.schema.json",
    "v1/archetypes/interaction-ledger.schema.json",
    "v1/archetypes/dual-track-telemetry.schema.json",
    "v1/archetypes/stage-gate-manifest.schema.json",
    "v1/archetypes/sovereign-vault.schema.json",
)


def _extract_frontmatter(content: str) -> str:
    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter ---")
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "".join(lines[1:idx])
    raise ValueError("missing closing frontmatter ---")


def _load_json(path: pathlib.Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _build_registry() -> Registry:
    registry = Registry()
    for rel in _ARCHETYPE_SCHEMAS:
        path = _SCHEMAS_DIR / rel
        obj = _load_json(path)
        registry = registry.with_resource(obj["$id"], Resource.from_contents(obj))
    envelope = _load_json(_SCHEMAS_DIR / "v1" / "meta" / "envelope.schema.json")
    registry = registry.with_resource(envelope["$id"], Resource.from_contents(envelope))
    relations = _load_json(_SCHEMAS_DIR / "v1" / "relations" / "relations.schema.json")
    registry = registry.with_resource(relations["$id"], Resource.from_contents(relations))
    return registry


def main() -> int:
    if not _CANONICAL_DIR.is_dir():
        print(f"FAIL: canonical fixtures directory missing: {_CANONICAL_DIR}", file=sys.stderr)
        return 1

    registry = _build_registry()
    failures = 0

    for filename, schema_key, expected_realm in _CANONICAL_FIXTURES:
        fixture_path = _CANONICAL_DIR / filename
        schema_path = _SCHEMAS_DIR / "v1" / "realms" / f"{schema_key}.schema.json"
        label = filename

        if not fixture_path.is_file():
            print(f"FAIL  {label}: file not found")
            failures += 1
            continue
        if not schema_path.is_file():
            print(f"FAIL  {label}: schema not found ({schema_path})")
            failures += 1
            continue

        try:
            raw = fixture_path.read_text(encoding="utf-8")
            data = yaml.safe_load(_extract_frontmatter(raw))
            if not isinstance(data, dict):
                raise ValueError("frontmatter did not parse to a mapping")
            pkm = data.get("$pkm")
            if not isinstance(pkm, dict):
                raise ValueError("missing $pkm envelope")
            note_id = pkm.get("id")
            if not isinstance(note_id, str) or not _UUIDV7_URN.match(note_id):
                raise ValueError(f"$pkm.id failed strict UUIDv7 URN regex: {note_id!r}")
            if pkm.get("realm") != expected_realm:
                raise ValueError(
                    f"$pkm.realm expected {expected_realm!r}, got {pkm.get('realm')!r}"
                )

            schema_obj = _load_json(schema_path)
            Draft202012Validator(schema_obj, registry=registry).validate(data)
        except Exception as exc:
            print(f"FAIL  {label}: {exc}")
            failures += 1
            continue

        print(f"PASS  {label}")

    total = len(_CANONICAL_FIXTURES)
    passed = total - failures
    print(f"\n{passed}/{total} canonical fixtures passed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
