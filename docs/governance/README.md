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

### Phase 1 実装完了レポート（アーカイブ）
- **ファイル**: `docs/operations/archive/2025/10/20251028_governance-phase1-completion-report.ja.md`
- **用途**: Phase 1（初期ADRシステム構築）の進捗レポート
- **対象**: 参考資料（一時的ドキュメント）
- **内容**:
  - 初期構築の経緯
  - 設計判断の理由
  - Phase 2 への引き継ぎ情報

---

**注記**: メタドキュメント（このディレクトリ内）は大文字で命名。一時的な進捗レポートは日付付き・archive/ 配下に配置する原則に従っています。

---

## 🎓 新規訪問者ガイド（推奨読む順序）

このディレクトリに初めて来た人・AIは、以下の順序で読んでください：

### � **あなたのユースケースを選択**

#### Case A: 「このプロジェクトのドキュメント体系を理解したい」

```
1️⃣  【5分】 このファイル（README.md）を読む ← 今ここ
2️⃣  【10分】 HIERARCHY_RULES.md で階層を理解
3️⃣  【5分】 DOCUMENTATION_STRUCTURE.yml で具体的パスを確認
4️⃣  【参考】 関連ADR（ADR-0002/0005など）で背景を理解
```

**まとめ**: 全体の構造 → 階層の説明 → パスの詳細 → 意思決定の根拠

---

#### Case B: 「新しいドキュメント・ADRを作成したい」

```
1️⃣  【3分】 AI_GUIDELINES.md の「クイックチェック」セクション
2️⃣  【1分】 作業前チェックリスト（5項目）を確認
3️⃣  【2分】 判定フロー「この変更は ADR が必要か？」で判断
   └─ Yes → scripts/record_decision.py を実行
   └─ No → 直接ファイル編集（コミットメッセージに理由記載）
```

**まとめ**: 判定フロー → 実行 → 記録

---

#### Case C: 「複数ドキュメント間の矛盾を見つけた」

```
1️⃣  【3分】 SSOT_PRIORITY_MATRIX.md で優先順位確認
2️⃣  【2分】 「ケース別対応例」で該当パターンを探す
3️⃣  【1分】 「矛盾・曖昧さの報告フロー」を実施
```

**まとめ**: 優先順位 → パターンマッチ → 修正 → 検証

---

#### Case D: 「命名規則・ファイルパス形式を確認したい」

```
1️⃣  【2分】 NAMING_DECISION_SUMMARY.md で最終規則を確認
2️⃣  【3分】 DOCUMENTATION_STRUCTURE.yml で具体例を探す
3️⃣  【参考】 ADR-0011/0012 で背景を理解
```

**まとめ**: 規則 → 例 → 背景

---

### 🗺️ クイック意思決定フロー

以下のフローに従って、適切なドキュメントにジャンプ：

```
┌─────────────────────────────┐
│  あなたのやりたいことは？     │
└────────────┬────────────────┘
             │
    ┌────────┼────────────┬─────────────┬─────────────┐
    │        │            │             │             │
    ↓        ↓            ↓             ↓             ↓
   
ドキュメント 新規作成 矛盾を 命名規則 ADRの
構造を理解  またはADR 発見  を確認  書き方を知る

   │        │            │             │             │
   ↓        ↓            ↓             ↓             ↓
   
HIERARCHY  AI_GUIDELINES SSOT_PRIORITY NAMING_     decisions/
RULES.md   .md          MATRIX.md      SUMMARY.md   README.md

   └────────┴────────────┴─────────────┴─────────────┘
             │
             ↓
    各ドキュメント内の
    セクション/リンクで
    詳細を参照
```

---

## �🔍 使い方（詳細版）

### AIがドキュメントを作成するとき

1. **[AI_GUIDELINES.md](AI_GUIDELINES.md)** を読む
   - 対象セクション: 「クイックリファレンス」と「作業前チェックリスト」
2. クイックチェックリストで判断
3. 必要ならADR作成

### ドキュメント構造を理解するとき

1. **[HIERARCHY_RULES.md](HIERARCHY_RULES.md)** で階層を理解
   - Tier 0-4 の役割と特性を把握
2. **[DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml)** で具体的なパスを確認
   - 実際のファイル配置・正規表現パターン

### 命名規則を確認するとき

1. **[NAMING_DECISION_SUMMARY.md](NAMING_DECISION_SUMMARY.md)** で最終規則を確認
2. 不明な点は関連ADR を参照
   - [ADR-0011](../decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md) - ケース規則
   - [ADR-0012](../decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) - ハイフン・アンダースコア

### 矛盾を解決したいとき

1. **[SSOT_PRIORITY_MATRIX.md](./SSOT_PRIORITY_MATRIX.md)** で優先順位を確認
   - 5段階の権威性レベル
   - 優先順位の決定フロー
2. ケース別対応例で該当パターンを探す
3. 必要なら修正 → ADR作成

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
