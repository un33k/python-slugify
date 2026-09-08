# Migrating to 9.0.0

This checkout is **unpublished**, with version `9.0.0` and no development suffix.
No commit, push, publication, tag, or public issue reply is part of these local checks.
Historical research remains in [historical-review.md](historical-review.md).

## The default stays legacy

`slugify(..., algorithm='legacy')` is the permanent default. Existing calls retain the historical
slug-output pipeline. Modern behavior requires `algorithm='modern'`, or CLI `--algorithm modern`.
There is no `slugify_v2` function. Unknown algorithm values raise `ValueError` in Python and are
rejected by argparse on the command line. All new controls are keyword-only; existing positional
parameters retain their order.

The compatibility fixture is frozen from revision `7b6d5d9`. Regression checks compare default and
explicit legacy calls to that implementation using the same installed backend. They cover entities,
invalid numeric references, wide/empty separators, case handling, Unicode mode, ordering, length
limits, and fresh replacement/stopword iterators. They are evidence for those cases, not proof
that every downstream application or dependency upgrade is safe.

| Input or option | Default / explicit legacy | Explicit modern |
| --- | --- | --- |
| `a&#39;b` | `ab` | `a-b` |
| `a&eacute;b` | `ae-b` | `aeb` |
| `a&#20320;b` (text-unidecode/Unidecode) | `a-b` | `ani-b` |
| `a b c`, separator `::`, max_length 3 | `a::b` | `a` |
| Replacement iterator `[('a', 'aa')]`, input `a` | `aa` (consumed by first pass) | `aaaa` (snapshotted and replayed) |
| Stopword iterator `['A', 'b']`, lowercase false, input `a b a b` | `a-b-a-b` | `a-a` |
| `xylophone x`, separator `x`, max_length 100 | `xylophonexx` | `xylophonexx` |

## What modern opts into

- Decode entities before quote handling and transliteration, matching literal input where applicable.
- Handle invalid numeric references independently instead of cancelling the substitution for that reference kind.
  Surrogate references are left for ordinary filtering.
- Snapshot replacement rules, including inner iterables, so both passes see the same rules.
- Snapshot stopwords so case-sensitive membership does not depend on iterator consumption.
- Budget the emitted separator width, including empty separators. Internal word boundaries are kept until
  selection/truncation completes. Output delimiters that also occur in words do not erase real characters.
  Hard cuts never emit a partial delimiter; a partial word can be emitted. Whole-word mode may skip oversized
  words unless `save_order=True`; if no word fits, a hard cut is used.

`max_length` in legacy mode applies before separator mapping, so the emitted string may exceed the budget
with wide separators. Modern limits count Python characters, not bytes or grapheme clusters. Nonpositive
limits are unlimited for `slugify` in both modes.

**The public `smart_truncate` is unchanged.** It retains character-set stripping via `str.strip(separator)`,
empty-separator `ValueError`, and negative slicing semantics. Modern slugify uses a separate private helper;
it does not silently modernize calls to this public function.

## Other controls and deliberate CLI fix

`backend='auto'` continues to prefer installed Unidecode, falling back to text-unidecode.
Explicit backend selection never silently falls back; errors inside an installed backend propagate.
`allow_unicode=True` uses NFKC and no transliteration import. The base distribution still depends on
text-unidecode; extras add dependencies, never subtract them. AnyASCII is opt-in and produces different
transliteration and word boundaries. Its presence does not change auto selection.

`replacement_stage='both'` retains two literal ordered passes for reusable rule lists;
`pre` and `post` select just one. Post replacements remain unfiltered, after stopword removal and before
truncation/mapping. Arbitrary replacements and custom regexes are not universally idempotent or safe.
UTF-8 bytes/bytearray remain accepted, with invalid bytes ignored. Decoding now precedes replacements,
so bytes with string replacement rules are supported where older combinations raised TypeError.
Unsupported input types receive an explicit TypeError message.

CLI `--regex-pattern` forwarding is an intentional bug fix in both modes: the flag was previously parsed
but ignored. CLI users who passed that flag should compare outputs. The legacy-default guarantee concerns
the historical Python slug pipeline, not preservation of this CLI forwarding bug.

Both modes retain global dash-to-separator mapping, including literal allowed dashes. There is no new
literal-hyphen preservation API. ASCII and curly apostrophes remain distinct; use explicit pre replacements
if your application needs a consistent apostrophe boundary. Backend-generated phonetic quotes are removed.
Entity flags remain separate; this is not a full HTML parser. Unicode normalization is not exact code-point
preservation, nor is transliteration translation or language detection.

## Application migration and packaging

- Do not regenerate persisted URLs, filenames, or database keys in place. Keep stored identifiers and plan
  redirects and collision handling before adopting modern output.
- Pin this package and transliteration dependencies; compare a representative application corpus before upgrading.
- Python 3.10 is the minimum. Older runtimes can remain on a compatible pinned earlier release.
- Slugs are not guaranteed unique or universally filesystem/URL/security safe. Validate for your destination.
- Metadata, typed marker, source tests, license and entry points are checked in wheel and source artifacts.
  `python tools/check_dist.py` builds and installs in temporary environments without publishing.
- python-slugify is MIT; text-unidecode offers Artistic-or-GPL licensing, Unidecode is GPL, AnyASCII is ISC.
  Review actual dependency licenses and distribution obligations; this is not a blanket legal assurance.

See [verification.md](verification.md) for measured results and remaining platform/downstream gaps.
Maintainers still own final review, downstream compatibility decisions, artifact retention, and separate
explicit authorization of any publication or tags. No published artifacts should be deleted as part of migration.
