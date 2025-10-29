#!/usr/bin/env python3
"""
トークン使用率監視スクリプト (v1 - Simple MVP)

VS Code Copilot Chatのトークン使用状況を推定し、警告を出力する。

Version: 1.0.0 (MVP - Manual Update)
Phase: 2

Usage:
    python scripts/check_token_usage.py
    python scripts/check_token_usage.py --detailed

TODO Phase 3:
    - 対話ログファイル自動スキャン機能
    - YAML frontmatter解析
    - リアルタイム集計
"""

import argparse
import sys
from pathlib import Path

# 定数定義
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# トークン制限（VS Code Copilot Chat）
MAX_TOKENS = 1_000_000  # 1M tokens/month

# 推定使用量（手動更新）
# TODO Phase 2: この値を定期的に手動更新する
# TODO Phase 3: 対話ログファイルをスキャンして自動算出
ESTIMATED_CURRENT_USAGE = 79_000  # 2025-10-29時点の推定値

# 警告閾値
WARNING_THRESHOLD = 0.70  # 70%
CRITICAL_THRESHOLD = 0.90  # 90%


def estimate_token_usage() -> int:
    """
    現在のトークン使用量を推定（MVP版：固定値）
    
    Returns:
        int: 推定トークン使用量
    
    Note:
        Phase 2: 手動更新の固定値を返す
        Phase 3: ログファイルをスキャンして自動集計予定
    """
    return ESTIMATED_CURRENT_USAGE


def calculate_usage_percentage(current_usage: int, max_tokens: int = MAX_TOKENS) -> float:
    """
    使用率を計算
    
    Args:
        current_usage: 現在の使用量
        max_tokens: 最大トークン数
    
    Returns:
        float: 使用率（0.0 - 1.0）
    """
    return current_usage / max_tokens


def estimate_remaining_conversations(
    current_usage: int,
    max_tokens: int = MAX_TOKENS,
    avg_tokens_per_conversation: int = 3000
) -> int:
    """
    残り可能会話数を推定
    
    Args:
        current_usage: 現在の使用量
        max_tokens: 最大トークン数
        avg_tokens_per_conversation: 1会話あたりの平均トークン数
    
    Returns:
        int: 推定残り会話数
    """
    remaining_tokens = max_tokens - current_usage
    return remaining_tokens // avg_tokens_per_conversation


def get_warning_level(usage_percentage: float) -> str:
    """
    使用率から警告レベルを判定
    
    Args:
        usage_percentage: 使用率（0.0 - 1.0）
    
    Returns:
        str: 警告レベル（'safe' | 'warning' | 'critical'）
    """
    if usage_percentage >= CRITICAL_THRESHOLD:
        return "critical"
    elif usage_percentage >= WARNING_THRESHOLD:
        return "warning"
    else:
        return "safe"


def format_number(num: int) -> str:
    """
    数値を読みやすくフォーマット（カンマ区切り）
    
    Args:
        num: フォーマットする数値
    
    Returns:
        str: フォーマット済み文字列
    """
    return f"{num:,}"


def print_usage_report(detailed: bool = False) -> None:
    """
    トークン使用状況レポートを出力
    
    Args:
        detailed: 詳細モードの有効化
    """
    current_usage = estimate_token_usage()
    usage_percentage = calculate_usage_percentage(current_usage)
    remaining_conversations = estimate_remaining_conversations(current_usage)
    warning_level = get_warning_level(usage_percentage)
    
    # 警告レベルに応じた色設定（ANSI エスケープコード）
    colors = {
        "safe": "\033[32m",      # 緑
        "warning": "\033[33m",   # 黄
        "critical": "\033[31m",  # 赤
        "reset": "\033[0m"
    }
    
    color = colors[warning_level]
    reset = colors["reset"]
    
    # ヘッダー
    print("=" * 60)
    print("📊 VS Code Copilot Chat - Token Usage Report")
    print("=" * 60)
    print()
    
    # 基本情報
    print(f"💾 Current Usage:  {color}{format_number(current_usage)}{reset} / {format_number(MAX_TOKENS)} tokens")
    print(f"📈 Usage Rate:     {color}{usage_percentage * 100:.1f}%{reset}")
    print(f"💬 Remaining Conv: {color}{format_number(remaining_conversations)}{reset} conversations (est.)")
    print()
    
    # 警告メッセージ
    if warning_level == "critical":
        print(f"{color}⚠️  CRITICAL: Token usage > 90%!{reset}")
        print(f"{color}   Please archive old conversations or wait for monthly reset.{reset}")
    elif warning_level == "warning":
        print(f"{color}⚠️  WARNING: Token usage > 70%{reset}")
        print(f"{color}   Consider archiving conversations soon.{reset}")
    else:
        print(f"{color}✅ SAFE: Token usage is healthy.{reset}")
    
    print()
    
    # 詳細モード
    if detailed:
        print("-" * 60)
        print("📋 Detailed Information")
        print("-" * 60)
        print(f"Version:          v1.0.0 (MVP - Manual Update)")
        print(f"Phase:            2")
        print(f"Update Method:    Manual (ESTIMATED_CURRENT_USAGE)")
        print(f"Warning Threshold: {WARNING_THRESHOLD * 100}%")
        print(f"Critical Threshold: {CRITICAL_THRESHOLD * 100}%")
        print(f"Avg Tokens/Conv:  3,000 tokens (estimated)")
        print()
        print("📌 Note:")
        print("  - Phase 2: Manual update required for ESTIMATED_CURRENT_USAGE")
        print("  - Phase 3: Auto-scanning from conversation logs (planned)")
        print()
    
    print("=" * 60)


def main() -> int:
    """
    メイン関数
    
    Returns:
        int: 終了コード（0: 正常, 1: 警告, 2: クリティカル）
    """
    parser = argparse.ArgumentParser(
        description="VS Code Copilot Chat token usage monitor"
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed information"
    )
    
    args = parser.parse_args()
    
    # レポート出力
    print_usage_report(detailed=args.detailed)
    
    # 警告レベルに応じた終了コード
    current_usage = estimate_token_usage()
    usage_percentage = calculate_usage_percentage(current_usage)
    warning_level = get_warning_level(usage_percentage)
    
    if warning_level == "critical":
        return 2
    elif warning_level == "warning":
        return 1
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
