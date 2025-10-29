# ドキュメント階層ルール（人間向け説明）

**対象**: nullvariant (human) および将来の人間の貢献者  
**バージョン**: 1.0.0  
**最終更新**: 2025-10-28

---

## 🎯 このドキュメントの目的

Null;Variant プロジェクトにおける「どこに何を書くか」を明確に定義し、**ドキュメント迷子**を防ぎます。

### 背景

以前は以下の問題がありました：

- ❌ AI環境（Claude Code, GitHub Copilot, Chat UI）を跨ぐと文脈が途切れる
- ❌ 「ドキュメントを残す」指示が曖昧で、記録場所が不統一
- ❌ 既存ドキュメントが散在し、Single Source of Truth (SSOT) が不明確
- ❌ CI/CD停止などの重要な決定が記録されず、矛盾が蓄積

### 解決策

**ADR (Architecture Decision Records)** を導入し、全ての重要な決定を時系列で記録します。

---

## 📊 ドキュメント階層の全体像

```
nullvariant/
├── docs/
│   ├── decisions/              # 🏆 Tier 0: SSOT（最重要）
│   │   ├── active/2025/10/
│   │   │   ├── 20251028_0001_ci-cd-pause_architecture.md
│   │   │   ├── 20251028_0002_naming-structure_documentation.md
│   │   │   └── ...
│   │   ├── INDEX.md            # ⚠️ 自動生成（編集禁止）ADR全体の索引
│   │   ├── deprecated/         # 非推奨ADR
│   │   ├── superseded/         # 上書きされたADR
│   │   ├── 0000_template.md    # ADRテンプレート
│   │   └── README.md
│   ├── governance/             # 🏛️ ガバナンス定義
│   │   ├── INDEX.md                    # ⚠️ 自動生成（編集禁止）参考資料一覧
│   │   ├── DOCUMENTATION_STRUCTURE.yml  # 機械可読
│   │   ├── HIERARCHY_RULES.md          # 人間向け（本文書）
│   │   ├── AI_GUIDELINES.md            # AI向け
│   │   └── NAMING_DECISION_SUMMARY.md  # 命名規則サマリー
│   ├── operations/             # 📋 Tier 2: 手順書
│   │   ├── INDEX.md            # ⚠️ 自動生成（編集禁止）current + archive 索引
│   │   ├── current/
│   │   │   ├── 20251028_OPERATIONS.ja.md
│   │   │   ├── 20251028_WORKFLOW_TEXT_ASSETS.ja.md
│   │   │   └── ...
│   │   └── archive/2025/10/
│   │       └── ...
│   ├── prd/                    # 💡 Tier 3: 要件定義
│   │   ├── INDEX.md            # ⚠️ 自動生成（編集禁止）PRD全体の索引
│   │   ├── active/
│   │   └── implemented/
│   ├── log/                    # � Tier 4.5: 作業ログ記録
│   │   ├── 2025/10/
│   │   │   └── *.md            # YYYYMMDD_{slug}.md
│   │   └── README.md
│   ├── project-status.ja.md    # 📊 Tier 1: 状態管理
│   └── README.md               # docs/ ガイド
├── content/                     # 🏆 Tier 0: 一次情報
│   ├── ja/
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   └── en/                      # CI自動生成
│       ├── AGENT.md
│       └── EmotionMood_Dictionary.md
├── CHANGELOG.md                 # 📊 Tier 1: 履歴
├── AGENT.md                     # ⚠️ 自動生成（編集禁止）
├── spec/
│   ├── agent.schema.json
│   └── agent.spec.yaml          # ⚠️ 自動生成（編集禁止）
└── .github/
    └── workflows/
        └── pr-guard.yml         # CI/CD 整合性チェック
```

---

## 🏆 Tier 0: Single Source of Truth (SSOT)

### 役割
AI/人間が**最初に参照すべき真実**。ここが間違っていたら全てが崩壊する。

### 配置場所
- `docs/decisions/` - ADR（全ての重要な決定）
- `content/` - 仕様書・辞書（日本語一次情報）

### 更新頻度
**重要な決定時のみ**（高い検討コストを要する）

### ファイル一覧

