"""Pass check for the is_slug task. Run from inside the repo (venv active).
Exit code 0 = PASS, 1 = FAIL. Prints the reason."""
import subprocess, sys

def fail(msg):
    print("FAIL:", msg); sys.exit(1)

# 1. full test suite must pass
r = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider"],
                   capture_output=True, text=True)
if r.returncode != 0:
    fail("pytest failed")

# 2. behaviour checks (fresh interpreter so no stale imports)
code = r'''
from slugify import is_slug
cases = [
    (("hello-world",), True),
    (("abc123",), True),
    (("Hello World",), False),
    (("hello world",), False),
    (("Hello-World",), False),
    (("hello--world",), False),
    (("-hello",), False),
    (("",), False),
    (("hello_world",), False),
    (("hello_world", "_"), True),
    (("hello-world", "_"), False),
]
for args, want in cases:
    got = is_slug(*args)
    assert got is want, f"is_slug{args} -> {got!r}, wanted {want!r}"
'''
r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
if r.returncode != 0:
    fail("behaviour: " + (r.stderr.strip().splitlines() or ["error"])[-1])

# 3. a new test file mentioning is_slug must exist; existing tests untouched
st = subprocess.run(["git", "status", "--porcelain", "--", "tests"],
                    capture_output=True, text=True).stdout.splitlines()
modified = [l for l in st if not l.startswith("??") and not l.startswith("A")]
if modified:
    fail("existing test files were modified: " + "; ".join(modified))
new = [l[3:] for l in st if l.startswith("??") or l.startswith("A")]
import os
if not any(f.endswith(".py") and "is_slug" in open(f).read() for f in new if os.path.isfile(f)):
    fail("no new test file that tests is_slug")

print("PASS")
