# Contributing

Thanks for wanting to help. This project keeps contributions simple on purpose.

## Issues first

**Open an issue before writing code.** We do not review unsolicited pull requests.

A pull request costs almost nothing to produce now, but verifying one is the
expensive part, and that cost falls on the maintainer. python-slugify also has a
hard compatibility promise: the default `legacy` output must never change,
because deployed sites depend on the exact slugs it has already produced. Every
proposed change has to be checked against that promise, which takes real time.

So the order is:

1. **Open an issue.** Describe a real problem you ran into. Include the input,
   what you got, what you expected, and the versions involved.
2. **Wait for a decision.** If we agree it needs fixing, we'll say so on the
   issue. Then a pull request is welcome, or we'll fix it ourselves.

A pull request with no linked, agreed issue will be closed with thanks. That is
not a judgment on the code — good work has been turned away for this reason
alone. Security fixes are the one exception.

## What makes an issue easy to act on

- A short, runnable example that shows the problem.
- The `python-slugify` version, the Python version, and which transliteration
  backend you use (`text-unidecode`, `Unidecode`, or `anyascii`).
- Whether the problem is in the default (`legacy`) behavior or in
  `algorithm='modern'`.
- Whether it affects slugs you have already stored.

## If your pull request was agreed

- Branch off `master` and open the pull request against `master`.
- Link the issue, and keep the change as small as the fix allows.
- Never change legacy output. `slugify/_legacy.py` and `tests/test_legacy.py`
  are frozen. Output-changing improvements belong behind the explicit
  `algorithm='modern'` opt-in.
- Add coverage for changed behavior under `tests/`.
- Run the checks before submitting:

  ```sh
  python -m pytest
  python -m mypy
  python tools/check_dist.py
  ```

- Update `CHANGELOG.md` only if asked; the maintainer writes release notes.

## Releases

Releases are made by the maintainer, and only when shipped library behavior
changes. Documentation, test, and CI changes do not get their own release.
