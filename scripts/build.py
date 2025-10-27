#!/usr/bin/env python3
# Build script: translates AGENT.ja.md to English and extracts YAML spec
import os, re, json, yaml, time
from pathlib import Path
from anthropic import Anthropic

MODEL_DEFAULT = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
ROOT = Path(__file__).resolve().parents[1]
JA = ROOT / "content" / "AGENT.ja.md"
EN = ROOT / "AGENT.md"                     # ← root-level output
SPEC = ROOT / "spec" / "agent.spec.yaml"
SCHEMA = ROOT / "spec" / "agent.schema.json"
GLOSS = ROOT / "i18n" / "glossary.yml"
PROMPTS = ROOT / "scripts" / "prompts"

# Rate limit: 8,000 output tokens/min
MAX_TOKENS_PER_CHUNK = 7000  # 安全マージン
RATE_LIMIT_WAIT = 65  # 60秒 + バッファ

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

def split_document(text: str, max_tokens: int = MAX_TOKENS_PER_CHUNK):
    """
    ドキュメントをセクション（## レベル）で分割し、
    大きすぎるセクションはさらに分割する
    """
    lines = text.split('\n')
    chunks = []
    current_chunk = []
    current_tokens = 0

    # ヘッダー部分（最初の## が出るまで）を抽出
    header_lines = []
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('## '):
            content_start = i
            break
        header_lines.append(line)

    header = '\n'.join(header_lines)
    header_tokens = estimate_tokens(header)

    # セクションごとに処理
    i = content_start
    while i < len(lines):
        line = lines[i]

        # 新しいセクション（## ）の開始
        if line.startswith('## '):
            # 現在のチャンクを保存
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append(chunk_text)
                current_chunk = []
                current_tokens = 0

            # 新しいセクションの開始
            section_lines = [line]
            section_start = i
            i += 1

            # 次のセクション（## ）まで読み込む
            while i < len(lines) and not lines[i].startswith('## '):
                section_lines.append(lines[i])
                i += 1

            section_text = '\n'.join(section_lines)
            section_tokens = estimate_tokens(section_text)

            # セクションが大きすぎる場合は分割
            if section_tokens > max_tokens:
                print(f"[INFO] Large section detected ({section_tokens} tokens), splitting...")
                # 行数で半分に分割
                mid = len(section_lines) // 2
                part1 = '\n'.join(section_lines[:mid])
                part2 = '\n'.join(section_lines[mid:])
                chunks.append(part1)
                chunks.append(part2)
            else:
                # そのまま追加
                current_chunk = section_lines
                current_tokens = section_tokens
        else:
            i += 1

    # 最後のチャンクを保存
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        chunks.append(chunk_text)

    # 各チャンクにヘッダーを追加（最初のチャンク以外）
    final_chunks = []
    for i, chunk in enumerate(chunks):
        if i == 0:
            # 最初のチャンクはヘッダーを含んでいる可能性
            if not chunk.startswith('Codename:'):
                final_chunks.append(header + '\n\n---\n\n' + chunk)
            else:
                final_chunks.append(chunk)
        else:
            # 後続チャンクにはヘッダーを付けない（結合時に重複を避けるため）
            final_chunks.append(chunk)

    return final_chunks, header

def chat(model, system, prompt, temperature=0.0):
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    rsp = client.messages.create(
        model=model,
        max_tokens=8000,  # レート制限: 8,000 tokens/分
        temperature=temperature,
        system=system,
        messages=[{"role":"user","content":prompt}],
        timeout=300.0  # 5分タイムアウト（小さいチャンクなので短縮）
    )
    return rsp.content[0].text

def main():
    ja = load(JA)
    gloss = load(GLOSS)
    entries, gloss_obj = compile_glossary(gloss)
    ja_anchored = inject_anchors(ja, entries)

    # glossary map for translator
    glossary_map = {}
    for t in yaml.safe_load(gloss).get("terms", []):
        if t.get("id") == "personas":
            for it in t.get("items", []):
                glossary_map[f'personas:{it["emoji"]}'] = it["en"]["term"]
        else:
            glossary_map[t["id"]] = t["en"]["term"]

    # ドキュメントを分割
    print("[INFO] Splitting document into chunks...")
    chunks, header = split_document(ja_anchored, MAX_TOKENS_PER_CHUNK)
    print(f"[INFO] Document split into {len(chunks)} chunks")

    # 各チャンクを翻訳
    sys_trans = load(PROMPTS / "01_en_translate.txt")
    translated_chunks = []

    for i, chunk in enumerate(chunks):
        tokens = estimate_tokens(chunk)
        print(f"[INFO] Translating chunk {i+1}/{len(chunks)} (~{tokens} tokens)...")

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
    print("[INFO] Merging translated chunks...")
    # 最初のチャンクはヘッダーを含む、以降はコンテンツのみ
    en_md = translated_chunks[0]
    for chunk in translated_chunks[1:]:
        # ヘッダー部分を除去して結合
        chunk_lines = chunk.split('\n')
        # "Codename:" で始まる行から "---" までをスキップ
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

    # 2) YAML spec (元のJAから抽出)
    print("[INFO] Extracting YAML spec...")
    sys_yaml = load(PROMPTS / "02_yaml_extract.txt")
    yaml_out = chat(MODEL_DEFAULT, sys_yaml, f"### JA (truth)\n{ja}")
    spec_obj = yaml.safe_load(yaml_out)

    save(EN, en_md.strip()+"\n")
    save(SPEC, yaml.dump(spec_obj, allow_unicode=True, sort_keys=False))
    print("[INFO] Build completed successfully!")

if __name__ == "__main__":
    main()
