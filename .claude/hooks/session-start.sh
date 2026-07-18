#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [[ "${CLAUDE_CODE_REMOTE:-}" != "true" ]]; then
  exit 0
fi

# Everything below depends on uv; fail loudly up front rather than partway in.
if ! command -v uv &>/dev/null; then
  echo "uv not present; cannot continue" >&2
  exit 1
fi

# Sync the Python environment and set up the pre-commit git hook. Remote boxes
# start with a bare checkout, so without this the hooks in
# .pre-commit-config.yaml never run on commits made from a remote session.
echo "Syncing Python environment..."
uv sync
uv run pre-commit install

# gh is installed by the environment's setup script (source of truth:
# .claude/setup-script.sh, pasted into the environment settings GUI). It is
# baked into the cached environment snapshot, so it should already be present;
# warn rather than fail if the setup script hasn't been synced to the GUI.
if ! command -v gh &>/dev/null; then
  echo "WARNING: gh not found. The environment's setup script may be missing" >&2
  echo "or stale; see .claude/setup-script.sh for the sync procedure." >&2
fi
