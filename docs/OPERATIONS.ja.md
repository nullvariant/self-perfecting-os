# 運用ドキュメント（Operations Guide / JA）

本書は `AGENT.ja.md` / `AGENT.md` / `spec/` / `scripts/` 間の生成・検証フローと、今回追加された構造 (`persona_legend`, TOC スクリプト等) の役割を **実務運用者視点** で整理したものです。

---
## 0. 全体パイプライン概要

```
編集 (content/AGENT.ja.md)
  ↓ (必要なら) 目次自動再生成 scripts/gen_toc.py
  ↓ make gen  (build.py) : JA→EN 翻訳 + YAML仕様抽出
  ↓ make val  (review.py) : スキーマ検証 / 用語網羅 / 意味類似度 / 自己レビュー
  ↓ Git commit & push
```

| フェーズ | 主担当ファイル | 主目的 | 生成/更新される成果物 |
|----------|----------------|--------|------------------------|
| 編集 | `content/AGENT.ja.md` | ソース・オリジナル（日本語真実ソース） | （同ファイル上書き） |
| TOC再生成 | `scripts/gen_toc.py` | ⽬次・アンカー整合 | `content/AGENT.ja.md` 内目次ブロック更新 |
| 生成 | `scripts/build.py` | 英語版 & YAML 仕様抽出 (LLM) | `AGENT.md`, `spec/agent.spec.yaml` |
| 検証 | `scripts/review.py` | スキーマ整合 & 用語網羅 & 意味差分 | 標準出力（ログ） |
| スキーマ | `spec/agent.schema.json` | 仕様構造定義 (JSON Schema) | 参照されるのみ |
| 構造データ | `spec/agent.spec.yaml` | LLM抽出 or 手動整形後の構造化ビュー | 手動 / 自動更新 |
| 用語集 | `i18n/glossary.yml` | 用語 ID ↔ JA/EN マッピング | 翻訳・抽出補助 |

---
## 1. 各ファイル役割詳細

### 1.1 `content/AGENT.ja.md`
- 人間が直接編集する**唯一の真実ソース**。
- 3.x ポリシー要約（引用ブロック + アイコン）・Emoji Legend・Appendix 要約を含む。
- 目次 (TOC) は半自動：構造変更多い場合は `python scripts/gen_toc.py` 実行推奨。

### 1.2 `AGENT.md`
- 英語版（`build.py` により LLM 翻訳生成）。
- 手動編集は原則禁止（差分は次回生成で上書きされる）。

### 1.3 `spec/agent.schema.json`
- JSON Schema 2020-12 草案形式。
- `review.py` が YAML 出力 (`agent.spec.yaml`) をここで検証。
- 追加済みフィールド: `persona_legend`（絵文字凡例と Markdown の同期用）。
- `emoji` パターンに `"^\p{Emoji}+$"` を指定。バリデータ環境により失敗する場合はパターン削除で回避可。

### 1.4 `spec/agent.spec.yaml`
- `build.py` LLM 抽出結果を初期値として生成する構造化仕様。
- その後、手動での整形・追記（例: `persona_legend` 調整）を許可。
- バリデーション：`make val` 実行時に Schema + Glossary チェック。

### 1.5 `scripts/gen_toc.py`
- `AGENT.ja.md` の見出し (`##` / `###`) と既存 `<a id="...">` アンカーを走査し TOC ブロックを再生成。
- 既存アンカーを尊重し、無い場合はスラグ生成。
- 失敗時復旧容易なように1ファイル in-place 編集のみ。

### 1.6 `scripts/build.py`
- 機能①: Glossary アンカー埋め込み後、日本語本文 → 英語 Markdown 翻訳 (OpenAI Chat)。
- 機能②: 日本語本文 → YAML 仕様抽出 (LLM prompt `02_yaml_extract.txt`)。
- 出力: `AGENT.md`, `spec/agent.spec.yaml` 上書き。
- **注意:** OpenAI API キー・モデル指定が必要。

