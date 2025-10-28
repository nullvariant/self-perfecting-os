#!/usr/bin/env python3
"""
ドキュメント内のパス参照チェックツール

用途:
- 古いパス参照を検出（例: content/AGENT.ja.md → content/ja/AGENT.md）
- 破損したリンクを検出
- 構造変更時の影響範囲を可視化

使用方法:
    python scripts/check_path_references.py [--fix]

オプション:
    --fix: 検出された問題を自動修正（対応パターンのみ）
"""

import re
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# プロジェクトルート
ROOT = Path(__file__).parent.parent

# チェック対象の古いパターン → 新しいパターン
DEPRECATED_PATTERNS = {
    # 多言語移行（2025-10-28）
    r'content/AGENT\.ja\.md': 'content/ja/AGENT.md',
    r'content/EmotionMood_Dictionary\.ja\.md': 'content/ja/EmotionMood_Dictionary.md',
    r'content/AGENT\.en\.md': 'content/en/AGENT.md',
    r'content/EmotionMood_Dictionary\.en\.md': 'content/en/EmotionMood_Dictionary.md',
    
    # API変更（2025-10-28）
    r'OPENAI_API_KEY': 'ANTHROPIC_API_KEY',
    
    # 廃止ファイル
    r'docs/OPERATIONS\.ja\.md': 'docs/operations/current/',
    r'docs/NOTE_SYNC_MANUAL\.ja\.md': 'docs/operations/current/',
    r'MIGRATION_STATUS\.md': 'docs/project-status.ja.md',
}

# 除外ディレクトリ
EXCLUDE_DIRS = {
    '.git', '__pycache__', '.venv', 'node_modules',
    '.github/workflows',      # CI設定は別途手動更新
    'docs/decisions',         # ADRは履歴情報として古いパスを保持（OK）
    'changelogs/note-archives',  # note公開記事アーカイブ（履歴として保持）
}

# 除外ファイル
EXCLUDE_FILES = {
    'check_path_references.py',  # 自身
}


def find_markdown_files(root: Path) -> List[Path]:
    """Markdownファイルを再帰的に検索"""
    md_files = []
    for path in root.rglob('*.md'):
        # 除外ディレクトリをスキップ
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        md_files.append(path)
    return md_files


def find_python_files(root: Path) -> List[Path]:
    """Pythonファイルを再帰的に検索"""
    py_files = []
    for path in root.rglob('*.py'):
        if any(excluded in path.parts for excluded in EXCLUDE_DIRS):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        py_files.append(path)
    return py_files


def check_file(filepath: Path) -> List[Dict[str, any]]:
    """ファイル内の古いパターンをチェック"""
    issues = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line_num, line in enumerate(lines, start=1):
        for old_pattern, new_pattern in DEPRECATED_PATTERNS.items():
            if re.search(old_pattern, line):
                issues.append({
                    'file': filepath,
                    'line': line_num,
                    'old': old_pattern,
                    'new': new_pattern,
                    'content': line.strip(),
                })
    
    return issues


def format_report(issues: List[Dict]) -> str:
    """検出結果をフォーマット"""
    if not issues:
        return "✅ 古いパス参照は検出されませんでした。"
    
    report = []
    report.append(f"⚠️  {len(issues)} 件の古いパス参照を検出しました:\n")
    
    # ファイル別にグルーピング
    by_file = {}
    for issue in issues:
        file_key = str(issue['file'].relative_to(ROOT))
        if file_key not in by_file:
            by_file[file_key] = []
        by_file[file_key].append(issue)
    
    for file_path, file_issues in sorted(by_file.items()):
        report.append(f"\n📄 {file_path}")
        for issue in file_issues:
            report.append(f"  Line {issue['line']}: {issue['old']} → {issue['new']}")
            report.append(f"    {issue['content'][:80]}...")
    
    report.append("\n\n💡 自動修正するには: python scripts/check_path_references.py --fix")
    
    return "\n".join(report)


def fix_issues(issues: List[Dict]) -> Dict[str, int]:
    """検出された問題を自動修正"""
    fixed_files = {}
    
    # ファイル別にグルーピング
    by_file = {}
    for issue in issues:
        if issue['file'] not in by_file:
            by_file[issue['file']] = []
        by_file[issue['file']].append(issue)
    
    for filepath, file_issues in by_file.items():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # 全パターンを適用
        for old_pattern, new_pattern in DEPRECATED_PATTERNS.items():
            content = re.sub(old_pattern, new_pattern, content)
        
        # 変更があれば書き戻し
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed_files[str(filepath.relative_to(ROOT))] = len(file_issues)
    
    return fixed_files


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ドキュメント内のパス参照をチェック')
    parser.add_argument('--fix', action='store_true', help='検出された問題を自動修正')
    args = parser.parse_args()
    
    print("🔍 ドキュメント内のパス参照をチェック中...\n")
    
    # MarkdownとPythonファイルをチェック
    all_files = find_markdown_files(ROOT) + find_python_files(ROOT)
    
    all_issues = []
    for filepath in all_files:
        issues = check_file(filepath)
        all_issues.extend(issues)
    
    # レポート出力
    print(format_report(all_issues))
    
    if args.fix and all_issues:
        print("\n\n🔧 自動修正を実行中...\n")
        fixed = fix_issues(all_issues)
        
        if fixed:
            print(f"✅ {len(fixed)} 個のファイルを修正しました:")
            for file_path, count in sorted(fixed.items()):
                print(f"  - {file_path} ({count} 箇所)")
            print("\n💡 変更内容を確認し、git commit してください。")
        else:
            print("⚠️  修正可能な問題が見つかりませんでした。")
        
        return 0 if fixed else 1
    
    # --fix なしの場合、問題があれば終了コード1
    return 1 if all_issues else 0


if __name__ == '__main__':
    sys.exit(main())
