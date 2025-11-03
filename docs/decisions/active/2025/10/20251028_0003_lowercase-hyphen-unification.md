---
category: documentation
date: 2025-10-28
number: 0003
status: Accepted
---

# ADR-0003: ディレクトリ・ファイル名の小文字・ハイフン統一

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: human (プロジェクトオーナー)

## Context

### 背景
Phase 2 実行後、ディレクトリ・ファイル名の大文字・小文字が混在していることが判明：

**現状の混在例:**
- ディレクトリ: `DECISIONS/`, `GOVERNANCE/`, `PRD/` (全て大文字)
- サブディレクトリ: `operations/`, `active/`, `current/` (全て小文字)
- ファイル: `project-status.ja.md`, `agent.en.md` (大文字 + アンダースコア)

統一ルールが不明瞭で、視覚的に不自然。プロジェクトオーナーより「小文字のほうが自然に見える」とのフィードバック。

### 検討した選択肢
1. **全て大文字**: 視認性高いが「叫んでいる」印象、タイプしにくい
2. **全て小文字 + ハイフン**: UNIX慣習、視覚的自然、タイプ容易 ← **採用**
3. **全て小文字 + アンダースコア**: プログラミング言語慣習だが、ドキュメントには不適

## Decision

**ディレクトリ・ファイル名を小文字・ハイフン区切りに統一する**

### ルール

#### ディレクトリ名
- **常に小文字 + ハイフン区切り**
- 例: `decisions/`, `governance/`, `prd/`, `operations/`

#### ファイル名
- **ドキュメントファイル**: 小文字 + ハイフン区切り
  - 例: `project-status.ja.md`, `agent.en.md`
- **GitHub慣習ファイル**: 大文字維持（例外）
  - 維持: `README.md`, `CHANGELOG.md`, `LICENSE`, `CONTRIBUTING.md`, `Makefile`
- **日付付きファイル**: 小文字・ハイフン（既存ルール維持）
  - 例: `20251028_0001_ci-cd-pause_architecture.md`

## Consequences

### ✅ メリット
- **視覚的自然さ**: 大文字の「叫び」感がなくなる
- **タイプ容易性**: Shiftキー不要、入力速度向上
- **UNIX慣習準拠**: 標準的なディレクトリ構造に合致
- **一貫性**: 全ファイル・ディレクトリが統一ルールに従う
- **モダンな印象**: 現代のプロジェクト標準に準拠

### ⚠️ デメリット
- **既存参照の更新**: 全スクリプト・ドキュメントのパス修正が必要
- **Gitリネーム履歴**: `git mv` による履歴追跡（影響は軽微）
- **一時的な混乱**: 移行期間中のパスエラーの可能性

### 📋 移行タスク（Phase 2b）
- [x] ADR-0003 作成
- [x] ディレクトリリネーム: `DECISIONS/` → `decisions/`, `GOVERNANCE/` → `governance/`, `PRD/` → `prd/`
- [x] ファイルリネーム: `project-status.ja.md` → `project-status.ja.md`, `agent.en.md` → `agent.en.md`
- [x] スクリプト更新: `scripts/*.py` の全パス参照を修正
- [x] ドキュメント更新: `DOCUMENTATION_STRUCTURE.yml`, `AI_GUIDELINES.md`, `.github/copilot-instructions.md`
- [x] バリデーション実行: `python scripts/validate_docs.py` → 0 エラー、0 警告
- [x] INDEX.md 再生成: `python scripts/generate_index.py` → 成功

## Related

### 関連するファイル
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - パス定義の更新必須
- `docs/governance/AI_GUIDELINES.md` - パス例の更新必須
- `.github/copilot-instructions.md` - パス例の更新必須
- `scripts/*.py` - 全スクリプトのパス参照を更新

### 関連する ADR
- ADR-0002: 命名規則とディレクトリ構造（日付・カテゴリルール）

### 関連する Issue/PR
- なし（内部改善）

### 関連する Commit
- （Phase 2b 実行後に記録）

---

**Status**: Accepted  
**次のアクション**: Phase 2b 実行（即座に移行）
