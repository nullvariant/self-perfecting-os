# Docs ディレクトリ

**Public Repository: 構造化ドキュメント管理**

---

## 🎯 設計思想

**カテゴリ分類 + ADRシステム**

このリポジトリは **公開仕様書**であり、外部からの参照を想定しています。そのため、カテゴリ別に整理された構造化ドキュメント管理を採用しています。

### 設計原則

1. **明確なカテゴリ分類**: ドキュメントの用途が一目でわかる
2. **ADR（Architecture Decision Records）**: 重要な決定を記録
3. **階層構造**: ガバナンス > 運用 > PRD の優先順位
4. **月別アーカイブ**: 完了した決定は月別に整理

---

## 📁 構造

```
docs/
├── decisions/              # ADR（全ての重要な決定）
│   ├── active/2025/10/    # 現在有効な決定（月別）
│   ├── deprecated/        # 非推奨
│   ├── superseded/        # 上書きされた決定
│   └── INDEX.md           # 自動生成索引
├── governance/            # ドキュメント管理ルール
│   ├── AI_GUIDELINES.md
│   ├── DOCUMENTATION_STRUCTURE.yml
│   └── HIERARCHY_RULES.md
├── prd/                   # Product Requirements Document
│   └── active/
├── operations/            # 運用手順書
│   └── current/
└── README.md              # このファイル
```

---

## 📝 命名規則

### ADR（Architecture Decision Records）

```
{YYYYMMDD}_{NNNN}_{slug}_{category}.md
```

**例**:
```
20251028_0005_script-cleanup-makefile_tooling.md
```

### PRD（要件定義書）

```
{YYYYMMDD}_{slug}.ja.md
```

**例**:
```
20251028_note-workflow-automation.ja.md
20251028_documentation-governance.ja.md
```

### 運用手順書（Operations）

```
{YYYYMMDD}_{TYPE}.ja.md
```

**注**: `{TYPE}`は`UPPER_SNAKE_CASE`形式（例: `OPERATIONS`, `NOTE_SYNC_MANUAL`, `WORKFLOW_TEXT_ASSETS`）

**例**:
```
20251028_OPERATIONS.ja.md
20251028_NOTE_SYNC_MANUAL.ja.md
20251029_GOVERNANCE_REMEDIATION_SUMMARY.ja.md
```

---

## 🔍 検索方法

### カテゴリで探す

```bash
# 決定記録
ls docs/decisions/active/2025/10/

# ガバナンスルール
ls docs/governance/

# PRD
ls docs/prd/active/
```

### 自動生成索引で探す

- [`docs/decisions/INDEX.md`](decisions/INDEX.md) - 全ADRの索引

---

## 🏷️ カテゴリ一覧

### decisions/ - ADR
- **用途**: 重要な技術的決定の記録
- **対象**: API変更、アーキテクチャ変更、CI/CD変更など
- **形式**: ADRテンプレート準拠
- **更新**: 決定時に記録、完了後はアーカイブ

### governance/ - ガバナンス
- **用途**: ドキュメント管理ルール自体の定義
- **対象**: 命名規則、階層ルール、AI向けガイドライン
- **形式**: Markdown（機械可読YAML含む）
- **更新**: ルール変更時のみ

### prd/ - 要件定義
- **用途**: 機能開発の要件定義
- **対象**: 新機能、改善提案
- **形式**: PRDテンプレート
- **更新**: 開発開始時に作成、完了後はアーカイブ

### operations/ - 運用手順書
- **用途**: 日常的な運用手順
- **対象**: リリース手順、トラブルシューティング
- **形式**: 手順書形式
- **更新**: プロセス変更時

---

## 🆚 nullvariant-writings との違い

| 項目 | nullvariant (Public) | nullvariant-writings (Private) |
|------|---------------------|--------------------------------|
| **目的** | 公開仕様書 | 執筆・開発作業ログ |
| **構造** | カテゴリ分類 | 完全時系列（月別のみ） |
| **命名** | カテゴリ付き | 日付 + 概要のみ |
| **分類方法** | ディレクトリ | タグ（Front Matter） |
| **対象読者** | 外部（AI含む） | 自分 + AI |
| **ADR** | ✅ 必須 | ❌ 不要 |

### 使い分けの理由

**nullvariant**: 
- 公開仕様書として外部参照される
- カテゴリで探しやすい構造が必要
- ADRで決定の履歴を追跡

