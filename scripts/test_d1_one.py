import gzip
import json

from src.laya_runner import LayaRunner


path = "../upstream-paper/harness/inputs/d1_neutral.jsonl.gz"

with gzip.open(path, "rt", encoding="utf-8") as f:
    record = json.loads(next(f))

runner = LayaRunner()

result = runner.predict(
    record["state"],
    record["questions"],
)

print("\n=== MODEL OUTPUT ===")
print(json.dumps(result, indent=2, ensure_ascii=False))

print("\n=== GOLD ===")
for qid, gold in record["gold"].items():
    print(qid, "->", gold["label"])