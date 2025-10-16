#!/usr/bin/env python3
"""
既存note記事のインポート

目的:
    Obsidian等に保存されている既存のnote記事を
    nullvariant-writingsのpublished/ディレクトリに
    インポートし、適切なメタデータを付与する。

使用例:
    # 対話的にインポート
    python import_note_articles.py \\
        --source ~/Obsidian/note記事/ \\
        --dest ../nullvariant-writings/writings/note/published/

    # バッチ処理（metadata.jsonを使用）
    python import_note_articles.py \\
        --source ~/Obsidian/note記事/ \\
        --dest ../nullvariant-writings/writings/note/published/ \\
        --batch metadata.json

依存関係: Python標準ライブラリのみ
"""

import argparse
import json
import re
import shutil
import yaml
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import sys


class ArticleImporter:
    """記事インポートのメインクラス"""
    
    def __init__(self, source_dir: Path, dest_dir: Path, dry_run: bool = False):
        self.source_dir = Path(source_dir)
        self.dest_dir = Path(dest_dir)
        self.dry_run = dry_run
        self.imported = []
        self.skipped = []
        
    def find_markdown_files(self) -> List[Path]:
        """Markdownファイルを検索"""
        markdown_files = []
        
        for pattern in ['*.md', '*.markdown']:
            markdown_files.extend(self.source_dir.glob(pattern))
            # サブディレクトリも検索
            markdown_files.extend(self.source_dir.glob(f'**/{pattern}'))
        
        # 重複除去・ソート
        unique_files = sorted(set(markdown_files))
        
        print(f"📁 検索ディレクトリ: {self.source_dir}")
        print(f"📄 見つかったMarkdownファイル: {len(unique_files)}件")
        
        return unique_files
    
    def extract_title_from_content(self, content: str) -> str:
        """ファイル内容からタイトルを抽出"""
        lines = content.split('\\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return ""
    
    def guess_date_from_filename(self, file_path: Path) -> Optional[str]:
        """ファイル名から日付を推測"""
        # YYYY-MM-DD パターンを検索
        date_pattern = r'(\\d{4}-\\d{2}-\\d{2})'
        match = re.search(date_pattern, file_path.name)
        if match:
            return match.group(1)
        
        # ファイルの更新日時を使用
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.strftime('%Y-%m-%d')
    
    def extract_note_url_from_content(self, content: str) -> Optional[str]:
        """記事内容からnoteのURLを抽出"""
        # note.comのURLパターンを検索
        url_pattern = r'https://note\\.com/[^\\s)]+/n/[a-zA-Z0-9]+'
        match = re.search(url_pattern, content)
        if match:
            return match.group(0)
        return None
    
    def interactive_metadata(self, file_path: Path, content: str) -> Optional[Dict]:
        """対話的にメタデータ入力"""
        print(f"\\n📄 ファイル: {file_path.name}")
        print("=" * 50)
        
        # タイトル自動抽出
        auto_title = self.extract_title_from_content(content)
        if auto_title:
            print(f"📝 抽出されたタイトル: {auto_title}")
            title = input(f"タイトル [{auto_title}]: ").strip() or auto_title
        else:
            title = input("タイトル (必須): ").strip()
            if not title:
                print("❌ タイトルが入力されませんでした。スキップします。")
                return None
        
        # 日付
        auto_date = self.guess_date_from_filename(file_path)
        date = input(f"公開日 (YYYY-MM-DD) [{auto_date}]: ").strip() or auto_date
        
        # URL
        auto_url = self.extract_note_url_from_content(content)
        if auto_url:
            print(f"🔗 抽出されたURL: {auto_url}")
            url = input(f"note URL [{auto_url}]: ").strip() or auto_url
        else:
            url = input("note URL (必須): ").strip()
            if not url:
                print("❌ URLが入力されませんでした。スキップします。")
                return None
        
        # プラットフォーム
        platform = input("プラットフォーム [note]: ").strip() or "note"
        
        # タグ
        tags_input = input("タグ (カンマ区切り): ").strip()
        tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
        
        # 確認
        print(f"\\n📋 設定内容:")
        print(f"  タイトル: {title}")
        print(f"  公開日: {date}")
        print(f"  URL: {url}")
        print(f"  プラットフォーム: {platform}")
        print(f"  タグ: {tags}")
        
        confirm = input("\\nこの設定でインポートしますか？ [Y/n]: ").strip()
        if confirm.lower() in ['', 'y', 'yes']:
            return {
                'title': title,
                'published_at': date,
                'platform': platform,
                'url': url,
                'canonical_url': url,
                'tags': tags,
                'status': 'published',
                'source_file': file_path.name
            }
        else:
            print("⏭️ スキップします。")
            return None
    
    def count_words(self, content: str) -> int:
        """文字数カウント"""
        # Front Matter除去
        content_clean = re.sub(r'^---.*?---\\s*', '', content, flags=re.DOTALL)
        # 空白除去して文字数カウント
        return len(re.sub(r'\\s', '', content_clean))
    
    def generate_frontmatter(self, metadata: Dict, word_count: int) -> str:
        """Front Matterを生成"""
        frontmatter_data = {
            'title': metadata['title'],
            'published_at': metadata['published_at'],
            'platform': metadata['platform'],
            'url': metadata['url'],
            'canonical_url': metadata['canonical_url'],
            'tags': metadata['tags'],
            'status': metadata['status'],
            'word_count': word_count,
            'source_file': metadata['source_file'],
            'imported_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        yaml_str = yaml.dump(frontmatter_data, default_flow_style=False, 
                            allow_unicode=True, sort_keys=False)
        return f"---\\n{yaml_str}---\\n\\n"
    
    def generate_dest_filename(self, metadata: Dict) -> str:
        """インポート先ファイル名を生成"""
        # タイトルからスラッグを生成
        title = metadata['title']
        slug = re.sub(r'[^\\w\\s-]', '', title)  # 英数字・ハイフン・空白のみ
        slug = re.sub(r'\\s+', '-', slug)  # 空白をハイフンに
        slug = slug.lower().strip('-')
        
        date = metadata['published_at']
        return f"{date}-{slug}.md"
    
    def import_article(self, file_path: Path, metadata: Dict) -> Optional[Path]:
        """記事をインポート"""
        try:
            # ファイル読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 既存のFront Matter除去
            content_clean = re.sub(r'^---.*?---\\s*', '', content, flags=re.DOTALL)
            
            # 文字数カウント
            word_count = self.count_words(content)
            
            # 新しいFront Matter生成
            frontmatter = self.generate_frontmatter(metadata, word_count)
            
            # インポート先ファイル名
            dest_filename = self.generate_dest_filename(metadata)
            dest_path = self.dest_dir / dest_filename
            
            if dest_path.exists():
                if not self.dry_run:
                    response = input(f"ファイル {dest_path} は既に存在します。上書きしますか？ [y/N]: ")
                    if response.lower() != 'y':
                        print("⏭️ スキップしました。")
                        return None
            
            # 最終コンテンツ
            final_content = frontmatter + content_clean
            
            if self.dry_run:
                print(f"[DRY RUN] {file_path} → {dest_path}")
                return dest_path
            
            # インポート先ディレクトリ作成
            self.dest_dir.mkdir(parents=True, exist_ok=True)
            
            # ファイル書き込み
            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            print(f"✅ インポート完了: {dest_path}")
            return dest_path
            
        except Exception as e:
            print(f"❌ インポートエラー ({file_path}): {e}")
            return None
    
    def load_batch_metadata(self, batch_file: Path) -> Dict[str, Dict]:
        """バッチ処理用メタデータを読み込み"""
        try:
            with open(batch_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ バッチファイル読み込みエラー: {e}")
            return {}
    
    def generate_report(self) -> str:
        """インポートレポート生成"""
        report = f"""
📊 インポート結果レポート

📄 処理対象ファイル数: {len(self.imported) + len(self.skipped)}
✅ インポート成功: {len(self.imported)}
⏭️ スキップ: {len(self.skipped)}

✅ インポート成功したファイル:
"""
        for file_path in self.imported:
            report += f"  - {file_path}\\n"
        
        if self.skipped:
            report += f"\\n⏭️ スキップしたファイル:\\n"
            for file_path in self.skipped:
                report += f"  - {file_path}\\n"
        
        return report
    
    def execute(self, batch_metadata: Optional[Dict[str, Dict]] = None):
        """メイン処理"""
        print(f"🚀 記事インポートを開始...")
        print(f"📁 ソース: {self.source_dir}")
        print(f"📁 インポート先: {self.dest_dir}")
        
        if self.dry_run:
            print("🔍 [DRY RUN MODE] 実際のファイル操作は行いません")
        
        markdown_files = self.find_markdown_files()
        
        if not markdown_files:
            print("❌ Markdownファイルが見つかりませんでした。")
            return
        
        for file_path in markdown_files:
            print(f"\\n" + "="*60)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"❌ ファイル読み込みエラー ({file_path}): {e}")
                self.skipped.append(file_path)
                continue
            
            # メタデータ取得
            if batch_metadata and file_path.name in batch_metadata:
                # バッチ処理
                metadata = batch_metadata[file_path.name]
                print(f"📄 バッチ処理: {file_path.name}")
            else:
                # 対話的入力
                metadata = self.interactive_metadata(file_path, content)
            
            if metadata is None:
                self.skipped.append(file_path)
                continue
            
            # インポート実行
            dest_path = self.import_article(file_path, metadata)
            if dest_path:
                self.imported.append(dest_path)
            else:
                self.skipped.append(file_path)
        
        # レポート表示
        print("\\n" + "="*60)
        print(self.generate_report())


def main():
    parser = argparse.ArgumentParser(
        description='既存note記事をnullvariant-writingsにインポート',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
    # 対話的インポート
    python import_note_articles.py \\
        --source ~/Obsidian/note記事/ \\
        --dest ../nullvariant-writings/writings/note/published/

    # バッチ処理
    python import_note_articles.py \\
        --source ~/Obsidian/note記事/ \\
        --dest ../nullvariant-writings/writings/note/published/ \\
        --batch metadata.json

    # ドライラン
    python import_note_articles.py \\
        --source ~/Obsidian/note記事/ \\
        --dest ../nullvariant-writings/writings/note/published/ \\
        --dry-run
        """)
    
    parser.add_argument('--source', type=Path, required=True, 
                       help='インポート元ディレクトリ')
    parser.add_argument('--dest', type=Path, required=True, 
                       help='インポート先ディレクトリ')
    parser.add_argument('--batch', type=Path, 
                       help='バッチ処理用メタデータJSONファイル')
    parser.add_argument('--dry-run', action='store_true', 
                       help='実行せずに処理内容を確認')
    
    args = parser.parse_args()
    
    # バリデーション
    if not args.source.exists():
        print(f"❌ ソースディレクトリが見つかりません: {args.source}")
        sys.exit(1)
    
    if not args.source.is_dir():
        print(f"❌ ソースはディレクトリである必要があります: {args.source}")
        sys.exit(1)
    
    # バッチメタデータ読み込み
    batch_metadata = None
    if args.batch:
        if not args.batch.exists():
            print(f"❌ バッチファイルが見つかりません: {args.batch}")
            sys.exit(1)
        importer = ArticleImporter(args.source, args.dest, args.dry_run)
        batch_metadata = importer.load_batch_metadata(args.batch)
    
    # インポート実行
    importer = ArticleImporter(args.source, args.dest, args.dry_run)
    importer.execute(batch_metadata)


if __name__ == '__main__':
    main()