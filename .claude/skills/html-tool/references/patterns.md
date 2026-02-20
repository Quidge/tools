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
Use ES module imports or script tags from jsdelivr/cdnjs.

```html
<!-- Script tag approach -->
<script src="https://cdn.jsdelivr.net/npm/library@version/dist/lib.min.js"></script>

<!-- ES module approach -->
<script type="module">
  import lib from 'https://cdn.jsdelivr.net/npm/library@version/+esm';
</script>
```

---

## CSS Conventions

### Font Stack
```css
font-family: system-ui, sans-serif;
```
For monospace content:
```css
font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
```

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
function toBase64(str) {
  const bytes = new TextEncoder().encode(str);
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function fromBase64(b64) {
  const binary = atob(b64);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
  return new TextDecoder().decode(bytes);
}

// Save to URL
function encodeStateToURL(data) {
  const encoded = toBase64(JSON.stringify(data));
  const url = new URL(window.location);
  url.searchParams.set('s', encoded);
  window.history.replaceState(null, '', url);
}

// Load from URL
function decodeStateFromURL() {
  const encoded = new URLSearchParams(window.location.search).get('s');
  if (!encoded) return null;
  try { return JSON.parse(fromBase64(encoded)); }
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

Prefer loading from CDN when vanilla JS is insufficient. Common choices:

| Need | Library | CDN |
|------|---------|-----|
| Markdown | marked | `https://cdn.jsdelivr.net/npm/marked/marked.min.js` |
| Syntax highlight | Prism | `https://cdn.jsdelivr.net/npm/prismjs` |
| PDF reading | PDF.js | `https://cdn.jsdelivr.net/npm/pdfjs-dist@latest/+esm` |
| Charts | Chart.js | `https://cdn.jsdelivr.net/npm/chart.js` |
| Date/time | dayjs | `https://cdn.jsdelivr.net/npm/dayjs` |
