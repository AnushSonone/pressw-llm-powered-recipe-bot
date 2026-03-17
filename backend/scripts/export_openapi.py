"""
Export FastAPI OpenAPI schema to a JSON file (repo root openapi.json).
Run from backend dir: PYTHONPATH=. python scripts/export_openapi.py
"""
import json
from pathlib import Path

# Run from backend/ so that parent is repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT = REPO_ROOT / "openapi.json"


def main() -> None:
    from main import app

    schema = app.openapi()
    OUTPUT.write_text(json.dumps(schema, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