### 1.7 `scripts/review.py`
- ステップ: (1) JSON Schema 検証 (2) Glossary 用語網羅性チェック (3) 英文逆翻訳→日本語 & 意味類似度計算 (4) 自己レビュー (LLM) を一括。
- 類似度閾値は `0.86`（`sentence-transformers/all-MiniLM-L6-v2`）。
- `--strict` 指定時、自己レビュー内に `[CRITICAL]` などが含まれればプロセス失敗。

### 1.8 `i18n/glossary.yml`
- 用語正規化のソース。`build.py` / `review.py` 両方で参照。
- `terms:` 内 `personas` 特殊 ID はペルソナ列挙をループ展開。

### 1.9 `persona_legend` (Schema + YAML + Markdown)
| 要素 | 用途 | 更新トリガー | 反映対象 |
|------|------|-------------|----------|
| Markdown Emoji Legend 表 | 読者可視・記述的 | ペルソナ特性/説明変更 | `content/AGENT.ja.md` |
| `persona_legend` (YAML) | 機械可読マッピング | Legend 変更時 | `spec/agent.spec.yaml` |
| Schema 定義 | 一貫性強制 | フィールド構造変えたい時 | `agent.schema.json` |

同期規則（推奨フロー）:
1. まず `content/AGENT.ja.md` の Legend 表を編集
2. 対応する `spec/agent.spec.yaml` の `persona_legend` 要素を同じ順序で更新
3. `make val` で Schema + 用語整合チェック

---
## 2. 環境変数 & 前提

| 変数 | 必須 | 用途 | 例 |
|------|------|------|----|
| `OPENAI_API_KEY` | Yes | OpenAI Chat API 呼び出し | sk-... |
| `OPENAI_MODEL` | No | 既定 LLM モデル（省略時 gpt-4.1） | gpt-4.1-mini |

Python 依存（例）: openai, jsonschema, pyyaml, sentence-transformers, torch (埋め込みモデル自動で要求)。

---
## 3. 代表コマンド

(※ 既存 Makefile 前提)

```bash
# 英語版 + YAML 仕様 再生成
make gen

# スキーマ & 意味整合レビュー
make val

# 目次再生成（見出し構造を大きく改変した後など）
python scripts/gen_toc.py
```

---
## 4. 変更ワークフロー詳細

### 4.1 ポリシー文面更新
1. `content/AGENT.ja.md` を編集
2. 大見出し追加/削除したら `python scripts/gen_toc.py`
3. `make gen` → 英語/仕様再生成
4. `make val` で整合確認
5. 問題なければ commit/push

### 4.2 ペルソナ特性更新
1. Legend 表と本文（該当ペルソナ説明）修正
2. `spec/agent.spec.yaml` の `personas` および `persona_legend` を同期
3. Glossary に新語が必要なら `i18n/glossary.yml` 追加
4. `make gen`（必要なら）→ `make val`

### 4.3 スキーマ拡張（例: metrics追加）
1. `agent.schema.json` へ新プロパティ（例: `metrics`）追加
2. `spec/agent.spec.yaml` にサンプル値追加
3. `make val` でバリデーション通過確認
4. LLM 抽出側（必要なら prompt 改修）

---
## 5. トラブルシュート

| 症状 | 原因候補 | 対処 |
|------|----------|------|
| `jsonschema` バリデーション失敗 | Schema と YAML 不整合 | フィールド欠落/タイプ確認 |
| Emoji pattern エラー | ランタイムの正規表現実装差異 | `pattern` を一時削除 or 緩和 |
| 類似度閾値未達 | 翻訳乖離/大幅編集 | 日本語原文の再調整 or 英文差分確認 |
| Glossary missing 〜 | 用語表現ゆらぎ / Glossary 未追加 | `glossary.yml` に用語追加 or 日本語本文表記合わせ |
| LLM 応答空/失敗 | API Key 不正 / Rate limit | Key/残クレジット確認、リトライ |

---
## 6. 運用ベストプラクティス
- 大改変前に `main` 最新を pull → 差分最小化。
- ペルソナ表の列構造は固定（順序変更は diff ノイズ増）。
- 3.x 要約行は **1行厳守**（英語抽出時の安定性向上）。
- Appendix 要約は「抽象→価値宣言」型で簡潔に。
- Schema 変更は **後方互換性** ある形（新フィールド optional → その後 required 化）を推奨。

