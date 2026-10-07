# Harness experiment report

**Repo:** un33k/python-slugify (forked)  
**Task:** add `is_slug(text, separator='-')` (new small feature; exact wording in `task.txt`)  
**Pass =** full `pytest` passes AND `is_slug` behaves correctly AND a new test file for it exists AND no existing test file was edited (see `check_task.py`).

## Results

PASTE THE TABLE PRINTED BY `./run.sh summary` HERE, for example:

| Condition | Passed | Avg turns | Avg cost (USD) | Hook blocks |
|---|---|---|---|---|
| baseline (10 runs) | ?/10 | ? | ? | 0 |
| harness (10 runs) | ?/10 | ? | ? | ? |

Per-run data: `results/baseline.csv`, `results/harness.csv`.

## Which harness change did the work?

WRITE ONE PARAGRAPH. Look at: how many times the hook fired (`results/hook_blocks_harness.log`),
whether harness runs used fewer turns (did Claude stop hunting for the test command / where to export?),
and whether baseline runs edited existing tests or forgot `__all__`/`__init__` (check `results/baseline_N.diff`).
Name one change and give evidence from a specific run.

## What 20 runs cannot tell you

WRITE ONE HONEST PARAGRAPH. Ideas: only one task, so no generalisation; 10 runs per condition is too few
to separate a real effect from luck (7/10 vs 9/10 could be noise); model output varies run to run; my pass
check cannot judge code quality or style; cost depends on caching; CLAUDE.md and the hook were tested
together, so I cannot say which one caused a difference unless I run each alone.
