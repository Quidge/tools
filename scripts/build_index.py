"""Generate index.html listing all HTML tools in the repository."""

import argparse
from dataclasses import dataclass
import subprocess
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Final

EXCLUDED = {"index.html", "404.html"}

# Example: Apr 9, 2026
# Example: Dec 31, 2025
DATE_DISPLAY_FORMAT: Final[str] = "%b %-d, %Y"


class MetadataParser(HTMLParser):
    """Extract <title> and <meta name="description"> from an HTML file."""

    def __init__(self):
        super().__init__()
        self.title: str | None = None
        self.description: str | None = None
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


def get_git_date(filepath: str, first: bool = False) -> datetime | None:
    """Get a git date for a file. If first=True, get creation date; otherwise last modified."""
    if first:
        cmd = [
            "git",
            "log",
            "--follow",
            "--diff-filter=A",
            "--format=%aI",
            "--",
            filepath,
        ]
    else:
        cmd = ["git", "log", "-1", "--format=%aI", "--", filepath]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        if lines:
            iso_date = lines[-1] if first else lines[0]
            return datetime.fromisoformat(iso_date)
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    return None


@dataclass
class Tool:
    filename: str
    title: str
    description: str
    created: datetime | None
    updated: datetime | None


def gather_tools() -> list[Tool]:
    """Scan root for HTML files and extract metadata."""
    tools = []
    for path in sorted(Path(".").glob("*.html")):
        if path.name in EXCLUDED:
            continue
        parser = MetadataParser()
        parser.feed(path.read_text())
        created_dt = get_git_date(path.name, first=True)
        updated_dt = get_git_date(path.name, first=False)
        tools.append(
            Tool(
                filename=path.name,
                title=parser.title or path.stem.replace("-", " ").title(),
                description=parser.description or "",
                created=created_dt,
                updated=updated_dt,
            )
        )
    return tools


def build_tool_card(tool: Tool) -> str:
    """Generate HTML for a single tool card."""
    created_text = tool.created.strftime(DATE_DISPLAY_FORMAT) if tool.created else None
    updated_text = tool.updated.strftime(DATE_DISPLAY_FORMAT) if tool.updated else None

    dates = ""
    if created_text:
        dates += f'<span class="date">Added {created_text}</span>'
        if updated_text and updated_text != created_text:
            dates += f' <span class="date sep">&middot;</span> <span class="date">Updated {updated_text}</span>'

    desc = f'<p class="desc">{tool.description}</p>' if tool.description else ""

    return f"""    <a class="card" href="{tool.filename}">
      <h2>{tool.title}</h2>
      {desc}
      <div class="dates">{dates}</div>
    </a>"""


def build_html(tools: list[Tool]) -> str:
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
    @media (max-width: 600px) {{
      body {{
        padding: 1.25rem 0.75rem;
      }}
      h1 {{
        font-size: 1.75rem;
      }}
      .tagline {{
        margin-bottom: 1.5rem;
        font-size: 1rem;
      }}
      .card {{
        padding: 1rem;
      }}
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to write the generated index HTML",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    tools = gather_tools()
    # Sort newest first
    tools.sort(key=lambda t: t.created or datetime.min, reverse=True)
    html = build_html(tools)
    if not args.output_file.parent.exists():
        raise SystemExit(
            f"Parent directory does not exist: {args.output_file.parent}"
        )
    args.output_file.write_text(html)
    print(f"Generated {args.output_file} with {len(tools)} tools")
