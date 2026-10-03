# Laya Reproduction

A lightweight reproduction of selected Laya experiments from the System One decision-model benchmark.

## Overview

This repository evaluates the official Laya checkpoint on two small-scale experiments:

1. a D1 typed-decision sanity check
2. the full D1 binary option-name robustness evaluation

The goal is not to reproduce the entire benchmark, but to reproduce one characteristic robustness issue reported for Laya: sensitivity to superficial changes in option names.

## Model

- Model: `convaiinnovations/laya`
- Checkpoint: English Laya checkpoint
- Interface: official `laya` Python package
- Output: probability distribution over explicitly defined options

Laya receives a structured state and typed questions, and returns a decision over the provided options.

## Experiment 1: D1 Sanity Evaluation

A preliminary evaluation was run on the first 20 records of the frozen `d1_neutral` input.

Each record contains five typed questions, resulting in 100 decisions in total.

| Metric | Result |
|---|---:|
| Records | 20 |
| Decisions | 100 |
| Accuracy | 42.0% |
| Mean top probability | 0.5736 |

This experiment is only a pipeline sanity check.

The subset consists of the first 20 records rather than a random or full benchmark sample, so the result should not be directly compared with the full D1 benchmark.

## Experiment 2: Option-Name Robustness

The full set of 400 shared D1 binary examples was evaluated under three frozen naming conditions.

- `kny`: semantically aligned `no/yes`
- `kswap`: the meanings associated with `yes/no` are swapped
- `k01`: options are named `0/1`

For robustness evaluation, predictions are compared by the semantic description associated with the selected option rather than by the surface option key.

For example, selecting `no` under `kny` and `yes` under `kswap` is not counted as a semantic flip if both keys refer to the same underlying description.

## Results

### Accuracy

| Condition | Accuracy |
|---|---:|
| aligned `no/yes` (`kny`) | 44.75% |
| swapped `yes/no` (`kswap`) | 53.75% |
| digits `0/1` (`k01`) | 48.25% |

### Semantic Flip Rate

| Comparison | Semantic Flips |
|---|---:|
| `kny → kswap` | **372 / 400 (93.0%)** |
| `kny → k01` | **74 / 400 (18.5%)** |

## Key Observation

The swapped `yes/no` condition changed the selected semantic decision in 93% of the 400 examples.

Interestingly, aggregate accuracy did not decrease under the swapped condition. In fact, `kswap` achieved a slightly higher accuracy than `kny`.

This illustrates why aggregate accuracy alone can hide severe instance-level instability: two conditions may have similar or even improved overall accuracy while producing very different decisions on the same examples.

The result reproduces the strong option-name sensitivity reported for Laya in the benchmark study.

## Repository Structure

```text
laya-reproduction/
├── data/
│   └── .gitkeep
├── results/
│   ├── d1_results.json
│   └── option_name_results.json
├── scripts/
│   ├── test_laya.py
│   ├── test_d1_one.py
│   ├── run_d1.py
│   └── run_option_names.py
├── src/
│   ├── __init__.py
│   └── laya_runner.py
├── .gitignore
├── requirements.txt
└── README.md