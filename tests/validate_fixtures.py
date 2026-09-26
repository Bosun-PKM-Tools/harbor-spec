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
    # Wave 1 (Core 5)
    "02-yeoman-person.md": ["realms/yeoman.schema.json", "realms/02-yeoman.schema.json"],
    "03-trice-task.md": ["realms/trice.schema.json", "realms/03-trice.schema.json"],
    "04-logbook-day.md": ["realms/logbook.schema.json", "realms/04-logbook.schema.json"],
    "05-quartermaster-receipt.md": ["realms/quartermaster.schema.json", "realms/05-quartermaster.schema.json"],
    "17-supercargo-tool.md": ["realms/supercargo.schema.json", "realms/17-supercargo.schema.json"],
    # Wave 2 (Realms 06-10)
    "06-harbor-route.md": ["realms/06-harbor.schema.json", "realms/harbor.schema.json"],
    "07-press-spec.md": ["realms/07-press.schema.json", "realms/press.schema.json"],
    "08-embers-capture.md": ["realms/08-embers.schema.json", "realms/embers.schema.json"],
    "09-careen-sprint.md": ["realms/09-careen.schema.json", "realms/careen.schema.json"],
    "10-primer-concept.md": ["realms/10-primer.schema.json", "realms/primer.schema.json"],
    # Wave 3 (Realms 11-15)
    "11-passage-itinerary.md": ["realms/11-passage.schema.json", "realms/passage.schema.json"],
    "12-galley-recipe.md": ["realms/12-galley.schema.json", "realms/galley.schema.json"],
    "13-pratique-telemetry.md": ["realms/13-pratique.schema.json", "realms/pratique.schema.json"],
    "14-tactician-regatta.md": ["realms/14-tactician.schema.json", "realms/tactician.schema.json"],
    "15-drydock-parcel.md": ["realms/15-drydock.schema.json", "realms/drydock.schema.json"],
    # Wave 4 (Realms 16, 18, 19, 20, 21)
    "16-squadron-vehicle.md": ["realms/16-squadron.schema.json", "realms/squadron.schema.json"],
    "18-commonplace-book.md": ["realms/18-commonplace.schema.json", "realms/commonplace.schema.json"],
    "19-chantey-episode.md": ["realms/19-chantey.schema.json", "realms/chantey.schema.json"],
    "20-marquee-rush.md": ["realms/20-marquee.schema.json", "realms/marquee.schema.json"],
    "21-scrimshaw-cam.md": ["realms/21-scrimshaw.schema.json", "realms/scrimshaw.schema.json"],
    # Wave 5 (Realms 22-26)
    "22-traverse-survey.md": ["realms/22-traverse.schema.json", "realms/traverse.schema.json"],
    "23-docent-citation.md": ["realms/23-docent.schema.json", "realms/docent.schema.json"],
    "24-proctor-contract.md": ["realms/24-proctor.schema.json", "realms/proctor.schema.json"],
    "25-ropewalk-repo.md": ["realms/25-ropewalk.schema.json", "realms/ropewalk.schema.json"],
    "26-gavel-minutes.md": ["realms/26-gavel.schema.json", "realms/gavel.schema.json"],
    # Wave 6 (Realms 27-31)
    "27-lineage-individual.md": ["realms/27-lineage.schema.json", "realms/lineage.schema.json"],
    "28-legacy-trust.md": ["realms/28-legacy.schema.json", "realms/legacy.schema.json"],
    "29-arbor-cultivar.md": ["realms/29-arbor.schema.json", "realms/arbor.schema.json"],
    "30-the_glass-barometer.md": ["realms/30-the_glass.schema.json", "realms/the_glass.schema.json"],
    "31-dispatch-letter.md": ["realms/31-dispatch.schema.json", "realms/dispatch.schema.json"]
}

def extract_frontmatter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8").lstrip("\r\n\ufeff")
    if not raw.startswith("---"):
        raise ValueError(f"{path.name} missing opening frontmatter fence")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path.name} missing closing frontmatter fence")
    return yaml.load(parts[1], Loader=yaml.CSafeLoader if hasattr(yaml, "CSafeLoader") else yaml.SafeLoader)

registry = build_registry()
passed = 0
failed = 0

print("=== Running Bosun Spec 30-Fixture Validation Suite ===")

for file_name, schema_candidates in fixture_map.items():
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
