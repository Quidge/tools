# HTML Tool Patterns Reference

Read this file for the implementation details behind the Pattern Index in `SKILL.md`, or for deeper guidance on the shared styling defaults used across new tools.

Use it to choose an architecture, apply reusable interaction patterns, persist state, extend the shared styling defaults, and load external libraries beyond the baseline defaults in `SKILL.md` and `assets/template.html`.

These patterns are opt-in. `assets/template.html` provides the baseline scaffold, but it does not preload optional helper markup, CSS, or JS.

## Pattern Index

Routing only — jump to the section below for the implementation details.

### [Architecture Patterns](#architecture-patterns)
- `Simple Stateless Tool` — the tool is mostly a direct input -> process -> output flow with no shared app state.
- `Interactive App with State` — multiple controls or views mutate shared state, or the UI is derived from combined state.
- `Tool with CDN Libraries` — vanilla JS is insufficient and a pinned external library is needed.

### [Shared Styling Defaults](#shared-styling-defaults)
- Deeper snippets and rationale for the font stack, color tokens, layout, spacing/type, touch targets, and responsive breakpoint.

### [UI Component Patterns](#ui-component-patterns)
- `Copy to Clipboard Button` — users can copy generated content.
- `Toast Notification` — feedback should be brief and non-blocking.
- `Error Display` — a failure affects the whole form or app, not just one field.
- `Form Field + Validation` — inputs need labels, hints, native validation, or field-level errors.
- `Loading State` — a user action triggers async work.
- `File Drag & Drop` — users can import files by dropping or selecting them.
- `Modal Dialog` — the tool opens a secondary flow or overlay.
- `Confirmation Dialog` — an action is destructive or hard to undo.
- `Show/Hide Sections` — UI regions are conditionally revealed.

### [Data & State Patterns](#data--state-patterns)
- `URL State Persistence` — tool state should be shareable or bookmarkable.
- `Hash-based State` — only a small amount of state needs to be encoded in the URL.

### [External Libraries](#external-libraries)
- Choosing a library or CDN loading strategy.

---

## Architecture Patterns

### Simple Stateless Tool
Use this pattern for direct input -> process -> output tools with no shared app state and no external APIs.

```html
<input type="text" id="input" placeholder="Paste something...">
<div id="output"></div>

<script>
  document.getElementById('input').addEventListener('input', (e) => {
    document.getElementById('output').textContent = process(e.target.value);
  });
</script>
```

When styling the input, follow the touch-target sizing guidance in `Shared Styling Defaults -> Touch Targets`.

### Interactive App with State
Use this pattern when multiple controls or views mutate shared state and the UI is rendered from that state.

```javascript
const state = {
  items: [],
  selectedId: null,
  history: { past: [], future: [] }
};

function saveHistory() {
  state.history.past.push(structuredClone(state.items));
  if (state.history.past.length > 50) state.history.past.shift();
  state.history.future = [];
}

function render() {
  // Rebuild DOM from state
}
```

### Tool with CDN Libraries
Use this pattern when vanilla JS is insufficient and the tool needs a pinned external library.

Default to classic script tags from jsdelivr/cdnjs with `defer`. Always pin an exact version (`@x.y.z`) instead of `@latest` or a versionless URL.

Use `defer` on script tags so the CDN fetch doesn't block rendering. A deferred script downloads in parallel with HTML parsing and executes after the DOM is parsed — **after** any inline `<script>` at end of `<body>` has already run. The library is available by the time event handlers fire, with zero render-blocking cost.

Omit `defer` only if the inline script calls the library at top-level during initialization (not inside event handlers). This is rare — most tools reference libraries from user-triggered callbacks.

```html
<!-- Default approach: classic script tag + defer -->
<script defer src="https://cdn.jsdelivr.net/npm/library@1.2.3/dist/lib.min.js"></script>
```

Use `type="module"` only when a library is ESM-only or meaningfully easier to consume via imports:
```html
<script type="module">
  import lib from 'https://cdn.jsdelivr.net/npm/library@1.2.3/+esm';
</script>
```

Guard against CDN load failure at runtime:
```javascript
if (typeof LibraryGlobal === 'undefined') {
  showToast('Library not loaded — check your connection');
  return;
}
```

