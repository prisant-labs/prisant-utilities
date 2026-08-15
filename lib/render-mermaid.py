#!/usr/bin/env python3
"""Pre-render Mermaid diagrams in an HTML file to EXTERNAL SVG files.

Finds Mermaid source blocks in the input HTML, calls `mmdc`
(@mermaid-js/mermaid-cli) to render each one to a standalone SVG file written
next to the HTML (named `<html-stem>_diagram-<N>.svg`), and replaces the source
block with an `<img src="<html-stem>_diagram-<N>.svg">` reference. Edits the
HTML in place via atomic write (temp file + rename).

Why external (v2.1.0; was inline through v2.0.0):
    Inlining a Mermaid SVG pasted 15-30KB of markup per diagram into the HTML,
    pushing a multi-diagram quick-reference toward ~350KB. That bloat made the
    HTML painful for the Edit tool to touch during the Phase 7 fit loop and cost
    ~100-150K tokens to read back. External SVG files keep the HTML around 30KB;
    headless Chrome embeds the referenced SVG into the print-to-PDF natively
    (verified), so the diagrams still ride through to the PDF.

Three block shapes are recognised, in this order:

    1. Markdown fenced blocks:    ```mermaid ... ```
    2. Pre/code blocks:           <pre><code class="language-mermaid">...</code></pre>
    3. Mermaid's native div:      <div class="mermaid">...</div>

When wrapped in a `.card.diagram` block, the produced `<img>` is sized by the
template's `.card.diagram img` rule (max-height 1.8in, or 2.2in for span-6).

Graceful degradation:
    If `mmdc` is not on PATH, the script logs a warning and leaves blocks
    untouched. Downstream gate G-18 (validate-no-mermaid-fences) then fails the
    bundle so the missing toolchain surfaces clearly.

Usage:
    lib/render-mermaid.py <html-path> [--quiet]

Exit codes:
    0  - success (or graceful no-op when mmdc missing)
    1  - bad arguments / file not found
    2  - mmdc invocation failed for one or more blocks
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FENCED_RE = re.compile(
    r"```mermaid\s*\n(?P<body>.*?)\n```",
    re.DOTALL,
)
PRE_CODE_RE = re.compile(
    r'<pre>\s*<code\s+class="language-mermaid">\s*(?P<body>.*?)\s*</code>\s*</pre>',
    re.DOTALL | re.IGNORECASE,
)
DIV_RE = re.compile(
    r'<div\s+class="mermaid">\s*(?P<body>.*?)\s*</div>',
    re.DOTALL | re.IGNORECASE,
)


def render_one(source: str, mmdc: str, work_dir: Path, out_dir: Path, stem: str, index: int) -> str:
    """Render one Mermaid source to an external SVG file; return an <img> tag referencing it.

    The .mmd source is written to a throwaway work_dir; the SVG output is written
    to out_dir (the HTML's own directory) so it ships alongside the bundle. The
    returned <img> uses a relative src (the bare filename), which resolves both
    when Chrome renders the HTML and when the bundle is moved.
    """
    src_path = work_dir / f"block-{index}.mmd"
    svg_path = out_dir / f"{stem}_diagram-{index}.svg"
    src_path.write_text(source, encoding="utf-8")
    result = subprocess.run(
        [mmdc, "-i", str(src_path), "-o", str(svg_path), "-b", "transparent"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"mmdc failed on block {index}:\n"
            f"  stderr: {result.stderr.strip()}\n"
            f"  source (first 200 chars): {source[:200]!r}"
        )
    if not svg_path.exists():
        raise RuntimeError(f"mmdc returned 0 but produced no SVG at {svg_path}")
    return f'<img src="{svg_path.name}" alt="diagram {index}">'


def render_blocks(html: str, mmdc: str, work_dir: Path, out_dir: Path, stem: str, quiet: bool) -> tuple[str, int]:
    """Replace every recognised Mermaid block in `html` with an external-SVG <img> tag."""
    counter = {"i": 0, "rendered": 0}

    def replace(match: re.Match) -> str:
        counter["i"] += 1
        body = match.group("body")
        try:
            img = render_one(body, mmdc, work_dir, out_dir, stem, counter["i"])
        except RuntimeError as exc:
            print(f"warn: {exc}", file=sys.stderr)
            return match.group(0)
        counter["rendered"] += 1
        if not quiet:
            svg = out_dir / f"{stem}_diagram-{counter['i']}.svg"
            print(f"rendered block {counter['i']} -> {svg.name} ({svg.stat().st_size:,} bytes external SVG)")
        return img

    out = FENCED_RE.sub(replace, html)
    out = PRE_CODE_RE.sub(replace, out)
    out = DIV_RE.sub(replace, out)
    return out, counter["rendered"]


def atomic_write(path: Path, content: str) -> None:
    """Write to a sibling temp file then rename, so a crash leaves the original intact."""
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("html_path", type=Path, help="HTML file to edit in place")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-block progress")
    args = parser.parse_args()

    if not args.html_path.exists():
        print(f"error: HTML file not found: {args.html_path}", file=sys.stderr)
        return 1
    if not args.html_path.is_file():
        print(f"error: not a regular file: {args.html_path}", file=sys.stderr)
        return 1

    mmdc = shutil.which("mmdc")
    if not mmdc:
        print(
            "warn: mmdc not found on PATH; leaving Mermaid blocks unrendered.\n"
            "      install with: npm install -g @mermaid-js/mermaid-cli",
            file=sys.stderr,
        )
        return 0

    html = args.html_path.read_text(encoding="utf-8")
    if not (FENCED_RE.search(html) or PRE_CODE_RE.search(html) or DIV_RE.search(html)):
        if not args.quiet:
            print("no Mermaid blocks found; nothing to do")
        return 0

    out_dir = args.html_path.parent
    stem = args.html_path.stem
    with tempfile.TemporaryDirectory() as tmp:
        work_dir = Path(tmp)
        try:
            new_html, rendered = render_blocks(html, mmdc, work_dir, out_dir, stem, args.quiet)
        except RuntimeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2

    atomic_write(args.html_path, new_html)
    if not args.quiet:
        print(f"done: {rendered} block(s) externalized to {stem}_diagram-*.svg next to {args.html_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
