# Changelogs Directory

このディレクトリは、AGENT.ja.md のバージョン別詳細ドキュメントを管理するためのものです。

## ディレクトリ構造

```
changelogs/
├── README.md              # 本ファイル
├── note-archives/         # 既存note記事のアーカイブ（md形式）
│   ├── v3.0-note.md      # ver3.0のnote記事
│   ├── v3.1-note.md      # ver3.1のnote記事
│   └── v4.0-note.md      # ver4.0のnote記事
└── (将来的にバージョン別詳細を追加可能)
```

## 使用方法

### note-archives/
- **目的**: 既存のnote記事をmd形式で保存し、Changelog抽出の元データとして保管
- **命名規則**: `v{major}.{minor}-note.md`
- **内容**: note記事の全文（Changelog部分 + AGENT.ja.md本文）

### バージョン別詳細（将来的な拡張）
必要に応じて、以下のような詳細ドキュメントを作成できます：

```
changelogs/
├── v4.1.md               # v4.1の詳細な変更記録
├── v4.0.md               # v4.0の詳細な変更記録
└── migration-guides/     # マイグレーションガイド
    └── v3-to-v4.md
```

## 関連ドキュメント

- [CHANGELOG.md](../CHANGELOG.md): 全バージョンの統合Changelog
- [docs/prd_CHANGELOG_MIGRATION.ja.md](../docs/prd_CHANGELOG_MIGRATION.ja.md): Changelog分離とnoteミラーリング運用のPRD
- [docs/operations/current/](../docs/operations/current/): note同期マニュアル

## 注意事項

- このディレクトリのファイルは**アーカイブ目的**であり、真実の情報源（SSOT）は常に `CHANGELOG.md` と `content/ja/AGENT.md` です
- note記事の原文を保持することで、将来的な参照や監査に対応できます
- バージョン別詳細が必要な場合のみ、このディレクトリに追加ファイルを作成してください

---

_Last Updated: 2025-10-13_