---

## Shared Styling Defaults

### Font Stack
```css
font-family: system-ui, sans-serif;
```
For monospace content:
```css
font-family: ui-monospace, 'SF Mono', 'Menlo', 'Consolas', monospace;
```
`ui-monospace` prefers the OS UI monospace face, while named fonts and `monospace` preserve fallback coverage.

### Color Palette
Use semantic color tokens from `assets/template.html`:

- Neutral: `--bg`, `--surface`, `--hover`, `--border`, `--text-primary`, `--text-secondary`, `--text-muted`, `--toast-bg`
- Accent: `--accent-light`, `--accent`, `--accent-hover`
- Semantic feedback: `--error-bg`, `--error`, `--success-bg`, `--success`, `--warning-bg`, `--warning`

Template defaults include hex fallbacks plus an `@supports (color: oklch(...))` layer. Keep token names stable and avoid raw color literals in new snippets unless there is a specific one-off reason.

### Layout
- Max-width container: `800px` (default) or `600px`-`1200px` as needed
- Centered: `margin: 0 auto`
- Padding: `24px` desktop, `16px` mobile

### Spacing + Typography
Treat `assets/template.html` as canonical for exact values.

The shared spacing scale is built on a 4px grid, and the type scale is anchored around a `1rem` base text size for body copy and controls.

Use:
- `--space-*` for layout and component spacing
- `--text-*` for type size
- `--line-heading`, `--line-ui`, and `--line-copy` for line-height

Prefer shared tokens over one-off values in new UI. Keep raw values only when a snippet needs component-specific geometry that the baseline scale does not cover.

### Touch Targets
Interactive controls should be easy to tap on touch devices:
- Aim for `44x44` CSS px targets for buttons, icon buttons, links styled as buttons, and primary form controls.
- In dense layouts, do not shrink below `24x24` CSS px.
- Prefer `min-height`/`min-width` plus padding over fixed heights so labels can wrap without clipping.
- Apply shared field styling to text-like inputs, selects, and textareas. Give specialized controls like checkboxes, radios, ranges, colors, and file inputs tool-specific treatment when needed.

```css
button,
input:is(
  [type="text"],
  [type="number"],
  [type="email"],
  [type="url"],
  [type="search"],
  [type="password"],
  [type="tel"],
  [type="date"],
  [type="time"],
  [type="datetime-local"],
  [type="month"],
  [type="week"]
),
select,
textarea {
  min-height: var(--control-min-height);
}

button.icon-only {
  min-width: var(--control-min-height);
  min-height: var(--control-min-height);
}
```

### Responsive Breakpoint
```css
@media (max-width: 600px) {
  #app { padding: var(--page-padding-mobile); }
  h1 { font-size: var(--text-xl); }
}
```

---

## UI Component Patterns

These snippets are intentionally not included in `assets/template.html` by default. Add them only when the tool needs them.

These CSS snippets assume the shared tokens from `assets/template.html` already exist. Use template tokens for shared decisions; keep raw values only for component-specific geometry.

### Copy to Clipboard Button
```javascript
function copyToClipboard(text) {
  if (!navigator.clipboard) {
    showToast('Could not copy — clipboard API unavailable');
    return;
  }
  navigator.clipboard.writeText(text).then(
    () => showToast('Copied to clipboard'),
    () => showToast('Could not copy — check clipboard permissions')
  );
}
```

### Toast Notification
```css
.toast {
  position: fixed;
  bottom: var(--space-6);
  left: 50%;
  transform: translateX(-50%);
  background: var(--toast-bg);
  color: var(--surface);
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-family: inherit;
  z-index: 2000;
  opacity: 0;
  transition: opacity 0.2s ease;
  pointer-events: none;
}

.toast.visible {
  opacity: 1;
}
```

```javascript
function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.classList.add('visible');
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => toast.classList.remove('visible'), 2000);
}
```

### Error Display
Use this for form-wide or app-wide failures, not validation on a specific input.

```html
<div id="error" class="error" role="alert" aria-live="assertive"></div>
```

