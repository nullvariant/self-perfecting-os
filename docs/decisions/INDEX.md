# Architecture Decision Records (ADR) Index

**最終更新**: 2025-11-03
**総件数**: 18件（Active: 18, Deprecated: 0, Superseded: 0）

---

## 📊 カテゴリ別

### 🏗️ アーキテクチャ変更
- [ADR-0001](active/2025/10/20251028_0001_ci-cd-pause_architecture.md) - Claude API レート制限対応によるCI/CD一時停止 (2025-10-28)
- [ADR-0007](active/2025/10/20251028_0007_changelogs-migration-nullvariant-writings_architecture.md) - changelogsディレクトリのnullvariant-atelierへの移行 (2025-10-28)

### 📚 ドキュメント構造変更
- [ADR-0002](active/2025/10/20251028_0002_naming-structure_documentation.md) - ドキュメント命名規則とディレクトリ構造の確立 (2025-10-28)
- [ADR-0003](active/2025/10/20251028_0003_lowercase-hyphen-unification_documentation.md) - ディレクトリ・ファイル名の小文字・ハイフン統一 (2025-10-28)
- [ADR-0005](active/2025/10/20251028_0005_multilingual-directory-structure_documentation.md) - 多言語対応: 言語別ディレクトリ構造への移行 (2025-10-28)
- [ADR-0006](active/2025/10/20251028_0006_github-pages-landing-implementation_documentation.md) - GitHub Pagesランディングページの実装 (2025-10-28)
- [ADR-0010](active/2025/10/20251029_0010_governance-audit_documentation.md) - ガバナンス系ドキュメント セルフレビューレポート (2025-10-29)
- [ADR-0011](active/2025/10/20251029_0011_filename-case-convention_documentation.md) - ファイル名ケース規則の明確化（大文字 vs 小文字） (2025-10-29)
- [ADR-0012](active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) - ハイフン vs アンダースコア使い分けルール (2025-10-29)
- [ADR-0013](active/2025/10/20251029_0013_ai-entry-point-reference-only_documentation.md) - AI Entry Point Documentation as Reference-Only (2025-10-29)
- [ADR-0014](active/2025/10/20251030_0014_tree-structure-reference-only_documentation.md) - Tree Structure Reference-Only Design (2025-10-30)

### 🏛️ ガバナンス・ポリシー
- [ADR-0008](active/2025/10/20251029_0008_dialogue-log-persistence-system_governance.md) - 対話生ログの永続保存システム確立 (2025-10-29)
- [ADR-0017](active/2025/10/20251030_0017_prd-status-management-enhancement_governance.md) - PRDステータス管理の拡張（deprecated対応） (2025-10-30)

### 📌 other
- [ADR-0018](active/2025/11/20251103_0018_adr-category-in-frontmatter.md) - カテゴリをファイル名から削除し、Frontmatterに移行 (2025-11-03)

### 📋 プロセス・手順変更
- [ADR-0009](active/2025/10/20251029_0009_test-fixtures-management_process.md) - テストファイル管理規則：tests/fixtures/配下に集約 (2025-10-29)

### 🔧 ツール・インフラ変更
- [ADR-0004](active/2025/10/20251028_0004_github-actions-doc-validation_tooling.md) - GitHub Actions によるドキュメント自動バリデーション導入 (2025-10-28)
- [ADR-0015](active/2025/10/20251030_0015_git-hooks-index-generation_tooling.md) - Git Hooks による INDEX.md 自動生成の実装 (2025-10-30)
- [ADR-0016](active/2025/10/20251030_0016_vscode-copilot-to-cursor-migration_tooling.md) - VSCode/Copilot から Cursor への開発環境移行 (2025-10-30)

---

## 📅 時系列

### 2025年11月
- 2025-11-03: [ADR-0018](active/2025/11/20251103_0018_adr-category-in-frontmatter.md) - カテゴリをファイル名から削除し、Frontmatterに移行

### 2025年10月
- 2025-10-30: [ADR-0014](active/2025/10/20251030_0014_tree-structure-reference-only_documentation.md) - Tree Structure Reference-Only Design
- 2025-10-30: [ADR-0015](active/2025/10/20251030_0015_git-hooks-index-generation_tooling.md) - Git Hooks による INDEX.md 自動生成の実装
- 2025-10-30: [ADR-0016](active/2025/10/20251030_0016_vscode-copilot-to-cursor-migration_tooling.md) - VSCode/Copilot から Cursor への開発環境移行
- 2025-10-30: [ADR-0017](active/2025/10/20251030_0017_prd-status-management-enhancement_governance.md) - PRDステータス管理の拡張（deprecated対応）
- 2025-10-29: [ADR-0008](active/2025/10/20251029_0008_dialogue-log-persistence-system_governance.md) - 対話生ログの永続保存システム確立
- 2025-10-29: [ADR-0009](active/2025/10/20251029_0009_test-fixtures-management_process.md) - テストファイル管理規則：tests/fixtures/配下に集約
- 2025-10-29: [ADR-0010](active/2025/10/20251029_0010_governance-audit_documentation.md) - ガバナンス系ドキュメント セルフレビューレポート
- 2025-10-29: [ADR-0011](active/2025/10/20251029_0011_filename-case-convention_documentation.md) - ファイル名ケース規則の明確化（大文字 vs 小文字）
- 2025-10-29: [ADR-0012](active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) - ハイフン vs アンダースコア使い分けルール
- 2025-10-29: [ADR-0013](active/2025/10/20251029_0013_ai-entry-point-reference-only_documentation.md) - AI Entry Point Documentation as Reference-Only
- 2025-10-28: [ADR-0001](active/2025/10/20251028_0001_ci-cd-pause_architecture.md) - Claude API レート制限対応によるCI/CD一時停止
- 2025-10-28: [ADR-0002](active/2025/10/20251028_0002_naming-structure_documentation.md) - ドキュメント命名規則とディレクトリ構造の確立
- 2025-10-28: [ADR-0003](active/2025/10/20251028_0003_lowercase-hyphen-unification_documentation.md) - ディレクトリ・ファイル名の小文字・ハイフン統一
- 2025-10-28: [ADR-0004](active/2025/10/20251028_0004_github-actions-doc-validation_tooling.md) - GitHub Actions によるドキュメント自動バリデーション導入
- 2025-10-28: [ADR-0005](active/2025/10/20251028_0005_multilingual-directory-structure_documentation.md) - 多言語対応: 言語別ディレクトリ構造への移行
- 2025-10-28: [ADR-0006](active/2025/10/20251028_0006_github-pages-landing-implementation_documentation.md) - GitHub Pagesランディングページの実装
- 2025-10-28: [ADR-0007](active/2025/10/20251028_0007_changelogs-migration-nullvariant-writings_architecture.md) - changelogsディレクトリのnullvariant-atelierへの移行

---

## 🔍 ステータス別

### Active (現行有効)
- ADR-0001, ADR-0002, ADR-0003, ADR-0004, ADR-0005, ADR-0006, ADR-0007, ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0013, ADR-0014, ADR-0015, ADR-0016, ADR-0017, ADR-0018

### Deprecated (非推奨)
- なし

### Superseded (上書き済み)
- なし
