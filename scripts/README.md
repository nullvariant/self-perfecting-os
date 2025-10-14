# Scripts Directory

NULLVARIANT OS の開発・運用を支援する自動化スクリプト集です。

---

## 📋 スクリプト一覧

### 1. build.py
**用途**: AGENT.ja.md の英訳 & YAML抽出

**機能**:
- `content/AGENT.ja.md` を英訳 → `AGENT.md`
- `content/AGENT.ja.md` からYAML構造抽出 → `spec/agent.spec.yaml`
- OpenAI API を使用（GPT-4o推奨）

**実行方法**:
```bash
python scripts/build.py
# または
make gen
```

**環境変数**:
- `OPENAI_API_KEY`: OpenAI APIキー（必須）

**プロンプト**:
- `prompts/01_en_translate.txt`: 英訳プロンプト
- `prompts/02_yaml_extract.txt`: YAML抽出プロンプト

---

### 2. gen_toc.py
**用途**: AGENT.ja.md の目次自動生成

**機能**:
- マークダウンの見出し（`##`, `###`）を解析
- 目次セクションを自動生成・更新
- 階層構造を保持したリンク付き目次

**実行方法**:
```bash
python scripts/gen_toc.py
```

**対象ファイル**:
- `content/AGENT.ja.md` の `## 目次 (Table of Contents)` セクション

**注意**:
- `<a id="xxx"></a>` アンカーを自動生成
- note投稿時は `prepare_note_article.py` でアンカー削除

---

### 3. prepare_note_article.py
**用途**: note記事の自動生成

**機能**:
1. `AGENT.ja.md` からアンカータグ `<a id="..."></a>` を除去
2. 目次セクション `## 目次 (Table of Contents)` を除去
3. 相対リンクを GitHub 絶対URLに変換:
   - `../CHANGELOG.md` → `https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md`
   - `content/EmotionMood_Dictionary.ja.md` → `https://github.com/.../content/EmotionMood_Dictionary.ja.md`
   - `EmotionMood_Dictionary.ja.md` → `https://github.com/.../content/EmotionMood_Dictionary.ja.md`

**実行方法**:
```bash
python scripts/prepare_note_article.py
# または特定バージョンを指定
python scripts/prepare_note_article.py --version 4.2
```

**入力**:
- `content/AGENT.ja.md`（メインドキュメント）
- `changelogs/note-archives/vX.X-note-draft.md`（存在すれば自動検出、`--draft`で上書き可能）

**出力**:
- `changelogs/note-archives/vX.X-note-complete.md`（バージョンは自動推定。`--output`で上書き可能）

**リンク変換パターン**:

| パターン | 元のリンク | 変換後 |
|---------|-----------|--------|
| Pattern 1 | `[text](../file.md)` | `[text](https://github.com/.../file.md)` |
| Pattern 2 | `[text](content/file.md)` | `[text](https://github.com/.../content/file.md)` |
| Pattern 3 | `[text](file.md)` | `[text](https://github.com/.../content/file.md)` |

**詳細**:
- [NOTE_SYNC_MANUAL.ja.md](../docs/NOTE_SYNC_MANUAL.ja.md) 参照

---

### 4. review.py
**用途**: 日英翻訳の類似度検証

**機能**:
- `AGENT.md` (英語) を日本語に逆翻訳
- `content/AGENT.ja.md` (原文) との類似度を測定
- コサイン類似度で評価（閾値: 0.86以上推奨）

**実行方法**:
```bash
python scripts/review.py
# または
make val
```

**環境変数**:
- `OPENAI_API_KEY`: OpenAI APIキー（必須）

**プロンプト**:
- `prompts/99_backtranslate.txt`: 逆翻訳プロンプト

**出力例**:
```
🔍 Similarity: 0.8932
✅ PASS (>= 0.86)
```

---

### 5. test_toc.py
**用途**: gen_toc.py のテストスクリプト

**機能**:
- 目次生成機能の単体テスト
- 見出し解析ロジックの検証

**実行方法**:
```bash
python scripts/test_toc.py
```

---

## 🔧 prompts/ ディレクトリ

スクリプトで使用するプロンプトテンプレート集です。

```
prompts/
├── 01_en_translate.txt      # 英訳プロンプト（build.py使用）
├── 02_yaml_extract.txt      # YAML抽出プロンプト（build.py使用）
├── 90_self_review.txt       # 自己レビュープロンプト（将来予定）
└── 99_backtranslate.txt     # 逆翻訳プロンプト（review.py使用）
```

---

## 🚀 よく使うコマンド

### 基本的なビルドフロー
```bash
# 1. 目次再生成（必要な場合）
python scripts/gen_toc.py

# 2. 英訳＆YAML生成
python scripts/build.py

# 3. 類似度検証
python scripts/review.py

# または Makefile経由
make gen  # build.py実行
make val  # review.py実行
```

### note記事公開フロー
```bash
# 1. note記事生成
python scripts/prepare_note_article.py

# 2. 生成ファイル確認
cat changelogs/note-archives/v4.1-note-complete.md

# 3. リンク変換確認
grep "github.com/nullvariant" changelogs/note-archives/v4.1-note-complete.md

# 4. noteに投稿（手動）
# - v4.1-note-complete.md をコピー＆ペースト
# - タイトル・ハッシュタグ設定
# - 公開

# 5. 公開版保存
cp changelogs/note-archives/v4.1-note-complete.md changelogs/note-archives/v4.1-note.md
rm changelogs/note-archives/v4.1-note-complete.md
```

---

## 📚 関連ドキュメント

- [OPERATIONS.ja.md](../docs/OPERATIONS.ja.md): 運用マニュアル
- [NOTE_SYNC_MANUAL.ja.md](../docs/NOTE_SYNC_MANUAL.ja.md): note同期手順
- [CONTRIBUTING.md](../CONTRIBUTING.md): コントリビューションガイド

---

## 🔍 トラブルシューティング

### Q1: OpenAI API エラーが出る
**A**: 環境変数 `OPENAI_API_KEY` を確認してください。

```bash
export OPENAI_API_KEY=sk-...
# または .env ファイルに記載
```

### Q2: 類似度が低い（< 0.86）
**A**: 以下を確認:
1. `i18n/glossary.yml` に用語が登録されているか
2. 翻訳プロンプト (`prompts/01_en_translate.txt`) が最新か
3. 原文（AGENT.ja.md）の構造が複雑すぎないか

### Q3: note記事のリンクが変換されない
**A**: `prepare_note_article.py` の変換パターンを確認:
```bash
# 未変換リンクの検出
grep -E '\[.*\]\([^h].*\.md' changelogs/note-archives/v4.1-note-complete.md
```

---

_Last Updated: 2025-10-13_