```css
.error {
  color: var(--error);
  padding: var(--space-3);
  background: var(--error-bg);
  border-radius: var(--radius-sm);
  font-size: var(--text-base);
  display: none;
  margin-top: var(--space-3);
}

.error.visible {
  display: block;
}
```

```javascript
function showError(message) {
  const el = document.getElementById('error');
  el.textContent = message;
  el.classList.add('visible');
}

function hideError() {
  const el = document.getElementById('error');
  el.classList.remove('visible');
  el.textContent = '';
}
```

### Form Field + Validation
Use visible labels, native validation attributes, hint text, and field-specific errors.

Use a `.field` wrapper so each control keeps its label, hint, and field-level error together. Reserve the app-wide `.error` pattern for form-wide or page-wide failures.

```html
<form id="settings-form">
  <div class="field">
    <label for="project-name">Project name</label>
    <input
      id="project-name"
      name="projectName"
      type="text"
      required
      minlength="3"
      maxlength="40"
      aria-describedby="project-name-hint project-name-error">
    <div id="project-name-hint" class="hint">3-40 characters.</div>
    <div id="project-name-error" class="field-error" role="alert" hidden></div>
  </div>

  <button type="submit">Save</button>
</form>
```

```css
.field-error {
  margin-top: var(--space-2);
  color: var(--error);
  font-size: var(--text-sm);
  line-height: var(--line-copy);
}

input[aria-invalid="true"] {
  border-color: var(--error);
}
```

```javascript
const form = document.getElementById('settings-form');
const input = document.getElementById('project-name');
const fieldError = document.getElementById('project-name-error');

function clearFieldError() {
  input.removeAttribute('aria-invalid');
  fieldError.hidden = true;
  fieldError.textContent = '';
}

form.addEventListener('submit', (e) => {
  clearFieldError();

  if (!input.checkValidity()) {
    e.preventDefault();
    input.setAttribute('aria-invalid', 'true');
    fieldError.textContent = input.validationMessage;
    fieldError.hidden = false;
    input.focus();
  }
});

input.addEventListener('input', clearFieldError);
```

Use `<label for>` + `id` for every form control. Placeholder text is optional hint text, not the label. Prefer native attributes like `required`, `minlength`, `maxlength`, `pattern`, and the right `type` before custom JS. Use `setCustomValidity()` only for domain-specific rules.

For opaque codes, IDs, hashes, slugs, and vote codes, disable browser writing aids:
```html
<input type="text" spellcheck="false" autocorrect="off" autocomplete="off" autocapitalize="characters">
```
Use `autocapitalize="off"` when case matters exactly, or `autocapitalize="characters"` when you normalize to uppercase.

### Loading State
```javascript
button.disabled = true;
button.textContent = 'Loading...';
try {
  const result = await doWork();
  displayResult(result);
} finally {
  button.disabled = false;
  button.textContent = 'Original Label';
}
```

Keep loading buttons at the same touch-target size while the label changes.

### File Drag & Drop
```javascript
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');

dropzone.addEventListener('click', () => fileInput.click());
dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('drag-over');
});
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('drag-over'));
dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('drag-over');
  handleFiles(e.dataTransfer.files);
});
fileInput.addEventListener('change', (e) => handleFiles(e.target.files));
```

Dropzone CSS:
```css
.dropzone {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  padding: 40px 20px;
  text-align: center;
  color: var(--text-secondary);
  cursor: pointer;
  transition: border-color var(--transition-fast), background var(--transition-fast);
}
.dropzone:hover, .dropzone.drag-over {
  border-color: var(--accent);
  background: var(--accent-light);
}
```

### Modal Dialog
Use the native `<dialog>` element with `.showModal()`. Provides Escape dismissal, focus trapping, and backdrop for free. If your CSS has a `* { margin: 0 }` reset, add `margin: auto` to restore centering.

```css
.modal {
  border: none; border-radius: 16px; padding: var(--space-6);
  max-width: 400px; width: 90%; margin: auto;
}
.modal::backdrop { background: rgba(0,0,0,0.5); }
```

```javascript
function showModal(contentHTML) {
  const dialog = document.createElement('dialog');
  dialog.className = 'modal';
  dialog.innerHTML = contentHTML;
  document.body.appendChild(dialog);
  dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => dialog.remove());
  dialog.showModal();
  return dialog;
}
```

