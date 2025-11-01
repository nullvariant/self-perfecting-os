# Contributing to Self-Perfecting OS

Self-Perfecting OSへのコントリビューションをありがとうございます!

> **📊 プロジェクト状況**: このプロジェクトは一部メンテナンスが追いついていない領域があります。  
> 現在のメンテナンス優先度と今後の方向性については **[docs/project-status.ja.md](docs/project-status.ja.md)** を参照してください。

## 📋 基本方針

- **編集対象**: `content/ja/AGENT.md`（日本語一次情報）のみ
- **自動生成**: CI が `content/en/AGENT.md`（英語）、`AGENT.md`（ルートエントリポイント）、`spec/agent.spec.yaml` を生成（**⚠️ 現在未稼働**）
- **Changelog**: 全ての変更は `CHANGELOG.md` に記録
- **現状**: 
  - ✅ `content/ja/`、`docs/decisions/`、`docs/governance/` は積極的に更新中
  - ✅ note記事原稿は [nullvariant-atelier](https://github.com/nullvariant/nullvariant-atelier/tree/main/changelogs) で管理（ADR-0007）
  - ⚠️ `docs/operations/`配下は整備中
  - ❌ CI/CDパイプラインは未稼働（Claude Sonnet 4.5評価中）

---

## 🚀 クイックスタート

### 1. ローカル環境構築

```bash
# リポジトリクローン
git clone https://github.com/nullvariant/nullvariant.git
cd nullvariant

# Python環境構築
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Anthropic API キー設定
export ANTHROPIC_API_KEY=sk-ant-...

# Git Hooks のインストール（推奨）
bash scripts/install-hooks.sh
# → INDEX.md の自動再生成が有効になります（ADR-0015）
# → docs/decisions/, docs/prd/, docs/operations/, docs/governance/ の変更時に自動実行
```

### 2. 編集フロー

> **⚠️ 注意**: 現在CI/CDパイプラインが未稼働のため、以下のステップ4は実行不要です。

```bash
# 1. AGENT.md を編集（日本語）
vim content/ja/AGENT.md

# 2. 目次再生成（必要な場合）
python scripts/gen_toc.py content/ja/AGENT.md

# 3. CHANGELOG.md 更新
vim CHANGELOG.md  # [Unreleased] セクションに変更を記録

# 4. (現在スキップ) ビルド＆検証
# make gen  # 多言語翻訳＆YAML生成 (Claude API設定後に実施予定)
# make val  # 類似度検証 (CI稼働後に実施予定)

# 5. Commit & Push
git add CHANGELOG.md content/ja/AGENT.md
# ⚠️ CI未稼働のため content/en/, AGENT.md, spec/ は現時点でコミット不要
git commit -m "feat: [変更内容の簡潔な説明]"
git push origin feature/your-feature-name
```

### 3. Pull Request

> **⚠️ 注意**: 現在CI/CDが未稼働のため、自動チェックは実行されません。

- 変更内容を説明
- ~~`make val` が PASS していることを確認~~ (CI稼働後に実施)
- ~~CI チェック（pr-guard.yml）が通過することを確認~~ (CI稼働後に実施)

---

## 📝 Changelog 運用

### バージョニング

本プロジェクトは [Semantic Versioning](https://semver.org/) を採用:

| 種類 | 形式 | 例 | 使用タイミング |
|------|------|----|----|
| **Major** | x.0.0 | 4.0.0 | 破壊的変更、アーキテクチャ再設計 |
| **Minor** | 4.x.0 | 4.1.0 | 新機能追加、大幅強化 |
| **Patch** | 4.1.x | 4.1.1 | バグ修正、小改善、誤字修正 |

### Changelogカテゴリ

変更内容は以下のカテゴリで分類:

- `Added`: 新機能・新セクション追加
- `Enhanced`: 既存機能の改善・拡張
- `Fixed`: バグ修正
- `Changed`: 仕様変更
- `Deprecated`: 非推奨化（将来削除予定）
- `Removed`: 削除
- `Security`: セキュリティ修正

### Changelog記載例

```markdown
## [Unreleased]

### Added
- **Section 6.4**: 新しい感情測定メカニズム
  - 詳細な説明...

### Enhanced
- **Section 2.1**: ペルソナシステムの精密化
  - 改善内容...

### Fixed
- Section 4.3の誤字修正
```

---

## 🔧 開発ツール

### スクリプト

| スクリプト | 用途 | コマンド |
|----------|------|---------|
| `build.py` | 多言語翻訳＆YAML生成 | `make gen` |
| `review.py` | 類似度検証 | `make val` |
| `gen_toc.py` | 目次生成 | `python scripts/gen_toc.py content/ja/AGENT.md` |
| `prepare_note_article.py` | note記事生成 | `python scripts/prepare_note_article.py` |
| `record_decision.py` | ADR作成支援 | `python scripts/record_decision.py --title "..." --context "..." --category <category>` |
| `generate_index.py` | INDEX.md自動生成 | `python scripts/generate_index.py` |
| `validate_docs.py` | ドキュメント整合性チェック | `python scripts/validate_docs.py` |

詳細: [`scripts/README.md`](scripts/README.md)

### Makefile コマンド

```bash
make gen   # build.py 実行（英訳＆YAML生成）
make val   # review.py 実行（類似度検証）
```

---

## 🌐 GitHub Actions

### build.yml（現在は `build.yml.disabled` として一時停止中）
- **トリガー**: `content/ja/AGENT.md` への push
- **処理**: 多言語翻訳＆YAML生成 → 自動commit
- **出力**: `content/en/*.md`, `AGENT.md`, `spec/agent.spec.yaml`
- **補足**: 2025-10-30 時点では Anthropic Tier 1 制限に到達し予想外のトークンコストが発生したため、自動実行を避ける目的でファイル名を `.disabled` に変更しています（コスト対策と運用方針が固まり次第、元の名称へ戻す想定）

### pr-guard.yml
- **トリガー**: Pull Request作成時
- **処理**: 
  - 類似度検証（>= 0.86）
  - スキーマ検証
  - Legend同期チェック

### validate-docs.yml (✅ 稼働中)
- **トリガー**: Pull Request作成時
- **処理**:
  - ADR番号連番チェック
  - ファイル存在確認
  - 更新日チェック

### 必要なSecrets
- `ANTHROPIC_API_KEY`: Anthropic Claude API キー（予定）

---

## 📂 リポジトリ構成

```
nullvariant/
├── content/
│   ├── ja/                       # 🇯🇵 編集対象（日本語一次情報）
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   ├── en/                       # 🇬🇧 CI自動生成（編集禁止）
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   └── README.md                 # 多言語管理の設計思想
├── AGENT.md                      # 🇬🇧 英語版エントリポイント（CI自動生成）
├── CHANGELOG.md                  # 📋 バージョン履歴
├── spec/
│   ├── agent.spec.yaml          # CI自動生成
│   └── agent.schema.json
├── docs/
│   ├── decisions/               # 🏆 ADR（全ての重要な決定）
│   │   ├── active/2025/10/     # 現在有効な決定（月別）
│   │   ├── deprecated/         # 非推奨
│   │   ├── superseded/         # 上書きされた決定
│   │   ├── INDEX.md            # 自動生成索引
│   │   └── README.md
│   ├── governance/             # 🏛️ ドキュメント管理ルール
│   │   ├── AI_GUIDELINES.md
│   │   ├── DOCUMENTATION_STRUCTURE.yml
│   │   ├── HIERARCHY_RULES.md
│   │   └── README.md
│   ├── prd/                    # 💡 要件定義
│   ├── operations/             # 📋 運用手順書
│   ├── project-status.ja.md    # 📊 プロジェクト状況・メンテナンス優先度
│   └── README.md
├── scripts/
│   ├── build.py                # 多言語翻訳＆YAML生成
│   ├── gen_toc.py              # 目次自動生成
│   ├── prepare_note_article.py # note記事自動生成（出力先: nullvariant-atelier）
│   ├── review.py               # 類似度検証
│   ├── record_decision.py      # ADR作成支援
│   ├── archive_conversation.py # 対話ログ保存（nullvariant-atelier）
│   ├── check_token_usage.py    # トークン使用量監視
│   ├── generate_index.py       # INDEX.md自動生成
│   ├── validate_docs.py        # ドキュメント整合性チェック
│   └── prompts/                # LLMプロンプトテンプレート
├── tests/                      # 🧪 テストファイル管理（ADR-0009）
│   ├── README.md               # テストファイル配置ガイド
│   └── fixtures/
│       ├── permanent/          # Git管理（単体テスト用・回帰テスト用）
│       └── temporary/          # .gitignore（一時的な動作確認用）
├── i18n/
│   ├── glossary.yml            # 用語固定辞書
│   └── style/                  # スタイルガイド（日英）
└── .github/
    └── workflows/
        ├── build.yml.disabled  # 多言語翻訳（Anthropic Tier 1 制限・コスト対策のため一時退避）
        ├── pr-guard.yml        # PR検証（未稼働）
        └── validate-docs.yml   # ドキュメント整合性チェック（✅ 稼働中）
```

---

## ✅ Pull Request チェックリスト

> **⚠️ CI未稼働**: 現在は以下の簡易版チェックリストを使用してください。

### 現在のチェックリスト（Phase 0）

#### 編集前
- [ ] `content/ja/AGENT.md` のみを編集対象としている
- [ ] `CHANGELOG.md` の `[Unreleased]` セクションに変更を記録
- [ ] 重要な決定は ADR として記録する（`python scripts/record_decision.py`）

#### 編集後
- [ ] 目次が正しく更新されている（必要な場合: `python scripts/gen_toc.py content/ja/AGENT.md`）
- [ ] マークダウンの構文が正しい（プレビューで確認）
- [ ] ドキュメント整合性チェックが通る（`python scripts/validate_docs.py`）

#### PR作成時
- [ ] PR説明に変更内容を明記
- [ ] コミットメッセージが明確

### 将来のチェックリスト（CI稼働後）

以下は現在実行不要です:

- ~~[ ] `make gen` 実行済み（`AGENT.md`, `agent.spec.yaml` 更新）~~
- ~~[ ] `make val` PASS（類似度 >= 0.86）~~
- ~~[ ] 新語は `i18n/glossary.yml` に登録済み~~
- ~~[ ] CI チェックが全て通過~~

---

## 🔗 関連ドキュメント

- [docs/project-status.ja.md](docs/project-status.ja.md): **📊 プロジェクト状況・メンテナンス優先度**
- [docs/decisions/](docs/decisions/): ADR（意思決定記録）
- [docs/governance/](docs/governance/): ドキュメント管理ルール
- [content/README.md](content/README.md): 多言語コンテンツ管理
- [nullvariant-atelier/changelogs/](https://github.com/nullvariant/nullvariant-atelier/tree/main/changelogs): note記事原稿管理（ADR-0007により移行）

---

## 💡 Tips

### 類似度が低い場合
1. `i18n/glossary.yml` に用語を追加
2. プロンプト (`scripts/prompts/01_en_translate.txt`) を調整
3. 原文の構造を簡潔に

### 新しいセクション追加時
1. `content/ja/AGENT.md` に追加
2. 目次を再生成: `python scripts/gen_toc.py content/ja/AGENT.md`
3. CHANGELOG.md の `Added` カテゴリに記載

---

## 📧 サポート

質問や提案がある場合:
- **Issues**: GitHub Issues で報告
- **Discussions**: 議論や質問

---

_Thank you for contributing to Self-Perfecting OS!_
