"""Check published SFT examples without printing message contents."""
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1] / "dataset_optimized"
    seen = set()
    counts = {}
    for split in ("train", "validation", "test"):
        rows = [json.loads(line) for line in (root / f"{split}.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
        for index, row in enumerate(rows):
            assert set(row) == {"input", "output"}, (split, index, "schema")
            assert all(isinstance(v, str) and v.strip() for v in row.values()), (split, index, "empty")
            assert len(row["output"].split()) <= 25, (split, index, "word limit")
            assert row["input"] not in seen, (split, index, "duplicate input")
            seen.add(row["input"])
        counts[split] = len(rows)
    report = json.loads((root / "audit_report.json").read_text(encoding="utf-8"))
    assert sum(counts.values()) == report["optimized_examples"]
    print(json.dumps({"splits": counts, "schema": "input/output", "duplicate_inputs": 0}))


if __name__ == "__main__":
    main()
