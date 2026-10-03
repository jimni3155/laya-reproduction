import gzip
import json
import random

from src.laya_runner import LayaRunner


BASE_PATH = "../upstream-paper/harness/inputs"

FILE_PATHS = {
    "kny": f"{BASE_PATH}/e2_d1_kny.jsonl.gz",
    "kswap": f"{BASE_PATH}/e2_d1_kswap.jsonl.gz",
    "k01": f"{BASE_PATH}/e2_d1_k01.jsonl.gz",
}

SAMPLE_SIZE = 400
RANDOM_SEED = 42


def load_data(path):
    data = {}

    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            data[record["item_id"]] = record

    return data


def get_question_id(record):
    return next(iter(record["questions"]))


def get_prediction(record, result):
    qid = get_question_id(record)

    answer = result["answers"][qid]
    selected_key = answer["choice"]

    criteria = record["questions"][qid]["criteria"]
    selected_meaning = criteria[selected_key]

    return selected_key, selected_meaning


def get_gold_meaning(record):
    qid = get_question_id(record)

    gold_key = record["gold"][qid]["label"]
    criteria = record["questions"][qid]["criteria"]

    return criteria[gold_key]


def calculate_flip_rate(base_predictions, other_predictions, sample_ids):
    flips = 0

    for item_id in sample_ids:
        if base_predictions[item_id] != other_predictions[item_id]:
            flips += 1

    return flips, flips / len(sample_ids)


# load three naming conditions
datasets = {}

for condition, path in FILE_PATHS.items():
    datasets[condition] = load_data(path)


# use only examples that exist in all three conditions
shared_ids = (
    set(datasets["kny"].keys())
    & set(datasets["kswap"].keys())
    & set(datasets["k01"].keys())
)

shared_ids = sorted(shared_ids)

print(f"Shared examples: {len(shared_ids)}")


# sample the same examples for every condition
random.seed(RANDOM_SEED)

if SAMPLE_SIZE < len(shared_ids):
    sample_ids = random.sample(shared_ids, SAMPLE_SIZE)
else:
    sample_ids = shared_ids


runner = LayaRunner()

predictions = {
    "kny": {},
    "kswap": {},
    "k01": {},
}

correct_counts = {
    "kny": 0,
    "kswap": 0,
    "k01": 0,
}


for i, item_id in enumerate(sample_ids):
    print(f"\n[{i + 1}/{len(sample_ids)}] {item_id}")

    for condition in ["kny", "kswap", "k01"]:
        record = datasets[condition][item_id]

        result = runner.predict(
            record["state"],
            record["questions"],
        )

        selected_key, selected_meaning = get_prediction(record, result)
        gold_meaning = get_gold_meaning(record)

        predictions[condition][item_id] = selected_meaning

        is_correct = selected_meaning == gold_meaning

        if is_correct:
            correct_counts[condition] += 1

        print(
            f"{condition:6s} "
            f"key={selected_key:4s} "
            f"correct={'Y' if is_correct else 'N'}"
        )


# accuracy for each naming condition
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)

for condition in ["kny", "kswap", "k01"]:
    accuracy = correct_counts[condition] / len(sample_ids)
    print(f"{condition:6s} accuracy: {accuracy:.4f}")


# compare semantic decisions against the aligned no/yes condition
swap_flips, swap_rate = calculate_flip_rate(
    predictions["kny"],
    predictions["kswap"],
    sample_ids,
)

digit_flips, digit_rate = calculate_flip_rate(
    predictions["kny"],
    predictions["k01"],
    sample_ids,
)

print()

print(
    f"kny -> kswap semantic flips: "
    f"{swap_flips}/{len(sample_ids)} "
    f"({swap_rate * 100:.1f} per 100 decisions)"
)

print(
    f"kny -> k01 semantic flips: "
    f"{digit_flips}/{len(sample_ids)} "
    f"({digit_rate * 100:.1f} per 100 decisions)"
)