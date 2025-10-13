#!/usr/bin/env python3
"""
note記事準備スクリプト
AGENT.ja.mdからアンカーと目次を除去し、note投稿用に整形する
"""

import re
import sys
from pathlib import Path

def remove_anchors_and_toc(content: str) -> str:
    """アンカータグと目次セクションを除去"""
    
    # アンカータグを除去
    content = re.sub(r'<a id="[^"]+"></a>\n', '', content)
    
    # 目次セクションを除去（"## 目次" から次の "##" セクションまで）
    content = re.sub(
        r'## 目次 \(Table of Contents\).*?(?=\n## )',
        '',
        content,
        flags=re.DOTALL
    )
    
    return content

def convert_relative_to_absolute_links(content: str) -> str:
    """相対パスリンクをGitHub絶対URLに変換"""
    
    base_url = 'https://github.com/nullvariant/nullvariant/blob/main'
    
    # 相対パスのリンクをGitHub絶対URLに変換
    # 例: [CHANGELOG.md](../CHANGELOG.md) 
    #  → [CHANGELOG.md](https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md)
    # 例: [感情辞書](content/EmotionMood_Dictionary.ja.md)
    #  → [感情辞書](https://github.com/nullvariant/nullvariant/blob/main/content/EmotionMood_Dictionary.ja.md)
    
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
    #  → [S0005(安堵感)](https://github.com/.../content/EmotionMood_Dictionary.ja.md#レベル3単一型)
    def replace_same_dir_path(match):
        text = match.group(1)
        filename = match.group(2)
        anchor = match.group(3) if match.lastindex >= 3 else ''
        
        # AGENT.ja.mdと同じディレクトリ（content/）と仮定
        full_url = f"{base_url}/content/{filename}{anchor}"
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

def main():
    # パス設定
    project_root = Path(__file__).parent.parent
    agent_file = project_root / 'content' / 'AGENT.ja.md'
    draft_file = project_root / 'changelogs' / 'note-archives' / 'v4.1-note-draft.md'
    output_file = project_root / 'changelogs' / 'note-archives' / 'v4.1-note-complete.md'
    
    # AGENT.ja.md を読み込み
    print(f"📖 Reading {agent_file}...")
    with open(agent_file, 'r', encoding='utf-8') as f:
        agent_content = f.read()
    
    # アンカーと目次を除去
    print("🔧 Removing anchors and TOC...")
    clean_content = remove_anchors_and_toc(agent_content)
    
    # ドラフトを読み込み
    print(f"📖 Reading {draft_file}...")
    with open(draft_file, 'r', encoding='utf-8') as f:
        draft_content = f.read()
    
    # プレースホルダーを置換
    print("✂️ Combining draft and content...")
    final_content = draft_content.replace(
        '[ここにAGENT.ja.mdの全文を貼り付け]',
        clean_content
    )
    
    # 相対パスリンクをGitHub絶対URLに変換
    print("🔗 Converting relative links to absolute URLs...")
    final_content = convert_relative_to_absolute_links(final_content)
    
    # 出力ファイルに保存
    print(f"💾 Saving to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print("✅ Complete! Ready for note publication.")
    print(f"📄 Output: {output_file}")
    print("\n次のステップ:")
    print("1. v4.1-note-complete.md をnoteにコピー＆ペースト")
    print("2. タイトル・ハッシュタグを設定して公開")
    print("3. 公開後、note URLをCHANGELOG.mdに追記")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
