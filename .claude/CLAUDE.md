# Overview

This repository contains simple tools and scripts. Many of these are simple HTML applications available statically when loaded from ./<name-of-tool>.html.

This repository is hosted via GitHub Pages at the domain `tools.jonathandemirgian.com`, serving from the `main` branch.

## Repository structure

```
./
├── .claude/                # Instructions and configuration for Claude Code
├── .github/
│   └── workflows/
│       └── pages.yml
├── 404.html                # 404 page GitHub Pages displays if it cannot resolve a path
├── CNAME                   # Record for DNS to resolve correctly
├── *.html                  # An HTML 'tool'
└── pyproject.toml          # Python project config and dependencies
```

## Useful commands

```shell
uv run python -m http.server 8000
```

To generate a webserver showing the current directory.

