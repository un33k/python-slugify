# Local verification — 9.0.0

## Latest algorithm opt-in verification — 2026-09-08

Version remains `9.0.0`, without a development suffix. All changes are local and uncommitted.
Nothing was staged, committed, pushed, tagged, published, or posted to an issue/PR.

**Result: the full local tox matrix and release checks pass.** The previous compatibility blocker
was reproduced and addressed by restoring the historical pipeline as the permanent default and
requiring explicit `algorithm='modern'` adoption. This is scoped compatibility evidence, not a
universal regression-free or deployment-safety guarantee.

### Interpreter/backend matrix

| Interpreter | text-unidecode | isolated Unidecode | AnyASCII + base dependency |
| --- | --- | --- | --- |
| CPython 3.10 | 104 passed | 103 passed, 1 skipped | 104 passed |
| CPython 3.11 | 104 passed | 103 passed, 1 skipped | 104 passed |
| CPython 3.12 | 104 passed | 103 passed, 1 skipped | 104 passed |
| CPython 3.13 | 104 passed | 103 passed, 1 skipped | 104 passed |
| CPython 3.14 | 104 passed | 103 passed, 1 skipped | 104 passed |
| PyPy 3.11 | 104 passed | 103 passed, 1 skipped | 104 passed |

All 18 cells ran on macOS. The six skips deliberately omit the fallback-package test in environments
where text-unidecode has been removed to isolate Unidecode. AnyASCII cells separately assert explicit
AnyASCII goldens while auto still selects the base text-unidecode dependency.
Dependency versions: text-unidecode 1.3, Unidecode 1.4.0, AnyASCII 0.3.3.

### Compatibility and opt-in contracts

- A frozen implementation from baseline `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4` is retained in
  `tools/legacy_reference.py`. It is a test oracle, not shipped runtime code. Its historical formatting
  is intentionally excluded from style modernization.
- Every matrix cell compares **2,688 input/option combinations** against the baseline, for both default
  calls and explicit legacy calls. Additional fresh-iterator checks cover replacement replay and
  case-sensitive stopword consumption. Public smart_truncate checks cover 256 combinations, including
  matching empty-separator exceptions and negative-limit behavior.
- The entire legacy `test.py` is byte-for-byte unchanged from baseline
  `7b6d5d96c1995e6dccb39a19a13ba78d7d0a3ee4`, verified with
  `git diff --exit-code -- test.py` and `git diff --exit-code 7b6d5d9 -- test.py`.
  All additional regression tests live independently in `test_release.py`; no baseline assertions are edited.
- Independent CLI tests assert exact historical default namespace and forwarded-parameter shapes, plus
  explicit forwarding of every algorithm, backend, replacement-stage choice and regex patterns (including
  an empty pattern). Omitted new options defer to API defaults; regex is forwarded only when supplied.
- Explicit modern tests cover early entity decoding, per-reference invalid numeric handling, generator
  snapshots, empty/wide separator budgets, and delimiters overlapping literal word characters.
- `xylophone x` with separator `x` and a large positive limit retains `xylophonexx` in both algorithms.
- Keyword-only/default signature checks and invalid algorithm checks run in source and installed API tests.
- CLI tests cover default, explicit legacy, explicit modern, rejected unknown algorithms, regex forwarding,
  and both module and console invocation for installed artifacts.

### Other checks

- Coverage gate: **99% aggregate**, 734 statements, 1 missed statement, 118 branches, 2 partial branches.
  The existing 97% gate was unchanged. Coverage includes legacy test.py; it is not a library-only metric.
- Strict mypy: no issues in 5 source files.
- pycodestyle and flake8: passed; flake8 is now in the default tox environment list.
- Packaging: isolated PEP 517 wheel/sdist builds, `twine check --strict`, archive contents, metadata,
  `pip check`, version agreement, installed API goldens and CLI behavior outside the checkout all passed.
- Both artifacts were checked for MIT License-Expression, Python >=3.10, backend extras, entry point,
  typed marker, and license. Source archive includes regression tools/fixture and migration docs;
  research JSON and bytecode/cache files are excluded.
- Unicode-only runtime checks pass after uninstalling the transliteration dependency in temporary
  artifact environments. This does not imply a dependency-free installation extra exists.
- `git diff --check`: passed.

The initial full run passed all runtime cells, typing, coverage and artifacts, but found an E402 import-order
error in the test wrapper. That error was corrected; the complete matrix and all other tox environments
were rerun successfully. No failing check remains from that run.

The untouched-baseline follow-up added two independent CLI test methods and reran the complete tox suite.
The first follow-up run could not discover the existing Python 3.12 interpreter; adding
`/Users/val/.pyenv/versions/3.12.11/bin` to PATH fixed discovery without changing repository configuration.
The complete rerun passed all 18 runtime cells and every quality/packaging environment (24 environments
including coverage setup/report). The table above records this latest run: 1,866 passes and six deliberate
skips across the runtime matrix.

Logs are retained locally at `/tmp/slugify-untouched-tests-tox.log` (initial follow-up) and
`/tmp/slugify-untouched-tests-tox-final.log` (successful complete rerun). Earlier algorithm opt-in logs remain
at `/tmp/slugify-optin-tox.log` and `/tmp/slugify-optin-tox-final.log`. The established runner was
`/Users/val/.dojo/workspace/scratch/667f1ab2-86f5-49ee-a130-01c846192281/slugify-test-runner/bin/tox`.
Artifacts were validated in temporary directories; these checks do not retain a publishable final artifact set. Rebuild with
`python tools/check_dist.py --outdir /path/to/new-empty-directory` when maintainers authorize final retention.

## Remaining limits and release ownership

Windows/Linux execution, optional dependency lower-bound testing, real downstream stored-slug comparisons,
and full regression execution against installed artifacts remain unverified. Artifact tests are focused API/CLI
checks; matrix suites run from the checkout. Backend upgrades and custom replacement/regex policies can still
change outputs. CLI regex forwarding is intentionally fixed even under legacy mode.

New tests, tools, and docs remain untracked and must be included in an eventual reviewed commit. Final maintainer
review, downstream migration decisions, public replies, publication and tags remain separate actions requiring
approval. README correctly describes an unpublished local checkout; update publication-facing wording only
when an actual publication occurs.

## Prior-run provenance

Earlier pre-opt-in runs passed 99 tests per full backend cell but failed compatibility comparison for entities,
wide/empty separators, iterators and delimiter-overlapping word content. Those test passes did not establish
legacy compatibility. The results above supersede those earlier runtime and compatibility claims.
See [migration.md](migration.md) for the exact legacy/modern boundary and remaining application precautions.
