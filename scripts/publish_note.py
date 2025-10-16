#!/usr/bin/env python3
"""
note記事公開後の処理を自動化

目的:
    note等のプラットフォームに記事を公開した後、
    下書きファイルを公開済みアーカイブに移動し、
    メタデータを追加してバージョン管理する。

使用例:
    python publish_note.py \
        ../nullvariant-writings/writings/note/drafts/2025-10-16-topic.md \
        --url https://note.com/nullvariant/n/xxxxx \
        --platform note \
        --date 2025-10-16

依存関係: Python標準ライブラリのみ
"""

import argparse
import shutil
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import sys


class NotePublisher:
    """note記事公開処理のメインクラス"""
    
    def __init__(self, draft_path: Path, url: str, platform: str, 
                 publish_date: str, dry_run: bool = False):
        self.draft_path = Path(draft_path)
        self.url = url
        self.platform = platform
        self.publish_date = publish_date
        self.dry_run = dry_run
        
        # パス設定
        # ../nullvariant-writings/writings/note/drafts/file.md から
        # ../nullvariant-writings を取得
        current_path = self.draft_path.parent  # drafts
        current_path = current_path.parent     # note
        current_path = current_path.parent     # writings
        self.writings_root = current_path.parent  # nullvariant-writings
        
        self.published_dir = self.writings_root / "writings" / platform / "published"
        self.corpus_file = self.writings_root / "CORPUS.md"
        
    def extract_title(self, content: str) -> str:
        """Markdownから記事タイトルを抽出"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        
        # H1が見つからない場合はファイル名から推測
        stem = self.draft_path.stem
        # YYYY-MM-DD- のプレフィックスを除去
        title_part = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
        return title_part.replace('-', ' ').title()
    
    def count_words(self, content: str) -> int:
        """日本語を考慮した文字数カウント"""
        # Markdownのメタデータ部分を除去
        content_without_frontmatter = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        # 改行・空白を除去して文字数をカウント
        clean_content = re.sub(r'\s', '', content_without_frontmatter)
        return len(clean_content)
    
    def extract_tags(self, content: str) -> List[str]:
        """記事末尾のタグを抽出"""
        # **タグ**: #tag1 #tag2 形式を検索
        tag_pattern = r'\*\*タグ\*\*[:\s]*(.+)'
        match = re.search(tag_pattern, content)
        if match:
            tag_text = match.group(1)
            # #で始まる単語を抽出
            tags = re.findall(r'#(\w+)', tag_text)
            return tags
        return []
    
    def generate_metadata(self, content: str) -> Dict:
        """記事のメタデータを生成"""
        title = self.extract_title(content)
        word_count = self.count_words(content)
        tags = self.extract_tags(content)
        
        return {
            'title': title,
            'published_at': self.publish_date,
            'platform': self.platform,
            'url': self.url,
            'canonical_url': self.url,
            'source_draft': self.draft_path.name,
            'tags': tags,
            'status': 'published',
            'word_count': word_count
        }
    
    def generate_frontmatter(self, title: str, word_count: int, tags: List[str]) -> str:
        """Front Matterを生成"""
        frontmatter = {
            'title': title,
            'published_at': self.publish_date,
            'platform': self.platform,
            'url': self.url,
            'canonical_url': self.url,  # SEO正規版URL
            'source_draft': self.draft_path.name,
            'tags': tags,
            'status': 'published',
            'word_count': word_count
        }
        
        yaml_str = yaml.dump(frontmatter, default_flow_style=False, 
                            allow_unicode=True, sort_keys=False)
        return f"---\n{yaml_str}---\n\n"
    
    def add_frontmatter(self, content: str) -> str:
        """既存コンテンツにFront Matterを追加"""
        title = self.extract_title(content)
        word_count = self.count_words(content)
        tags = self.extract_tags(content)
        
        frontmatter = self.generate_frontmatter(title, word_count, tags)
        
        # 既存のFront Matterがあれば除去
        content_without_frontmatter = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        
        return frontmatter + content_without_frontmatter
    
    def generate_published_filename(self) -> str:
        """公開済みファイル名を生成"""
        # ファイル名からトピック部分を抽出
        stem = self.draft_path.stem
        topic_part = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', stem)
        return f"{self.publish_date}-{topic_part}.md"
    
    def move_to_published(self) -> Path:
        """drafts/ から published/ へ移動"""
        if not self.draft_path.exists():
            raise FileNotFoundError(f"下書きファイルが見つかりません: {self.draft_path}")
        
        # 公開済みディレクトリが存在しない場合は作成
        self.published_dir.mkdir(parents=True, exist_ok=True)
        
        # 公開済みファイルパス
        published_filename = self.generate_published_filename()
        published_path = self.published_dir / published_filename
        
        if published_path.exists():
            if not self.dry_run:
                response = input(f"ファイル {published_path} は既に存在します。上書きしますか？ [y/N]: ")
                if response.lower() != 'y':
                    print("処理を中止しました。")
                    sys.exit(1)
        
        # ファイル内容を読み込み
        with open(self.draft_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Front Matter追加
        content_with_metadata = self.add_frontmatter(content)
        
        if self.dry_run:
            print(f"[DRY RUN] {self.draft_path} → {published_path}")
            print(f"[DRY RUN] Front Matter:")
            frontmatter_only = content_with_metadata.split('---\n\n')[0] + '---'
            print(frontmatter_only)
            return published_path
        
        # 公開済みファイルに書き込み
        with open(published_path, 'w', encoding='utf-8') as f:
            f.write(content_with_metadata)
        
        print(f"✅ 公開済みファイルを作成: {published_path}")
        return published_path
    
    def update_corpus(self, published_path: Path, metadata: Dict):
        """CORPUS.mdを更新"""
        if not self.corpus_file.exists():
            print(f"⚠️ CORPUS.mdが見つかりません: {self.corpus_file}")
            return
        
        if self.dry_run:
            print(f"[DRY RUN] CORPUS.md更新をスキップ")
            return
        
        # CORPUS.mdを読み込み
        with open(self.corpus_file, 'r', encoding='utf-8') as f:
            corpus_content = f.read()
        
        # 記事情報を追加
        year_month = metadata['published_at'][:7]  # 2025-10
        year, month = year_month.split('-')
        section_header = f"#### {year}年{int(month)}月"
        
        article_entry = (
            f"- **[{metadata['title']}]({metadata['url']})** "
            f"({metadata['published_at']}) - {metadata['word_count']}文字\n"
            f"  - タグ: {', '.join(metadata['tags'])}\n"
        )
        
        # セクションが存在するか確認し、適切な位置に挿入
        if section_header in corpus_content:
            # 既存セクションに追加
            pattern = f"({re.escape(section_header)}.*?)\n\n"
            match = re.search(pattern, corpus_content, re.DOTALL)
            if match:
                section_content = match.group(1)
                new_section = section_content + "\n" + article_entry
                corpus_content = corpus_content.replace(section_content, new_section)
        else:
            # 新しいセクションを作成
            note_section_start = corpus_content.find("### note記事")
            if note_section_start != -1:
                # note記事セクションの直後に挿入
                insertion_point = corpus_content.find("\n", note_section_start) + 1
                new_section = f"\n{section_header}（1件）\n\n{article_entry}\n"
                corpus_content = corpus_content[:insertion_point] + new_section + corpus_content[insertion_point:]
        
        # 統計情報の更新
        # 総記事数と総文字数の更新（簡易実装）
        corpus_content = re.sub(
            r'総記事数: \d+',
            f'総記事数: {corpus_content.count("- **[")}"',
            corpus_content
        )
        
        # 最終更新日の更新
        today = datetime.now().strftime('%Y-%m-%d')
        corpus_content = re.sub(
            r'最終更新: \d{4}-\d{2}-\d{2}',
            f'最終更新: {today}',
            corpus_content
        )
        
        # ファイルに書き戻し
        with open(self.corpus_file, 'w', encoding='utf-8') as f:
            f.write(corpus_content)
        
        print(f"📚 CORPUS.md更新: {published_path.name}")
    
    def cleanup_draft(self):
        """下書きファイルの削除確認"""
        if self.dry_run:
            print(f"[DRY RUN] 下書きファイル削除をスキップ: {self.draft_path}")
            return
        
        response = input(f"下書きファイル {self.draft_path} を削除しますか？ [y/N]: ")
        if response.lower() == 'y':
            self.draft_path.unlink()
            print(f"🗑️ 下書きファイルを削除: {self.draft_path}")
        else:
            print(f"📝 下書きファイルを保持: {self.draft_path}")
    
    def execute(self) -> bool:
        """メイン処理実行"""
        try:
            print(f"🚀 note記事公開処理を開始...")
            print(f"📄 下書き: {self.draft_path}")
            print(f"🌐 URL: {self.url}")
            print(f"📅 公開日: {self.publish_date}")
            
            if self.dry_run:
                print("🔍 [DRY RUN MODE] 実際の処理は行いません")
            
            # 1. published/ へ移動・メタデータ追加
            published_path = self.move_to_published()
            
            # 2. CORPUS.md更新
            # メタデータを再生成
            content = self.draft_path.read_text(encoding='utf-8')
            metadata = self.generate_metadata(content)
            self.update_corpus(published_path, metadata)
            
            # 3. 下書きファイルの削除確認
            if not self.dry_run:
                self.cleanup_draft()
            
            print("✅ 処理完了!")
            return True
            
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            if self.dry_run:
                print("🔍 [DRY RUN] エラーを無視して続行")
                return True
            return False


def validate_url(url: str) -> bool:
    """URLの基本的なバリデーション"""
    if not url.startswith(('http://', 'https://')):
        return False
    if 'note.com' in url and '/n/' not in url:
        return False
    return True


def main():
    parser = argparse.ArgumentParser(
        description='note記事公開後の処理を自動化',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
    python publish_note.py \\
        ../nullvariant-writings/writings/note/drafts/2025-10-16-topic.md \\
        --url https://note.com/nullvariant/n/xxxxx \\
        --platform note \\
        --date 2025-10-16

    # ドライラン（実際の処理は行わない）
    python publish_note.py \\
        draft.md --url https://example.com --dry-run
        """)
    
    parser.add_argument('draft', type=Path, help='下書きファイルのパス')
    parser.add_argument('--url', required=True, help='公開URL')
    parser.add_argument('--platform', default='note', 
                       choices=['note', 'zenn', 'medium'], 
                       help='公開プラットフォーム (default: note)')
    parser.add_argument('--date', help='公開日（YYYY-MM-DD形式、未指定時は今日）')
    parser.add_argument('--dry-run', action='store_true', 
                       help='実行せずに処理内容を確認')
    
    args = parser.parse_args()
    
    # バリデーション
    if not args.draft.exists():
        print(f"❌ ファイルが見つかりません: {args.draft}")
        sys.exit(1)
    
    if not validate_url(args.url):
        print(f"❌ 無効なURLです: {args.url}")
        sys.exit(1)
    
    # 公開日設定
    publish_date = args.date or datetime.now().strftime('%Y-%m-%d')
    
    # 処理実行
    publisher = NotePublisher(
        draft_path=args.draft,
        url=args.url,
        platform=args.platform,
        publish_date=publish_date,
        dry_run=args.dry_run
    )
    
    success = publisher.execute()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()