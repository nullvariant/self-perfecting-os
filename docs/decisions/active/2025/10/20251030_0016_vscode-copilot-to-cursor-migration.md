---
category: tooling
date: 2025-10-30
number: 0016
status: Accepted
---

# ADR-0016: VSCode/Copilot から Cursor への開発環境移行

## Status
- **提案日**: 2025-10-30
- **状態**: Accepted
- **決定者**: human + Claude Code

## Context

### 背景

プロジェクトオーナーが開発環境を VSCode + GitHub Copilot から Cursor に完全移行することを決定。

- **現在の状況**: VSCode + GitHub Copilot で開発してきた
- **問題点**: Copilot のセッション管理が煩雑（30-50メッセージで新セッション推奨）
- **解決すべき課題**: Cursor に最適化された設定ファイルの構築

### 検討した選択肢

1. **選択肢A**: 全内容移行（429行すべて）
   - メリット: 情報の欠損なし
   - デメリット: Cursor不要な情報も含まれる、冗長

2. **選択肢B**: Cursor最適化版（約280行）← **採用**
   - メリット: Cursor特有の機能に合わせた構成、不要セクション削除
   - デメリット: 移行作業に判断が必要

3. **選択肢C**: 段階的移行（まず150行のコア版）
   - メリット: すぐに使い始められる
   - デメリット: 初期は情報不足の可能性

4. **選択肢D**: 複数ファイル分割
   - メリット: 状況別にルール適用可能
   - デメリット: ファイル管理が複雑

## Decision

**選択肢B（Cursor最適化版）を採用し、2ファイル構成で実装する。**

### ファイル構成

```
.cursor/rules/
├── project.mdc          (alwaysApply: true)  - プロジェクトの本質（約250行）
└── coding-style.mdc     (alwaysApply: false) - 実装詳細（約70行）
```

### 削除した内容

- **Copilot Chatセッション管理**（7章、62行）→ 完全削除
  - Cursor は大規模コンテキスト窓（100万トークン）でセッション管理の重要度が低い
- **プロジェクト構造図**（40行）→ 権威文書への参照に簡潔化（5行）
- **スクリプト使用方法**（17行）→ 簡潔化（3行）
- **開発セットアップ詳細**（20行）→ 簡潔化（5行）

### 追加した内容

- **Cursor特有の機能説明**（Composer, Agent, @mention）
- **大規模コンテキスト窓**の説明

### 分離基準

- **project.mdc**: 常時必要、不変・高抽象度（プロジェクト理解の本質）
- **coding-style.mdc**: コード編集時のみ、変わりやすい・低抽象度（実装詳細）

### 権威文書への参照

情報の分散を避けるため、以下の権威文書への参照を活用：

- `docs/governance/HIERARCHY_RULES.md` - 人間向け階層ルール
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 機械可読形式
- `docs/governance/AI_GUIDELINES.md` - AI向けガイドライン
- `docs/governance/SSOT_PRIORITY_MATRIX.md` - 情報源の優先順位

## Consequences

### ✅ メリット

- Cursor の特性に最適化された設定（大規模コンテキスト、Composer機能）
- 不要な情報（Copilotセッション管理）を削除し、読み込み速度向上
- 権威文書への参照で情報の分散を回避
- 2ファイル構成で管理負担が低い
- 将来的に必要なら分割可能（拡張性）

### ⚠️ デメリット

- Copilot に戻る場合は `.github/copilot-instructions.md` を再利用する必要がある
  - ただし、ファイルは残存するため問題なし
- 2つのファイルの整合性維持が必要
  - ただし、分離基準が明確なため管理は容易

### 📋 TODO

- [x] `.cursor/rules/project.mdc` を作成
- [x] `.cursor/rules/coding-style.mdc` を作成
- [x] ADR-0016 を記録
- [ ] CHANGELOG.md に記録
- [ ] `.github/copilot-instructions.md` は残存（将来的な互換性のため）

## Related

### 関連するファイル

- `.cursor/rules/project.mdc` - 新規作成
- `.cursor/rules/coding-style.mdc` - 新規作成
- `.github/copilot-instructions.md` - 残存（参照用）

### 関連する ADR

- ADR-0013: AI entry point reference only（AI向けエントリーポイント）
- ADR-0011: filename case convention（ファイル名ケース規則）
- ADR-0012: hyphen underscore convention（ハイフン規則）

### 移行の背景

プロジェクトオーナーは以下の理由で Cursor に完全移行：

1. **Copilot有料版を解約済み**
2. **ツールの進化に対応するため、いつでも戻れる構成を維持**
3. **長期的な美しさと保守性を重視**

### 設計哲学

- **権威文書への参照**: 情報の分散を避ける
- **長期的な美しさ**: 更新頻度・粒度・抽象度による分離
- **拡張性**: 将来的に分割可能な設計

---

**この ADR は Cursor 移行の記録として、ツール選択の柔軟性と設定の最適化を両立する方針を示しています。**

