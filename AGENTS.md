# Self-Perfecting OS

## Overview

Specification document for a 6-persona cooperative AI system architecture. Defines the "Bizarre Beast Zoo" metaphor — six archetypes that collaborate to form a self-improving operating system. Built around the core principle: "Choose from love, not fear." Primary source is in Japanese (`content/ja/`).

## Key Constraints

1. `content/ja/` is the single source of truth. All edits go there.
2. `content/en/` is a manual translation output. Auto-translation CI is discontinued; translation is done manually with AI assistance.
3. Translation quality: prioritize meaning accuracy over literal translation.
4. The persona system (6 characters) defined in `content/ja/AGENT.md` Section 2 is immutable — do not alter character definitions, relationships, or roles.
5. The EBI (Ecosystem Balance Index) measurement system is immutable — do not change metrics or calculation methods.

## Design Documents

- `content/ja/AGENT.md` — Primary specification (Japanese, ~43,000 tokens)
- `content/ja/EmotionMood_Dictionary.md` — Emotion taxonomy (54 types)
- `CHANGELOG.md` — Change history (Keep a Changelog format)

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/gen_toc.py          # Regenerate table of contents
```