---
## 7. 将来拡張候補（メモ）
| 項目 | 概要 | 期待効果 |
|------|------|----------|
| metrics セクション | EBI/協調スコア式の構造化 | 自動可視化 / アラート化 |
| persona_interactions | 典型調停パターンの DSL 化 | 対話シミュレーション |
| build高速化 | 翻訳/抽出を diff ベース再生成 | LLMコスト削減 |
| review並列 | 埋め込み/LLM チェック並列化 | 時間短縮 |

---
## 8. Changelog 運用フロー

### 8.1 アップデート時の手順
AGENT.ja.md を更新する際は、以下の手順で Changelog も同時に管理します。

```bash
# 1. content/AGENT.ja.md を編集
# 2. 必要なら目次再生成
python scripts/gen_toc.py

# 3. CHANGELOG.md の [Unreleased] セクションに変更を記録
# 4. バージョン確定時は Unreleased → バージョン番号に変更

# 5. ビルドと検証
make gen  # 英訳 & YAML抽出
make val  # スキーマ検証

# 6. Git commit & push
git add CHANGELOG.md content/AGENT.ja.md AGENT.md spec/agent.spec.yaml
git commit -m "Release vX.X.X: [変更サマリー]"
git push origin main

# 7. note 記事作成（NOTE_SYNC_MANUAL.ja.md 参照）
```

### 8.2 バージョニングルール
本プロジェクトは [Semantic Versioning](https://semver.org/) を採用しています。

| 種類 | 形式 | 例 | 使用タイミング |
|------|------|----|----|
| **Major** | x.0.0 | 4.0.0 | アーキテクチャ変更、破壊的変更、ペルソナシステム再設計 |
| **Minor** | 4.x.0 | 4.1.0 | 新機能追加、大幅強化（感情辞書統合等） |
| **Patch** | 4.1.x | 4.1.1 | バグ修正、小改善、誤字脱字修正 |

### 8.3 CHANGELOG.md のカテゴリ
変更内容は以下のカテゴリで分類します：

- `Added`: 新機能・新セクション追加
- `Enhanced`: 既存機能の改善・拡張
- `Fixed`: バグ修正
- `Changed`: 仕様変更
- `Deprecated`: 非推奨化（将来削除予定）
- `Removed`: 削除
- `Security`: セキュリティ修正

### 8.4 関連ドキュメント
- [CHANGELOG.md](../CHANGELOG.md): 全バージョンの統合Changelog
- [PRD_CHANGELOG_MIGRATION.ja.md](PRD_CHANGELOG_MIGRATION.ja.md): Changelog分離運用のPRD
- [NOTE_SYNC_MANUAL.ja.md](NOTE_SYNC_MANUAL.ja.md): note同期マニュアル

---
## 9. 最小チェックリスト (PR 前)
- [ ] 目次崩れていない（必要なら TOC 再生成）
- [ ] `CHANGELOG.md` に変更を記録済み
- [ ] `make gen` で生成物更新済
- [ ] `make val` PASS（エラーなし / 類似度 >= 0.86）
- [ ] Legend ↔ persona_legend 同期
- [ ] 新語は `glossary.yml` 登録済

---
## 10. FAQ
**Q. 英語版だけ微修正したい** → 日本語原文を修正して再生成してください。直接英語編集は再生成で消えます。

**Q. persona_legend と personas の差異が出やすい** → `scripts` に将来的に同期チェック追加を検討（現状は手動）。

**Q. Similarity 0.84 など僅差失敗** → 意味が保持されているなら文章冗長部を戻すか、Glossary 固有語の揺れを減らすと改善することが多いです。

---
## 10. 連絡メモ
- OpenAI モデル変更時は `OPENAI_MODEL` を一時指定、差分品質を `make val` で観察。
- 外部API制限時は翻訳/抽出部分のみコメントアウトし、既存出力を使ってレビューのみ回すことも可能。

---
以上。疑問点があればこのファイルへ追記し運用知識を増やしていく方針を推奨します。
