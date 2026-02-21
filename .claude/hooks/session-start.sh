#!/bin/bash
set -euo pipefail

# Only run in remote (Claude Code on the web) environments
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

# The goal here is to install `gh`. For some bizarre reason, Anthropic doesn't
# provision their boxes with a `gh` tool. They ship a ton of other dev tools but
# not `gh`.

# This will pull latest gh release on session start

# Resolve latest version from GitHub's redirect
GH_VERSION=$(curl -sI https://github.com/cli/cli/releases/latest | grep -i '^location:' | sed 's/.*tag\/v//' | tr -d '\r')
echo "Installing gh v${GH_VERSION}..."

# Download and extract
curl -L "https://github.com/cli/cli/releases/download/v${GH_VERSION}/gh_${GH_VERSION}_linux_amd64.tar.gz" -o /tmp/gh.tar.gz
tar -xzf /tmp/gh.tar.gz -C /tmp

# Install to ~/bin
mkdir -p ~/.local/bin
mv "/tmp/gh_${GH_VERSION}_linux_amd64/bin/gh" ~/.local/bin/gh
chmod +x ~/.local/bin/gh

# Clean up
rm -rf /tmp/gh.tar.gz "/tmp/gh_${GH_VERSION}_linux_amd64"

echo "Installed: $(~/.local/bin/gh --version)"
