#!/usr/bin/env python3
"""
ADR Frontmatter Migration Script

既存のADRファイルから：
1. ファイル名末尾のカテゴリ（_category.md）を削除
2. YAMLフロントマターを追加（FRONTMATTER_STANDARDS.md準拠）
3. git mv でリネーム

Standards:
    docs/governance/FRONTMATTER_STANDARDS.md
    _meta/governance/FRONTMATTER_STANDARDS.md

Usage:
    python scripts/migrate_adr_frontmatter.py --dry-run    # 確認のみ
    python scripts/migrate_adr_frontmatter.py              # 実行
"""

import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
import argparse


def extract_metadata_from_filename(filename: str) -> dict:
    """
    ファイル名からメタデータを抽出
    
    例: 20251028_0001_ci-cd-pause_architecture.md
    → date=2025-10-28, number=0001, slug=ci-cd-pause, category=architecture
    """
    pattern = r'^(\d{8})_(\d{4})_([a-z0-9-]+)_([a-z]+)\.md$'
    match = re.match(pattern, filename)
    
    if not match:
        return None
    
    date_str, number, slug, category = match.groups()
    
    # 日付をYYYY-MM-DD形式に変換
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    date = f"{year}-{month}-{day}"
    
    return {
        'date': date,
        'number': number,
        'slug': slug,
        'category': category,
        'new_filename': f"{date_str}_{number}_{slug}.md"
    }


def extract_status_from_content(content: str) -> str:
    """
    ファイル内容からStatusを抽出
    
    例: **Status**: Accepted → 'Accepted'
    """
    pattern = r'\*\*Status\*\*:\s*(\w+)'
    match = re.search(pattern, content)
    
    if match:
        return match.group(1)
    
    return 'Accepted'  # デフォルト


def extract_author_from_content(content: str) -> str:
    """
    ファイル内容からAuthorを抽出
    
    例: **Author**: Claude (Cursor) → 'Claude (Cursor)'
    """
    pattern = r'\*\*Author\*\*:\s*(.+?)(?:\s*\*\*|\n)'
    match = re.search(pattern, content)
    
    if match:
        return match.group(1).strip()
    
    return 'Unknown'  # デフォルト


def has_frontmatter(content: str) -> bool:
    """
    既にYAMLフロントマターが存在するか確認
    """
    return content.startswith('---\n')


def create_frontmatter(metadata: dict, status: str, author: str) -> str:
    """
    YAMLフロントマターを生成
    
    Standards: docs/governance/FRONTMATTER_STANDARDS.md
    
    必須フィールド:
    - category: architecture, documentation, tooling, process, governance
    - date: YYYY-MM-DD
    - number: NNNN
    - status: Accepted, Superseded, Deprecated
    
    任意フィールド:
    - author: 決定者名
    """
    # 必須フィールド（FRONTMATTER_STANDARDS.md 準拠）
    fm = f"""---
category: {metadata['category']}
date: {metadata['date']}
number: {metadata['number']}
status: {status}
"""
    
    # 任意フィールド: author（存在する場合のみ）
    if author and author != 'Unknown':
        fm += f"author: {author}\n"
    
    fm += "---\n\n"
    
    return fm


def migrate_adr_file(file_path: Path, dry_run: bool = True) -> dict:
    """
    1つのADRファイルを移行
    
    Returns:
        result: {'success': bool, 'old_path': str, 'new_path': str, 'message': str}
    """
    filename = file_path.name
    
    # ファイル名からメタデータを抽出
    metadata = extract_metadata_from_filename(filename)
    
    if not metadata:
        return {
            'success': False,
            'old_path': str(file_path),
            'new_path': None,
            'message': f'パターンに一致しない: {filename}'
        }
    
    # ファイル内容を読み込み
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'success': False,
            'old_path': str(file_path),
            'new_path': None,
            'message': f'読み込みエラー: {e}'
        }
    
    # 既にFrontmatterがある場合はスキップ
    if has_frontmatter(content):
        return {
            'success': False,
            'old_path': str(file_path),
            'new_path': None,
            'message': '既にFrontmatterが存在（スキップ）'
        }
    
    # StatusとAuthorを抽出
    status = extract_status_from_content(content)
    author = extract_author_from_content(content)
    
    # 新しいファイルパス
    new_file_path = file_path.parent / metadata['new_filename']
    
    # Frontmatterを追加した新しい内容
    frontmatter = create_frontmatter(metadata, status, author)
    new_content = frontmatter + content
    
    if dry_run:
        return {
            'success': True,
            'old_path': str(file_path),
            'new_path': str(new_file_path),
            'message': 'DRY RUN（実行しない）',
            'category': metadata['category'],
            'status': status
        }
    
    # 実際の移行処理
    try:
        # 1. 新しい内容で書き込み
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # 2. git mv でリネーム
        result = subprocess.run(
            ['git', 'mv', str(file_path), str(new_file_path)],
            capture_output=True,
            text=True,
            cwd=file_path.parent.parent.parent.parent  # リポジトリルート
        )
        
        if result.returncode != 0:
            return {
                'success': False,
                'old_path': str(file_path),
                'new_path': str(new_file_path),
                'message': f'git mv 失敗: {result.stderr}'
            }
        
        return {
            'success': True,
            'old_path': str(file_path),
            'new_path': str(new_file_path),
            'message': '移行完了',
            'category': metadata['category'],
            'status': status
        }
        
    except Exception as e:
        return {
            'success': False,
            'old_path': str(file_path),
            'new_path': str(new_file_path),
            'message': f'エラー: {e}'
        }


