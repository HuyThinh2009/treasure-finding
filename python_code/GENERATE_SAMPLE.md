# generate_sample.py

Generates grid-view samples as JSON files, one sample per file.

## Usage

```bash
python generate_sample.py -f 10
```

Creates `samples/sample_001.json` ... `samples/sample_010.json`.

## Arguments

| Argument | Description | Default |
|---|---|---|
| `-f`, `--files` | Number of files to generate | `1` |
| `-o`, `--output-dir` | Folder to write the files into (created if missing) | `samples` |
| `--prefix` | File name prefix (`<prefix>_001.json`, ...) | `sample` |
| `-n` | View distance from the center; the view is `(2n+1) x (2n+1)` | `2` |
| `--wall-prob` | Probability that a cell is a wall (`"1"`) | `0.3` |
| `--min-path` | Minimum length of `result` | `1` |
| `--wall-outside-map` | Mark cells with negative row/column (outside the map) as walls | off |
| `--seed` | Random seed, for reproducible output | none |

Examples:

```bash
python python_code/generate_sample.py -f 100 -n 3 -o samples/7x7      # 100 files, 7x7 views, in ./out
python python_code/generate_sample.py -f 5 --seed 42          # same files on every run
python python_code/generate_sample.py -f 50 --prefix train    # train_001.json, ...
```

## JSON format

```json
{
  "view": [
    ["1", "1", "0"],
    ["0", "P", "0"],
    ["0", "1", "0"]
  ],
  "target": {"row": 10, "column": 10},
  "result": [1, 2]
}
```

| Field | Description |
|---|---|
| `view` | `(2n+1) x (2n+1)` grid. `"P"` is the player, always at the center and at absolute position (0, 0). `"1"` is a wall, `"0"` is a free cell. |
| `target` | Always row 10, column 10. |
| `result` | Shortest path from `P` to the reachable cell closest to the target, as a list of moves. |

Moves in `result`:

| Value | Direction |
|---|---|
| `0` | up |
| `1` | right |
| `2` | down |
| `3` | left |