# Governance ディレクトリ

**ドキュメント管理ルール**

---

## 🎯 このディレクトリについて

このリポジトリ全体のドキュメント管理ルール、命名規則、階層構造を定義するディレクトリです。

**メタドキュメント**: ドキュメントについてのドキュメント

---

## 📁 ファイル一覧

### AI_GUIDELINES.md
- **用途**: AI向けドキュメント記録ガイドライン
- **対象**: GitHub Copilot, Claude Code, その他のAIアシスタント
- **内容**: 
  - ADRが必要な場合の判断基準
  - 作業前チェックリスト
  - 記録場所の一覧

### DOCUMENTATION_STRUCTURE.yml
- **用途**: ドキュメント階層の機械可読定義
- **対象**: スクリプト、自動化ツール
- **内容**:
  - Tier 0-4の階層定義
  - ファイルパスのリスト
  - バリデーションルール

### HIERARCHY_RULES.md
- **用途**: ドキュメント階層ルールの人間向け説明
- **対象**: 人間（開発者、コントリビュータ）
- **内容**:
  - Tier 0-4の説明
  - Single Source of Truthの定義
  - 更新順序のルール

### NAMING_DECISION_SUMMARY.md
- **用途**: 命名規則変更の経緯まとめ
- **対象**: 人間、AI
- **内容**:
  - Phase 1-3の変更履歴
  - 最終的な命名規則
  - 移行作業の記録

### PHASE1_SUMMARY.md
- **用途**: Phase 1（初期ADRシステム構築）のまとめ
- **対象**: 人間、AI
- **内容**:
  - 初期構築の経緯
  - 設計判断の理由

---

## 🔍 使い方

### AIがドキュメントを作成するとき

1. **[AI_GUIDELINES.md](AI_GUIDELINES.md)** を読む
2. クイックチェックリストで判断
3. 必要ならADR作成

### ドキュメント構造を理解するとき

1. **[HIERARCHY_RULES.md](HIERARCHY_RULES.md)** で階層を理解
2. **[DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml)** で具体的なパスを確認

### 命名規則を確認するとき

1. **[NAMING_DECISION_SUMMARY.md](NAMING_DECISION_SUMMARY.md)** で最終規則を確認
2. 不明な点は関連ADRを参照

---

## 📊 優先順位（Tier 0）

このディレクトリのファイルは **Tier 0（Single Source of Truth）** です。

### 優先順位ルール

1. **AI_GUIDELINES.md** - AIの行動指針
2. **HIERARCHY_RULES.md** - 階層構造の定義
3. **DOCUMENTATION_STRUCTURE.yml** - 機械可読定義
4. 関連ADR（`docs/decisions/active/`）

---

## 🔗 関連ドキュメント

- [`docs/decisions/README.md`](../decisions/README.md) - ADRの書き方
- [`docs/README.md`](../README.md) - 全体のガイド
- [`.github/copilot-instructions.md`](../../.github/copilot-instructions.md) - GitHub Copilot向け指示

---

## ⚠️ 重要な注意事項

### このディレクトリのファイルを変更する場合

1. **ADRを作成**: 変更理由を記録
2. **DOCUMENTATION_STRUCTURE.yml を更新**: 機械可読性を維持
3. **関連ファイルを更新**: `.github/copilot-instructions.md` など

### 矛盾を発見した場合

1. **ADRで解決**: 新しいADRで上書き
2. **Status更新**: 古いADRを `Superseded` に
3. **関連ファイル更新**: 一貫性を保つ

---

**最終更新**: 2025年10月28日
