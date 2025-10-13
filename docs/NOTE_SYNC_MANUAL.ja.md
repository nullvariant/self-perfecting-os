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

### Step 1: CHANGELOG.md の該当バージョンをコピー

1. `CHANGELOG.md` を開く
2. 該当バージョンのセクションをコピー（例: `## [4.1.0] - 2025-10-13` から次のバージョンの手前まで）
3. テキストエディタに一時保存

**コピー範囲の例:**
```markdown
## [4.1.0] - 2025-10-13

### Added
...

### Enhanced
...

### Impact
...

### Related Links
...
```

---

### Step 2: AGENT.ja.md 本文をコピー

1. `content/AGENT.ja.md` を開く
2. 全文をコピー（Ctrl+A / Cmd+A → Ctrl+C / Cmd+C）
3. テキストエディタに一時保存

---

### Step 3: note記事テンプレートを使用

以下の「note記事テンプレート」セクションのテンプレートをコピーし、以下を置き換え：

- `{VERSION}`: バージョン番号（例: `v4.1`）
- `{TITLE}`: アップデートのタイトル（例: `感情辞書統合アップデート`）
- `{CHANGELOG_CONTENT}`: Step 1でコピーしたChangelog
- `{AGENT_CONTENT}`: Step 2でコピーしたAGENT.ja.md本文
- `{GITHUB_REPO_URL}`: GitHubリポジトリのURL
- `{CHANGELOG_URL}`: CHANGELOG.mdへの直リンク

---

### Step 4: note に新規投稿

1. note の「投稿」ボタンをクリック
2. テンプレートを貼り付け
3. プレビューで確認：
   - [ ] リンクが正しく機能するか
   - [ ] マークダウンが正しくレンダリングされているか
   - [ ] 見出し構造が適切か

4. タイトルを設定：
   ```
   [AGENT.ja.md] v{VERSION} {TITLE}
   ```
   例: `[AGENT.ja.md] v4.1 感情辞書統合アップデート`

5. ハッシュタグを追加：
   ```
   #AI #AIエージェント #6ペルソナシステム #感情辞書 #EBI測定
   ```

6. **公開設定を確認**:
   - [ ] 公開範囲: 全体公開
   - [ ] コメント設定: お好みで
   - [ ] AI学習: 許可（noteのデフォルト設定）

7. 「公開する」をクリック

---

### Step 5: note URL を CHANGELOG.md に追記

1. 公開されたnote記事のURLをコピー
2. `CHANGELOG.md` を開く
3. 該当バージョンの `Related Links` セクションに追記：

```markdown
### Related Links
- [AGENT.ja.md v4.1](content/AGENT.ja.md)
- [感情辞書 v1.0](content/EmotionMood_Dictionary.ja.md)
- [note記事: v4.1アップデート](https://note.com/your_account/n/nxxxxxxxx) ← 追加
```

4. Git commit & push:
```bash
git add CHANGELOG.md
git commit -m "docs: Add note article URL for v4.1"
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

### 📝 投稿前チェック

- [ ] CHANGELOG.md の該当バージョンをコピー済み
- [ ] AGENT.ja.md 本文をコピー済み
- [ ] テンプレートの全ての `{変数}` を置き換え済み
- [ ] GitHub URL が正しい
- [ ] バージョン番号が正しい

### 🔍 投稿時チェック

- [ ] note のプレビューで確認済み
- [ ] タイトルが `[AGENT.ja.md] v{VERSION} {TITLE}` 形式
- [ ] ハッシュタグを追加済み
- [ ] 公開範囲が「全体公開」
- [ ] AI学習が許可されている（noteデフォルト）

### ✅ 投稿後チェック

- [ ] 公開されたnote記事のURLをコピー
- [ ] CHANGELOG.md に note URL を追記
- [ ] Git commit & push 完了
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

### Q5: 手動コピーが面倒

**A**: Phase 4（自動化検討）で、スクリプト化を検討します。ただし、現時点では手動運用が最も安全で確実です。

---

## 付録: 過去バージョンの移行

既存のnote記事（ver3.0, 3.1, 4.0）を GitHub CHANGELOG.md へ統合する場合：

1. 既存note記事のmd形式ファイルを `changelogs/note-archives/` に配置
2. Changelog部分を抽出
3. CHANGELOG.md の該当バージョンセクションに統合
4. 既存note記事に「最新版はGitHubで管理」の注記を追記（編集機能で）

詳細は [PRD_CHANGELOG_MIGRATION.ja.md](PRD_CHANGELOG_MIGRATION.ja.md) の Phase 2 を参照。

---

## 更新履歴（本マニュアル）

| バージョン | 日付 | 変更内容 |
|-----------|------|----------|
| 1.0 | 2025-10-13 | 初版作成 |

---

**質問・改善提案**: GitHub Issues でお知らせください。

---

_このマニュアルは nullvariant プロジェクトの運用効率化のために作成されました。_
