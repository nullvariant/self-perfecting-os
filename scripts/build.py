#!/usr/bin/env python3
# Build script: translates content/ja/*.md to content/en/*.md and extracts YAML spec
import os, re, json, yaml, time, shutil
from pathlib import Path
from anthropic import Anthropic

MODEL_DEFAULT = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
ROOT = Path(__file__).resolve().parents[1]

# ソース言語とターゲット言語
SOURCE_LANG = "ja"
TARGET_LANGS = ["en"]  # 将来: ["en", "zh", "fr", ...]

# 入出力パス（多言語対応）
CONTENT_DIR = ROOT / "content"
SOURCE_DIR = CONTENT_DIR / SOURCE_LANG
TARGET_DIR = CONTENT_DIR / TARGET_LANGS[0]  # 現状はenのみ
ROOT_AGENT_MD = ROOT / "AGENT.md"  # 英語版エントリポイント

SPEC = ROOT / "spec" / "agent.spec.yaml"
SCHEMA = ROOT / "spec" / "agent.schema.json"
GLOSS = ROOT / "i18n" / "glossary.yml"
PROMPTS = ROOT / "scripts" / "prompts"

# Rate limit: 8,000 output tokens/min
LINES_PER_CHUNK = 100  # 行数ベースの分割（トークン推定が不正確なため）
MAX_OUTPUT_TOKENS = 5000  # 出力トークン制限（レート制限8K/分の範囲内）
RATE_LIMIT_WAIT = 70  # 60秒 + バッファ

def load(p: Path): return p.read_text(encoding="utf-8")
def save(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def compile_glossary(gloss):
    data = yaml.safe_load(gloss)
    entries = []
    for t in data.get("terms", []):
        if t.get("id") == "personas":
            for it in t.get("items", []):
                entries.append((it["ja"], f'personas:{it["emoji"]}', it["en"]["term"]))
        else:
            entries.append((t["ja"], t["id"], t["en"]["term"]))
    entries.sort(key=lambda x: len(x[0]), reverse=True)
    return entries, data

def inject_anchors(text: str, entries):
    out = text
    for ja, id_, _en in entries:
        out = re.sub(rf'(?<!\{{\#){re.escape(ja)}(?!\}})', f'{ja}{{#{id_}}}', out)
    return out

def estimate_tokens(text: str) -> int:
    """文字数からトークン数を概算（日本語: 1文字≈1.5トークン, 英数字: 1文字≈0.25トークン）"""
    # 簡易的に、総文字数 / 2.5 でトークン数を推定
    return int(len(text) / 2.5)

def split_document_by_lines(text: str, lines_per_chunk: int = LINES_PER_CHUNK):
    """
    ドキュメントを行数ベースで単純に分割
    （トークン推定が不正確なため、シンプルな行数分割を使用）
    """
    lines = text.split('\n')
    chunks = []

    # ヘッダー部分を抽出
    header_lines = []
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            content_start = i
            break
        header_lines.append(line)

    header = '\n'.join(header_lines)
    content_lines = lines[content_start:]

    # 行数ベースで分割
    for i in range(0, len(content_lines), lines_per_chunk):
        chunk_lines = content_lines[i:i + lines_per_chunk]
        chunks.append('\n'.join(chunk_lines))

    return chunks, header

def chat(model, system, prompt, temperature=0.0):
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    rsp = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,  # レート制限: 8,000 tokens/分を守る
        temperature=temperature,
        system=system,
        messages=[{"role":"user","content":prompt}],
        timeout=300.0  # 5分タイムアウト
    )
    return rsp.content[0].text

