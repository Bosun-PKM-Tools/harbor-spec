import json
import sys
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

candidate_fixture_dirs = [
    Path("fixtures/canonical"),
    Path("tests/fixtures/canonical")
]

schemas_dir = Path("schemas/v1")

# Build local referencing registry from all schemas in schemas/v1
def build_registry() -> Registry:
    reg = Registry()
    for p in schemas_dir.rglob("*.json"):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "$id" in data:
                res = Resource.from_contents(data)
                reg = reg.with_resource(data["$id"], res)
        except Exception:
            pass
    return reg

fixture_map = {
    "02-yeoman-person.md": ["realms/yeoman.schema.json", "realms/02-yeoman.schema.json"],
    "03-trice-task.md": ["realms/trice.schema.json", "realms/03-trice.schema.json"],
    "04-logbook-day.md": ["realms/logbook.schema.json", "realms/04-logbook.schema.json"],
    "05-quartermaster-receipt.md": ["realms/quartermaster.schema.json", "realms/05-quartermaster.schema.json"],
    "17-supercargo-tool.md": ["realms/supercargo.schema.json", "realms/17-supercargo.schema.json"],
    "06-harbor-route.md": ["realms/06-harbor.schema.json", "realms/harbor.schema.json"],
    "07-press-spec.md": ["realms/07-press.schema.json", "realms/press.schema.json"],
    "08-embers-capture.md": ["realms/08-embers.schema.json", "realms/embers.schema.json"],
    "09-careen-sprint.md": ["realms/09-careen.schema.json", "realms/careen.schema.json"],
    "10-primer-concept.md": ["realms/10-primer.schema.json", "realms/primer.schema.json"]
}

def extract_frontmatter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"{path.name} missing opening frontmatter fence")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path.name} missing closing frontmatter fence")
    return yaml.load(parts[1], Loader=yaml.CSafeLoader if hasattr(yaml, "CSafeLoader") else yaml.SafeLoader)

registry = build_registry()
passed = 0
failed = 0

print("=== Running Bosun Spec 10-Fixture Validation Suite ===")

for file_name, schema_candidates in fixture_map.items():
    # 1. Resolve fixture path
    fixture_path = None
    for f_dir in candidate_fixture_dirs:
        candidate = f_dir / file_name
        if candidate.exists():
            fixture_path = candidate
            break

    if not fixture_path:
        print(f"MISSING FIXTURE: {file_name}")
        failed += 1
        continue

    # 2. Resolve schema path
    schema_path = None
    for s_rel in schema_candidates:
        candidate = schemas_dir / s_rel
        if candidate.exists():
            schema_path = candidate
            break

    if not schema_path:
        print(f"MISSING SCHEMA: {schema_candidates[0]}")
        failed += 1
        continue

    # 3. Validate against Draft 2020-12 using the local registry
    try:
        schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema_data, registry=registry)
        data = extract_frontmatter(fixture_path)
        errors = list(validator.iter_errors(data))

        if errors:
            print(f"FAIL  {file_name}")
            for err in errors:
                print(f"      -> {err.message} at path: {list(err.path)}")
            failed += 1
        else:
            print(f"PASS  {file_name}")
            passed += 1
    except Exception as e:
        print(f"ERROR {file_name}: {e}")
        failed += 1

print(f"\nResult: {passed}/{passed + failed} canonical fixtures passed")
if failed > 0:
    sys.exit(1)
