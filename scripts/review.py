import os, json, yaml, time
from pathlib import Path
from jsonschema import Draft202012Validator
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer, util

MODEL_DEFAULT = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "content" / "AGENT.ja.md"
EN = ROOT / "AGENT.md"
SPEC = ROOT / "spec" / "agent.spec.yaml"
SCHEMA = ROOT / "spec" / "agent.schema.json"
GLOSS = ROOT / "i18n" / "glossary.yml"
PROMPTS = ROOT / "scripts" / "prompts" / "90_self_review.txt"
BACKPROMPT = ROOT / "scripts" / "prompts" / "99_backtranslate.txt"

# Rate limit: 8,000 output tokens/min
MAX_TOKENS_PER_CHUNK = 7000
RATE_LIMIT_WAIT = 65

def load(p: Path): return p.read_text(encoding="utf-8")

def estimate_tokens(text: str) -> int:
    """文字数からトークン数を概算"""
    return int(len(text) / 3.5)  # 英語は日本語より効率的

def split_text(text: str, max_tokens: int = MAX_TOKENS_PER_CHUNK):
    """テキストを行数ベースで分割"""
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_est_tokens = 0

    for line in lines:
        line_tokens = estimate_tokens(line)
        if current_est_tokens + line_tokens > max_tokens and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_est_tokens = line_tokens
        else:
            current_chunk.append(line)
            current_est_tokens += line_tokens

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

def backtranslate(en_md: str):
    """英語を日本語に逆翻訳（チャンク分割）"""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    system = load(BACKPROMPT)

    # ドキュメントを分割
    chunks = split_text(en_md, MAX_TOKENS_PER_CHUNK)
    print(f"[INFO] Backtranslating {len(chunks)} chunks...")

    translated_chunks = []
    for i, chunk in enumerate(chunks):
        tokens = estimate_tokens(chunk)
        print(f"[INFO] Backtranslating chunk {i+1}/{len(chunks)} (~{tokens} tokens)...")

        rsp = client.messages.create(
            model=MODEL_DEFAULT,
            max_tokens=8000,
            temperature=0.0,
            system=system,
            messages=[{"role":"user","content":chunk}],
            timeout=300.0
        )
        translated_chunks.append(rsp.content[0].text)

        if i < len(chunks) - 1:
            print(f"[INFO] Waiting {RATE_LIMIT_WAIT}s for rate limit...")
            time.sleep(RATE_LIMIT_WAIT)

    return '\n\n'.join(translated_chunks)

def llm_review(jp: str, en: str, spec: str):
    """LLMによるレビュー（入力を要約してレート制限を回避）"""
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    system = load(PROMPTS)

    # 入力が大きすぎる場合は、サンプリングして確認
    jp_lines = jp.split('\n')
    en_lines = en.split('\n')

    # 冒頭200行 + 末尾200行をサンプリング
    if len(jp_lines) > 500:
        jp_sample = '\n'.join(jp_lines[:200] + ['... (中略) ...'] + jp_lines[-200:])
    else:
        jp_sample = jp

    if len(en_lines) > 500:
        en_sample = '\n'.join(en_lines[:200] + ['... (omitted) ...'] + en_lines[-200:])
    else:
        en_sample = en

    prompt = f"# JA (sample)\n{jp_sample}\n\n# EN (sample)\n{en_sample}\n\n# YAML\n{spec}"

    rsp = client.messages.create(
        model=MODEL_DEFAULT,
        max_tokens=4000,  # レビューは短いので4000で十分
        temperature=0.0,
        system=system,
        messages=[{"role":"user","content":prompt}],
        timeout=180.0
    )
    return rsp.content[0].text

def ensure_keys(ja: str, en: str, gloss_obj: dict):
    must_ja, must_en = [], []
    for t in gloss_obj.get("terms", []):
        if t.get("id") == "personas":
            for it in t.get("items", []):
                must_ja.append(it["ja"]); must_en.append(it["en"]["term"])
        else:
            must_ja.append(t["ja"]); must_en.append(t["en"]["term"])
    miss_ja = [k for k in must_ja if k not in ja]
    miss_en = [k for k in must_en if k not in en]
    return miss_ja, miss_en

def embed_similarity(a: str, b: str):
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    ea = model.encode(a, convert_to_tensor=True, normalize_embeddings=True)
    eb = model.encode(b, convert_to_tensor=True, normalize_embeddings=True)
    return float(util.cos_sim(ea, eb).item())

def main(strict=False):
    ja = load(JA)
    en = load(EN)
    spec_txt = load(SPEC)
    spec_obj = yaml.safe_load(spec_txt)
    schema = json.loads(load(SCHEMA))
    gloss_obj = yaml.safe_load(load(GLOSS))

    Draft202012Validator(schema).validate(spec_obj)

    miss_ja, miss_en = ensure_keys(ja, en, gloss_obj)
    if miss_ja: raise SystemExit(f"[CRITICAL] JA missing glossary terms: {miss_ja}")
    if miss_en: raise SystemExit(f"[CRITICAL] EN missing glossary terms: {miss_en}")

    back_ja = backtranslate(en)
    sim = embed_similarity(ja, back_ja)
    print(f"[INFO] JA↔EN back-translation similarity: {sim:.4f}")
    if sim < 0.86: raise SystemExit(f"[CRITICAL] Semantic similarity below threshold: {sim:.4f}")

    review = llm_review(ja, en, spec_txt)
    print("=== LLM SELF-REVIEW ==="); print(review)
    if strict and ("[CRITICAL]" in review or "重大" in review):
        raise SystemExit("[CRITICAL] Self-review reported critical issues.")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    main(strict=args.strict)
