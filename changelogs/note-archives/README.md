# note公開版アーカイブ

このディレクトリは、**note に実際に公開した記事のアーカイブ**を保存します。

---

## 📂 ディレクトリの目的

- **アーカイブ**: 公開済みnote記事のスナップショット保存
- **監査**: 過去の公開内容を追跡可能に
- **再現性**: 「何を公開したか」を正確に記録

---

## 📋 ファイル一覧（現在）

| ファイル | 公開日 | バージョン | note URL |
|---------|-------|-----------|----------|
| v2.0-note.md | (TBD) | 2.0.0 | - |
| v3.0-note.md | (TBD) | 3.0.0 | - |
| v3.1-note.md | (TBD) | 3.1.0 | - |
| v4.0-note.md | (TBD) | 4.0.0 | - |
| v4.1-note.md | 2025-10-13 | 4.1.0 | [note.com/nullvariant/n/n2a9a5fbf6e57](https://note.com/nullvariant/n/n2a9a5fbf6e57) |

---

## 🔄 運用フロー

### 新バージョン公開時

1. **note記事生成**:
   ```bash
   python scripts/prepare_note_article.py
   # → changelogs/note-archives/vX.X-note-complete.md 生成
   ```

2. **noteに投稿**:
   - `vX.X-note-complete.md` を全文コピー
   - noteにペースト・タイトル設定・公開

3. **公開版保存**:
   ```bash
   cp changelogs/note-archives/vX.X-note-complete.md changelogs/note-archives/vX.X-note.md
   rm changelogs/note-archives/vX.X-note-complete.md
   ```

4. **CHANGELOG.md更新**:
   - note URLを追記
   - Git commit & push

**詳細**: [`docs/NOTE_SYNC_MANUAL.ja.md`](../../docs/NOTE_SYNC_MANUAL.ja.md) を参照

---

## 📝 ファイル構造

各 `vX.X-note.md` は以下の構造を持ちます:

```markdown
# NULLVARIANT OS バージョンX.X.X リリースノート

> 🔗 最新版は GitHub で管理しています
> https://github.com/nullvariant/nullvariant

---

## 📋 vX.X アップデート内容

## [X.X.X] - YYYY-MM-DD

### Added
...

### Enhanced
...

---

## 📖 AGENT.ja.md 本文

（AGENT.ja.md の全文、リンクはGitHub絶対URLに変換済み）

---

## 🔗 関連リンク

- GitHub リポジトリ: https://github.com/nullvariant/nullvariant
- Changelog 全体: https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md
- note Magazine: https://note.com/nullvariant/m/m0d682a2ae34d
```

---

## 🚫 このディレクトリに含めないもの

- ❌ `-draft.md`: 草稿（一時ファイル、公開後削除）
- ❌ `-complete.md`: スクリプト出力（公開後削除）
- ✅ `-note.md`: 公開版のみ保存

**理由**: 
- 元データは `CHANGELOG.md` + `content/AGENT.ja.md` に存在
- 必要なら `scripts/prepare_note_article.py` で再生成可能
- 最終的に必要なのは「実際に公開した内容」のみ

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
