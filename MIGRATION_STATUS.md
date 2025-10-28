# OpenAI → Anthropic API Migration Status

**Status**: In Progress (CI/CD Disabled)
**Date**: 2025-10-28
**Branch**: `claude/review-code-011CURpzmxoqdeS8TvhsXGCU`

## Summary

Migration from OpenAI API to Anthropic API (Claude Sonnet 4.5) for the translation pipeline has been implemented but requires rate limit upgrade before production deployment.

## Completed Work

### ✅ API Migration
- [x] Migrated `scripts/build.py` from OpenAI to Anthropic client
- [x] Migrated `scripts/review.py` from OpenAI to Anthropic client
- [x] Updated `requirements.txt`: `openai` → `anthropic>=0.18.0`
- [x] Updated `.github/workflows/build.yml`: Environment variable changes
- [x] Updated documentation (README.md, CONTRIBUTING.md)

### ✅ Rate Limit Handling
- [x] Implemented chunked translation (100 lines per chunk)
- [x] Added 70s wait between chunks to respect rate limits
- [x] Reduced max_tokens to 5,000 (from initial 64,000)
- [x] Fixed YAML extraction to strip markdown code blocks
- [x] Translation successfully completes (20 chunks)

### ✅ Model Configuration
- Model: `claude-sonnet-4-5-20250929`
- Max tokens per chunk: 5,000
- Temperature: 0.0
- Timeout: 300s per chunk

## Current Issue

### Rate Limit Constraint (Tier 1)

**Problem**: Anthropic API Tier 1 has 8,000 output tokens/minute limit

**Impact**:
- Document split into 20 chunks
- Total execution time: ~25 minutes
- Cost per build+review: $2-3 USD
- Risk of timeout/errors with small chunks

**Current Tier Status**: Tier 1 (8K tokens/min)

**Cost So Far** (testing/debugging):
```
Input tokens:  424,474 × $3/1M  = $1.27
Output tokens: 254,934 × $15/1M = $3.82
Total: $5.09 USD
```

## Next Steps

### 1. Request Rate Limit Increase (Priority: HIGH)

**Action Required**:
1. Visit: https://console.anthropic.com/settings/limits
2. Click "Request a limit increase"
3. Request Tier 2 (40K/min) or Tier 3 (80K/min)
4. Expected approval time: Hours to 1 business day

**Benefits After Upgrade**:

| Tier | Rate Limit | Chunks Needed | Execution Time | Stability |
|------|-----------|---------------|----------------|-----------|
| Tier 1 (current) | 8K/min | 20 chunks | 25 minutes | Low |
| Tier 2 (target) | 40K/min | 4 chunks | 5 minutes | High |
| Tier 3 (ideal) | 80K/min | 2 chunks | 3 minutes | Very High |

**Note**: Cost per build remains $2-3 regardless of tier. Only execution time and stability improve.

### 2. Add Credits to Account

Current status: **Insufficient credits**

**Action Required**:
- Add $20-50 USD to Anthropic account
- Location: https://console.anthropic.com/settings/billing

### 3. Local Testing Before Production

**Recommended workflow**:

```bash
# Set environment variable
export ANTHROPIC_API_KEY=sk-ant-...

# Test with first 200 lines only (~$0.20)
python3 -c "
from scripts.build import *
ja_full = load(JA)
ja_test = '\n'.join(ja_full.split('\n')[:200])
# Run translation test...
"
```

This validates the pipeline without large cost.

### 4. Re-enable CI/CD

Once rate limit is increased and credits are added:

```bash
# Re-enable workflow
mv .github/workflows/build.yml.disabled .github/workflows/build.yml
git add .github/workflows/build.yml
git commit -m "chore: re-enable CI/CD after rate limit upgrade"
```

## File Changes Summary

### Modified Files
- `scripts/build.py`: Chunked translation with rate limit handling
- `scripts/review.py`: Chunked backtranslation and sampled review
- `requirements.txt`: anthropic>=0.18.0
- `.github/workflows/build.yml.disabled`: Temporarily disabled
- `README.md`: API key setup instructions
- `CONTRIBUTING.md`: API key setup instructions

### Key Implementation Details

**build.py**:
```python
LINES_PER_CHUNK = 100  # 100 lines per chunk
MAX_OUTPUT_TOKENS = 5000  # Stay within 8K/min limit
RATE_LIMIT_WAIT = 70  # 70s wait between chunks

# Translation loop
for i, chunk in enumerate(chunks):
    en_chunk = chat(MODEL_DEFAULT, sys_trans, chunk_prompt)
    translated_chunks.append(en_chunk)
    if i < len(chunks) - 1:
        time.sleep(RATE_LIMIT_WAIT)
```

**review.py**:
- Backtranslation: Same chunking strategy
- LLM review: Samples first/last 200 lines to reduce tokens

## Known Issues

### ✅ Fixed
- [x] Initial timeout errors (10min → 5min per chunk)
- [x] Token estimation inaccuracy (switched to line-based chunking)
- [x] YAML parsing error (strip markdown code blocks)

### ⏸️ Blocked (Waiting for Rate Limit Upgrade)
- [ ] Full pipeline execution test
- [ ] Translation quality verification
- [ ] Philosophical compatibility check (思想的適合性テスト)

## Rollback Plan

If issues arise, rollback is simple:

```bash
# Restore OpenAI API
git checkout main
git merge --no-ff claude/review-code-011CURpzmxoqdeS8TvhsXGCU
git revert HEAD
```

Previous OpenAI configuration is preserved in git history.

## Contact & Resources

- Anthropic Rate Limits: https://docs.anthropic.com/en/api/rate-limits
- Anthropic Console: https://console.anthropic.com/
- Support: https://www.anthropic.com/contact-sales

## Timeline

- **2025-10-28**: Migration implemented, rate limit issue identified
- **TBD**: Rate limit upgrade requested
- **TBD**: Full pipeline testing after upgrade
- **TBD**: Production deployment

---

**Status**: Ready for rate limit upgrade. CI/CD disabled to prevent unnecessary token consumption.
