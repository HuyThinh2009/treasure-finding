"""Generate grid-view sample files (one JSON file per sample).

The player is always at (0, 0) and the target is always at (10, 10), so the
target is always down-right of the player.

Each file looks like:
{
  "view": [["1","0","1"], ["0","P","0"], ["0","1","0"]],   # (2n+1) x (2n+1)
  "target": {"row": 10, "column": 10},
  "result": [1, 2]
}

Rules
- "P" is always the centre of the view (the player, at absolute (1, 1)).
- "1" = wall, "0" = free cell.
- Moves: 0 = up, 1 = right, 2 = down, 3 = left.
- The cell at view offset (dr, dc) from P has absolute position (dr, dc).
- "result" is the shortest path (inside the view) from P to the reachable cell
  that is closest (Manhattan distance) to the target. [] means P is already the
  closest reachable cell.

Examples
  python generate_sample.py -f 10                  # 10 files in ./samples
  python generate_sample.py -f 100 -n 3 -o out     # 100 files, 7x7 views, in ./out
  python generate_sample.py -f 5 --seed 42 --wall-outside-map
"""

import argparse
import json
import os
import random
from collections import deque

PLAYER = (0, 0)  # absolute position of the player, always
TARGET = (10, 10)  # (row, column), always fixed
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # 0 up, 1 right, 2 down, 3 left


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def generate_view(n, wall_prob, rng, wall_outside_map):
    size = 2 * n + 1
    view = [
        ["1" if rng.random() < wall_prob else "0" for _ in range(size)]
        for _ in range(size)
    ]

    # Optionally treat cells with negative row/column (outside the map) as walls.
    if wall_outside_map:
        for r in range(size):
            for c in range(size):
                if PLAYER[0] + r - n < 0 or PLAYER[1] + c - n < 0:
                    view[r][c] = "1"

    view[n][n] = "P"

    # If the target happens to be visible (n >= 10), make sure it is a free cell.
    tr = TARGET[0] - PLAYER[0] + n
    tc = TARGET[1] - PLAYER[1] + n
    if 0 <= tr < size and 0 <= tc < size and (tr, tc) != (n, n):
        view[tr][tc] = "0"
    return view


def solve(view, n):
    """BFS from P; stop at the first cell on the edge of the view.

    Edge cells are terminal: the path ends as soon as it touches one and never
    walks along the edge. Among the edge cells reached this way, the one nearest
    the target wins (ties: shorter path). If P is enclosed and no edge cell is
    reachable, return the path to the reachable cell nearest the target instead.
    """
    size = len(view)
    start = (n, n)

    def dist_to_target(r, c):
        return manhattan((PLAYER[0] + r - n, PLAYER[1] + c - n), TARGET)

    def on_edge(r, c):
        return r in (0, size - 1) or c in (0, size - 1)

    prev = {start: None}
    depth = {start: 0}
    queue = deque([start])
    best = start  # fallback: nearest reachable cell
    best_key = (dist_to_target(*start), 0)  # (distance to target, path length)
    best_edge = None  # nearest edge cell reached
    best_edge_key = None

    while queue:
        r, c = queue.popleft()
        key = (dist_to_target(r, c), depth[(r, c)])
        if on_edge(r, c):
            if best_edge is None or key < best_edge_key:
                best_edge, best_edge_key = (r, c), key
            continue  # stop here, do not expand from an edge cell
        if key < best_key:
            best, best_key = (r, c), key
        for d, (dr, dc) in enumerate(DIRS):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < size
                and 0 <= nc < size
                and view[nr][nc] != "1"
                and (nr, nc) not in prev
            ):
                prev[(nr, nc)] = ((r, c), d)
                depth[(nr, nc)] = depth[(r, c)] + 1
                queue.append((nr, nc))

    cur = best_edge if best_edge is not None else best
    path = []
    while prev[cur] is not None:
        parent, d = prev[cur]
        path.append(d)
        cur = parent
    path.reverse()
    return path


def ends_on_edge(path, n):
    """True if following `path` from the center of the view ends on the edge."""
    size = 2 * n + 1
    r = c = n
    for d in path:
        r += DIRS[d][0]
        c += DIRS[d][1]
    return r in (0, size - 1) or c in (0, size - 1)


def make_sample(n, wall_prob, rng, min_path, wall_outside_map, max_tries=10000):
    for _ in range(max_tries):
        view = generate_view(n, wall_prob, rng, wall_outside_map)
        path = solve(view, n)
        # keep only samples where P can reach the edge of the view
        if len(path) >= min_path and ends_on_edge(path, n):
            return {
                "view": view,
                "target": {"row": TARGET[0], "column": TARGET[1]},
                "result": path,
            }
    raise RuntimeError(
        "Could not generate a sample with the requested constraints; "
        "try a lower --wall-prob or --min-path."
    )


def format_sample(s):
    """Pretty JSON with one view row per line (like the example)."""
    rows = ",\n".join(f"    {json.dumps(r)}" for r in s["view"])
    parts = [
        f'  "view": [\n{rows}\n  ]',
        f'  "target": {json.dumps(s["target"])}',
        f'  "result": {json.dumps(s["result"])}',
    ]
    return "{\n" + ",\n".join(parts) + "\n}"


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "-f",
        "--files",
        type=int,
        default=1,
        help="number of files to generate, one sample per file (default 1)",
    )
    ap.add_argument(
        "-o",
        "--output-dir",
        default="samples",
        help="directory to write the files into (default ./samples)",
    )
    ap.add_argument(
        "--prefix",
        default="sample",
        help="file name prefix, files are named <prefix>_001.json, ... (default 'sample')",
    )
    ap.add_argument(
        "-n",
        type=int,
        default=2,
        help="view distance from centre; view size is (2n+1)x(2n+1) (default 2)",
    )
    ap.add_argument(
        "--wall-prob",
        type=float,
        default=0.3,
        help="probability that a cell is a wall '1' (default 0.3)",
    )
    ap.add_argument(
        "--min-path",
        type=int,
        default=1,
        help="minimum length of 'result' (default 1, i.e. no empty paths)",
    )
    ap.add_argument(
        "--wall-outside-map",
        action="store_true",
        help="mark cells with negative row/column (outside the map) as walls",
    )
    ap.add_argument("--seed", type=int, default=None, help="random seed")
    args = ap.parse_args()

    if args.files < 1:
        ap.error("-f/--files must be >= 1")
    if args.n < 1:
        ap.error("-n must be >= 1")

    os.makedirs(args.output_dir, exist_ok=True)
    rng = random.Random(args.seed)
    width = max(3, len(str(args.files)))

    for i in range(1, args.files + 1):
        sample = make_sample(
            args.n, args.wall_prob, rng, args.min_path, args.wall_outside_map
        )
        path = os.path.join(args.output_dir, f"{args.prefix}_{i:0{width}d}.json")
        with open(path, "w", encoding="utf-8") as f:
            f.write(format_sample(sample) + "\n")

    print(f"Generated {args.files} file(s) in {os.path.abspath(args.output_dir)}")


if __name__ == "__main__":
    main()
