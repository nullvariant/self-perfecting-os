#!/usr/bin/env python3
"""
対話ログ自動保存スクリプト

VS Code Copilot Chatの対話を、Frontmatter付きMarkdownとして保存する。

Usage:
    # 基本使用（対話テキストをファイルから読み込み）
    python scripts/archive_conversation.py \\
      --topic "nullvariant-atelier設計" \\
      --conversation-file conversation.txt
    
    # Frontmatterカスタマイズ
    python scripts/archive_conversation.py \\
      --topic "ADR-0008実装" \\
      --context "生ログ保存システム検討" \\
      --decisions "Phase 1完了,Phase 2開始" \\
      --emotions "👮:S0011(誇り)-体系的実装,🦥:S0041(平安)-自動化見通し" \\
      --related "ADR-0008" \\
      --conversation-text "$(pbpaste)" \\
      --auto-commit
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
import subprocess
from typing import List, Optional


def generate_frontmatter(
    date: str,
    topic: str,
    context: Optional[str] = None,
    decisions: Optional[List[str]] = None,
    emotions: Optional[List[str]] = None,
    related: Optional[List[str]] = None
) -> str:
    """
    Frontmatter YAML生成
    
    Args:
        date: 日付（YYYY-MM-DD）
        topic: トピック
        context: 文脈
        decisions: 決定事項リスト
        emotions: 感情記録リスト
        related: 関連ファイルリスト
    
    Returns:
        str: Frontmatter YAML文字列
    """
    lines = ["---"]
    lines.append(f"date: {date}")
    lines.append(f"topic: {topic}")
    
    if context:
        lines.append(f"context: {context}")
    
    if decisions:
        lines.append("decisions:")
        for decision in decisions:
            lines.append(f"  - {decision}")
    
    if emotions:
        lines.append("emotions:")
        for emotion in emotions:
            lines.append(f"  - {emotion}")
    
    if related:
        lines.append("related:")
        for rel in related:
            lines.append(f"  - {rel}")
    
    lines.append("---")
    lines.append("")
    
    return "\n".join(lines)


def create_log_content(
    topic: str,
    conversation_text: str,
    frontmatter: str,
    token_usage: Optional[str] = None
) -> str:
    """
    対話ログの完全な内容を生成
    
    Args:
        topic: トピック
        conversation_text: 対話テキスト本文
        frontmatter: Frontmatter YAML
        token_usage: トークン使用率（オプション）
    
    Returns:
        str: 完全なログ内容
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    content = frontmatter
    content += f"# {topic}\n\n"
    content += f"**日時**: {date_str}\n"
    
    if token_usage:
        content += f"**トークン使用率**: {token_usage}\n"
    
    content += "\n---\n\n"
    content += conversation_text
    
    return content


def ensure_directory_exists(file_path: Path) -> None:
    """ディレクトリが存在しない場合は作成"""
    file_path.parent.mkdir(parents=True, exist_ok=True)


def save_conversation_log(
    topic: str,
    conversation_text: str,
    output_dir: Path,
    date: Optional[str] = None,
    context: Optional[str] = None,
    decisions: Optional[List[str]] = None,
    emotions: Optional[List[str]] = None,
    related: Optional[List[str]] = None,
    token_usage: Optional[str] = None
) -> Path:
    """
    対話ログを保存
    
    Args:
        topic: トピック
        conversation_text: 対話テキスト
        output_dir: 出力ディレクトリ
        date: 日付（省略時は今日）
        context: 文脈
        decisions: 決定事項リスト
        emotions: 感情記録リスト
        related: 関連ファイルリスト
        token_usage: トークン使用率
    
    Returns:
        Path: 保存されたファイルのパス
    """
    # 日付処理
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    dt = datetime.strptime(date, "%Y-%m-%d")
    year = dt.strftime("%Y")
    month = dt.strftime("%m")
    
    # ファイル名生成（トピックから安全な文字列に変換）
    safe_topic = topic.replace(" ", "_").replace("/", "_")
    filename = f"{date}_{safe_topic}.md"
    
    # 出力パス
    file_path = output_dir / year / month / filename
    
    # ディレクトリ作成
    ensure_directory_exists(file_path)
    
    # Frontmatter生成
    frontmatter = generate_frontmatter(
        date=date,
        topic=topic,
        context=context,
        decisions=decisions,
        emotions=emotions,
        related=related
    )
    
    # コンテンツ生成
    content = create_log_content(
        topic=topic,
        conversation_text=conversation_text,
        frontmatter=frontmatter,
        token_usage=token_usage
    )
    
    # ファイル書き込み
    file_path.write_text(content, encoding='utf-8')
    
    return file_path


