# HTML Tool Patterns Reference

Load this file when building a tool that needs UI components, architecture guidance, or CSS patterns beyond what the template provides.

## Table of Contents

- [Architecture Patterns](#architecture-patterns)
- [CSS Conventions](#css-conventions)
- [UI Component Patterns](#ui-component-patterns)
- [Data & State Patterns](#data--state-patterns)
- [External Libraries](#external-libraries)

---

## Architecture Patterns

### Pattern 1: Simple Stateless Tool
Input -> Process -> Output. Real-time event listeners, no external APIs.

```html
<input type="text" id="input" placeholder="Paste something...">
<div id="output"></div>

<script>
  document.getElementById('input').addEventListener('input', (e) => {
    document.getElementById('output').textContent = process(e.target.value);
  });
</script>
```

When you style the input, follow the touch-target sizing guidance in `CSS Conventions -> Touch Targets`.

### Pattern 2: Interactive App with State
Centralized state object, render function, history/undo support.

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

### Pattern 3: Tool with CDN Libraries
Default to classic script tags from jsdelivr/cdnjs with `defer`. Always pin an exact version (`@x.y.z`) instead of `@latest` or a versionless URL.

Use `defer` on script tags so the CDN fetch doesn't block rendering. A deferred script downloads in parallel with HTML parsing and executes after the DOM is parsed — but **before** the inline `<script>` at end of `<body>` runs. This means the library is available by the time event handlers fire, with zero render-blocking cost.

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

## CSS Conventions

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
| Purpose | Value |
|---------|-------|
| Background | `#f8f9fa` |
| Surface/cards | `white` |
| Border | `#dadce0` |
| Text primary | `#202124` |
| Text secondary | `#5f6368` |
| Text muted | `#9aa0a6` |
| Accent/link | `#1a73e8` |
| Accent hover | `#1765cc` |
| Error text | `#d93025` |
| Error bg | `#fce8e6` |
| Success | `#188038` |

### Layout
- Max-width container: `800px` (default) or `600px`-`1200px` as needed
- Centered: `margin: 0 auto`
- Padding: `20px` desktop, `12px` mobile

### Touch Targets
Interactive controls should be easy to tap on touch devices:
- Aim for `44x44` CSS px targets for buttons, icon buttons, links styled as buttons, and primary form controls.
- In dense layouts, do not shrink below `24x24` CSS px.
- Prefer `min-height`/`min-width` plus padding over fixed heights so labels can wrap without clipping.

```css
button,
input,
select,
textarea {
  min-height: 44px;
}

button.icon-only {
  min-width: 44px;
  min-height: 44px;
}
```

### Responsive Breakpoint
```css
@media (max-width: 600px) {
  #app { padding: 12px; }
  h1 { font-size: 1.25rem; }
}
```

---

## UI Component Patterns

### Copy to Clipboard Button
```javascript
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(
    () => showToast('Copied to clipboard'),
    () => showToast('Could not copy — check clipboard permissions')
  );
}
```

### Toast Notification
```javascript
function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
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

```javascript
function showError(message) {
  const el = document.getElementById('error');
  el.textContent = message;
  el.classList.add('visible');
}

function hideError() {
  document.getElementById('error').classList.remove('visible');
}
```

### Form Field + Validation
Use visible labels, native validation attributes, hint text, and field-specific errors.

```html
<form id="settings-form">
  <label for="project-name">Project name</label>
  <input
    id="project-name"
    name="projectName"
    type="text"
    required
    minlength="3"
    maxlength="40"
    aria-describedby="project-name-hint project-name-error">
  <div id="project-name-hint">3-40 characters.</div>
  <div id="project-name-error" role="alert" hidden></div>

  <button type="submit">Save</button>
</form>
```

```javascript
const form = document.getElementById('settings-form');
const input = document.getElementById('project-name');
const error = document.getElementById('project-name-error');

function clearFieldError() {
  input.removeAttribute('aria-invalid');
  error.hidden = true;
  error.textContent = '';
}

form.addEventListener('submit', (e) => {
  clearFieldError();

  if (!input.checkValidity()) {
    e.preventDefault();
    input.setAttribute('aria-invalid', 'true');
    error.textContent = input.validationMessage;
    error.hidden = false;
    input.focus();
  }
});

input.addEventListener('input', clearFieldError);
```

Use `<label for>` + `id` for every form control. Placeholder text is optional hint text, not the label. Prefer native attributes like `required`, `minlength`, `maxlength`, `pattern`, and the right `type` before custom JS. Use `setCustomValidity()` only for domain-specific rules, and style invalid fields with `:invalid` or `[aria-invalid="true"]`.

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
  border: 2px dashed #dadce0;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  color: #5f6368;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.dropzone:hover, .dropzone.drag-over {
  border-color: #1a73e8;
  background: #e8f0fe;
}
```

### Modal Dialog
Use the native `<dialog>` element with `.showModal()`. Provides Escape dismissal, focus trapping, and backdrop for free. If your CSS has a `* { margin: 0 }` reset, add `margin: auto` to restore centering.

```css
.modal {
  border: none; border-radius: 16px; padding: 24px;
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
  gap: 8px;
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
