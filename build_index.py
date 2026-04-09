"""Generate index.html listing all HTML tools in the repository."""

import subprocess
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

EXCLUDED = {"index.html", "404.html"}


class MetadataParser(HTMLParser):
    """Extract <title> and <meta name="description"> from an HTML file."""

    def __init__(self):
        super().__init__()
        self.title = None
        self.description = None
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag == "meta":
            attrs_dict = dict(attrs)
            if attrs_dict.get("name", "").lower() == "description":
                self.description = attrs_dict.get("content", "")

    def handle_data(self, data):
        if self._in_title:
            self.title = data.strip()

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def get_git_date(filepath: str, first: bool = False) -> str | None:
    """Get a git date for a file. If first=True, get creation date; otherwise last modified."""
    if first:
        cmd = ["git", "log", "--follow", "--diff-filter=A", "--format=%aI", "--", filepath]
    else:
        cmd = ["git", "log", "-1", "--format=%aI", "--", filepath]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        if lines:
            return lines[-1] if first else lines[0]
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return None


def format_date(iso_date: str | None) -> str | None:
    """Format an ISO date string to 'Mon D, YYYY'."""
    if not iso_date:
        return None
    try:
        dt = datetime.fromisoformat(iso_date)
        return dt.strftime("%b %-d, %Y")
    except ValueError:
        return None


def gather_tools() -> list[dict]:
    """Scan root for HTML files and extract metadata."""
    tools = []
    for path in sorted(Path(".").glob("*.html")):
        if path.name in EXCLUDED:
            continue
        parser = MetadataParser()
        parser.feed(path.read_text())
        created_iso = get_git_date(path.name, first=True)
        updated_iso = get_git_date(path.name, first=False)
        tools.append({
            "filename": path.name,
            "title": parser.title or path.stem.replace("-", " ").title(),
            "description": parser.description or "",
            "created": format_date(created_iso),
            "updated": format_date(updated_iso),
            "created_iso": created_iso or "",
        })
    # Sort newest first
    tools.sort(key=lambda t: t["created_iso"], reverse=True)
    return tools


def build_tool_card(tool: dict) -> str:
    """Generate HTML for a single tool card."""
    dates = ""
    if tool["created"]:
        dates += f'<span class="date">Added {tool["created"]}</span>'
        if tool["updated"] and tool["updated"] != tool["created"]:
            dates += f' <span class="date sep">&middot;</span> <span class="date">Updated {tool["updated"]}</span>'

    desc = f'<p class="desc">{tool["description"]}</p>' if tool["description"] else ""

    return f"""    <a class="card" href="{tool['filename']}">
      <h2>{tool['title']}</h2>
      {desc}
      <div class="dates">{dates}</div>
    </a>"""


def build_html(tools: list[dict]) -> str:
    """Generate the full index.html page."""
    cards = "\n".join(build_tool_card(t) for t in tools)
    count = len(tools)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tools</title>
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: system-ui, sans-serif;
      background: #f8f9fa;
      color: #202124;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 640px;
      margin: 0 auto;
    }}
    h1 {{
      font-size: 2rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
    }}
    .tagline {{
      color: #5f6368;
      margin-bottom: 2rem;
      font-size: 1.05rem;
    }}
    .cards {{
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }}
    .card {{
      display: block;
      background: #fff;
      border: 1px solid #dadce0;
      border-radius: 8px;
      padding: 1.25rem;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.15s, box-shadow 0.15s;
    }}
    .card:hover {{
      border-color: #1a73e8;
      box-shadow: 0 1px 6px rgba(26, 115, 232, 0.15);
    }}
    .card h2 {{
      font-size: 1.15rem;
      font-weight: 600;
      color: #1a73e8;
      margin-bottom: 0.35rem;
    }}
    .desc {{
      color: #3c4043;
      font-size: 0.95rem;
      margin-bottom: 0.5rem;
    }}
    .dates {{
      font-size: 0.8rem;
      color: #5f6368;
    }}
    .sep {{
      margin: 0 0.15rem;
    }}
    footer {{
      margin-top: 3rem;
      color: #5f6368;
      font-size: 0.8rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Tools</h1>
    <p class="tagline">Simple HTML tools. Mostly vibe coded.</p>
    <div class="cards">
{cards}
    </div>
    <footer>{count} tool{"s" if count != 1 else ""} &middot; auto-generated on deploy</footer>
  </div>
</body>
</html>
"""


if __name__ == "__main__":
    tools = gather_tools()
    html = build_html(tools)
    Path("index.html").write_text(html)
    print(f"Generated index.html with {len(tools)} tools")
