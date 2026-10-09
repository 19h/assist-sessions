#!/usr/bin/env python3
"""Copy session exports unchanged and generate a static, dependency-free index."""

from html import escape
from html.parser import HTMLParser
from pathlib import Path
import shutil
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent


class PageTitle(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def build(source: Path, output: Path) -> int:
    paths = list(source.rglob("*"))
    if not source.is_dir():
        raise ValueError(f"Session directory does not exist: {source}")
    if source.is_symlink() or any(path.is_symlink() for path in paths):
        raise ValueError("Session files and directories must not be symbolic links")
    if any(path.name.casefold() == "index.html" for path in source.iterdir()):
        raise ValueError("sessions/index.html is reserved for the generated index")

    pages = sorted(
        (path for path in paths if path.is_file() and path.suffix.lower() in {".html", ".htm"}),
        key=lambda path: path.relative_to(source).as_posix().casefold(),
    )
    entries = []
    for page in pages:
        relative = page.relative_to(source).as_posix()
        parser = PageTitle()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        title = " ".join("".join(parser.parts).split()) or page.stem
        entries.append(
            f'<li><a href="{quote(relative, safe="/")}">{escape(title)}</a>'
            f'<code>{escape(relative)}</code></li>'
        )

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(source, output, ignore=shutil.ignore_patterns(".DS_Store"))
    (output / ".nojekyll").touch()
    listing = "\n".join(entries) or "<li>No sessions published yet.</li>"
    (output / "index.html").write_text(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>IDA Assist sessions</title>
  <style>
    :root { color-scheme: dark; }
    body { max-width: 960px; margin: 64px auto; padding: 0 24px;
           background: #1e1e1e; color: #d4d4d4; font: 16px/1.6 system-ui, sans-serif; }
    h1 { font-size: 2rem; margin-bottom: 8px; }
    p, code { color: #a5a5a8; }
    ul { list-style: none; padding: 0; }
    li { padding: 20px 0; border-bottom: 1px solid #3a3a3d; overflow-wrap: anywhere; }
    a { color: #7cb7f0; text-underline-offset: 3px; }
    a:hover { color: #b3d5ff; }
    code { display: block; margin-top: 6px; font-size: 13px; }
  </style>
</head>
<body>
  <h1>IDA Assist sessions</h1>
  <p>Published session exports. Select a session to open it.</p>
  <ul>
"""
        + listing
        + "\n  </ul>\n</body>\n</html>\n",
        encoding="utf-8",
    )
    return len(pages)


if __name__ == "__main__":
    count = build(ROOT / "sessions", ROOT / "_site")
    print(f"Built {count} session page(s) in {ROOT / '_site'}")