def find_adr_files(decisions_dir: Path) -> list:
    """
    移行対象のADRファイルを検出
    
    パターン: {YYYYMMDD}_{NNNN}_{slug}_{category}.md
    """
    adr_files = []
    
    pattern = r'^\d{8}_\d{4}_[a-z0-9-]+_[a-z]+\.md$'
    
    for root, dirs, files in os.walk(decisions_dir):
        for filename in files:
            if re.match(pattern, filename):
                file_path = Path(root) / filename
                adr_files.append(file_path)
    
    return sorted(adr_files)


def main():
    parser = argparse.ArgumentParser(description='ADR Frontmatter Migration')
    parser.add_argument('--dry-run', action='store_true', help='確認のみ（実行しない）')
    parser.add_argument('--repo', choices=['nullvariant', 'nullvariant-atelier', 'both'], 
                        default='both', help='対象リポジトリ')
    args = parser.parse_args()
    
    # リポジトリパス
    base_dir = Path(__file__).parent.parent
    
    repos = []
    if args.repo in ['nullvariant', 'both']:
        repos.append({
            'name': 'nullvariant',
            'decisions_dir': base_dir / 'docs' / 'decisions'
        })
    if args.repo in ['nullvariant-atelier', 'both']:
        atelier_dir = base_dir.parent / 'nullvariant-atelier'
        if atelier_dir.exists():
            repos.append({
                'name': 'nullvariant-atelier',
                'decisions_dir': atelier_dir / '_meta' / 'decisions'
            })
    
    print("=" * 60)
    print("📝 ADR Frontmatter Migration")
    print("=" * 60)
    print()
    
    if args.dry_run:
        print("🔍 DRY RUN モード（実際には変更しません）")
        print()
    
    all_results = []
    
    for repo in repos:
        print(f"📦 リポジトリ: {repo['name']}")
        print(f"📂 ディレクトリ: {repo['decisions_dir']}")
        print()
        
        # ADRファイルを検出
        adr_files = find_adr_files(repo['decisions_dir'])
        
        if not adr_files:
            print("  ⚠️  移行対象のファイルが見つかりません")
            print()
            continue
        
        print(f"  ✅ {len(adr_files)} 個のファイルを検出")
        print()
        
        # 各ファイルを移行
        for file_path in adr_files:
            result = migrate_adr_file(file_path, dry_run=args.dry_run)
            all_results.append(result)
            
            if result['success']:
                symbol = '🔹' if args.dry_run else '✅'
                print(f"  {symbol} {file_path.name}")
                print(f"     → {Path(result['new_path']).name}")
                if 'category' in result:
                    print(f"     category: {result['category']}, status: {result['status']}")
            else:
                print(f"  ⚠️  {file_path.name}")
                print(f"     {result['message']}")
            print()
    
    # サマリー
    print("=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    success_count = sum(1 for r in all_results if r['success'])
    skip_count = sum(1 for r in all_results if not r['success'] and '既にFrontmatter' in r['message'])
    error_count = sum(1 for r in all_results if not r['success'] and '既にFrontmatter' not in r['message'])
    
    print(f"✅ 成功: {success_count}")
    print(f"⏭️  スキップ: {skip_count}")
    print(f"❌ エラー: {error_count}")
    print(f"📝 合計: {len(all_results)}")
    print()
    
    if args.dry_run:
        print("💡 実際に実行する場合は --dry-run を外してください")
    else:
        print("✅ 移行完了")


if __name__ == '__main__':
    main()

