#!/usr/bin/env python3
"""Generate or update the Table of Contents in AGENT.ja.md.

Rules:
- Detect headings starting with ## (level 2) and ### (level 3) but skip the TOC section itself.
- Preserve existing custom anchors (<a id="..."></a>) if present; generate slug ids if missing.
- Insert/replace block between lines starting with '## 目次' and the next '---' delimiter after it.
- Output is written in-place.

Assumptions:
- File encoding UTF-8.
- Anchors use pattern <a id="slug"></a> immediately preceding heading.
"""
from __future__ import annotations
import re
from pathlib import Path

MD_PATH = Path(__file__).resolve().parent.parent / 'content' / 'AGENT.ja.md'
TOC_HEADER_PATTERN = re.compile(r'^## 目次')
ANCHOR_PATTERN = re.compile(r'<a id="([^"]+)"></a>')
HEADING_PATTERN = re.compile(r'^(#{2,3})\s+(.+?)\s*$')
SLUG_SAFE = re.compile(r'[^a-z0-9\-]')

# Map Japanese / punctuation variants to simpler slug tokens if anchor missing
REPLACE_MAP = {
    '：': ':', '（': '(', '）': ')', '　': ' ', ' / ': '-', ' ': '-', '—': '-', '–': '-', '’': '', '「': '', '」': ''
}

def slugify(text: str) -> str:
    lower = text.lower()
    for k, v in REPLACE_MAP.items():
        lower = lower.replace(k, v)
    lower = re.sub(r'[#:().,_]+', '-', lower)
    lower = SLUG_SAFE.sub('-', lower)
    lower = re.sub(r'-{2,}', '-', lower).strip('-')
    if not lower:
        lower = 'section'
    return lower[:60]


def parse(md: str):
    lines = md.splitlines()
    toc_start = toc_end = None
    for i, line in enumerate(lines):
        if TOC_HEADER_PATTERN.match(line):
            toc_start = i
            # find next delimiter '---'
            for j in range(i+1, len(lines)):
                if lines[j].strip() == '---':
                    toc_end = j
                    break
            break
    headings = []
    current_anchor = None
    for i, line in enumerate(lines):
        m_anchor = ANCHOR_PATTERN.search(line)
        if m_anchor:
            current_anchor = m_anchor.group(1)
            continue
        m_head = HEADING_PATTERN.match(line)
        if m_head:
            level = len(m_head.group(1))
            title = m_head.group(2)
            if '目次' in title:  # skip TOC heading itself
                current_anchor = None
                continue
            anchor = current_anchor or slugify(title)
            headings.append((level, anchor, title))
            current_anchor = None
    return lines, toc_start, toc_end, headings


def build_toc(headings):
    out = ["## 目次 (Table of Contents)", ""]
    for level, anchor, title in headings:
        if level == 2:
            out.append(f"- [{title}](#{anchor})")
        elif level == 3:
            out.append(f"  - [{title.split(' ')[0]}](#{anchor})" if title.startswith(('3.', '6.')) else f"  - [{title}](#{anchor})")
    out.append("")
    return '\n'.join(out)


def main():
    text = MD_PATH.read_text(encoding='utf-8')
    lines, toc_start, toc_end, headings = parse(text)
    toc_block = build_toc(headings)
    # If no existing TOC, insert after metadata (first blank line after metadata block)
    if toc_start is None:
        # Insert after first triple-dash block or at top
        insertion_index = 0
        lines.insert(insertion_index, '---')
        lines.insert(insertion_index, toc_block)
        lines.insert(insertion_index, '---')
    else:
        # Replace old block (from toc_start to toc_end inclusive)
        new_lines = lines[:toc_start] + toc_block.splitlines() + lines[toc_end:]
        lines = new_lines
    joined = '\n'.join(lines)
    if not joined.endswith('\n'):
        joined += '\n'
    MD_PATH.write_text(joined, encoding='utf-8')
    print(f"TOC updated: {MD_PATH}")

if __name__ == '__main__':
    main()
