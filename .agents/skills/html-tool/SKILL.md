---
name: html-tool
description: Build and modify single-file HTML tools in this repository. Use when creating a new html-tool, modifying an existing html-tool, or turning a request for a web utility, widget, or interactive tool into a self-contained repo-style HTML file.
---

# HTML Tool Guide

Treat this skill as the current best-practice source for root-level single-file HTML tools in this repo. Use existing tools as examples, not standards: they may reflect older patterns. When editing, preserve the file's architecture. When creating or touching new areas, follow current skill guidance unless the tool has a clear reason to differ.

Build every tool as a single self-contained HTML file in the repo root. GitHub Pages serves these files statically at `tools.jonathandemirgian.com`.

## Start Here

### Create a New Tool

Hard rule: do not hand-author a new tool file from scratch, and do not use a "create new file" shortcut that bypasses the canonical template. The first change to the new tool file must be a copied `assets/template.html`.

Preflight (do this before you add any app-specific HTML/CSS/JS):
1. From the repository root, copy the template: `cp .claude/skills/html-tool/assets/template.html <repo-root>/{tool-name}.html`
2. Confirm the copy succeeded: `cmp .claude/skills/html-tool/assets/template.html {tool-name}.html` should report the files identical before you edit.
3. Replace `TOOL_TITLE` and `TOOL_DESCRIPTION` placeholders
4. Decide whether the tool is simple or non-trivial
5. If it is non-trivial, read [references/patterns.md](references/patterns.md) before implementing
6. Test locally with `uv run livereload . --port 8000 --target {tool-name}.html`

### Edit an Existing Tool

1. Read the full file first
2. Preserve its current architecture and overall patterns
3. Apply current skill guidance to new or newly touched details
4. If older local patterns differ meaningfully from current best practice, check with the user before modernizing them; otherwise flag it as separate follow-up work instead of silently expanding scope

### File Naming
- Keep file names lowercase and hyphen-separated: `day-visualizer.html`, `color-picker.html`
- Choose a name that describes the tool's purpose

## Non-Negotiable Constraints

- Keep all HTML, CSS, and JS inline in one root-level `.html` file; skip any build step
- Default to zero external dependencies and vanilla JS; add a CDN library only when vanilla JS is clearly insufficient, and pin it to an exact version (`@x.y.z`, never `@latest`)
- Make the layout mobile-friendly and responsive

## Defaults For Every New Tool

Start from the canonical template (`assets/template.html`): document structure, semantic color tokens, spacing/type tokens, field and button styling, and responsive rules. Only deviate with a clear reason. Repeat policy in prose, not raw CSS values — the canonical template owns the exact color, spacing, and type tokens.

Default visual goal: boring, comfortable, utility-first UI. Prefer readability and predictable hierarchy over novelty.

Default hierarchy rhythm:
- Small gap inside a field block (label, control, hint)
- Medium gap between related controls in the same section
- Large gap between sections or major content groups

When reviewing the implementation, still check a few high-signal defaults that are easy to get wrong when extending the template:
- Prefer visible labels and native form semantics
- Use `:focus-visible` instead of custom `:focus` styles
- Aim for `44x44` CSS px touch targets for primary controls; do not go below `24x24` in dense layouts
- Prefer shared spacing/type tokens over ad hoc one-off values in newly touched UI
- Add helper functions and extra UI only when the tool needs them
- If the tool has shared interactive state, use a centralized `state` object plus `render()` instead of ad hoc DOM mutation

## Open Patterns When Needed

Open [references/patterns.md](references/patterns.md) before implementing when the tool needs any of the following:
- Shared app state or multiple interactive regions derived from the same data
- Async loading flows or richer feedback states
- Form validation, field hints, or field-level errors
- Modal or confirmation dialogs
- File import via click-to-upload or drag-and-drop
- Shareable or bookmarkable state in the URL or hash
- External libraries
- Reusable interaction patterns like toasts, clipboard actions, app-level errors, or show/hide sections
- Deeper styling snippets or rationale than the template covers (colors, layout, touch targets, responsive refinements)

`patterns.md` opens with a Pattern Index that routes each of these to the exact snippet. If none apply and the tool is mostly a direct input -> process -> output flow, the template baseline is probably enough.

## Local Testing

- Serve the repo with `uv run livereload . --port 8000`
- Serve and watch a specific tool with `uv run livereload . --port 8000 --target {tool-name}.html`
- Verify desktop and mobile behavior
- Remember that `index.html` is generated; do not hand-edit it
