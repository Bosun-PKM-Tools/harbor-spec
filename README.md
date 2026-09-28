# Harbor Spec

[![Namespace](https://img.shields.io/badge/namespace-Bosun--PKM--Tools-1B4F72)](https://alanwoodyard.com)
[![Stack](https://img.shields.io/badge/stack-Python_stdlib_JSON_Schema-1A5276)](https://alanwoodyard.com)
[![IP](https://img.shields.io/badge/IP-open__core_%7C_MIT_OR_Apache--2.0-196F3D)](https://alanwoodyard.com)

[Alan Woodyard](https://alanwoodyard.com)

## System Role

Harbor Spec is the formal specification repository for Harbor and the Knowledge Processing Protocol. It holds the RFC contracts, realm URN registry, and the Python linters that check those contracts. Implementations (Marlinspike, Harbormaster, Charthouse) enforce or validate against this tree. They do not redefine it.

The GitHub repository was renamed from `bosun-spec` to `harbor-spec` under `Bosun-PKM-Tools`. The local package name in `pyproject.toml` is still `bosun-spec` 0.1.0. Remote name and checkout directory are `harbor-spec`.

Registered tagline: open specification and realm URN registry for the Bosun substrate. Harvest maturity: working core (6,026 implementation LOC, 8,557 test LOC).

## Audited Architecture & Runtime

Python, standard library. The audit recorded no third-party imports. Tooling is a set of `__main__` scripts under `scripts/`:

| Script | Role |
| --- | --- |
| `lint_realm_schemas.py` | Lint realm JSON Schemas |
| `lint_relations_graph.py` | Lint the relations graph |
| `telemetry_contracts.py` | Telemetry contract checks |
| `postel_coercion.py` | Postel-style coercion fixtures |
| `graph_query.py` | Graph query helper |
| `bench_graph_traversal.py` | Traversal benchmark |
| `generate_realm_templates.py` | Realm template generator |
| `generate_synthetic_vault.py` | Synthetic vault fixture generator |
| `scaffold_fleet_vault.py` | Fleet vault scaffold |
| `parquet_codec.py` | Parquet codec experiment |

RFC and contract documents:

- `docs/harbormaster-protocol-v1-rfc.md` — Harbormaster protocol v1 RFC
- `docs/SPEC_CONTRACTS.md` — specification contracts
- `docs/event-vocab-v0.md` — event vocabulary
- `docs/USER_1_QUICKSTART.md` — quickstart
- `schemas/` — JSON Schema sources
- `fixtures/canonical/` — canonical fixtures, including `07-press-spec.md`

Fleet relationships: Marlinspike `enforces_spec` in process. Harbormaster `validates_payloads` in process. Charthouse keeps manuscript storage inside this boundary in process.

## CLI / API Surface

No console script entry points are declared in packaging. Invoke the linters as modules:

```text
python scripts/lint_realm_schemas.py
python scripts/lint_relations_graph.py
python scripts/telemetry_contracts.py
python scripts/postel_coercion.py
python scripts/graph_query.py
```

There is no HTTP server and no JSON-RPC server in this repository. The API surface is the document contract: realm URNs, event vocabulary, and the Harbormaster protocol RFC. Callers in other repositories must match those names.

## Operational Boundaries

Public open core. License posture: MIT OR Apache-2.0. Visibility `public`.

This repository is normative text and linters. It does not store vaults, manuscripts, or telemetry samples from production machines. Synthetic generators (`generate_synthetic_vault.py`, `scaffold_fleet_vault.py`) exist to feed tests. Ship contract changes here before implementations start accepting a new method or realm.
