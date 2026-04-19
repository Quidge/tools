# Overview

This repository contains simple tools and scripts. Most tools are single-file HTML apps served statically at `/<tool-name>.html`.

The site is deployed via GitHub Pages at `tools.jonathandemirgian.com` from the `main` branch.

## Repository structure

```
./
├── .claude/                # Instructions and configuration for Claude Code
├── .github/
│   └── workflows/
│       └── pages.yml       # Builds index and deploys to GitHub Pages
├── scripts/
│   └── build_index.py      # Generates index.html from root-level tool files
├── 404.html                # GitHub Pages fallback page
├── CNAME                   # Custom domain mapping
├── *.html                  # Root-level HTML tools
├── index.html              # Generated tool index page
└── pyproject.toml          # Python project metadata
```

## Useful commands

```shell
# Build index page
uv run python scripts/build_index.py --output-file index.html

# Serve repo locally (with live reload)
uv run livereload . --port 8000

# Serve and watch a specific tool file
uv run livereload . --port 8000 --target <tool-name>.html
```

Local site URL: `http://localhost:8000`

## Notes

- `index.html` is generated; do not hand-edit.
- Tool `created` / `updated` dates are derived from git history for each tool file.
- CI deploy workflow rebuilds `index.html` before publishing.

