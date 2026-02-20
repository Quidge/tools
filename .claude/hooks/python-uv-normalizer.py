#!/usr/bin/env -S uv run
"""
PreToolUse hook to automatically transform python commands to use 'uv run python'.

This hook intercepts Bash commands and transforms:
- 'python ...' -> 'uv run python ...'
- 'python3 ...' -> 'uv run python ...'

The transformation happens transparently without disrupting agent workflow.
"""

import json
import re
import sys


def main():
    # Read input from Claude
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error reading input JSON: {e}")
        sys.exit(1)

    # Extract the command from the tool input
    command = input_data.get("tool_input", {}).get("command", "")

    if not command:
        # No command to process, just allow
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            }
        }
        sys.stdout.write(json.dumps(output))
        sys.exit(0)

    # Check if command needs modification
    new_command = command
    modified = False

    # Pattern: Match commands that start with 'python' or 'python3'
    # But don't modify if already using 'uv run'
    if not re.search(r"\buv\s+run\s+python", command):
        # Match 'python3' or 'python' at the start (with optional leading whitespace)
        match = re.match(r"^(\s*)(python3|python)\b", command)
        if match:
            python_cmd = match.group(2)

            # Transform to 'uv run python' using regex substitution to preserve spacing
            new_command = re.sub(
                r"^(\s*)(python3|python)\b", r"\1uv run python", command
            )
            modified = True

            # Provide feedback to the agent
            sys.stderr.write(
                f"⚠️  Modified: Using 'uv run python' instead of '{python_cmd}'",
            )

    # Return the result
    if modified:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "updatedInput": {"command": new_command},
            }
        }
    else:
        # No modification needed, just allow
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
            }
        }

    sys.stdout.write(json.dumps(output))
    sys.exit(0)


if __name__ == "__main__":
    main()