Dismisses via Escape (native), backdrop click (`e.target === dialog`), or any button calling `dialog.close()`. The `close` event handles cleanup for all paths — no leaked listeners or DOM nodes. Use the `autofocus` attribute on the primary action or close button inside the dialog, and keep modal action buttons at the same touch-target size as the rest of the app.

### Confirmation Dialog
Use this for irreversible or high-cost actions, such as deleting saved work, clearing all votes, or wiping local data. For routine single-item removals in a list or draft the user is actively editing, prefer direct action with an undo path instead of interrupting the user with a modal.

Use a native `<dialog>` with a clear title, consequence text, and explicit action labels. Put `Cancel` first, give it `autofocus`, and label the destructive action with the action itself (`Delete ballot`, not `Yes`). Skip backdrop-click dismissal by default for destructive confirms.

```html
<button type="button" id="delete-ballot-btn">Delete ballot</button>

<dialog
  id="delete-ballot-dialog"
  class="modal"
  aria-labelledby="delete-ballot-title"
  aria-describedby="delete-ballot-desc">
  <form method="dialog">
    <h3 id="delete-ballot-title">Delete ballot?</h3>
    <p id="delete-ballot-desc">
      This removes the saved ballot and entered votes from this browser. This can't be undone.
    </p>
    <div class="modal-actions">
      <button value="cancel" autofocus>Cancel</button>
      <button value="delete">Delete ballot</button>
    </div>
  </form>
</dialog>
```

```css
.modal-actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}
```

```javascript
const deleteBallotBtn = document.getElementById('delete-ballot-btn');
const deleteBallotDialog = document.getElementById('delete-ballot-dialog');

deleteBallotBtn.addEventListener('click', () => deleteBallotDialog.showModal());

deleteBallotDialog.addEventListener('close', () => {
  if (deleteBallotDialog.returnValue !== 'delete') return;
  deleteBallot();
});
```

### Show/Hide Sections
Toggle visibility with a CSS class:
```html
<div id="results" class="results">
  <!-- Results go here -->
</div>
```

```css
.results { display: none; }
.results.visible { display: block; }
```
```javascript
document.getElementById('results').classList.add('visible');
```

---

## Data & State Patterns

### URL State Persistence
Encode state in query params so tools produce shareable links.

```javascript
function toBase64Url(str) {
  const bytes = new TextEncoder().encode(str);
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary)
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
}

function fromBase64Url(b64url) {
  const base64 = b64url
    .replace(/-/g, '+')
    .replace(/_/g, '/');
  const padding = (4 - (base64.length % 4)) % 4;
  const binary = atob(base64 + '='.repeat(padding));
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

// Save to URL
function encodeStateToURL(data) {
  const encoded = toBase64Url(JSON.stringify(data));
  const url = new URL(window.location);
  url.searchParams.set('s', encoded);
  window.history.replaceState(null, '', url);
}

// Load from URL
function decodeStateFromURL() {
  const encoded = new URLSearchParams(window.location.search).get('s');
  if (!encoded) return null;
  try { return JSON.parse(fromBase64Url(encoded)); }
  catch { return null; }
}
```

### Hash-based State
Lighter alternative for simple values:
```javascript
// Write
window.location.hash = `key=${encodeURIComponent(value)}`;

// Read
const match = window.location.hash.match(/key=([^&]+)/);
if (match) value = decodeURIComponent(match[1]);
```

---

## External Libraries

Prefer loading from CDN when vanilla JS is insufficient. Pin exact versions so tools stay reproducible and upgrades stay intentional.

| Need | Library | CDN |
|------|---------|-----|
| Markdown | marked | `https://cdn.jsdelivr.net/npm/marked@18.0.2/lib/marked.umd.js` |
| Syntax highlight | Prism | `https://cdn.jsdelivr.net/npm/prismjs@1.30.0` |
| PDF reading (ES module) | PDF.js | `https://cdn.jsdelivr.net/npm/pdfjs-dist@5.6.205/+esm` |
| Charts | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js@4.5.1` |
| Date/time | dayjs | `https://cdn.jsdelivr.net/npm/dayjs@1.11.20` |
