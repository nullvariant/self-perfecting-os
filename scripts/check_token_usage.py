#!/usr/bin/env python3
"""
トークン使用率監視スクリプト

VS Code Copilot Chatのトークン使用状況を推定し、警告を出力する。

Usage:
    python scripts/check_token_usage.py
    python scripts/check_token_usage.py --detailed
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Iterable, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency
    yaml = None


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONVERSATION_DIR_CANDIDATES = [
    PROJECT_ROOT / "conversations",
    PROJECT_ROOT / "docs" / "log",
]
LOG_FILE_EXTENSIONS = {".md", ".markdown", ".json", ".yaml", ".yml", ".txt"}
TOTAL_TOKEN_PATTERN = re.compile(
    r"total[\s_-]*tokens?(?:\s*[:=]\s*|\s+[^\d]*)(\d[\d,]*)",
    re.IGNORECASE,
)
GENERIC_TOKEN_PATTERN = re.compile(
    r"tokens?(?:_total|_used|_usage|[\s_-]*(?:使用量|合計|消費))?\s*[:=]?\s*(\d[\d,]*)",
    re.IGNORECASE,
)

# 定数
TOKEN_LIMIT = 1_000_000  # VS Code Copilot Chatの上限
WARNING_THRESHOLD = 0.60  # 60%で警告
CRITICAL_THRESHOLD = 0.80  # 80%で緊急アラート

# 推定値（現在の対話から算出）
# 2025-10-29時点: 約79,000トークン使用（要約前）
ESTIMATED_CURRENT_USAGE = 79_000


def _coerce_int(value: Any) -> Optional[int]:
    """Convert supported values to int, ignoring booleans and invalid data."""
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        digits = re.sub(r"[^\d]", "", value)
        if digits:
            return int(digits)
    return None


def _extract_tokens_from_mapping(data: Any) -> Optional[int]:
    totals = []
    partials = []
    stack: list[tuple[str, Any]] = [("", data)]

    while stack:
        path, node = stack.pop()
        if isinstance(node, dict):
            for key, value in node.items():
                key_str = str(key)
                next_path = f"{path}.{key_str}" if path else key_str
                stack.append((next_path, value))
        elif isinstance(node, list):
            for item in node:
                stack.append((path, item))
        else:
            numeric = _coerce_int(node)
            if numeric is None or not path:
                continue
            path_lower = path.lower()
            if "token" not in path_lower:
                continue
            if "total" in path_lower:
                totals.append(numeric)
            else:
                partials.append(numeric)

    if totals:
        return sum(totals)
    if partials:
        return sum(partials)
    return None


def _extract_frontmatter(text: str) -> Optional[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            return "\n".join(lines[1:idx])
    return None


def _extract_tokens_from_text(text: str) -> Optional[int]:
    values = [
        _coerce_int(match.group(1))
        for match in TOTAL_TOKEN_PATTERN.finditer(text)
    ]
    totals = [value for value in values if value is not None]
    if totals:
        return sum(totals)

    values = [
        _coerce_int(match.group(1))
        for match in GENERIC_TOKEN_PATTERN.finditer(text)
    ]
    generic = [value for value in values if value is not None]
    if generic:
        return sum(generic)

    return None


def _extract_tokens_from_frontmatter(text: str) -> Optional[int]:
    if not text:
        return None
    if yaml is not None:
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        if data is not None:
            usage = _extract_tokens_from_mapping(data)
            if usage is not None:
                return usage
    return _extract_tokens_from_text(text)


def _extract_usage_from_file(path: Path) -> int:
    try:
        contents = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        contents = path.read_text(encoding="utf-8", errors="ignore")

    frontmatter = _extract_frontmatter(contents)
    if frontmatter:
        usage = _extract_tokens_from_frontmatter(frontmatter)
        if usage is not None:
            return usage

    usage = _extract_tokens_from_text(contents)
    return usage or 0


def _iter_conversation_log_files() -> Iterable[Path]:
    seen = set()
    for candidate in CONVERSATION_DIR_CANDIDATES:
        if not candidate.exists():
            continue
        for path in candidate.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in LOG_FILE_EXTENSIONS:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            yield resolved


def estimate_token_usage():
    """
    現在のトークン使用量を推定
    
    Returns:
        int: 推定トークン使用量
    
    Note:
        会話ログから算出できない場合はフェイルセーフとして推定値にフォールバックする。
    """
    total_usage = 0
    observed_files = False

    for log_file in _iter_conversation_log_files():
        observed_files = True
        total_usage += _extract_usage_from_file(log_file)

    if observed_files and total_usage > 0:
        return total_usage

    return ESTIMATED_CURRENT_USAGE


def calculate_usage_percentage(current_usage: int) -> float:
    """使用率を計算"""
    return (current_usage / TOKEN_LIMIT) * 100


def estimate_remaining_conversations(current_usage: int) -> int:
    """
    残り対話可能回数を推定
    
    仮定: 1回の対話で平均3,000トークン使用
    """
    avg_tokens_per_conversation = 3_000
    remaining_tokens = TOKEN_LIMIT - current_usage
    return remaining_tokens // avg_tokens_per_conversation


def get_status_emoji(usage_percentage: float) -> str:
    """使用率に応じた絵文字を返す"""
    if usage_percentage >= CRITICAL_THRESHOLD * 100:
        return "🚨"  # 緊急
    elif usage_percentage >= WARNING_THRESHOLD * 100:
        return "⚠️"  # 警告
    else:
        return "✅"  # 安全


def print_usage_report(current_usage: int, detailed: bool = False):
    """使用状況レポートを出力"""
    usage_percentage = calculate_usage_percentage(current_usage)
    remaining_conversations = estimate_remaining_conversations(current_usage)
    status_emoji = get_status_emoji(usage_percentage)
    
    print("=" * 60)
    print("📊 トークン使用率レポート")
    print("=" * 60)
    print()
    print(f"{status_emoji} 現在の使用率: {usage_percentage:.1f}%")
    print(f"   使用量: {current_usage:,} / {TOKEN_LIMIT:,} tokens")
    print(f"   残量: {TOKEN_LIMIT - current_usage:,} tokens")
    print()
    print(f"📈 残り対話可能回数（推定）: 約{remaining_conversations}回")
    print()
    
    # ステータス判定
    if usage_percentage >= CRITICAL_THRESHOLD * 100:
        print("🚨 【緊急】 80%超過！")
        print("   推奨アクション:")
        print("   1. 重要な対話のみに絞る")
        print("   2. 現在のセッションを保存し、新規セッション開始を検討")
        print("   3. 対話ログを即座にバックアップ")
    elif usage_percentage >= WARNING_THRESHOLD * 100:
        print("⚠️  【警告】 60%超過")
        print("   推奨アクション:")
        print("   1. 重要な対話を優先する")
        print("   2. 近日中に新規セッション開始を検討")
        print("   3. 対話ログの定期バックアップを確認")
    else:
        print("✅ 安全範囲内（60%未満）")
        print("   現在のペースで使用を継続できます。")
    
    print()
    
    if detailed:
        print("=" * 60)
        print("📋 詳細情報")
        print("=" * 60)
        print(f"警告閾値: {WARNING_THRESHOLD * 100:.0f}% ({int(TOKEN_LIMIT * WARNING_THRESHOLD):,} tokens)")
        print(f"緊急閾値: {CRITICAL_THRESHOLD * 100:.0f}% ({int(TOKEN_LIMIT * CRITICAL_THRESHOLD):,} tokens)")
        print(f"推定平均トークン/対話: 3,000 tokens")
        print()
        print("⚠️  注意:")
        print("   - この推定は概算です")
        print("   - 実際の使用量は対話の複雑さにより変動します")
        print("   - Phase 2以降で精度向上予定")
        print()
    
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="VS Code Copilot Chat トークン使用率監視",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # 基本使用
    python scripts/check_token_usage.py
    
    # 詳細情報表示
    python scripts/check_token_usage.py --detailed
        """
    )
    
    parser.add_argument(
        '--detailed',
        action='store_true',
        help='詳細情報を表示'
    )
    
    args = parser.parse_args()
    
    # トークン使用量を推定
    current_usage = estimate_token_usage()
    
    # レポート出力
    print_usage_report(current_usage, detailed=args.detailed)
    
    # 終了コード
    usage_percentage = calculate_usage_percentage(current_usage)
    if usage_percentage >= CRITICAL_THRESHOLD * 100:
        return 2  # 緊急
    elif usage_percentage >= WARNING_THRESHOLD * 100:
        return 1  # 警告
    else:
        return 0  # 正常


if __name__ == '__main__':
    sys.exit(main())
