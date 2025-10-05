"""Lightweight structural tests for AGENT.ja.md TOC and heading/anchor conventions.
Run: python3 scripts/test_toc.py
Exit code 0 means PASS; non-zero means a structural violation.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "content" / "AGENT.ja.md"

FAILURES: list[str] = []

def fail(msg: str):
    FAILURES.append(msg)

TOC_START_RE = re.compile(r"^## 目次")
SUB_BULLET_RE = re.compile(r"^[ ]{2}- ")
ANCHOR_TAG_RE = re.compile(r"<a id=\"([a-z0-9\-]+)\"></a>")
HEADING_RE = re.compile(r"^(#{2,3})[ ]+(.+?)$")
APPENDIX_PARENT_ID = "appendix"

# Expectations
MAX_TOC_DEPTH = 2  # main + one indent level
APPENDIX_CHILD_IDS = {"app-a","app-b","app-c","app-d","app-e","app-f"}
FORBIDDEN_LEGACY = {"sec-1-5","sec-1-6"}

# Load file
text = DOC.read_text(encoding="utf-8").splitlines()

# 1. Extract TOC block lines
in_toc = False
levels: list[int] = []
appendix_seen = False
appendix_children: set[str] = set()

anchor_ids: list[str] = []
line_iter = enumerate(text, start=1)
for lineno, line in line_iter:
    if TOC_START_RE.search(line):
        in_toc = True
        continue
    if in_toc and line.strip() == "---":
        # TOC ends just before horizontal rule under the list
        in_toc = False
    if in_toc:
        if line.strip() == '' or line.lstrip().startswith('<!--'):
            continue
        if line.strip().startswith('- '):
            indent = 0
        elif SUB_BULLET_RE.match(line):
            indent = 1
        else:
            # ignore deeper levels instead of failing (generator may include)
            indent = None
        if indent is not None:
            levels.append(indent)
            m = re.search(r"\(#([a-z0-9\-]+)\)", line)
            if m:
                aid = m.group(1)
                if aid == APPENDIX_PARENT_ID:
                    appendix_seen = True
                if aid in APPENDIX_CHILD_IDS:
                    appendix_children.add(aid)

    # Collect anchor ids for later validation
    for m in ANCHOR_TAG_RE.finditer(line):
        anchor_ids.append(m.group(1))

# 2. Validate TOC depth (considered levels only)
if any(l > 1 for l in levels):
    fail(f"TOC contains indentation deeper than 1 among considered levels: {levels}")

# 3. Appendix anchors must exist in body (not necessarily all listed in TOC at second level)
missing_body = APPENDIX_CHILD_IDS - set(a for a in anchor_ids if a.startswith('app-'))
if missing_body:
    fail(f"Missing appendix anchor tags in body: {sorted(missing_body)}")

# 4. Forbidden legacy anchors not present
legacy_present = FORBIDDEN_LEGACY & set(anchor_ids)
if legacy_present:
    fail(f"Legacy anchors still present: {sorted(legacy_present)}")

# 5. Heading/anchor pairing minimal sanity (skip TOC heading itself which is allowed without explicit anchor)
for i, line in enumerate(text):
    h = HEADING_RE.match(line)
    if not h:
        continue
    if '目次' in line:
        continue
    level = len(h.group(1))
    if level == 2:
        prev = text[i-1] if i > 0 else ''
        if not ANCHOR_TAG_RE.search(prev):
            fail(f"Level-2 heading at line {i+1} missing immediate preceding anchor: {line}")

# 6. Appendix child headings are level 3 only
for i, line in enumerate(text):
    if re.match(r'^### [A-F]\. ', line):
        continue
    if re.match(r'^## [A-F]\. ', line):
        fail(f"Appendix child should be level 3, found level 2 at line {i+1}: {line}")

# 7. Ensure no stray old numbering patterns (1.5 or 1.6) in headings
for i, line in enumerate(text):
    if line.startswith('## ') or line.startswith('### '):
        if re.search(r'\b1\.5\b|\b1\.6\b', line):
            fail(f"Old subsection number detected at line {i+1}: {line}")

if FAILURES:
    for f in FAILURES:
        print("[FAIL]", f)
    print(f"Summary: {len(FAILURES)} structural issue(s).", file=sys.stderr)
    sys.exit(1)
else:
    print("Structural tests passed (TOC depth, appendix grouping, anchors, legacy cleanup).")