**nullvariant-writings**:
- 私的な作業ログ
- カテゴリ判断の認知負荷を避ける
- 時系列で作業の流れを追う

---

## 📚 関連ドキュメント

- [DOCUMENTATION_STRUCTURE.yml](governance/DOCUMENTATION_STRUCTURE.yml) - 機械可読形式の定義
- [HIERARCHY_RULES.md](governance/HIERARCHY_RULES.md) - 階層ルール詳細
- [AI_GUIDELINES.md](governance/AI_GUIDELINES.md) - AI向けドキュメント記録ガイドライン
- [decisions/INDEX.md](decisions/INDEX.md) - ADR索引

---

## 🎯 あなたが知りたいこと別ガイド

### ❓ 「このプロジェクトは何か」を知りたい

→ **[プロジェクトルート README.md](../README.md)** を読む

- プロジェクト概要
- 基本的な使い方
- ファイル構成

---

### ❓ 「なぜこういう構造なのか」を知りたい

→ **[governance/HIERARCHY_RULES.md](governance/HIERARCHY_RULES.md)** を読む

- Tier 0-4 階層の説明
- 各ドキュメント種別の役割
- 優先度関係

---

### ❓ 「具体的にどのファイルを読めばいいのか」を知りたい

→ **[.github/copilot-instructions.md](../.github/copilot-instructions.md)** を読む

このファイルに **Tier 0（最優先）ドキュメント**が明記されています：

1. **nullvariantリポジトリ仕様書**
   - `content/ja/AGENT.md` - 6ペルソナシステム + 自己完成論

2. **ガバナンス体系**
   - `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 構造定義
   - `docs/governance/HIERARCHY_RULES.md` - 階層説明
   - `docs/governance/AI_GUIDELINES.md` - AI向けガイド

3. **意思決定記録**
   - `docs/decisions/INDEX.md` - ADR一覧

---

### ❓ 「過去の決定」を知りたい

→ **[decisions/INDEX.md](decisions/INDEX.md)** を使う

- **カテゴリ別に見る** - 「アーキテクチャ変更」「ドキュメント構造」など
- **時系列で見る** - 「2025年10月のすべての決定」など
- **ステータス別に見る** - 「現在有効な決定」「非推奨」など

**例**:
```
🏗️ アーキテクチャ変更 → ADR-0001, ADR-0007
📘 ドキュメント構造変更 → ADR-0002, ADR-0011, ADR-0012
📙 ツール・インフラ → ADR-0004
```

---

### ❓ 「ファイル名の命名規則」を知りたい

→ **[governance/NAMING_DECISION_SUMMARY.md](governance/NAMING_DECISION_SUMMARY.md)** を読む

以下の3つのルールが統合されています：

1. **ケース規則**（大文字 vs 小文字）
   - メタドキュメント = 大文字（README.md, OPERATIONS.ja.md）
   - 流動ドキュメント = 小文字（20251028_0001_ci-cd-pause_architecture.md）
   - 詳細: [ADR-0011](decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md)

2. **区切り文字**（ハイフン vs アンダースコア）
   - アンダースコア = 主要セクション区切り（日付・シーケンス・カテゴリ）
   - ハイフン = slug内の単語繋ぎ（URLフレンドリー）
   - 詳細: [ADR-0012](decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md)

---

### ❓ 「運用手順」を知りたい

→ **[operations/current/](operations/current/)** を参照

- `OPERATIONS.ja.md` - 全体的な運用手順
- `NOTE_SYNC_MANUAL.ja.md` - note公開手順
- `WORKFLOW_TEXT_ASSETS.ja.md` - テキスト資産管理

---

### ❓ 「これからの予定」を知りたい

→ **[prd/active/](prd/active/)** を参照

- 策定中の要件定義がリストされています

---

## 🚀 よくある作業

### 新しい決定を記録

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "human"

# INDEX.mdを再生成
python scripts/generate_index.py
```

### ADRを検索

```bash
# カテゴリで検索
ls docs/decisions/active/2025/10/*_architecture.md

# 索引で確認（ブラウザで見やすい）
cat docs/decisions/INDEX.md
```

### ドキュメント整合性確認

```bash
python scripts/validate_docs.py
```

---

**最終更新**: 2025年10月29日  
**関連リポジトリ**: [nullvariant-writings](https://github.com/nullvariant/nullvariant-writings) (Private)
