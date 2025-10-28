# note 同期マニュアル

**Version**: 1.0  
**Last Updated**: 2025-10-13  
**Purpose**: GitHub → note へのミラーリング手順を標準化

---

## 📋 目次

1. [概要](#概要)
2. [前提条件](#前提条件)
3. [アップデート時の手順](#アップデート時の手順)
4. [note記事テンプレート](#note記事テンプレート)
5. [チェックリスト](#チェックリスト)
6. [トラブルシューティング](#トラブルシューティング)

---

## 概要

### 基本方針
- **GitHub = 真実の情報源（SSOT）**: 全ての更新は GitHub で行う
- **note = 公開用ミラー**: AI学習用に note へコピー投稿
- **手動同期**: 現時点では手動コピー＆ペースト運用

### note記事の構成
```
1. GitHub リンク（最新版への誘導）
2. 当該バージョンの Changelog
3. AGENT.ja.md 本文全文
4. 関連リンク
5. フッターに GitHub リンク再掲
```

---

## 前提条件

### GitHub側の準備完了
- [ ] `CHANGELOG.md` にバージョン情報が記載済み
- [ ] `content/AGENT.ja.md` が最新状態
- [ ] `make gen` と `make val` が正常完了
- [ ] Git commit & push 完了

### note側の準備
- [ ] note アカウントにログイン済み
- [ ] 投稿先のマガジン（オプション）を確認

---

## アップデート時の手順

### Step 1: 手動草稿の作成（オプション）

新バージョンの草稿を手動で作成する場合:

1. `changelogs/note-archives/` に `vX.X-note-draft.md` を作成
2. CHANGELOG.mdから該当バージョンをコピー
3. ヘッダー・フッターを追加

**推奨**: Step 2のスクリプトで自動生成する方が簡単です。

---

### Step 2: 自動スクリプトでnote記事を生成

**準備:**
- `CHANGELOG.md` に新バージョンのエントリが記載済み
- `content/AGENT.ja.md` が最新状態

**実行:**
```bash
python scripts/prepare_note_article.py
# 任意: バージョンを明示する場合
python scripts/prepare_note_article.py --version 4.2
```

**スクリプトの処理内容:**
1. `AGENT.ja.md` を読み込み
2. アンカータグ `<a id="..."></a>` とTOCを削除
3. 相対リンクを GitHub 絶対URLに変換
   - `../CHANGELOG.md` → `https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md`
   - `EmotionMood_Dictionary.ja.md` → `https://github.com/.../content/EmotionMood_Dictionary.ja.md`
4. バージョン番号を `AGENT.ja.md` から自動検出（`--version` で上書き可能）
5. `changelogs/note-archives/vX.X-note-complete.md` を出力（`--draft` / `--output` でパス指定可。ドラフト未作成時はAGENT本文のみを出力）

**確認:**
```bash
# 出力ファイルの確認
cat changelogs/note-archives/v{VERSION}-note-complete.md | head -50

# リンク変換の確認
grep -n "github.com/nullvariant" changelogs/note-archives/v{VERSION}-note-complete.md
```

---

### Step 3: note に新規投稿

1. **ファイルを開く**: `changelogs/note-archives/v{VERSION}-note-complete.md`
2. **全文をコピー**: Cmd+A → Cmd+C (macOS) / Ctrl+A → Ctrl+C (Windows)
3. **noteの投稿画面**へペースト
4. **プレビューで確認**:
   - [ ] GitHubリンクが正しく機能するか
   - [ ] 見出し構造が適切か
   - [ ] 画像・表が正しく表示されるか

5. **タイトルを設定**:
   ```
   【AI向け文書】 Self-Perfecting OS Version {VERSION}: Changelog


   ```
   例: `【AI向け文書】 Self-Perfecting OS Version 4.1: Changelog

`

6. **ハッシュタグを追加**:
   ```
   #自己紹介 #AI向け文書 #AI活用 #AIエージェント #メタ認知 #AIと自由研究 #AIと自分研究 #自己探求 #仕様書 #オイラーの等式 #コンテキストエンジニアリング #NullVariant #自己紹介芸人
   ```

7. **マガジンに追加**:
   - マガジン: `AI専用マガジン`
   - URL: https://note.com/nullvariant/m/m0d682a2ae34d

8. **公開設定を確認**:
   - [ ] 公開範囲: 全体公開
   - [ ] AI学習: 許可（noteのデフォルト設定）

9. **「公開する」をクリック**

---

### Step 4: 公開版を保存

公開後、実際に投稿した内容を記録として保存:

```bash
# スクリプト出力ファイルを公開版として保存
cp changelogs/note-archives/v{VERSION}-note-complete.md changelogs/note-archives/v{VERSION}-note.md

# 中間ファイルを削除（不要なファイルの整理）
rm changelogs/note-archives/v{VERSION}-note-draft.md 2>/dev/null
rm changelogs/note-archives/v{VERSION}-note-complete.md
```

**最終的なファイル構成:**
```
changelogs/note-archives/
├── v{VERSION}-note.md  # 実際に公開した最終版（保存）
```

---

### Step 5: note URL を CHANGELOG.md に追記

1. 公開されたnote記事のURLをコピー
   - 例: `https://note.com/nullvariant/n/n2a9a5fbf6e57`

2. `CHANGELOG.md` を開く

3. 該当バージョンの `Related Links` セクションを更新:

```markdown
### Related Links
- [AGENT.ja.md v4.1](content/AGENT.ja.md)
- [感情辞書 v1.0](content/EmotionMood_Dictionary.ja.md)
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)
- [note記事 v4.1](https://note.com/nullvariant/n/n2a9a5fbf6e57)  # ← 追加
```

4. Git commit & push:
```bash
git add CHANGELOG.md changelogs/note-archives/v4.1-note.md
git commit -m "docs: Add note article URL for v4.1 and archive published version"
git push origin main
```

---

## note記事テンプレート

```markdown
# [AGENT.ja.md] {VERSION} {TITLE}

> 🔗 **最新版は GitHub で管理しています**  
> {GITHUB_REPO_URL}  
> 本記事は AI学習用に note へミラーリングしたものです。

---

## 📋 {VERSION} アップデート内容

{CHANGELOG_CONTENT}

---

## 📖 AGENT.ja.md 本文

{AGENT_CONTENT}

---

## 🔗 関連リンク

- **GitHub リポジトリ（最新版）**: {GITHUB_REPO_URL}
- **Changelog 全体**: {CHANGELOG_URL}
- **感情辞書**: {GITHUB_REPO_URL}/blob/main/content/EmotionMood_Dictionary.ja.md
- **note Magazine: AI向けChangelog**: https://note.com/nullvariant/m/m0d682a2ae34d

---

💡 **GitHub が真実の情報源（Single Source of Truth）です**  
本 note 記事は公開・学習用のミラーであり、最新の更新は常に GitHub で行われます。

#AI #AIエージェント #6ペルソナシステム #感情辞書 #EBI測定
```

### テンプレート使用例（v4.1の場合）

```markdown
# [AGENT.ja.md] v4.1 感情辞書統合アップデート

> 🔗 **最新版は GitHub で管理しています**  
> https://github.com/nullvariant/nullvariant  
> 本記事は AI学習用に note へミラーリングしたものです。

---

## 📋 v4.1 アップデート内容

## [4.1.0] - 2025-10-13

### Added
- **Section 2.1.1**: ペルソナ別感情プロファイル概要テーブル
  - 各ペルソナの典型的感情を感情辞書IDで明示化
  ...

（以下、CHANGELOG.md の該当バージョン全文）

---

## 📖 AGENT.ja.md 本文

（AGENT.ja.md の全文を貼り付け）

---

## 🔗 関連リンク

- **GitHub リポジトリ（最新版）**: https://github.com/nullvariant/nullvariant
- **Changelog 全体**: https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md
- **感情辞書**: https://github.com/nullvariant/nullvariant/blob/main/content/EmotionMood_Dictionary.ja.md
- **note Magazine: AI向けChangelog**: https://note.com/nullvariant/m/m0d682a2ae34d

---

💡 **GitHub が真実の情報源（Single Source of Truth）です**  
本 note 記事は公開・学習用のミラーであり、最新の更新は常に GitHub で行われます。

#AI #AIエージェント #6ペルソナシステム #感情辞書 #EBI測定
```

---

## チェックリスト

### 📝 準備段階（GitHub側）

- [ ] CHANGELOG.md に新バージョンのエントリが記載済み
- [ ] content/AGENT.ja.md が最新状態
- [ ] `make gen` と `make val` が正常完了
- [ ] Git commit & push 完了

### 🔧 スクリプト実行

- [ ] `python scripts/prepare_note_article.py` 実行
- [ ] `changelogs/note-archives/vX.X-note-complete.md` が生成された
- [ ] リンク変換の確認:
  ```bash
  grep -n "github.com/nullvariant" changelogs/note-archives/v4.1-note-complete.md
  ```
- [ ] 未変換リンクがないことを確認:
  ```bash
  grep -E '\[.*\]\([^h].*\.md' changelogs/note-archives/v4.1-note-complete.md
  ```

### � note投稿

- [ ] `vX.X-note-complete.md` の全文をコピー
- [ ] note投稿画面にペースト
- [ ] プレビューで確認（リンク・見出し・表）
- [ ] タイトル設定: `NULLVARIANT OS バージョンX.X.X リリースノート`
- [ ] ハッシュタグ追加: `#AI #AIエージェント #NULLVARIANT #エージェントOS`
- [ ] マガジンに追加（オプション）
- [ ] 公開範囲: 全体公開
- [ ] AI学習: 許可
- [ ] 「公開する」をクリック

### ✅ 投稿後処理

- [ ] note記事URLをコピー
- [ ] `cp changelogs/note-archives/vX.X-note-complete.md changelogs/note-archives/vX.X-note.md`
- [ ] `rm changelogs/note-archives/vX.X-note-draft.md` （存在する場合）
- [ ] `rm changelogs/note-archives/vX.X-note-complete.md`
- [ ] CHANGELOG.md に note URL を追記
- [ ] Git commit & push:
  ```bash
  git add CHANGELOG.md changelogs/note-archives/vX.X-note.md
  git commit -m "docs: Add note article URL for vX.X and archive published version"
  git push origin main
  ```
- [ ] note記事とGitHubのリンクが双方向に機能することを確認

---

## トラブルシューティング

### Q1: note でマークダウンが正しく表示されない

**A**: note は独自のマークダウン処理を行うため、一部の記法が異なる場合があります。

- **コードブロック**: バッククォート3つ（\`\`\`）は note でも使用可能
- **テーブル**: note では一部のテーブル記法が非対応の場合あり → プレビューで確認
- **絵文字**: note は絵文字対応しているため、そのまま使用可能

### Q2: CHANGELOG.md に note URL を追記し忘れた

**A**: 後から追記しても問題ありません。

```bash
# CHANGELOG.md を編集して URL 追記
git add CHANGELOG.md
git commit -m "docs: Add missing note article URL for vX.X"
git push origin main
```

### Q3: note 記事を公開後、間違いに気づいた

**A**: note の編集機能で修正可能です。

1. note記事の「編集」ボタンをクリック
2. 修正を行う
3. 「更新する」をクリック

**重要**: GitHub側が正しいことを確認し、GitHub → note の方向で修正してください。

### Q4: バージョン番号を間違えた

**A**: 
1. note記事を編集して修正
2. CHANGELOG.md も確認・修正
3. Git commit & push

### Q5: スクリプトのリンク変換が正しく動作しない

**A**: 以下を確認してください:

1. **相対パスの種類を確認**:
   - `../file.md` → Pattern 1で変換
   - `content/file.md` → Pattern 2で変換
   - `file.md`（同ディレクトリ） → Pattern 3で変換

2. **変換結果の確認**:
   ```bash
   grep -n "https://github.com" changelogs/note-archives/v4.1-note-complete.md
   ```

3. **未変換リンクの検出**:
   ```bash
   # 相対パスが残っていないか確認
   grep -E '\[.*\]\([^h].*\.md' changelogs/note-archives/v4.1-note-complete.md
   ```

4. **スクリプトの再実行**:
   ```bash
   python scripts/prepare_note_article.py
   ```

### Q6: note記事のタイトルフォーマットは固定ですか？

**A**: いいえ、推奨フォーマットですが変更可能です。

- **推奨**: `NULLVARIANT OS バージョン{VERSION} リリースノート`
- **理由**: 一貫性とSEO、AI学習データとしての明確性
- **変更OK**: プロジェクトの方針に応じて調整可能

---

## 付録A: スクリプト詳細

### prepare_note_article.py の仕様

**場所**: `scripts/prepare_note_article.py`

**機能**:
1. アンカータグ削除: `<a id="xxx"></a>` を除去
2. TOC削除: `## 目次 (Table of Contents)` セクションを除去（絵文字付きでも対応）
3. 相対リンク変換: 3つのパターンで絶対URLに変換

**変換パターン**:

| パターン | 元のリンク | 変換後 |
|---------|-----------|--------|
| Pattern 1 | `[text](../file.md)` | `[text](https://github.com/nullvariant/nullvariant/blob/main/file.md)` |
| Pattern 2 | `[text](content/file.md)` | `[text](https://github.com/.../content/file.md)` |
| Pattern 3 | `[text](file.md)` | `[text](https://github.com/.../content/file.md)` |

**実行方法**:
```bash
python scripts/prepare_note_article.py
# バージョン・ファイル指定が必要な場合
python scripts/prepare_note_article.py --version 4.2 --draft path/to/custom-draft.md --output path/to/output.md
```

**入力**:
- `content/AGENT.ja.md`（メインドキュメント）
- `changelogs/note-archives/vX.X-note-draft.md`（存在すれば自動読込。省略可）

**出力**:
- `changelogs/note-archives/vX.X-note-complete.md`（バージョン自動推定。`--output`で変更可）

---

## 付録B: 過去バージョンの移行

既存のnote記事（ver3.0, 3.1, 4.0）を GitHub CHANGELOG.md へ統合する場合：

1. 既存note記事のmd形式ファイルを `changelogs/note-archives/` に配置
2. Changelog部分を抽出
3. CHANGELOG.md の該当バージョンセクションに統合
4. 既存note記事に「最新版はGitHubで管理」の注記を追記（編集機能で）

詳細は [changelog-migration.ja.md](changelog-migration.ja.md) の Phase 2 を参照。

---

## 更新履歴（本マニュアル）

| バージョン | 日付 | 変更内容 |
|-----------|------|----------|
| 1.0 | 2025-10-13 | 初版作成 |

---

**質問・改善提案**: GitHub Issues でお知らせください。

---

_このマニュアルは nullvariant プロジェクトの運用効率化のために作成されました。_
