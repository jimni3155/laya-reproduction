import gzip
import json
from statistics import mean

from src.laya_runner import LayaRunner


DATA_PATH = "../upstream-paper/harness/inputs/d1_neutral.jsonl.gz"
MAX_RECORDS = 20   # 20 records × 5 questions = 100 decisions


def get_prediction(answer):
    qtype = answer["type"]

    if qtype == "choice":
        return answer["choice"]

    if qtype == "noul":
        p_true = answer["noul"]
        p_false = 1.0 - p_true
        return "true" if p_true > p_false else "false"

    if qtype == "score":
        probs = answer["probabilities"]
        return max(probs, key=probs.get)

    raise ValueError(f"Unknown question type: {qtype}")


def get_top_probability(answer):
    qtype = answer["type"]

    if qtype == "choice":
        return max(answer["probabilities"].values())

    if qtype == "noul":
        p_true = answer["noul"]
        return max(p_true, 1.0 - p_true)

    if qtype == "score":
        return max(answer["probabilities"].values())

    raise ValueError(f"Unknown question type: {qtype}")


runner = LayaRunner()

total = 0
correct = 0
top_probs = []

with gzip.open(DATA_PATH, "rt", encoding="utf-8") as f:
    for record_idx, line in enumerate(f):
        if record_idx >= MAX_RECORDS:
            break

        record = json.loads(line)

        result = runner.predict(
            record["state"],
            record["questions"],
        )

        for qid, answer in result["answers"].items():
            pred = get_prediction(answer)
            gold = record["gold"][qid]["label"]

            total += 1
            correct += int(pred == gold)
            top_probs.append(get_top_probability(answer))

            print(
                f"[{record_idx:02d}] "
                f"{qid:15s} "
                f"pred={pred:5s} "
                f"gold={gold:5s} "
                f"{'✓' if pred == gold else '✗'}"
            )

accuracy = correct / total
mean_top_prob = mean(top_probs)

print("\n=== SUMMARY ===")
print(f"Records: {MAX_RECORDS}")
print(f"Decisions: {total}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.4f}")
print(f"Mean top probability: {mean_top_prob:.4f}")