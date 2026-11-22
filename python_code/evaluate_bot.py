"""Evaluate a bot (your model) against sample JSON files.

For every sample the harness:
  1. reads the sample JSON (view, target, result)
  2. gives the bot the current player position, the view and the target
  3. asks the bot to build one input per direction          -> Bot.build_inputs()
  4. asks the bot to score the 4 directions                 -> Bot.predict()
  5. moves the player in the direction with the highest score
  6. repeats 3-5 until the player leaves the view (or can't move any further),
     then compares the path taken with "result" from the sample
  7. reports the accuracy over all samples

Directions (index in every list): 0 = up, 1 = right, 2 = down, 3 = left.

Usage
  python evaluate_bot.py                                  # built-in BasicBot on ./samples
  python evaluate_bot.py -s samples -b my_model:MyBot     # your bot, class MyBot in my_model.py
  python evaluate_bot.py -s samples/sample_001.json -v    # one file, print every sample
"""

import argparse
import glob
import importlib
import json
import os
import sys
from collections import Counter
from bot import BasicBot
from state_const import DIRS, START, Episode, State


def run_episode(bot, sample, max_steps=None):
    view = sample["view"]
    size = len(view)
    n = size // 2
    target = (sample["target"]["row"], sample["target"]["column"])
    if max_steps is None:
        max_steps = size * size  # a shortest path can never be longer than this

    pos = START
    path = []
    reason = "max_steps"
    all_scores = []
    for step in range(max_steps):
        vr, vc = n + pos[0], n + pos[1]
        state = State(
            view=view, position=pos, view_position=(vr, vc), target=target, step=step
        )

        inputs = bot.build_inputs(state)
        if len(inputs) != 4:
            raise ValueError(f"build_inputs() must return 4 items, got {len(inputs)}")
        scores = bot.predict(inputs)
        all_scores.append(scores)
        if len(scores) != 4:
            raise ValueError(f"predict() must return 4 scores, got {len(scores)}")

        direction = max(range(4), key=lambda i: scores[i])  # ties -> lowest index

        dr, dc = DIRS[direction]
        if 0 == vr or vr == size - 1 or 0 == vc or vc == size - 1:
            reason = "exit_view"  # Player is standing on the edge of the view
            break
        nr, nc = vr + dr, vc + dc
        if not (0 <= nr < size and 0 <= nc < size):
            reason = (
                "exit_view"  # the move that leaves the view is not part of the path
            )
            break
        if view[nr][nc] == "1":
            reason = "hit_wall"  # blocked by a wall, the bot can't continue
            break
        pos = (pos[0] + dr, pos[1] + dc)
        path.append(direction)

    return Episode(path, pos, reason, all_scores=all_scores)


def end_position(moves):
    r, c = START
    for m in moves:
        r += DIRS[m][0]
        c += DIRS[m][1]
    return (r, c)


def load_samples(path):
    if os.path.isdir(path):
        files = sorted(glob.glob(os.path.join(path, "*.json")))
    else:
        files = [path]
    if not files:
        raise SystemExit(f"No .json files found in {path}")

    samples = []
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        items = data if isinstance(data, list) else [data]
        for i, item in enumerate(items):
            name = os.path.basename(fp) + (f"[{i}]" if isinstance(data, list) else "")
            samples.append((name, item))
    return samples


def load_bot(spec):
    if not spec:
        return BasicBot()
    if ":" not in spec:
        raise SystemExit("--bot must look like module:ClassName (e.g. my_model:MyBot)")
    module_name, class_name = spec.split(":", 1)
    sys.path.insert(0, os.getcwd())
    bot = getattr(importlib.import_module(module_name), class_name)()
    if not (hasattr(bot, "build_inputs") and hasattr(bot, "predict")):
        raise SystemExit(f"{spec} must implement build_inputs() and predict()")
    return bot


def evaluate(bot, samples, max_steps=None, verbose=False, verbose_failed=False):
    total = len(samples)
    exact = 0
    end_ok = 0
    reasons = Counter()

    for name, sample in samples:
        ep = run_episode(bot, sample, max_steps)
        expected = sample["result"]
        is_exact = ep.path == expected
        is_end = ep.final_position == end_position(expected)
        exact += is_exact
        end_ok += is_end
        reasons[ep.stop_reason] += 1
        if verbose:
            tag = "OK  " if is_exact else "FAIL"
            print(
                f"{tag} {name}  expected={expected}  got={ep.path}  stop={ep.stop_reason}"
            )
            for i, scores in enumerate(ep.all_scores):
                print(f"  step {i:02d}: scores={scores}")
        elif verbose_failed and not is_exact:
            print(
                f"FAIL {name}  expected={expected}  got={ep.path}  stop={ep.stop_reason}"
            )
            for i, scores in enumerate(ep.all_scores):
                print(f"  step {i:02d}: scores={scores}")

    print()
    print(f"Samples:           {total}")
    print(
        f"Exact path match:  {exact}/{total} ({100 * exact / total:.2f}%)  <- accuracy"
    )
    print(f"Same end cell:     {end_ok}/{total} ({100 * end_ok / total:.2f}%)")
    print(
        "Stopped by:        "
        + ", ".join(f"{k}={v}" for k, v in sorted(reasons.items()))
    )
    return exact / total


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "-s",
        "--samples",
        default="samples",
        help="sample .json file or a directory of them (default ./samples)",
    )
    ap.add_argument(
        "-b",
        "--bot",
        default=None,
        help="your bot as module:ClassName (default: built-in BasicBot)",
    )
    ap.add_argument(
        "--max-steps",
        type=int,
        default=None,
        help="safety limit on moves per sample (default (2n+1)^2)",
    )
    ap.add_argument(
        "-v", "--verbose", action="store_true", help="print the result of every sample"
    )
    ap.add_argument(
        "-vf",
        "--verbose_failed",
        action="store_true",
        help="print the result of every failed sample",
    )
    args = ap.parse_args()

    samples = load_samples(args.samples)
    bot = load_bot(args.bot)
    evaluate(bot, samples, args.max_steps, args.verbose, args.verbose_failed)


if __name__ == "__main__":
    main()
