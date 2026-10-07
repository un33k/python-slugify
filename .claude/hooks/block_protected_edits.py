#!/usr/bin/env python3
"""PreToolUse hook. Exit code 2 = BLOCK the tool call (message goes back to Claude).
Blocks: (1) editing any EXISTING file under tests/  (2) editing slugify/_legacy.py.
Creating NEW test files is allowed."""
import json, os, sys, datetime

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path") or ""
norm = path.replace("\\", "/")

reason = None
if norm.endswith("slugify/_legacy.py"):
    reason = "slugify/_legacy.py is frozen and must not be edited."
elif "/tests/" in norm and os.path.exists(path):
    reason = "Existing test files are protected. Create a NEW test file instead."

if reason:
    log = os.environ.get("HOOK_LOG")
    if log:
        with open(log, "a") as f:
            f.write(f"{datetime.datetime.now().isoformat()} BLOCKED {path}\n")
    print("Blocked: " + reason, file=sys.stderr)
    sys.exit(2)
sys.exit(0)
