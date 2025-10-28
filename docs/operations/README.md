# Operations ディレクトリ

**運用手順書管理**

---

## 🎯 このディレクトリについて

日常的な運用手順、トラブルシューティング、メンテナンス手順を管理するディレクトリです。

---

## 📁 構造

```
operations/
├── current/                    # 現在有効な手順書
│   ├── release-process.ja.md
│   └── troubleshooting.ja.md
├── deprecated/                 # 非推奨（参考のみ）
└── README.md                   # このファイル
```

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

### 1. テンプレートをコピー

```bash
cp docs/operations/template.md docs/operations/current/my-procedure.ja.md
```

### 2. 内容を記入

- 手順を具体的に
- コマンドを明記
- 確認項目を網羅

### 3. 動作確認

- 実際に手順を実行
- 問題がないか確認

---

## 🔍 トラブルシューティング索引

### よくあるエラー

| エラー | 対処法 | 参照 |
|-------|--------|------|
| ADR番号重複 | `scripts/generate_index.py` 実行 | [troubleshooting.ja.md](current/troubleshooting.ja.md) |
| CI失敗 | ログ確認 | [troubleshooting.ja.md](current/troubleshooting.ja.md) |

詳細は [`current/troubleshooting.ja.md`](current/troubleshooting.ja.md) を参照。

---

## 🔄 運用手順書のライフサイクル

### 1. Current（現在有効）

```bash
# current/ に配置
docs/operations/current/my-procedure.ja.md
```

### 2. Deprecated（非推奨）

```bash
# deprecated/ に移動
mv docs/operations/current/my-procedure.ja.md \
   docs/operations/deprecated/
```

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
