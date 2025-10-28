#!/usr/bin/env python3
"""
note記事準備スクリプト
content/ja/AGENT.mdからアンカーと目次を除去し、note投稿用に整形する
"""

import argparse
import re
import sys
from pathlib import Path

TOC_BLOCK_PATTERN = re.compile(
    r'## (?:📋 )?目次 \(Table of Contents\).*?(?=\n## )',
    re.DOTALL
)


def remove_anchors_and_toc(content: str) -> str:
    """アンカータグと目次セクションを除去"""

    # アンカータグを除去
    content = re.sub(r'<a id="[^"]+"></a>\n', '', content)

    # 目次セクションを除去（"## 目次" から次の "##" セクションまで）
    content = TOC_BLOCK_PATTERN.sub('', content)

    return content

def convert_relative_to_absolute_links(content: str) -> str:
    """相対パスリンクをGitHub絶対URLに変換"""
    
    base_url = 'https://github.com/nullvariant/nullvariant/blob/main'
    
    # 相対パスのリンクをGitHub絶対URLに変換
    # 例: [CHANGELOG.md](../CHANGELOG.md) 
    #  → [CHANGELOG.md](https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md)
    # 例: [感情辞書](content/ja/EmotionMood_Dictionary.md)
    #  → [感情辞書](https://github.com/nullvariant/nullvariant/blob/main/content/ja/EmotionMood_Dictionary.md)
    
    def replace_relative_path(match):
        text = match.group(1)
        path = match.group(2)
        anchor = match.group(3) if match.lastindex >= 3 else ''
        
        # ../を削除してパス正規化
        path = path.replace('../', '')
        
        # content/などのプレフィックスがない場合は維持
        if not path.startswith('content/') and not path.startswith('changelogs/'):
            # ルートレベルのファイル（CHANGELOG.md等）
            full_url = f"{base_url}/{path}{anchor}"
        else:
            full_url = f"{base_url}/{path}{anchor}"
        
        return f"[{text}]({full_url})"
    
    # パターン1: ../付き相対パス
    content = re.sub(
        r'\[([^\]]+)\]\(\.\./([^\)#]+\.md)(#[^\)]+)?\)',
        replace_relative_path,
        content
    )
    
    # パターン2: ../なしの相対パス（content/やchangelogs/で始まる）
    content = re.sub(
        r'\[([^\]]+)\]\(((?:content|changelogs)/[^\)#]+\.md)(#[^\)]+)?\)',
        replace_relative_path,
        content
    )
    
    # パターン3: content/ プレフィックスなしの同ディレクトリファイル参照
    # 例: [S0005(安堵感)](EmotionMood_Dictionary.ja.md#レベル3単一型)
    #  → [S0005(安堵感)](https://github.com/.../content/ja/EmotionMood_Dictionary.md#レベル3単一型)
    def replace_same_dir_path(match):
        text = match.group(1)
        filename = match.group(2)
        anchor = match.group(3) if match.lastindex >= 3 else ''
        
        # 多言語移行後: content/ja/ に配置
        # AGENT.ja.md → AGENT.md, EmotionMood_Dictionary.ja.md → EmotionMood_Dictionary.md
        filename_clean = filename.replace('.ja.md', '.md').replace('.en.md', '.md')
        full_url = f"{base_url}/content/ja/{filename_clean}{anchor}"
        return f"[{text}]({full_url})"
    
    # [任意のテキスト](ファイル名.md) または [任意のテキスト](ファイル名.md#アンカー)
    # ファイル名は英数字、ハイフン、アンダースコア、ドットのみ
    content = re.sub(
        r'\[([^\]]+)\]\(([A-Za-z0-9_\-\.]+\.md)(#[^\)]+)?\)',
        replace_same_dir_path,
        content
    )
    
    # セクション内部参照のみのリンクは削除
    # 例: [Section 2.1.1](#sec-2-1-1) → Section 2.1.1
    content = re.sub(
        r'\[([^\]]+)\]\(#[^\)]+\)',
        r'\1',
        content
    )
    
    return content


VERSION_PATTERN = re.compile(r'^Version:\s*([0-9A-Za-z.\-_]+)\s*$', re.MULTILINE)


def detect_version(agent_content: str) -> str | None:
    """content/ja/AGENT.mdの先頭にあるVersion行からバージョン番号を推定"""
    match = VERSION_PATTERN.search(agent_content)
    return match.group(1) if match else None


def load_draft(draft_path: Path) -> str:
    """ドラフトを読み込む。存在しない場合は警告を出しテンプレートを返す。"""
    if draft_path.exists():
        print(f"📖 Reading {draft_path}...")
        return draft_path.read_text(encoding='utf-8')

    print(f"⚠️ Draft file not found: {draft_path}")
    print("   Using fallback template (AGENT本文のみ) for note export.")
    return '[ここにcontent/ja/AGENT.mdの全文を貼り付け]'


def main():
    parser = argparse.ArgumentParser(description="note投稿用Markdown生成スクリプト")
    parser.add_argument(
        "--version",
        help="出力ファイルのバージョン。省略時は content/ja/AGENT.md の Version 行から推定"
    )
    parser.add_argument(
        "--draft",
        help="note草稿ファイルパス。省略時は changelogs/note-archives/v{version}-note-draft.md"
    )
    parser.add_argument(
        "--output",
        help="出力ファイルパス。省略時は changelogs/note-archives/v{version}-note-complete.md"
    )
    args = parser.parse_args()

    # パス設定
    project_root = Path(__file__).parent.parent
    agent_file = project_root / 'content' / 'ja' / 'AGENT.md'

    print(f"📖 Reading {agent_file}...")
    agent_content = agent_file.read_text(encoding='utf-8')

    version = args.version or detect_version(agent_content)
    if not version:
        print("❌ Version could not be detected. Provide --version explicitly.", file=sys.stderr)
        sys.exit(1)

    draft_file = Path(args.draft) if args.draft else (
        project_root / 'changelogs' / 'note-archives' / f'v{version}-note-draft.md'
    )
    output_file = Path(args.output) if args.output else (
        project_root / 'changelogs' / 'note-archives' / f'v{version}-note-complete.md'
    )

    # アンカーと目次を除去
    print("🔧 Removing anchors and TOC...")
    clean_content = remove_anchors_and_toc(agent_content)

    # ドラフトを読み込みして本文を差し込み
    draft_content = load_draft(draft_file)

    print("✂️ Combining draft and content...")
    if '[ここにcontent/ja/AGENT.mdの全文を貼り付け]' in draft_content:
        final_content = draft_content.replace('[ここにcontent/ja/AGENT.mdの全文を貼り付け]', clean_content)
    else:
        print("   Placeholder not found in draft. Appending AGENT content at the end.")
        final_content = f"{draft_content.rstrip()}\n\n{clean_content}\n"

    # 相対パスリンクをGitHub絶対URLに変換
    print("🔗 Converting relative links to absolute URLs...")
    final_content = convert_relative_to_absolute_links(final_content)

    # 出力ファイルに保存
    print(f"💾 Saving to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(final_content, encoding='utf-8')

    print("✅ Complete! Ready for note publication.")
    print(f"📄 Output: {output_file}")
    print("\n次のステップ:")
    print(f"1. {output_file.name} をnoteにコピー＆ペースト")
    print("2. タイトル・ハッシュタグを設定して公開")
    print("3. 公開後、note URLをCHANGELOG.mdに追記")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
