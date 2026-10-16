## Please open an issue first

This project is **issues first**. We do not review unsolicited pull requests.

Generating a pull request is cheap now. Verifying one against this library's
frozen output contract is not, and that cost lands on the maintainer. So the
order here is:

1. Open an **issue** describing a real problem you hit, with an example.
2. If we agree it needs fixing, we'll fix it, or say so on the issue — then a
   pull request against that issue is welcome.

**A pull request with no linked, agreed issue will be closed with thanks,**
however good the code is. Please don't take that personally; several fine
pieces of work have been turned away for exactly this reason.

Before you submit, check what applies to you:

- [ ] This pull request links an issue where the change was agreed
- [ ] This is a security fix
- [ ] Neither — I should close this and open an issue instead

## If your pull request was agreed

- Which issue does it close?
- What did you change, and how did you verify it?
- Does it touch `slugify/_legacy.py` or `tests/test_legacy.py`? Those are frozen:
  any change to legacy output is rejected. New behavior belongs behind
  `algorithm='modern'`.
- Did you run `python -m pytest`, `python -m mypy`, and the style checks?