def translate_file(source_file: Path, target_file: Path, target_lang: str, glossary_map: dict):
    """
    単一ファイルを翻訳
    
    Args:
        source_file: ソースファイルパス（content/ja/AGENT.md等）
        target_file: ターゲットファイルパス（content/en/AGENT.md等）
        target_lang: ターゲット言語コード（"en", "zh"等）
        glossary_map: 用語辞書マップ
    """
    print(f"[INFO] Translating {source_file.name} ({SOURCE_LANG} → {target_lang})...")
    
    ja = load(source_file)
    gloss = load(GLOSS)
    entries, _ = compile_glossary(gloss)
    ja_anchored = inject_anchors(ja, entries)
    
    # ドキュメントを分割
    print(f"[INFO] Splitting {source_file.name} into chunks...")
    chunks, header = split_document_by_lines(ja_anchored, LINES_PER_CHUNK)
    print(f"[INFO] Document split into {len(chunks)} chunks (each ~{LINES_PER_CHUNK} lines)")
    
    # 各チャンクを翻訳
    sys_trans = load(PROMPTS / "01_en_translate.txt")
    translated_chunks = []
    
    for i, chunk in enumerate(chunks):
        lines = chunk.count('\n') + 1
        print(f"[INFO] Translating chunk {i+1}/{len(chunks)} (~{lines} lines)...")
        
        en_chunk = chat(
            MODEL_DEFAULT,
            sys_trans,
            f"### Glossary Map (id->EN)\n{json.dumps(glossary_map, ensure_ascii=False)}\n\n### JA (anchored)\n{chunk}"
        )
        translated_chunks.append(en_chunk)
        
        # レート制限対策: 最後のチャンク以外は待機
        if i < len(chunks) - 1:
            print(f"[INFO] Waiting {RATE_LIMIT_WAIT}s for rate limit...")
            time.sleep(RATE_LIMIT_WAIT)
    
    # 翻訳結果を結合
    print(f"[INFO] Merging translated chunks for {source_file.name}...")
    en_md = translated_chunks[0]
    for chunk in translated_chunks[1:]:
        chunk_lines = chunk.split('\n')
        content_start = 0
        in_header = False
        for j, line in enumerate(chunk_lines):
            if line.startswith('Codename:') or line.startswith('Version:'):
                in_header = True
            elif line.strip() == '---' and in_header:
                content_start = j + 1
                break
        
        if content_start > 0:
            chunk_content = '\n'.join(chunk_lines[content_start:])
        else:
            chunk_content = chunk
        
        en_md += '\n\n' + chunk_content.strip()
    
    # 保存
    save(target_file, en_md.strip() + "\n")
    print(f"[INFO] ✅ {source_file.name} → {target_file.name} completed")

def main():
    """
    多言語翻訳 + YAML抽出 + ルートAGENT.md生成
    """
    print("=" * 60)
    print("📝 Multilingual Build Started")
    print("=" * 60)
    
    # 用語辞書を読み込み
    gloss = load(GLOSS)
    entries, gloss_obj = compile_glossary(gloss)
    
    # glossary map for translator
    glossary_map = {}
    for t in yaml.safe_load(gloss).get("terms", []):
        if t.get("id") == "personas":
            for it in t.get("items", []):
                glossary_map[f'personas:{it["emoji"]}'] = it["en"]["term"]
        else:
            glossary_map[t["id"]] = t["en"]["term"]
    
    # 1) 多言語翻訳: ja/ の全.mdファイルを en/ に翻訳
    print("\n" + "=" * 60)
    print(f"📚 Step 1: Translating {SOURCE_LANG}/ → {TARGET_LANGS[0]}/")
    print("=" * 60)
    
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    
    for source_file in SOURCE_DIR.glob("*.md"):
        target_file = TARGET_DIR / source_file.name
        translate_file(source_file, target_file, TARGET_LANGS[0], glossary_map)
    
    # 2) ルートAGENT.mdを英語版からコピー
    print("\n" + "=" * 60)
    print("📄 Step 2: Copying content/en/AGENT.md → AGENT.md (entry point)")
    print("=" * 60)
    
    en_agent = TARGET_DIR / "AGENT.md"
    if en_agent.exists():
        shutil.copy(en_agent, ROOT_AGENT_MD)
        print(f"[INFO] ✅ AGENT.md created at root (English entry point)")
    else:
        print(f"[WARN] ⚠️ content/en/AGENT.md not found, skipping root copy")
    
    # 3) YAML spec (元のJAから抽出)
    print("\n" + "=" * 60)
    print("📦 Step 3: Extracting YAML spec from content/ja/AGENT.md")
    print("=" * 60)
    
    ja_agent = SOURCE_DIR / "AGENT.md"
    ja = load(ja_agent)
    
    sys_yaml = load(PROMPTS / "02_yaml_extract.txt")
    yaml_out = chat(MODEL_DEFAULT, sys_yaml, f"### JA (truth)\n{ja}")
    
    # マークダウンコードブロックを除去
    yaml_clean = yaml_out.strip()
    if yaml_clean.startswith('```'):
        lines = yaml_clean.split('\n')
        yaml_clean = '\n'.join(lines[1:-1])  # 最初と最後の```行を除去
    
    spec_obj = yaml.safe_load(yaml_clean)
    save(SPEC, yaml.dump(spec_obj, allow_unicode=True, sort_keys=False))
    print(f"[INFO] ✅ spec/agent.spec.yaml generated")
    
    print("\n" + "=" * 60)
    print("✅ Multilingual Build Completed Successfully!")
    print("=" * 60)
    print(f"\n📁 Generated files:")
    print(f"  - content/{TARGET_LANGS[0]}/*.md (translations)")
    print(f"  - AGENT.md (English entry point)")
    print(f"  - spec/agent.spec.yaml (YAML spec)")

if __name__ == "__main__":
    main()
```
