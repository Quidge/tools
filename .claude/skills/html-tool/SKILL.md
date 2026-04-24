---
name: html-tool
description: Build and modify single-file HTML tools in this repository. Use when creating a new html-tool, modifying an existing html-tool, or turning a request for a web utility, widget, or interactive tool into a self-contained repo-style HTML file.
---

# HTML Tool Guide

Treat this skill as the current best-practice source for root-level single-file HTML tools in this repo. Use existing tools as examples, not standards: they may reflect older patterns. When editing, preserve the file's architecture. When creating or touching new areas, follow current skill guidance unless the tool has a clear reason to differ.

Build every tool as a single self-contained HTML file in the repo root. Default to zero external dependencies, no build step, and vanilla JS. GitHub Pages serves these files statically at `tools.jonathandemirgian.com`.

## Editorial Contract

Treat the skill files as the only design authority.

- `SKILL.md` defines policy, invariants, and exception rules.
- `assets/template.html` defines the canonical visual defaults and token values.
- `references/patterns.md` defines token-aligned optional patterns for non-trivial tools.

Repeat policy in prose, not raw CSS values. The template should be the single source of truth for exact color, spacing, and type tokens.

## Start Here

### Create a New Tool

Hard rule: do not hand-author a new tool file from scratch, and do not use a "create new file" shortcut that bypasses the template. The first change to the new tool file must be based on a copied `assets/template.html`.

Preflight (do this before you add any app-specific HTML/CSS/JS):
1. From the repository root, copy the template: `cp .claude/skills/html-tool/assets/template.html <repo-root>/{tool-name}.html`
2. Quick verification (optional but recommended): the new file should start out identical to the template (except you have not yet edited it). If you need confidence, `cmp` the two files before you start building features.
3. Replace `TOOL_TITLE` and `TOOL_DESCRIPTION` placeholders
4. Decide whether the tool is simple or non-trivial
5. If it is non-trivial, read [references/patterns.md](references/patterns.md) before implementing
6. Test locally with `uv run livereload . --port 8000 --target {tool-name}.html`

### Edit an Existing Tool

1. Read the full file first
2. Preserve its current architecture and overall patterns
3. Apply current skill guidance to new or newly touched details
4. If older local patterns differ meaningfully from current best practice, call that out as separate follow-up work instead of silently expanding scope

### File Naming
- Keep file names lowercase and hyphen-separated: `day-visualizer.html`, `color-picker.html`
- Choose a name that describes the tool's purpose

## Non-Negotiable Constraints

- Keep all HTML, CSS, and JS in one self-contained root-level `.html` file
- Skip any build step; GitHub Pages serves the file as-is
- Prefer vanilla JS; add a CDN library only when vanilla JS is clearly insufficient
- Ensure the tool works when opened directly in a browser
- Make the layout mobile-friendly and responsive
- Pin exact CDN versions whenever a library is needed

## Defaults For Every New Tool

Start from `assets/template.html`. It is the baseline scaffold and canonical default implementation: document structure, semantic color tokens, spacing/type tokens, field and button styling, and responsive rules. Only deviate with a clear reason.

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
- Add helper functions and extra UI only when the tool needs them; use [references/patterns.md](references/patterns.md) for toasts, clipboard actions, app-level errors, dialogs, and other opt-in behaviors
- If the tool has shared interactive state, use a centralized `state` object plus `render()` instead of ad hoc DOM mutation

See `Shared Styling Defaults` in [references/patterns.md](references/patterns.md) for deeper snippets and rationale around colors, layout, touch targets, and responsive refinements.

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

If none of those apply and the tool is mostly a direct input -> process -> output flow, the template baseline is probably enough.

## Pattern Index

Use this section for routing only. Read [references/patterns.md](references/patterns.md) for the actual implementation details.

### Architecture
- `Simple Stateless Tool` — Read when the tool is mostly a direct input -> process -> output flow with no shared app state.
- `Interactive App with State` — Read when multiple controls or views mutate shared state or the UI is derived from combined state.
- `Tool with CDN Libraries` — Read when vanilla JS is insufficient and a pinned external library is needed.

### Common Interaction Patterns
- `Copy to Clipboard Button` — Read when users can copy generated content.
- `Toast Notification` — Read when feedback should be brief and non-blocking.
- `Error Display` — Read when a failure affects the whole form or app, not just one field.
- `Form Field + Validation` — Read when inputs need labels, hints, native validation, or field-level errors.
- `Loading State` — Read when a user action triggers async work.
- `File Drag & Drop` — Read when users can import files by dropping or selecting them.
- `Modal Dialog` — Read when the tool opens a secondary flow or overlay.
- `Confirmation Dialog` — Read when an action is destructive or hard to undo.
- `Show/Hide Sections` — Read when UI regions are conditionally revealed.

### Data + State
- `URL State Persistence` — Read when tool state should be shareable or bookmarkable.
- `Hash-based State` — Read when only a small amount of state needs to be encoded in the URL.

### Libraries
- `External Libraries` — Read when choosing a library or CDN loading strategy.

## Modifying Existing Tools

- Read the full file first
- Follow the file's CURRENT architecture and naming patterns, unless explicitly told otherwise.
- Apply defaults from patterns.md or template.html ONLY for functionality that is being added.
- If you notice opportunities for modernization/updating the requested tool against content in patterns.md/template.html, explicitly check with the user that they want to modernize.

## Local Testing

- Serve the repo with `uv run livereload . --port 8000`
- Serve and watch a specific tool with `uv run livereload . --port 8000 --target {tool-name}.html`
- Verify desktop and mobile behavior
- Remember that `index.html` is generated; do not hand-edit it
