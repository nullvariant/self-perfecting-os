---
category: tooling
date: 2025-10-28
number: 0004
status: Accepted
---

# ADR-0004: GitHub Actions によるドキュメント自動バリデーション導入

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: human (プロジェクトオーナー) + GitHub Copilot

## Context

### 背景
Phase 1-2 でドキュメント管理ガバナンスを確立したが、手動チェックに依存していた：
- ADR 番号の連番チェック
- `DOCUMENTATION_STRUCTURE.yml` に記載されたファイルの存在確認
- `project-status.ja.md` の更新日チェック

PR 時の手動チェック漏れを防ぎ、品質を担保するため、CI/CD による自動バリデーションが必要。

### 検討した選択肢
1. **Git Hooks（pre-commit）**: ローカル実行だが、スキップ可能でHSP特性に不適（ADR-0002で却下済み）
2. **GitHub Actions（PR時）**: リモート強制実行、スキップ不可 ← **採用**
3. **手動運用継続**: チェック漏れリスクあり

## Decision

**GitHub Actions で `validate_docs.py` を PR 時に自動実行する**

### 実装内容

#### ワークフロー定義
- **ファイル**: `.github/workflows/validate-docs.yml`
- **トリガー**: 
  - PR 作成・更新時（`docs/**`, `content/**` に変更がある場合）
  - `main` ブランチへのプッシュ時
- **実行内容**:
  1. `python scripts/validate_docs.py` を実行
  2. エラー時は PR をブロック
  3. 結果を GitHub Summary に表示

#### チェック項目
- ✅ ADR 番号の連番チェック（欠番検出）
- ✅ `DOCUMENTATION_STRUCTURE.yml` 記載ファイルの存在確認
- ✅ `project-status.ja.md` の最終更新日チェック（7日以上前で警告）
- ✅ 自動生成ファイルへの直接編集チェック

## Consequences

### ✅ メリット
- **品質担保**: PR 時の自動チェックで人為的ミスを防止
- **強制実行**: Git Hooks と異なりスキップ不可（確実性）
- **可視性**: GitHub Summary で結果を即座に確認可能
- **継続的改善**: バリデーションルールの追加が容易
- **HSP適合**: ローカル環境を汚さない（心理的負担軽減）

### ⚠️ デメリット
- **GitHub Actions 依存**: GitHub がダウンすると実行不可（影響は軽微）
- **実行時間**: PR ごとに数十秒の待機（許容範囲）
- **Python 依存**: PyYAML のインストールが必要（軽量）

### 📋 実装タスク
- [x] `.github/workflows/validate-docs.yml` 作成
- [x] ADR-0004 作成
- [ ] INDEX.md 更新
- [ ] 初回 PR でテスト実行
- [ ] README.md にバッジ追加（任意）

## Related

### 関連するファイル
- `.github/workflows/validate-docs.yml` - GitHub Actions ワークフロー定義
- `scripts/validate_docs.py` - バリデーションスクリプト本体
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - チェック対象の定義

### 関連する ADR
- ADR-0001: CI/CD 一時停止（翻訳パイプライン）
- ADR-0002: 命名規則とディレクトリ構造
- ADR-0003: 小文字・ハイフン統一

### 関連する PRD
- `docs/prd/active/20251028_documentation-governance.ja.md` - Phase 3 定義

### 関連する Issue/PR
- （初回テストPR番号を後で記録）

### 関連する Commit
- （Phase 3-B 実装コミットSHAを後で記録）

---

**Status**: Accepted  
**次のアクション**: INDEX.md 更新 → テストPR作成
