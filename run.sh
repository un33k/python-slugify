#!/bin/bash
# Usage:  ./run.sh baseline      (10 runs, no harness)
#         ./run.sh harness       (10 runs, with CLAUDE.md + hook)
#         ./run.sh summary       (print the results table)
#         ./run.sh baseline 1     (optional 2nd arg = number of runs, e.g. 1 for a test run)
# Run it from the folder that contains this file AND the python-slugify folder.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
REPO="${REPO:-$HERE/python-slugify}"
RES="$HERE/results"
MODE="${1:-}"
N="${2:-10}"
mkdir -p "$RES"

if [ "$MODE" = "summary" ]; then python3 "$HERE/summarize.py" "$RES"; exit 0; fi
if [ "$MODE" != "baseline" ] && [ "$MODE" != "harness" ]; then
  echo "Usage: ./run.sh baseline|harness|summary [runs]"; exit 1; fi

cd "$REPO" || { echo "Can't find $REPO"; exit 1; }
source .venv/bin/activate || { echo "venv missing: create it first"; exit 1; }
command -v claude >/dev/null || { echo "claude not installed"; exit 1; }

# keep git from ever touching the venv or our own result files
grep -qx ".venv" .git/info/exclude 2>/dev/null || echo ".venv" >> .git/info/exclude

# The starting point = original code, no harness. Saved once, reused by both conditions.
if [ ! -f "$RES/base_commit.txt" ]; then
  if [ -n "$(git status --porcelain)" ]; then
    echo "Repo has uncommitted changes. Commit or stash them first, then re-run."; exit 1; fi
  git rev-parse HEAD > "$RES/base_commit.txt"
fi
BASE="$(cat "$RES/base_commit.txt")"

export HOOK_LOG="$RES/hook_blocks_$MODE.log"
CSV="$RES/$MODE.csv"
[ -f "$CSV" ] || echo "run,pass,turns,cost_usd,reason" > "$CSV"

for i in $(seq 1 "$N"); do
  echo "=== $MODE run $i of $N ==="
  git reset --hard "$BASE" -q
  git clean -fd -q
  if [ "$MODE" = "harness" ]; then
    cp "$HERE/harness/CLAUDE.md" .
    mkdir -p .claude && cp -R "$HERE/harness/.claude/." .claude/
  fi

  claude -p "$(cat "$HERE/task.txt")" \
    --output-format json \
    --max-turns 40 \
    --allowedTools "Read" "Edit" "Write" "MultiEdit" "Glob" "Grep" "Bash(pytest:*)" "Bash(python:*)" "Bash(python3:*)" "Bash(git diff:*)" "Bash(git status:*)" \
    > "$RES/${MODE}_$i.json" 2> "$RES/${MODE}_$i.err"

  RESULT="$(python3 "$HERE/check_task.py" 2>&1 | tail -1)"
  PASS=fail; [ "$RESULT" = "PASS" ] && PASS=pass
  git diff > "$RES/${MODE}_$i.diff"
  git ls-files --others --exclude-standard | grep -v -e '^CLAUDE.md$' -e '^.claude/' >> "$RES/${MODE}_$i.diff" 2>/dev/null

  python3 - "$RES/${MODE}_$i.json" "$i" "$PASS" "$RESULT" >> "$CSV" << 'PY'
import json, sys
f, i, p, reason = sys.argv[1:5]
try:
    d = json.load(open(f))
    turns = d.get("num_turns", ""); cost = d.get("total_cost_usd", d.get("cost_usd", ""))
except Exception:
    turns = cost = ""
print(f'{i},{p},{turns},{cost},"{reason}"')
PY
  echo "  -> $PASS  ($RESULT)"
done
python3 "$HERE/summarize.py" "$RES"
