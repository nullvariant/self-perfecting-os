# Scripts Directory

Self Perfecting OS の開発・運用を支援する自動化スクリプト集です。

---

## 📋 スクリプト一覧

### 1. build.py
**用途**: content/ja/AGENT.md の英訳 & YAML抽出

**機能**:
### 処理内容

- `content/ja/*.md` を多言語翻訳 → `content/en/*.md`
- `content/ja/AGENT.md` からYAML構造抽出 → `spec/agent.spec.yaml`
- `content/en/AGENT.md` をルートにコピー → `AGENT.md`（英語版エントリポイント）
- Claude Sonnet 4.5 使用（第一候補、選定中）

**実行方法**:
```bash
python scripts/build.py
# または
make gen
```

**環境変数**:
- `ANTHROPIC_API_KEY`: Anthropic Claude APIキー（必須）

**プロンプト**:
- `prompts/01_en_translate.txt`: 英訳プロンプト
- `prompts/02_yaml_extract.txt`: YAML抽出プロンプト

---

### 2. gen_toc.py
**用途**: content/ja/AGENT.md の目次自動生成

**機能**:
- マークダウンの見出し（`##`, `###`）を解析
- 目次セクションを自動生成・更新
- 階層構造を保持したリンク付き目次

**実行方法**:
```bash
python scripts/gen_toc.py
```

### 対象ファイル

- `content/ja/AGENT.md` の `## 目次 (Table of Contents)` セクション

### 使用方法

```bash
python scripts/gen_toc.py content/ja/AGENT.md
```

**注意**:
- `<a id="xxx"></a>` アンカーを自動生成
- note投稿時は `prepare_note_article.py` でアンカー削除

---

### 3. prepare_note_article.py
**用途**: note記事の自動生成

**機能**:
1. `content/ja/AGENT.md` からアンカータグ `<a id="..."></a>` を除去
2. 目次セクション `## 目次 (Table of Contents)` を除去
3. 相対リンクを GitHub 絶対URLに変換:
   - `../CHANGELOG.md` → `https://github.com/nullvariant/nullvariant/blob/main/CHANGELOG.md`
   - `content/ja/EmotionMood_Dictionary.md` → `https://github.com/.../content/ja/EmotionMood_Dictionary.md`
   - `EmotionMood_Dictionary.md` → `https://github.com/.../content/ja/EmotionMood_Dictionary.md`

