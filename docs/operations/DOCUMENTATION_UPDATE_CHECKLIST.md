# ドキュメント更新チェックリスト

**用途**: プロジェクト構造・パス・API変更時に、影響を受けるドキュメントを網羅的に更新するためのガイド

---

## 📋 構造変更時のチェックリスト

### ステップ1: ADR作成

構造変更を決定したら、必ず最初にADRを作成:

```bash
python scripts/record_decision.py \
  --title "構造変更の内容" \
  --context "変更理由と影響範囲" \
  --category documentation
```

### ステップ2: 影響範囲の特定

以下のツールで影響を受けるファイルを洗い出し:

```bash
# 古いパス参照を検出
python scripts/check_path_references.py

# 特定のパターンを検索
grep -r "旧パス" . --include="*.md" --include="*.py"
```

### ステップ3: 優先度順に更新

#### 🔴 Tier 0: 最優先（SSOT）

**必ず手動で確認・更新**

- [ ] `content/ja/AGENT.md` - 日本語一次仕様書
- [ ] `content/ja/EmotionMood_Dictionary.md` - 感情辞書
- [ ] `docs/decisions/active/` - 新ADR作成
- [ ] `CHANGELOG.md` - `[Unreleased]` に記録
- [ ] `docs/governance/DOCUMENTATION_STRUCTURE.yml` - **構造変更時は必ず更新**

#### 🟡 Tier 1: 高優先度（状態管理）

**自動検出 → 手動で確認・更新**

- [ ] `docs/project-status.ja.md` - プロジェクト状況
- [ ] `.github/copilot-instructions.md` - AI向けガイド
- [ ] `README.md` - プロジェクト概要
- [ ] `CONTRIBUTING.md` - コントリビューターガイド
- [ ] **このチェックリスト自身** (`docs/operations/DOCUMENTATION_UPDATE_CHECKLIST.md`) - パターンや手順の更新

#### 🟢 Tier 2: 中優先度（プロセス・手順書）

**自動検出 → 選択的に更新**

- [ ] `docs/governance/*.md` - ドキュメント管理ルール
- [ ] `docs/operations/current/*.md` - 運用手順書
- [ ] `scripts/README.md` - スクリプト説明

#### ⚪ Tier 3: 低優先度（補助文書）

**自動修正でOK（確認のみ）**