| ファイル | 目的 | 編集可否 | 備考 |
|---------|------|---------|------|
| `docs/decisions/active/{YYYY}/{MM}/*.md` | 決定記録 | ✅ | 新規ADRは追加のみ（既存は編集禁止） |
| `content/ja/AGENT.md` | 仕様書（日本語） | ✅ | 自動生成の source ファイル |
| `content/ja/EmotionMood_Dictionary.md` | 感情辞書 | ✅ | 感情定義変更時のみ |
| `AGENT.md` | 仕様書（英語） | ❌ | CI/CDが自動生成 |
| `spec/agent.spec.yaml` | YAML仕様 | ❌ | CI/CDが自動生成 |

### ルール

1. **ADRは追記のみ、削除・編集禁止**
   - 古くなった決定は Status を `Deprecated` に変更
   - 新しい決定で上書きする場合は、新ADRを作成し Related に旧番号を記載

2. **自動生成ファイルは絶対に直接編集しない**
   - `AGENT.md` と `spec/agent.spec.yaml` は CI/CD が生成
   - 編集したい場合は `content/ja/AGENT.md` を変更

3. **仕様書の変更は慎重に**
   - `content/ja/AGENT.md` の変更は ADR に記録
   - 破壊的変更は `CHANGELOG.md` にも記載

---

## 📊 Tier 1: 状態管理

### 役割
プロジェクトの**現在の状態**を反映。週次 or 重要な状態変化時に更新。

### 配置場所
- ルートレベル（`CHANGELOG.md`）
- `docs/`（`project-status.ja.md`）

### 更新頻度
**週次 or 重要な状態変化時**

### ファイル一覧

| ファイル | 目的 | 更新タイミング | 必須メタデータ |
|---------|------|--------------|-------------|
| `docs/project-status.ja.md` | 現在の状態・優先度 | 週次 or 大きな変化時 | 最終更新日、次回更新予定日 |
| `CHANGELOG.md` | バージョン履歴 | リリース時 or Unreleased追記 | - |

### ルール

1. **project-status.ja.md には最終更新日を必ず記載**
   - 7日以上更新がない場合、`scripts/validate_docs.py` が警告
   - フォーマット: `**最終更新**: 2025-10-28`

2. **CHANGELOG.md は Keep a Changelog 形式に従う**
   - リリース前は `[Unreleased]` セクションに追記
   - リリース時に `[X.X.X] - YYYY-MM-DD` に変更

3. **一時的な状態変化は project-status.ja.md に記録**
   - 例: CI/CD停止中、移行作業進行中、レビュー待ち
   - 恒久的な決定は ADR に記録

---

## 📋 Tier 2: プロセス・手順書

### 役割
**運用・実行手順**の記録。プロセス変更時に更新。

### 配置場所
- `docs/operations/`

### 更新頻度
**プロセス変更時**（高頻度ではない）

### ファイル一覧

| ファイル | 目的 | ADR必要 | 備考 |
|---------|------|---------|------|
| `docs/operations/current/{YYYYMMDD}_{type}.ja.md` | 運用手順書（最新版） | ✅ | 例: `20251028_OPERATIONS.ja.md` |
| 過去版は `docs/operations/archive/{YYYY}/{MM}/` へ移動 | 手順書の履歴管理 | - | ADR の新実装に準ずる |

### ルール

1. **プロセス変更は ADR が必要**
   - 例: リリースフローの変更、レビュープロセスの変更
   - ADR に変更理由と影響を記録

2. **手順書は具体的に**
   - コマンド例を含める
   - 実行結果の期待値を明示

3. **古い手順は削除せず、アーカイブ**
   - `docs/operations/archive/{YYYY}/{MM}/` に移動
   - ADR に「なぜ変更したか」を記録

---

## 💡 Tier 3: 設計文書（PRD）

### 役割
**機能開発・改善の要件定義**。機能開発時に作成・更新。

### 配置場所
- `docs/` (または将来的に `docs/plans/`)

### 更新頻度
**機能開発時**（不定期）

### ファイル一覧

| ファイル | 目的 | ADR必要 | 備考 |
|---------|------|---------|------|
| `docs/prd/active/{YYYYMMDD}_{slug}.ja.md` | 各機能のPRD（実装前） | ❌ | 例: `20251028_changelog-migration.ja.md` |
| 実装完了後は `docs/prd/implemented/` へ移動 | PRDの履歴管理 | - | 将来参照用 |

### ルール

