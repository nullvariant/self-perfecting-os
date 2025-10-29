# PRD ディレクトリ

**Product Requirements Document（要件定義書）管理**

---

## 🎯 このディレクトリについて

新機能開発や改善提案の要件を定義するディレクトリです。

---

## 📁 構造

```
prd/
├── active/                     # 現在進行中・計画中
│   ├── 20251028_note-workflow-automation.ja.md
│   └── ...
├── implemented/                # 実装完了
├── cancelled/                  # キャンセル
└── README.md                   # このファイル
```

### ファイル名規則

PRDファイルは以下の命名規則に従います（英小文字・ケバブケースのスラッグ）：

```
{YYYYMMDD}_{slug}.ja.md
```

**例:**
- `20251029_dialogue-log-persistence.ja.md`
- `20251028_note-workflow-automation.ja.md`

**理由:**
- 作成日が明確で、時系列ソートが容易
- URLフレンドリーかつプログラマティックに扱いやすい（ケバブケース）
- ルールは ADR-0011（ケース規則）/ ADR-0012（ハイフン・アンダースコア）に整合

---

## 📝 PRDとは

### Product Requirements Document

- **定義**: 機能の要件を明確に定義したドキュメント
- **目的**: 開発前に「何を作るか」を明確にする
- **形式**: テンプレートに従う

---

## ✅ PRDが必要な場合

- ✅ 新機能の開発
- ✅ 既存機能の大幅な改善
- ✅ 複数ステップが必要な開発
- ✅ 複数のリポジトリにまたがる変更

---

## 📋 PRDのテンプレート（このページ内のブロックをコピー）

```markdown
# PRD: [機能名]

## 📋 概要
- **目的**: なぜこの機能が必要か
- **対象ユーザー**: 誰が使うか
- **優先度**: High / Medium / Low

## 🎯 要件

### 機能要件
1. ...
2. ...

### 非機能要件
- パフォーマンス: ...
- セキュリティ: ...

## 🔧 実装方針

### アーキテクチャ
...

### 技術スタック
...

## 📊 成功基準

- [ ] ...
- [ ] ...

## 📅 スケジュール

- Phase 1: ...
- Phase 2: ...

## 🔗 関連ドキュメント

- ADR-XXXX: ...
- Issue #XX: ...
```

---

## 🚀 PRDの作成方法

### 1. ファイル名を決定

命名規則に従ってファイル名を決定：

```
{YYYYMMDD}_{slug}.ja.md
```

例: `20251029_new-feature-name.ja.md`

### 2. テンプレートを使用

このREADME内の「📋 PRDのテンプレート」コードブロックを新規ファイルへ貼り付け、各項目を埋めてください（専用テンプレートファイルは現時点では提供していません）。

### 3. 内容を記入

- 目的を明確に
- 要件を具体的に
- 成功基準を定義

### 3. レビュー

- 自己レビュー
- 必要なら他者レビュー

---

## 🔄 PRDのライフサイクル

### 1. Draft（草案）

```markdown
## Status
- Draft
```

### 2. Active（開発中）

```bash
# active/ に配置
docs/prd/active/my-feature.ja.md
```

### 3. Implemented（実装完了）

```bash
# implemented/ に移動
mv docs/prd/active/my-feature.ja.md \
   docs/prd/implemented/
```

### 4. Cancelled（キャンセル）

```bash
# cancelled/ に移動
mv docs/prd/active/my-feature.ja.md \
   docs/prd/cancelled/
```

---

## 🏷️ タグ（任意）

ファイル名末尾でのカテゴリ付与は行いません（命名規則簡素化のため）。必要に応じて本文冒頭やFront Matter（使用する場合）で以下のようなタグを付与してください：

- `feature`（新機能）
- `improvement`（改善）
- `refactor`（リファクタリング）
- `infrastructure`（インフラ改善）

---

## 📚 参考資料

- [`docs/decisions/README.md`](../decisions/README.md) - ADRとの違い
- [`docs/README.md`](../README.md) - 全体のガイド

---

## 💡 PRD vs ADR

| 項目 | PRD | ADR |
|------|-----|-----|
| **用途** | 要件定義 | 決定記録 |
| **タイミング** | 開発前 | 決定時 |
| **内容** | 「何を作るか」 | 「なぜこの決定をしたか」 |
| **ライフサイクル** | Draft → Active → Completed | Draft → Accepted → (Deprecated) |

---

**最終更新**: 2025年10月29日
