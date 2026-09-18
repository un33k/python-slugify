# DOJO.md

The source repository is `python-slugify/`. This is the single, top-level guidance file; there is no per-repo `DOJO.md` inside `python-slugify/`.

## Compatibility comes first

- We do not change legacy architecture. Legacy stays in the past: its behavior, output pipeline, and code paths are frozen and must not be altered, refactored, "improved", or "fixed". The frozen legacy implementation lives in its own module (`slugify/_legacy.py`); any change to that file that alters legacy output is rejected on principle. The only permitted changes to legacy are those that do not alter its behavior at all (verified against the frozen baseline). All new work targets the explicit `algorithm='modern'` opt-in.
- Many deployed sites depend on exact slug output. Existing calls must retain legacy behavior: `algorithm='legacy'` is the permanent default. Output-changing improvements require explicit `algorithm='modern'` opt-in; do not silently switch the default in a future release.
- Preserve the original upstream legacy test suite unchanged. It lives frozen at `tests/test_legacy.py` (the original `test.py`, contents unchanged), mirroring the frozen `slugify/_legacy.py` code split. Add new/modern coverage in separate files under `tests/` (e.g. `tests/test_release.py`); keep legacy and modern test coverage separate and do not edit the legacy suite. Compare default and explicit legacy behavior against the frozen baseline using identical transliteration backends/dependency versions.
- Preserve the public `smart_truncate` contract. Modern slug generation uses separate internal handling; do not silently apply its semantics to old helper calls.
- Keep existing stored URLs/keys unchanged. Applications own migration, aliases, redirects and collision detection. Slug generation cannot automatically know which URL exists in a database.
- Passing tests establishes tested behavior, not universal compatibility. Report concrete gaps honestly. The CLI regex-forwarding correction is a documented intentional exception to old CLI behavior.

## Dependencies and licensing

- Project license: MIT. Do not silently introduce a GPL-only default dependency or change transliteration defaults.
- Prefer appropriately licensed Creative Commons material for documentation/media (especially CC0 or CC BY, preserving attribution). Check the exact variant and its restrictions; Creative Commons is not a single license and is generally not the right license family for software dependencies.
- For software, prefer suitable permissive licenses such as MIT, ISC, BSD or Apache-2.0 when evaluating new dependencies. Do not replace an existing backend solely for licensing preference if that changes legacy output; propose a compatible, explicit opt-in alternative.
- Base dependency `text-unidecode` offers an Artistic-or-GPL licensing choice; do not describe it as GPL-only or claim blanket legal safety.
- `Unidecode` is GPL-licensed and optional. Historical `backend='auto'` prefers it if already installed, otherwise text-unidecode. Preserve this behavior for compatibility; document the licensing implications.
- AnyASCII is ISC-licensed and explicitly opt-in. Its installation must not change auto selection.
- Extras add dependencies; selecting an extra/backend does not remove text-unidecode. Inspect actual dependency license files and metadata when changing dependencies. Do not equate runtime selection with installation licensing.

## Validation and releases

- Default upstream branch is `master`, not `main`.
- Run the unchanged legacy suite, separate release/differential checks, supported interpreter/backend tox matrix, typing/style checks, and wheel/sdist artifact validation before releases. Record actual platform and dependency coverage; never infer untested results.
- Use `tools/check_dist.py` for isolated build/artifact checks. Use build/Twine, not a `setup.py publish` shortcut.
- User prefers plain release versions (for example `9.0.0`), not an unsolicited `.dev0` suffix. A version string is not evidence of publication.
- Publishing, pushing, PR creation/closure, merges and tags require applicable explicit user authorization. Publishing to PyPI does not authorize a GitHub release or tag.
- Never put tokens in source, logs, chat or command arguments. Use securely configured credentials only with the authorized official destination. Do not record credential backup paths here.
- Verify published artifact hashes against validated local builds. After publication, update current README/install/migration guidance; preserve historical verification notes as dated evidence.

## Issue and PR handling

- Read each item and verify what the implementation actually addresses. Distinguish incorporated, superseded, partially addressed, declined and deferred work, including modern-only fixes.
- When authorized to consolidate/close items, add an individual explanatory cross-reference to the aggregate PR and a disposition index there. Credit contributors; never represent a closed-unmerged PR as merged or deferred work as implemented.
- Identify agent-authored interactions as Dojo. For every Dojo-authored interaction in this repository—including opening, replying to, reviewing, or closing issues, pull requests, discussions, and releases—end the authored body or comment with the following attribution as the final line, separated from preceding content by a blank line: `🚀 Generated with [Dojo](https://heydojo.ai) ⛩️`
- Do not blanket-close unrelated items or merge PRs without authorization. A merged PR does not mean a package was published.
- Historical review drafts may predate compatibility decisions: check current source and migration documentation before posting them.
- Licensing questions deserve calm, factual answers, not dismissal or blanket assurances. Separate this project's MIT license, installed dependency licenses, and runtime backend selection. Link the current README licensing section, migration guide, and relevant upstream license files; explain available choices and their limits.
- When authorized to close a licensing item that is answered or duplicates an existing discussion, leave a respectful explanation and direct links to the authoritative documentation or tracking item. State whether it was answered, superseded, declined or deferred. Do not close a new unresolved licensing defect merely because similar questions recur. Never claim that an optional extra removes base dependencies, that GPL-associated means GPL-only, or that documentation constitutes legal advice.
