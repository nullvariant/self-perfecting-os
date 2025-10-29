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
20251028_0005_script-cleanup-makefile_dev.md
```

### PRD・運用手順書

```
{YYYYMMDD}_{slug}.ja.md
```

**例**:
```
20251028_note-workflow-automation.ja.md
20251028_OPERATIONS.ja.md
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

## 🚀 クイックスタート

### 新しい決定を記録

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "human"
```

### ADRを検索

```bash
# カテゴリで検索
ls docs/decisions/active/2025/10/*_dev.md

# 索引で確認
cat docs/decisions/INDEX.md
```

### ドキュメントの妥当性確認

```bash
python scripts/validate_docs.py
```

---

**最終更新**: 2025年10月28日  
**関連リポジトリ**: [nullvariant-writings](https://github.com/nullvariant/nullvariant-writings) (Private)