1. **PRD自体は ADR 不要**
   - PRDは「これから実装する機能」の要件定義
   - 実装完了後、重要な決定があれば ADR に記録

2. **PRDのステータス管理**
   - Draft → Review → Approved → Implemented
   - Implemented 後は `docs/prd/implemented/` に移動

3. **実装状況を project-status.ja.md に記録**
   - 各PRDの進捗状況を可視化

---

## 📝 Tier 4: 一時的文書（廃止・Tier 4.5 に統合）

> 💡 **注記**: 従来の Tier 4（ルートレベル一時文書）は、Tier 4.5（`docs/log/`）に統合されました。詳細は [Tier 4.5](#tier-45-ログ記録作業の時系列記録) を参照してください。

### ルール（レガシー）

1. **完了後は必ずアーカイブ**
   - `docs/operations/archive/{YYYY}/{MM}/` に移動
   - ファイル名を `YYYYMMDD_original-name.md` にリネーム

2. **恒久的な決定は ADR に抽出**
   - 一時文書から重要な決定を ADR に転記
   - ADR の Related に一時文書へのリンクを記載

3. **長期化する場合は Tier 1 に昇格**
   - 1ヶ月以上続く場合は `project-status.ja.md` に統合検討

---

## 📝 Tier 4.5: ログ記録（作業の時系列記録）

### 役割
**ガバナンス監査・品質レビュー・デバッグログなど、作業の時系列記録**。参照対象ではなく、単なる「記録」。

### 配置場所
- `docs/log/{YYYY}/{MM}/`

### 更新頻度
**適宜**（作業内容に応じて）

### ファイル一覧

| ファイル | 目的 | ステータス管理 | 備考 |
|---------|------|--------------|------|
| `docs/log/2025/10/20251029_governance-self-review.md` | ガバナンス監査レポート | ❌ なし | 月別フォルダで時系列管理 |
| `docs/log/2025/10/20251030_quality-check-log.md` | 品質チェック結果 | ❌ なし | 任意のスラッグ名可 |
| `docs/log/2025/11/20251105_performance-test-report.md` | パフォーマンステスト結果 | ❌ なし | YYYYMMDD_{slug}.md 形式 |

### ルール

1. **参照対象ではなく、単なる「記録」**
   - これらのログから情報を抽出する場合は、ADR や project-status.ja.md に記録
   - ログ自体は grep や ls で検索可能（INDEX.md 不要）

2. **ステータス管理（active/deprecated）は不要**
   - 時系列記録なので、すべてのログが保存対象
   - 削除ポリシーなし（永続保存）

3. **月別フォルダで時系列整理**
   - `docs/log/{YYYY}/{MM}/` の構造で自動管理
   - 過去のログは grep で検索可能

4. **命名規則: YYYYMMDD_{slug}.md**
   - 例: `20251029_governance-self-review.md`
   - ハイフン使用（urlフレンドリー）

---

## 🚫 自動生成ファイル（編集禁止）

### 役割
CI/CD または scripts が自動生成するファイル。**絶対に直接編集しない**。

### ファイル一覧

| ファイル | Source | 生成タイミング | 備考 |
|---------|--------|--------------|------|
| `AGENT.md` | `content/ja/AGENT.md` | CI実行時 | 英語版仕様書 |
| `spec/agent.spec.yaml` | `content/ja/AGENT.md` | CI実行時 | YAML構造化仕様 |
| `docs/decisions/INDEX.md` | scripts/generate_index.py | 手動実行 | ADR索引 |
| `docs/governance/INDEX.md` | scripts/generate_index.py | 手動実行 | ガバナンス索引 |
| `docs/operations/INDEX.md` | scripts/generate_index.py | 手動実行 | 運用手順索引 |
| `docs/prd/INDEX.md` | scripts/generate_index.py | 手動実行 | PRD索引 |

### ルール

1. **編集したい場合は Source を変更**
   - `content/ja/AGENT.md` を編集 → CI が自動的に `AGENT.md` と `spec/agent.spec.yaml` を生成
   - INDEX.md の内容を修正したい → `scripts/generate_index.py` を修正してから再生成

2. **INDEX.md の再生成方法**
   ```bash
   python scripts/generate_index.py --target [adr|prd|operations|governance|all]
   ```

3. **自動生成ファイルへの直接編集を検出**
   - `scripts/validate_docs.py` が検出
   - Git Hooks でも警告（将来的に検討）

---

## 🔄 ワークフロー例

### 例1: API変更の記録

```bash
# 1. ADR作成
python scripts/record_decision.py \
  --title "Claude API レート制限対応" \
  --context "レート制限が判明したため、CI/CDを一時停止" \
  --author "Claude Code"

# 2. ADRを編集（Status を Accepted に変更）
vim docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md

# 3. 関連ドキュメントを更新
vim docs/project-status.ja.md  # 現在の状態を記録
vim CHANGELOG.md               # [Unreleased] に追記（必要なら）

# 4. コミット
git add docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md \
        docs/project-status.ja.md \
        CHANGELOG.md
git commit -m "docs: Add ADR-0001 for CI/CD pause decision"
git push origin main
```

### 例2: 手順書の変更

```bash
# 1. ADR作成（プロセス変更は重要な決定）
python scripts/record_decision.py \
  --title "note公開手順の簡略化" \
  --context "手動コピペが多く、ミスが発生しやすいため自動化" \
  --author "human"

# 2. 手順書を更新
vim docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md

# 3. 古い手順をアーカイブ
mkdir -p docs/operations/archive/2025/10
git mv docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md \
       docs/operations/archive/2025/10/20251028_NOTE_SYNC_MANUAL.ja.md

# 4. 新しい手順を作成
vim docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md

# 5. コミット
git add docs/decisions/active/2025/10/*.md \
        docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md \
        docs/operations/archive/2025/10/20251028_NOTE_SYNC_MANUAL.ja.md
git commit -m "docs: Simplify note publishing workflow (ADR-XXXX)"
git push origin main
```

### 例3: 一時的な状態変化の記録

```bash
# 1. project-status.ja.md を編集
vim docs/project-status.ja.md

# 内容:
# **CI/CD Status**: 一時停止中（API移行作業中）
# **最終更新**: 2025-10-28
# **次回更新予定**: 2025-11-04

# 2. コミット（ADR不要）
git add docs/project-status.ja.md
git commit -m "docs: Update CI/CD status to paused"
git push origin main
```

---

## 🎓 ベストプラクティス

### ✅ 推奨

1. **迷ったら ADR を作成**
   - 重要性の判断が難しい場合は、とりあえず ADR を作成
   - 後で Deprecated にすることも可能

2. **定期的な棚卸し**
   - 月次で `docs/project-status.ja.md` を更新
   - 古い ADR の Status を見直し

3. **関連ドキュメントへのリンクを明記**
   - ADR に関連ファイル・Issue・Commitを記載
   - トレーサビリティを確保

4. **簡潔かつ明確に**
   - 後から読む人（AI含む）のために書く
   - 冗長な説明は避け、要点を明確に

### ❌ 避けるべき

1. **ADRの削除**
   - 削除せず、Status を `Deprecated` に変更

2. **ドキュメント間の矛盾の放置**
   - 矛盾を発見したら、必ず ADR で解決

3. **勝手なディレクトリ構造の変更**
   - 変更する場合は ADR が必要

4. **自動生成ファイルの直接編集**
   - 絶対に禁止

---

## 📚 関連ドキュメント

- [docs/governance/DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml) - 機械可読形式の定義
- [docs/governance/AI_GUIDELINES.md](AI_GUIDELINES.md) - AI向けガイドライン
- [docs/prd/active/20251028_documentation-governance.ja.md](../prd/active/20251028_documentation-governance.ja.md) - 本ガバナンス体系のPRD
- [Architecture Decision Records (ADR)](https://adr.github.io/) - ADR公式サイト

---

## 🔄 次のステップ

1. [ ] 本ドキュメントをレビュー
2. [ ] Phase 1 の成果物を作成（ADRテンプレート等）
3. [ ] 既存ドキュメントの棚卸し（Phase 2）

---

**最終更新**: 2025-10-29  
**次回レビュー**: 2025-11-28  
**バージョン**: 1.1.0

---

## 📚 更新履歴

| バージョン | 日付 | 変更内容 |
|-----------|------|---------|
| 1.1.0 | 2025-10-29 | log/ ディレクトリ追加、Tier 4.5 新規定義、INDEX.md 各種追加対応 |
| 1.0.0 | 2025-10-28 | 初版公開 |