```

**実行方法**:
```bash
python scripts/prepare_note_article.py
# または特定バージョンを指定
python scripts/prepare_note_article.py --version 4.2
```

**入力**:
### 対象ファイル

- `content/ja/AGENT.md`（メインドキュメント）
- `../nullvariant-writings/changelogs/note-archives/vX.X-note-draft.md`（存在すれば自動検出、`--draft`で上書き可能）

**出力**:
- `../nullvariant-writings/changelogs/note-archives/vX.X-note-complete.md`（バージョンは自動推定。`--output`で上書き可能）

> **Note**: ADR-0007により、note記事原稿は [nullvariant-writings](https://github.com/nullvariant/nullvariant-writings/tree/main/changelogs) リポジトリで管理されています。スクリプトは nullvariant に残存しますが、出力先は nullvariant-writings です。

**リンク変換パターン**:

| パターン | 元のリンク | 変換後 |
|---------|-----------|--------|
| Pattern 1 | `[text](../file.md)` | `[text](https://github.com/.../file.md)` |
| Pattern 2 | `[text](content/file.md)` | `[text](https://github.com/.../content/file.md)` |
| Pattern 3 | `[text](file.md)` | `[text](https://github.com/.../content/file.md)` |

**詳細**:
- [NOTE_SYNC_MANUAL.ja.md](../docs/operations/current/) 参照

---

### 4. review.py
**用途**: 日英翻訳の類似度検証

**機能**:
- `content/en/AGENT.md` (英語) を日本語に逆翻訳
- `content/ja/AGENT.md` (原文) との類似度を測定
- コサイン類似度で評価（閾値: 0.86以上推奨）

**実行方法**:
```bash
python scripts/review.py
# または
make val
```

**環境変数**:
- `ANTHROPIC_API_KEY`: Anthropic Claude APIキー（予定）

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

# 2. 生成ファイル確認（出力先: nullvariant-writings）
cat ../nullvariant-writings/changelogs/note-archives/v4.1-note-complete.md

# 3. リンク変換確認
grep "github.com/nullvariant" ../nullvariant-writings/changelogs/note-archives/v4.1-note-complete.md

# 4. noteに投稿（手動）
# - v4.1-note-complete.md をコピー＆ペースト
# - タイトル・ハッシュタグ設定
# - 公開

# 5. 公開版保存
cd ../nullvariant-writings/changelogs/note-archives
cp v4.1-note-complete.md v4.1-note.md
rm v4.1-note-complete.md
```

---

## 📚 関連ドキュメント

- [OPERATIONS.ja.md](../docs/operations/current/): 運用マニュアル
- [NOTE_SYNC_MANUAL.ja.md](../docs/operations/current/): note同期手順
- [CONTRIBUTING.md](../CONTRIBUTING.md): コントリビューションガイド

---

## 🧪 テストファイル配置ルール（ADR-0009）

スクリプトのテスト・デバッグ中に生成されるファイルは、すべて `tests/fixtures/` 配下に配置してください。

### 配置先の判断基準

| 配置先 | 用途 | Git管理 | 例 |
|--------|------|---------|-----|
| `tests/fixtures/permanent/` | 単体テスト、回帰テスト、継続的に使用 | ✅ する | `sample_agent.md`, `expected_output.yaml` |
| `tests/fixtures/temporary/` | 一時的な動作確認、デバッグ | ❌ しない | `test_conversation.txt`, `debug_output.json` |

### 判断の6つの質問

1. **再現性**: 他の開発者が同じテストを実行できるべきか？ → Yes: permanent
2. **バージョン管理**: 将来のコード変更でこのデータが必要か？ → Yes: permanent
3. **一時性**: このファイルは今回限りの確認用か？ → Yes: temporary
4. **共有**: 他の開発者やCIでも使用するか？ → Yes: permanent
5. **削除**: テスト完了後に削除してよいか？ → Yes: temporary
6. **回帰**: 将来のバグ検出に役立つか？ → Yes: permanent

### 具体例

**✅ Good: 一時検証ファイルを temporary/ に配置**
```bash
# スクリプトのデバッグ中
python scripts/check_token_usage.py > tests/fixtures/temporary/debug_output.txt
```

**❌ Bad: プロジェクトルートに直接作成**
```bash
# これは避ける（ADR-0009違反）
python scripts/archive_conversation.py --output test_conversation.txt
```

**✅ Good: 回帰テスト用データを permanent/ に配置**
```bash
# 将来のテストで再利用するサンプルデータ
cp sample_agent.md tests/fixtures/permanent/
git add tests/fixtures/permanent/sample_agent.md
```

詳細: [`tests/README.md`](../tests/README.md)

---

## 🔍 トラブルシューティング

### Q1: Anthropic Claude API エラーが出る
**A**: 環境変数 `ANTHROPIC_API_KEY` を確認してください。

```bash
export ANTHROPIC_API_KEY=sk-ant-...
# または .env ファイルに記載
```

### Q2: 類似度が低い（< 0.86）
**A**: 以下を確認:
1. `i18n/glossary.yml` に用語が登録されているか
2. 翻訳プロンプト (`prompts/01_en_translate.txt`) が最新か
3. 原文（content/ja/AGENT.md）の構造が複雑すぎないか

### Q3: note記事のリンクが変換されない
**A**: `prepare_note_article.py` の変換パターンを確認:
```bash
# 未変換リンクの検出
grep -E '\[.*\]\([^h].*\.md' changelogs/note-archives/v4.1-note-complete.md
```

---

_Last Updated: 2025-10-13_
