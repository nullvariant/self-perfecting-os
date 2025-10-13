# 既存note記事の受領と整理

このディレクトリに、既存のnote記事（md形式）を配置してください。

## 必要なファイル

以下の3つのファイルを `changelogs/note-archives/` に配置してください：

1. **v3.0-note.md** - ver3.0 のnote記事全文
2. **v3.1-note.md** - ver3.1 のnote記事全文
3. **v4.0-note.md** - ver4.0 のnote記事全文

## ファイル形式

各ファイルは以下の構造を含むことを想定しています：

```markdown
# [タイトル]

## v{VERSION} アップデート内容
（Changelog部分）

## AGENT.ja.md 本文
（本文全文）
```

## 次のステップ

ファイルを配置後、以下の作業を行います：

1. 各ファイルから Changelog 部分を抽出
2. CHANGELOG.md へ統合（時系列順）
3. フォーマットの統一
4. セクション参照の追加
5. note記事URLの記録

---

## ファイル配置状況

| ファイル | 配置日 | 文字数 | 状態 |
|---------|--------|--------|------|
| v2.0-note.md | 2025-10-13 | 384行 | ✅ 配置完了（コンテスト用形式） |
| v3.0-note.md | 2025-10-13 | 1,053行 | ✅ 配置完了 |
| v3.1-note.md | 2025-10-13 | 1,604行 | ✅ 配置完了 |
| v4.0-note.md | 2025-10-13 | 2,886行 | ✅ 配置完了 |

## Changelog 抽出状況

| バージョン | CHANGELOG.md統合 | note URL | 抽出完了日 |
|-----------|------------------|----------|-----------|
| v4.0.0 (2025-10-11) | ✅ 完了 | https://note.com/nullvariant/n/n0c2b7c97a0ba | 2025-10-13 |
| v3.1.0 (2025-10-05) | ✅ 完了 | https://note.com/nullvariant/n/n353d60ed5ae0 | 2025-10-13 |
| v3.0.0 (2025-10-04) | ✅ 完了 | https://note.com/nullvariant/n/naf2590195055 | 2025-10-13 |
| v2.0 (2025-08-16) | ⏸️ 保留 | https://note.com/nullvariant/n/n7f150b19f6a7 | - |

**Note**: v2.0は「AIと自由研究」コンテスト用の特殊形式のため、CHANGELOG.md への統合は保留中。必要に応じて将来的に追加可能。

### note Magazine
全てのAI向けChangelog記事は以下のマガジンに収録されています：
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)

---

**Status**: ✅ Phase 2完了（2025-10-13）

全てのnote記事ファイルを受領し、v3.0, v3.1, v4.0のChangelog部分をCHANGELOG.mdへ統合完了。
