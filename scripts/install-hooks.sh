#!/usr/bin/env bash
#
# Git Hooks インストールスクリプト
#
# このスクリプトは、scripts/hooks/ 配下のフックファイルを
# .git/hooks/ にコピーして実行権限を付与します。
#
# Usage:
#   bash scripts/install-hooks.sh
#

set -e

# カラー出力定義
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Git Hooks をインストールしています...${NC}"
echo ""

# リポジトリルートの確認
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ エラー: このスクリプトはリポジトリのルートディレクトリから実行してください${NC}" >&2
    exit 1
fi

# scripts/hooks/ ディレクトリの確認
if [ ! -d "scripts/hooks" ]; then
    echo -e "${RED}❌ エラー: scripts/hooks/ ディレクトリが見つかりません${NC}" >&2
    exit 1
fi

# .git/hooks/ ディレクトリの確認（通常は存在するはず）
if [ ! -d ".git/hooks" ]; then
    echo -e "${YELLOW}⚠️  .git/hooks/ ディレクトリが存在しないため作成します${NC}"
    mkdir -p .git/hooks
fi

# インストールカウンター
INSTALLED_COUNT=0

# scripts/hooks/ 配下の全ファイルをコピー
for hook_file in scripts/hooks/*; do
    if [ -f "$hook_file" ]; then
        hook_name=$(basename "$hook_file")
        target_path=".git/hooks/$hook_name"
        
        # 既存のフックがある場合はバックアップ
        if [ -f "$target_path" ]; then
            backup_path="${target_path}.backup.$(date +%Y%m%d_%H%M%S)"
            echo -e "${YELLOW}⚠️  既存の $hook_name をバックアップします: $backup_path${NC}"
            mv "$target_path" "$backup_path"
        fi
        
        # フックをコピー
        cp "$hook_file" "$target_path"
        
        # 実行権限を付与
        chmod 755 "$target_path"
        
        echo -e "${GREEN}✅ $hook_name をインストールしました${NC}"
        INSTALLED_COUNT=$((INSTALLED_COUNT + 1))
    fi
done

echo ""
echo -e "${GREEN}🎉 Git Hooks のインストールが完了しました（${INSTALLED_COUNT} 個）${NC}"
echo ""
echo -e "${BLUE}📋 インストールされたフック:${NC}"
ls -lh .git/hooks/ | grep -v "\.sample$" | grep -v "^total" || echo "  （なし）"
echo ""
echo -e "${YELLOW}💡 ヒント:${NC}"
echo -e "  - フックをスキップしたい場合: ${BLUE}git commit --no-verify${NC}"
echo -e "  - フックを一時的に無効化: ${BLUE}chmod -x .git/hooks/pre-commit${NC}"
echo -e "  - フックを再度有効化: ${BLUE}chmod +x .git/hooks/pre-commit${NC}"
echo ""

exit 0

