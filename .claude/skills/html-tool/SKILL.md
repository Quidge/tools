---
name: html-tool
description: Guide for creating and modifying single-file HTML tools in the tools repository. Use when (1) creating a new HTML tool from scratch, (2) modifying or enhancing an existing HTML tool, (3) adding features, fixing bugs, or refactoring any .html tool file in the repo root, or (4) the user asks to build a web-based utility, widget, or interactive tool for this project. Covers structure, styling, JS architecture, and deployment conventions.
---

# HTML Tool Guide

Every tool is a **single, self-contained HTML file** in the repo root. Zero external dependencies by default, no build step, vanilla JS. Served statically via GitHub Pages at `tools.jonathandemirgian.com`.

## Creating a New Tool

1. Copy `assets/template.html` to `<repo-root>/{tool-name}.html`
2. Replace `TOOL_TITLE` and `TOOL_DESCRIPTION` placeholders
3. Build the UI and logic within the single file
4. Test locally: `uv run python -m http.server 8000`

### File Naming
- Lowercase, hyphen-separated: `day-visualizer.html`, `color-picker.html`
- Name describes the tool's purpose

## Core Rules

- **Single file**: All HTML, CSS, and JS in one `.html` file
- **No build step**: File is served as-is by GitHub Pages
- **Vanilla JS first**: Only add CDN libraries when vanilla JS is clearly insufficient
- **Self-contained**: Tool must work when opened directly in a browser
- **Mobile-friendly**: Responsive design with `max-width` container and `@media (max-width: 600px)` breakpoint

## HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Tool Name}</title>
  <style>/* All CSS here */</style>
</head>
<body>
  <div id="app"><!-- All UI here --></div>
  <script>/* All JS here */</script>
</body>
</html>
```

Always include both meta tags. CSS goes in `<style>` in `<head>`. JS goes in `<script>` at end of `<body>`.

## CSS Conventions

- Reset: `* { box-sizing: border-box; margin: 0; padding: 0; }`
- Font: `system-ui, sans-serif`
- Background: `#f8f9fa`, surfaces: `white`, borders: `#dadce0`
- Text: `#202124` primary, `#5f6368` secondary, `#9aa0a6` muted
- Accent: `#1a73e8` (links, focus, primary buttons)
- Container: `max-width: 800px; margin: 0 auto; padding: 20px;`
- Transitions: `0.1s`-`0.2s` for hover/focus states
- Responsive: reduce padding and font sizes at `max-width: 600px`

## JS Conventions

- Script goes at end of `<body>` — DOM is already available, no `DOMContentLoaded` wrapper needed
- Use `const`/`let`, never `var`
- Use `structuredClone()` for deep cloning, not `JSON.parse(JSON.stringify())`
- DOM queries via `document.getElementById()` or `document.querySelector()`
- Use `:focus-visible` (not `:focus`) for custom focus styles to preserve keyboard accessibility
- Event delegation on container elements when managing dynamic children
- For interactive apps: centralized `state` object + `render()` function that rebuilds DOM from state

## Modifying Existing Tools

When modifying an existing tool:
1. Read the full file first to understand its patterns
2. Follow the existing code style (naming, indentation, patterns)
3. If the tool uses a state/render pattern, maintain it — update state then call render
4. Keep changes minimal and focused

## Advanced Patterns

For UI components (toasts, clipboard, drag-and-drop, error display), state management, URL persistence, or CDN library usage, read [references/patterns.md](references/patterns.md).
