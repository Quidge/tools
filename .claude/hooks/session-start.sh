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

install_gh() {
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
}

# Skip if gh is already installed
if ! command -v gh &>/dev/null; then
  install_gh
fi
