import sys, json

input_data = json.load(sys.stdin)
tool_input = input_data.get("tool_input", {})
file_path = tool_input.get("file_path", "")

if "tests/" in file_path:
    print("Blocking edit to existing test file. Put new tests in a new file.", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
