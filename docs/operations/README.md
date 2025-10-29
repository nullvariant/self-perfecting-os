# Operations ディレクトリ

**運用手順書管理**

---

## 🎯 このディレクトリについて

日常的な運用手順、トラブルシューティング、メンテナンス手順を管理するディレクトリです。

---

## 📁 構造

> **📘 全体構造とルール**: [`../../governance/HIERARCHY_RULES.md`](../../governance/HIERARCHY_RULES.md) を参照してください。

**ディレクトリ概要**：

- **`current/`** - 現在有効な運用手順書（`{YYYYMMDD}_{type}.ja.md` 形式）
- **`archive/`** - 過去版アーカイブ（`{YYYY}/{MM}/` で月別管理）

**具体的なファイル構成、命名規則、アーカイブルールの詳細は権威文書を参照してください。**

---

## 📝 運用手順書とは

### 定義

- **日常的な運用手順**: リリース、デプロイ、メンテナンス
- **トラブルシューティング**: よくあるエラーと対処法
- **チェックリスト**: 作業確認項目

---

## ✅ 運用手順書が必要な場合

- ✅ リリースフロー
- ✅ デプロイ手順
- ✅ バックアップ手順
- ✅ トラブルシューティング
- ✅ メンテナンス作業

---

## 📋 運用手順書のテンプレート

```markdown
# [手順名]

## 📋 概要
- **目的**: ...
- **頻度**: 毎週 / 毎月 / 必要時
- **所要時間**: 約XX分

## 🔧 前提条件

- [ ] ...
- [ ] ...

## 📝 手順

### ステップ1: ...

```bash
# コマンド
```

### ステップ2: ...

...

## ✅ 確認項目

- [ ] ...
- [ ] ...

## ⚠️ トラブルシューティング

### エラー: ...
**対処法**: ...
```

---

## 🚀 運用手順書の作成方法

### 1. 既存ファイルをベースにコピー

```bash
# 既存の運用手順書をベースにして新規作成
cp docs/operations/current/20251028_OPERATIONS.ja.md docs/operations/current/{YYYYMMDD}_{TYPE}.ja.md
```

### 2. 内容を記入

- 手順を具体的に
- コマンドを明記
- 確認項目を網羅

### 3. 動作確認

- 実際に手順を実行
- 問題がないか確認

---

##  運用手順書のライフサイクル

### 1. Current（現在有効）

```bash
# current/ に配置（最新の手順）
docs/operations/current/{YYYYMMDD}_{type}.ja.md

# 例
docs/operations/current/20251028_OPERATIONS.ja.md
```

### 2. Archive（過去版保管）

```bash
# 古い手順を月別アーカイブに移動
mkdir -p docs/operations/archive/{YYYY}/{MM}/
mv docs/operations/current/20251027_OPERATIONS.ja.md \
   docs/operations/archive/2025/10/

# 結果
docs/operations/archive/2025/10/20251027_OPERATIONS.ja.md
```

**注意**: `deprecated/` ディレクトリではなく、`archive/{YYYY}/{MM}/` 形式で月別管理

---

## 📚 参考資料

- [`docs/decisions/README.md`](../decisions/README.md) - ADRとの違い
- [`docs/prd/README.md`](../prd/README.md) - PRDとの違い

---

## 💡 運用手順書 vs ADR vs PRD

| 項目 | 運用手順書 | ADR | PRD |
|------|----------|-----|-----|
| **用途** | 手順書 | 決定記録 | 要件定義 |
| **内容** | 「どうやるか」 | 「なぜこの決定をしたか」 | 「何を作るか」 |
| **更新頻度** | プロセス変更時 | 決定時 | 開発前 |
| **実行性** | ✅ 実行可能 | ❌ 記録のみ | ❌ 計画のみ |

---

**最終更新**: 2025年10月28日