def git_operations(file_path: Path, repo_path: Path) -> bool:
    """
    Git add/commit/push
    
    Args:
        file_path: 保存されたファイルのパス
        repo_path: Gitリポジトリのルートパス
    
    Returns:
        bool: 成功時True
    """
    try:
        # 相対パス取得
        rel_path = file_path.relative_to(repo_path)
        
        # git add
        subprocess.run(
            ['git', 'add', str(rel_path)],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"   ✅ git add: {rel_path}")
        
        # git commit
        date = datetime.now().strftime("%Y-%m-%d")
        commit_message = f"docs: 対話ログ追加 ({date})"
        
        result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"   ✅ git commit: {commit_message}")
        
        # git push
        subprocess.run(
            ['git', 'push', 'origin', 'main'],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"   ✅ git push: origin/main")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Git操作エラー: {e.stderr}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(
        description="VS Code Copilot Chat 対話ログ自動保存",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # 基本使用
    python scripts/archive_conversation.py \\
      --topic "PRD作成" \\
      --conversation-file conversation.txt
    
    # クリップボードから直接
    python scripts/archive_conversation.py \\
      --topic "ADR-0008実装" \\
      --conversation-text "$(pbpaste)"
    
    # フル指定
    python scripts/archive_conversation.py \\
      --topic "Phase 2実装開始" \\
      --context "スクリプト開発" \\
      --decisions "check_token_usage.py完成,archive_conversation.py実装開始" \\
      --emotions "👮:S0011(誇り)-段階的実装,🦥:S0041(平安)-自動化見通し" \\
      --related "ADR-0008,20251029_対話生ログ永続保存システム.md" \\
      --conversation-file conversation.txt \\
      --auto-commit
        """
    )
    
    # 必須引数
    parser.add_argument(
        '--topic',
        required=True,
        help='対話のトピック'
    )
    
    # 対話テキスト（どちらか必須）
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--conversation-file',
        type=Path,
        help='対話テキストファイルパス'
    )
    group.add_argument(
        '--conversation-text',
        help='対話テキスト（直接指定）'
    )
    
    # オプション引数
    parser.add_argument(
        '--date',
        help='日付（YYYY-MM-DD、省略時は今日）'
    )
    parser.add_argument(
        '--context',
        help='文脈'
    )
    parser.add_argument(
        '--decisions',
        help='決定事項（カンマ区切り）'
    )
    parser.add_argument(
        '--emotions',
        help='感情記録（カンマ区切り、例: "👮:S0011(誇り)-理由"）'
    )
    parser.add_argument(
        '--related',
        help='関連ファイル（カンマ区切り）'
    )
    parser.add_argument(
        '--token-usage',
        help='トークン使用率（例: "8.5%% (85,000 / 1,000,000)"）'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('../nullvariant-atelier/docs/log/'),
        help='出力先ディレクトリ（デフォルト: ../nullvariant-atelier/docs/log/）'
    )
    parser.add_argument(
        '--auto-commit',
        action='store_true',
        help='自動でgit commit/push'
    )
    
    args = parser.parse_args()
    
    # 対話テキスト取得
    if args.conversation_file:
        if not args.conversation_file.exists():
            print(f"❌ エラー: ファイルが見つかりません: {args.conversation_file}", file=sys.stderr)
            return 1
        conversation_text = args.conversation_file.read_text(encoding='utf-8')
    else:
        conversation_text = args.conversation_text
    
    # リスト変換
    decisions = args.decisions.split(',') if args.decisions else None
    emotions = args.emotions.split(',') if args.emotions else None
    related = args.related.split(',') if args.related else None
    
    # 出力ディレクトリの絶対パス取得
    output_dir = args.output_dir.resolve()
    
    print("=" * 60)
    print("📝 対話ログ保存")
    print("=" * 60)
    print()
    
    try:
        # ログ保存
        file_path = save_conversation_log(
            topic=args.topic,
            conversation_text=conversation_text,
            output_dir=output_dir,
            date=args.date,
            context=args.context,
            decisions=decisions,
            emotions=emotions,
            related=related,
            token_usage=args.token_usage
        )
        
        print(f"✅ 対話ログ保存完了:")
        print(f"   {file_path}")
        print()
        
        # Git操作
        if args.auto_commit:
            print("🔄 Git操作:")
            repo_path = output_dir.parent.parent  # docs/log/ -> docs/ -> repo_root/
            success = git_operations(file_path, repo_path)
            print()
            
            if not success:
                print("⚠️  Git操作に失敗しましたが、ファイルは保存されています。")
                return 1
        
        print("=" * 60)
        print("✅ 完了")
        print("=" * 60)
        
        return 0
        
    except Exception as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