- [ ] [nullvariant-atelier/changelogs/](https://github.com/nullvariant/nullvariant-atelier/tree/main/changelogs) - note記事原稿（ADR-0007により移行）
- [ ] `i18n/*.yml` - 翻訳辞書
- [ ] `spec/*.yaml` - 自動生成ファイル（CI稼働後は不要）

### ステップ4: 自動修正の実行

```bash
# 自動修正（対応パターンのみ）
python scripts/check_path_references.py --fix

# 結果を確認
git diff

# 問題なければコミット
git add -A
git commit -m "docs: Update path references after structural change"
```

### ステップ5: ドキュメント整合性チェック

```bash
# ADR番号連番チェック、ファイル存在確認
python scripts/validate_docs.py
```

### ステップ6: コミット＆プッシュ

```bash
git push origin feature/your-structural-change
```

---

## 🔍 典型的な構造変更パターン

### パターン1: ファイルパス変更

**例**: `content/AGENT.ja.md` → `content/ja/AGENT.md`

**チェック対象**:
- [ ] `.github/copilot-instructions.md` - サンプルコード内のパス
- [ ] `README.md` - 構造図・リンク
- [ ] `CONTRIBUTING.md` - ワークフロー例
- [ ] `docs/project-status.ja.md` - ファイル一覧
- [ ] `scripts/*.py` - ハードコードされたパス
- [ ] `scripts/README.md` - スクリプト説明

### パターン2: API変更

**例**: `ANTHROPIC_API_KEY` → `ANTHROPIC_API_KEY`

**チェック対象**:
- [ ] `README.md` - セットアップ手順
- [ ] `CONTRIBUTING.md` - CI/CD設定
- [ ] `scripts/build.py` - 環境変数参照
- [ ] `scripts/README.md` - 環境変数説明
- [ ] `.github/workflows/*.yml` - Secrets設定（将来）

### パターン3: ディレクトリ構造変更

**例**: `docs/` 配下の再編成、`tests/` ディレクトリの追加

**チェック対象**:
- [ ] `README.md` - ディレクトリ構造図
- [ ] `.github/copilot-instructions.md` - 構造説明
- [ ] `CONTRIBUTING.md` - コントリビューターガイド
- [ ] `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 階層定義
- [ ] `docs/governance/HIERARCHY_RULES.md` - 階層ルール
- [ ] `scripts/README.md` - スクリプト説明（テストファイル配置ルールなど）
- [ ] 全ての相対リンク（`grep -r "\.\./docs/" .`）

**tests/ディレクトリ追加時の追加チェック**（ADR-0009）:
- [ ] `.github/copilot-instructions.md` - テストファイル配置ルール追加
- [ ] `README.md` - tests/構造図追加
- [ ] `CONTRIBUTING.md` - tests/構造図追加
- [ ] `scripts/README.md` - テストファイル配置ルール追加
- [ ] `tests/README.md` - 配置ガイド作成
- [ ] `.gitignore` - tests/fixtures/temporary/ 追加

### パターン4: ドキュメント廃止

**例**: `docs/project-status.ja.md` の廃止

**チェック対象**:
- [ ] リンクを張っている全ファイル（`grep -r "docs/project-status.ja.md" .`）
- [ ] 新しい移行先を明記（例: `docs/project-status.ja.md`）
- [ ] ADRに廃止理由を記録

---

## 🤖 自動化ツールの活用

### 1. check_path_references.py

**用途**: 古いパス参照の検出＆自動修正

**実行**:
```bash
# 検出のみ
python scripts/check_path_references.py

# 自動修正
python scripts/check_path_references.py --fix
```

**対応パターン**:
- 多言語移行（`content/AGENT.ja.md` → `content/ja/AGENT.md`）
- API変更（`OPENAI_API_KEY` → `ANTHROPIC_API_KEY`）
- 廃止ファイル（`MIGRATION_STATUS.md` → `docs/project-status.ja.md`）
- changelogs移行（`changelogs/` → `../nullvariant-atelier/changelogs/`、ADR-0007）

**除外対象**:
- `docs/decisions/` - ADRは履歴として古いパスを保持
- `nullvariant-atelier/changelogs/note-archives/` - 公開済み記事は履歴として保持
- `.github/workflows/` - CI設定は手動更新

**パターン辞書の更新**:
新しい廃止パターンが発生した場合、`scripts/check_path_references.py`の`DEPRECATED_PATTERNS`辞書を更新:

```python
DEPRECATED_PATTERNS = {
    r'旧パターン': '新パターン',
    # 新しいパターンを追加
}
```

更新後、このチェックリストにも記載すること。

### 2. validate_docs.py

**用途**: ドキュメント整合性チェック

**実行**:
```bash
python scripts/validate_docs.py
```

**チェック内容**:
- ADR番号の連番確認
- ファイル存在確認
- 最終更新日チェック

### 3. grep_search（パターン検索）

**用途**: 特定のパターンを含むファイルを検索

**例**:
```bash
# Markdown内の特定パスを検索
grep -r "content/ja/AGENT.md" . --include="*.md"

# Python内の特定APIキーを検索
grep -r "ANTHROPIC_API_KEY" . --include="*.py"

# 相対リンクの検索
grep -r "\.\./content/" . --include="*.md"
```

---

## 📝 更新忘れを防ぐベストプラクティス

### 1. ADRに「影響を受けるファイル」セクションを必ず含める

```markdown
## 影響を受けるファイル

- [ ] .github/copilot-instructions.md
- [ ] README.md
- [ ] CONTRIBUTING.md
- [ ] docs/project-status.ja.md
- [ ] scripts/*.py
```

### 2. PRテンプレートに「ドキュメント更新チェック」を含める

```markdown
## ドキュメント更新

- [ ] `python scripts/check_path_references.py` を実行
- [ ] 影響を受けるドキュメントを更新
- [ ] `python scripts/validate_docs.py` を実行
```

### 3. 定期的な全体チェック

月次で以下を実行:

```bash
# 古いパス参照の検出
python scripts/check_path_references.py

# ドキュメント整合性チェック
python scripts/validate_docs.py

# リンク切れチェック（将来実装）
# python scripts/check_broken_links.py
```

---

## 🔗 関連ドキュメント

- [docs/governance/AI_GUIDELINES.md](../governance/AI_GUIDELINES.md) - AI向けドキュメント記録ガイドライン
- [docs/governance/DOCUMENTATION_STRUCTURE.yml](../governance/DOCUMENTATION_STRUCTURE.yml) - ドキュメント階層定義
- [scripts/check_path_references.py](../../scripts/check_path_references.py) - パス参照チェックツール
- [scripts/validate_docs.py](../../scripts/validate_docs.py) - ドキュメント整合性チェック

---

**Last Updated**: 2025-10-28  
**Version**: 1.0.0
