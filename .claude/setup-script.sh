#!/bin/bash
# Setup script for Claude Code on the web (cloud environments).
#
# Last-edited commit: 02481cb
#
# This file is NOT executed from the repo. It is the version-controlled source
# of truth for the environment's "Setup script" field, which can only be set by
# pasting into the GUI: claude.ai/code -> environment settings -> Setup script.
#
# Keeping them in sync (manual, hokey, but the only option today):
#   1. Edit this file and commit.
#   2. Replace the "Last-edited commit" sha above with `git rev-parse --short
#      HEAD` and commit again (the stamp commit).
#   3. Paste the whole file into the environment's Setup script field.
# To check whether the GUI copy is stale, compare its stamp against:
#   git log --oneline -2 -- .claude/setup-script.sh
#
# How this differs from .claude/hooks/session-start.sh:
#   - This runs as root on Ubuntu 24.04, BEFORE Claude Code launches, and only
#     when no cached environment snapshot exists (the filesystem is snapshotted
#     after it succeeds, so installs here are effectively free on later
#     sessions). Install system tools the cloud lacks here.
#   - The SessionStart hook runs on EVERY session (including resumes, and
#     locally) and handles per-clone project setup: uv sync, pre-commit install.
#
# Constraints (per https://code.claude.com/docs/en/claude-code-on-the-web):
#   - A non-zero exit blocks the session from starting, so non-critical steps
#     are best-effort (`|| ...`).
#   - Keep total runtime under ~5 minutes or the environment cache won't build.
#   - Network is subject to the environment's network access policy. Stock
#     Ubuntu mirrors (archive.ubuntu.com) are reachable; cli.github.com and
#     github.com are currently NOT, so gh comes from Ubuntu's repo (2.45.x).
#     For a newer gh, add github.com + cli.github.com to the environment's
#     allowed domains (or switch to Trusted access) and swap in GitHub's
#     official apt repo.

set -uo pipefail

echo "Installing gh from Ubuntu archive..."
apt-get update
apt-get install -y gh || echo "WARNING: gh install failed; continuing without it" >&2

gh --version || true
