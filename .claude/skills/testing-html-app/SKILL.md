---
name: testing-html-app
description: Test a single-file HTML tool by driving it in a real browser. Use when asked to test an HTML tool or app, verify a tool still works, or check a change end-to-end in the browser.
---

# Testing an HTML App

Drive the tool in a real headless browser with `rodney` (Chrome automation CLI, run as `uv run rodney <cmd>`). Testing means *exercising the tool the way a user would and observing what actually happens* — not reading the source and reasoning about it.

## Loop

1. **Launch.** `uv run rodney start`, then `uv run rodney open "file://$PWD/<tool>.html"`. (For tools that fetch or need a server, run `uv run livereload . --port 8000` first and open `http://localhost:8000/<tool>.html`.)
2. **Exercise.** Take the tool's main path a real user takes: enter values (`input`, `select`), press things (`click`), then `waitstable`. Read what changed with `js "<expression>"`.
3. **Verify.** After each meaningful interaction, confirm the result — `screenshot <file.png>` then read the PNG to see it, and `assert "<js expression>" -m "<what should be true>"` for exact checks (exit 1 = mismatch). Report every mismatch; don't smooth it over.
4. **Stop** with `uv run rodney stop` when done.

Run `uv run rodney --help` for the full command surface. Reach for `count`, `exists`, `visible`, and `ax-tree` to inspect structure.

## Notes

- `js` takes a plain JavaScript expression and prints its value: `uv run rodney js "document.querySelector('#total').textContent"`.
- Always `waitstable` between an interaction and the check that reads its result.
- Done means: the main path ran in the browser and every check either passed or is reported as a real mismatch.
