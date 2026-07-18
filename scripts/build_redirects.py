"""Generate client-side redirect stub pages from _redirects.json.

GitHub Pages cannot issue real HTTP 3xx redirects for arbitrary paths, so we
approximate one with a tiny static HTML page per alias. Each stub stacks four
mechanisms so the redirect works across environments:

  - <meta http-equiv="refresh">  : redirects even with JavaScript disabled.
  - location.replace(...)        : instant, and *replaces* the history entry so
                                   the Back button skips the stub instead of
                                   bouncing the visitor forward again.
  - <link rel="canonical">       : tells search engines the target is the real
                                   URL (a meta refresh is a weak SEO signal).
  - <a href> in the body         : last-resort clickable fallback.

_redirects.json maps a source name to a target. The target may be an absolute
path on this site ("/sound-board.html") or a full external URL
("https://example.com/"). Each entry produces "<source>.html" at the repo root.

These stubs are generated (and .gitignored) just like index.html; the source of
truth is _redirects.json.
"""

import argparse
import json
from pathlib import Path

# NOTE: Query strings and URL fragments (?foo / #bar) on the incoming request
# are DELIBERATELY dropped, not forwarded to the target. This keeps the stub
# dead simple and means the destination tool never has to reason about state
# arriving from an old or aliased URL. If you hit the wrong URL, you land on a
# fresh copy of the tool at its root. Simplicity over preserving deep-link state.
REDIRECT_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Redirecting…</title>
  <link rel="canonical" href="{url}">
  <meta http-equiv="refresh" content="0; url={url}">
  <script>
    // Query string and hash are intentionally not forwarded; see build_redirects.py.
    location.replace("{url}");
  </script>
</head>
<body>
  <p>This page has moved to <a href="{url}">{url}</a>.</p>
</body>
</html>
"""


def build_redirects(redirects_file: Path, output_dir: Path) -> int:
    """Write a redirect stub for each entry in redirects_file. Returns the count."""
    if not redirects_file.exists():
        print(f"No {redirects_file} found, skipping redirect generation")
        return 0

    redirects = json.loads(redirects_file.read_text())
    for source, target in redirects.items():
        stub = output_dir / f"{source}.html"
        stub.write_text(REDIRECT_TEMPLATE.format(url=target))
        print(f"Generated redirect: {stub.name} -> {target}")
    return len(redirects)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--redirects-file",
        type=Path,
        default=Path("_redirects.json"),
        help="Path to the JSON map of source name -> target URL",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Directory to write the generated redirect stubs into",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    count = build_redirects(args.redirects_file, args.output_dir)
    print(f"Generated {count} redirect page{'s' if count != 1 else ''}")
