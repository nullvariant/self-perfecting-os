#!/usr/bin/env python3
"""
ドキュメント整合性検証スクリプト

このスクリプトは以下をチェックします:
1. ADR 番号の連番チェック（欠番がないか）
2. DOCUMENTATION_STRUCTURE.yml に記載された全ファイルの存在確認
3. project-status.ja.md の最終更新日チェック（7日以上前なら警告）
4. 自動生成ファイル（AGENT.md, spec/agent.spec.yaml）への直接編集チェック

Usage:
    python scripts/validate_docs.py
"""

from pathlib import Path
from datetime import datetime, timedelta
import yaml
import sys
import re

# ディレクトリ定義
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DECISIONS_DIR = ROOT / "docs" / "decisions"
STRUCTURE_FILE = ROOT / "docs" / "governance" / "DOCUMENTATION_STRUCTURE.yml"
PROJECT_STATUS = ROOT / "docs" / "project-status.ja.md"
AUTO_GEN_FILES = [
    ROOT / "AGENT.md",
    ROOT / "spec" / "agent.spec.yaml",
]

# エラーカウンター
errors = 0
warnings = 0


def check_adr_numbering():
    """ADR番号の連番チェック（新ディレクトリ構造対応）"""
    global errors
    print("\n📋 ADR番号の連番チェック...")

    # active/YYYY/MM/ 配下の全ADRを検索
    active_dir = DECISIONS_DIR / "active"
    
    if not active_dir.exists():
        print("  ℹ️  active/ ディレクトリが見つかりません")
        return

    # YYYYMMDD_NNNN_*.md パターンのファイルを検索
    adr_files = list(active_dir.rglob("*.md"))
    numbers = []

    for f in adr_files:
        # 新形式: YYYYMMDD_NNNN_slug_category.md
        match = re.match(r"\d{8}_(\d{4})_", f.name)
        if match:
            numbers.append(int(match.group(1)))

    if not numbers:
        print("  ℹ️  ADRファイルが見つかりません")
        return

    # 連番チェック
    numbers_sorted = sorted(numbers)
    expected = list(range(1, max(numbers_sorted) + 1))
    missing = set(expected) - set(numbers_sorted)

    if missing:
        print(f"  ❌ ADR番号に欠番があります: {sorted(missing)}")
        errors += 1
    else:
        print(f"  ✅ ADR番号は連番です（ADR-{min(numbers_sorted):04d} 〜 ADR-{max(numbers_sorted):04d}、計{len(numbers_sorted)}件）")


def check_file_existence():
    """DOCUMENTATION_STRUCTURE.yml に記載されたファイルの存在確認"""
    global errors, warnings
    print("\n📂 ファイル存在チェック...")

    if not STRUCTURE_FILE.exists():
        print(f"  ⚠️  DOCUMENTATION_STRUCTURE.yml が見つかりません")
        warnings += 1
        return

    try:
        with STRUCTURE_FILE.open("r", encoding="utf-8") as f:
            structure = yaml.safe_load(f)
    except Exception as e:
        print(f"  ❌ DOCUMENTATION_STRUCTURE.yml の読み込みに失敗: {e}")
        errors += 1
        return

    missing_files = []

    # 各Tierのファイルをチェック
    for tier_name, tier_data in structure.get("hierarchy", {}).items():
        for file_entry in tier_data.get("files", []):
            path_str = file_entry.get("path", "")

            # ディレクトリの場合はスキップ
            if path_str.endswith("/"):
                continue

            # パターンマッチの場合はスキップ（ADR-*.md など）
            if "*" in path_str:
                continue

            file_path = ROOT / path_str

            if not file_path.exists():
                missing_files.append((tier_name, path_str))

    if missing_files:
        print(f"  ❌ 以下のファイルが見つかりません:")
        for tier, path in missing_files:
            print(f"     - [{tier}] {path}")
        errors += len(missing_files)
    else:
        print(f"  ✅ 全ての記載ファイルが存在します")


def check_project_status_date():
    """project-status.ja.md の最終更新日チェック"""
    global warnings
    print("\n📊 project-status.ja.md の更新日チェック...")

    if not PROJECT_STATUS.exists():
        print(f"  ⚠️  project-status.ja.md が見つかりません")
        warnings += 1
        return

    try:
        content = PROJECT_STATUS.read_text(encoding="utf-8")

        # 最終更新日を抽出（フォーマット: **最終更新**: YYYY-MM-DD）
        match = re.search(r"\*\*最終更新\*\*:\s*(\d{4}-\d{2}-\d{2})", content)

        if not match:
            print(f"  ⚠️  最終更新日が記載されていません")
            warnings += 1
            return

        last_updated = datetime.strptime(match.group(1), "%Y-%m-%d")
        days_ago = (datetime.now() - last_updated).days

        if days_ago > 7:
            print(f"  ⚠️  最終更新から {days_ago} 日経過しています（最終更新: {match.group(1)}）")
            warnings += 1
        else:
            print(f"  ✅ 最終更新は {days_ago} 日前です（{match.group(1)}）")

    except Exception as e:
        print(f"  ❌ project-status.ja.md の読み込みに失敗: {e}")
        errors += 1


def check_auto_gen_files():
    """自動生成ファイルへの直接編集チェック（簡易版）"""
    global warnings
    print("\n🤖 自動生成ファイルチェック...")

    for file_path in AUTO_GEN_FILES:
        if not file_path.exists():
            continue

        try:
            content = file_path.read_text(encoding="utf-8")

            # 警告コメントが含まれているかチェック
            if "⚠️" not in content and "WARNING" not in content and "古い" not in content:
                print(
                    f"  ⚠️  {file_path.relative_to(ROOT)} に古い・手動更新不要の警告がありません"
                )
                warnings += 1

        except Exception as e:
            print(f"  ❌ {file_path.relative_to(ROOT)} の読み込みに失敗: {e}")
            errors += 1


def main():
    print("=" * 60)
    print("📝 ドキュメント整合性検証")
    print("=" * 60)

    check_adr_numbering()
    check_file_existence()
    check_project_status_date()
    check_auto_gen_files()

    print("\n" + "=" * 60)
    print(f"📊 検証結果: {errors} エラー, {warnings} 警告")
    print("=" * 60)

    if errors > 0:
        print("\n❌ エラーが検出されました。修正してください。")
        sys.exit(1)
    elif warnings > 0:
        print("\n⚠️  警告があります。確認してください。")
        sys.exit(0)
    else:
        print("\n✅ 全てのチェックに合格しました！")
        sys.exit(0)


if __name__ == "__main__":
    main()
