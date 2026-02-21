#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [[ "${CLAUDE_CODE_REMOTE:-}" != "true" ]]; then
  exit 0
fi

# Skip if gh is already installed
if command -v gh &>/dev/null; then
  exit 0
fi

# The goal here is to install `gh`. For some bizarre reason, Anthropic doesn't
# provision their boxes with a `gh` tool. They ship a ton of other dev tools but
# not `gh`.

# Resolve latest version from GitHub's redirect
GH_VERSION=$(curl -sI https://github.com/cli/cli/releases/latest | grep -i '^location:' | sed 's/.*tag\/v//' | tr -d '\r')

if [[ -z "$GH_VERSION" ]]; then
  echo "Failed to resolve gh version" >&2
  exit 1
fi

echo "Installing gh v${GH_VERSION}..."

# Download and extract into a temporary directory
tmpdir=$(mktemp -d)
trap 'rm -rf "$tmpdir"' EXIT

curl -fL "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" -o "$tmpdir/gh.tar.gz"
tar -xzf "$tmpdir/gh.tar.gz" -C "$tmpdir"

# Install to ~/.local/bin
mkdir -p ~/.local/bin
mv "$tmpdir/gh_${GH_VERSION}_linux_amd64/bin/gh" ~/.local/bin/gh
chmod +x ~/.local/bin/gh

echo "Installed: $(~/.local/bin/gh --version)"
