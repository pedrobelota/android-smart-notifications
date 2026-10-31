"""Opt-in real-tokenizer regression check. Downloads tokenizer files, never model weights."""
import ast
import json
from pathlib import Path


def main():
    from transformers import AutoTokenizer

    root = Path(__file__).resolve().parents[1]
    notebook = json.loads((root / "notebooks/notification_qlora_pilot.ipynb").read_text(encoding="utf-8"))
    nodes = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        tree = ast.parse("".join(cell["source"]))
        for call in ast.walk(tree):
            if isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute) and call.func.attr == "apply_chat_template":
                assert any(k.arg == "return_dict" for k in call.keywords), "Specify the tokenizer return contract"
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in {"message", "encode"}:
                nodes.append(node)
            elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PROMPT" for t in node.targets):
                nodes.append(node)
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-1b-it")
    scope = {"tokenizer": tokenizer}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "notebook-functions", "exec"), scope)
    counts = {}
    for split in ("train", "validation", "test"):
        rows = [json.loads(line) for line in (root / "dataset_optimized" / f"{split}.jsonl").read_text(encoding="utf-8").splitlines()]
        retained = 0
        for row in rows:
            result = scope["encode"](row)
            ids, labels = result["input_ids"], result["labels"]
            assert isinstance(ids, list) and all(isinstance(x, int) for x in ids)
            assert len(ids) == len(labels) == len(result["attention_mask"])
            boundary = next(i for i, value in enumerate(labels) if value != -100)
            assert boundary > 0 and all(x == -100 for x in labels[:boundary])
            assert labels[boundary:] == ids[boundary:]
            retained += len(ids) <= 768
        counts[split] = {"checked": len(rows), "within_768_tokens": retained}
    print(json.dumps(counts, indent=2))


if __name__ == "__main__":
    main()
