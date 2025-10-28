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
│   ├── DECISIONS/              # 🏆 Tier 0: SSOT（最重要）
│   │   ├── 0000-adr-template.md
│   │   ├── 0001-ci-cd-pause.md
│   │   └── README.md
│   ├── GOVERNANCE/             # 🏛️ ガバナンス定義
│   │   ├── DOCUMENTATION_STRUCTURE.yml  # 機械可読
│   │   ├── AI_GUIDELINES.md            # AI向け
│   │   └── HIERARCHY_RULES.md          # 人間向け（本文書）
│   ├── operations/             # 📋 Tier 2: 手順書
│   │   ├── OPERATIONS.ja.md
│   │   └── NOTE_SYNC_MANUAL.ja.md
│   ├── PRD_*.md                # 💡 Tier 3: 要件定義
│   ├── project-status.ja.md    # 📊 Tier 1: 状態管理
│   └── archive/                # 🗄️ アーカイブ
│       ├── deprecated/         # 非推奨ドキュメント
│       └── completed/          # 完了した一時文書
├── content/                     # 🏆 Tier 0: 一次情報
│   ├── AGENT.ja.md
│   └── EmotionMood_Dictionary.ja.md
├── CHANGELOG.md                 # 📊 Tier 1: 履歴
└── MIGRATION_STATUS.md          # 📝 Tier 4: 一時文書
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
| `docs/decisions/ADR-*.md` | 決定記録 | ✅ | 新規ADRは追加のみ（既存は編集禁止） |
| `content/AGENT.ja.md` | 仕様書（日本語） | ✅ | 自動生成の source ファイル |
| `content/EmotionMood_Dictionary.ja.md` | 感情辞書 | ✅ | 感情定義変更時のみ |
| `AGENT.md` | 仕様書（英語） | ❌ | CI/CDが自動生成 |
| `spec/agent.spec.yaml` | YAML仕様 | ❌ | CI/CDが自動生成 |

### ルール

1. **ADRは追記のみ、削除・編集禁止**
   - 古くなった決定は Status を `Deprecated` に変更
   - 新しい決定で上書きする場合は、新ADRを作成し Related に旧番号を記載

2. **自動生成ファイルは絶対に直接編集しない**
   - `AGENT.md` と `spec/agent.spec.yaml` は CI/CD が生成
   - 編集したい場合は `content/AGENT.ja.md` を変更

3. **仕様書の変更は慎重に**
   - `content/AGENT.ja.md` の変更は ADR に記録
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
| `docs/operations/OPERATIONS.ja.md` | 運用手順書 | ✅ | プロセス変更は重要な決定 |
| `docs/operations/NOTE_SYNC_MANUAL.ja.md` | note公開手順 | ✅ | 手順変更時 |

### ルール

1. **プロセス変更は ADR が必要**
   - 例: リリースフローの変更、レビュープロセスの変更
   - ADR に変更理由と影響を記録

2. **手順書は具体的に**
   - コマンド例を含める
   - 実行結果の期待値を明示

3. **古い手順は削除せず、アーカイブ**
   - `docs/archive/deprecated/` に移動
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
| `docs/prd_CHANGELOG_MIGRATION.ja.md` | Changelog分離の要件 | ❌ | PRD自体は要件定義 |
| `docs/prd_NOTE_WORKFLOW_AUTOMATION.ja.md` | note自動化の要件 | ❌ | |
| `docs/prd_DOCUMENTATION_GOVERNANCE.ja.md` | 本ガバナンス体系の要件 | ❌ | |

### ルール

1. **PRD自体は ADR 不要**
   - PRDは「これから実装する機能」の要件定義
   - 実装完了後、重要な決定があれば ADR に記録

2. **PRDのステータス管理**
   - Draft → Review → Approved → Implemented
   - Implemented 後は `docs/archive/completed/` に移動

3. **実装状況を project-status.ja.md に記録**
   - 各PRDの進捗状況を可視化

---

## 📝 Tier 4: 一時的文書

### 役割
**期限付きの作業記録**。完了後はアーカイブ。

### 配置場所
- ルートレベル or `docs/temporary/` (検討中)

### 更新頻度
**適宜**（作業進捗に応じて）

### ファイル一覧

| ファイル | 目的 | 完了後の扱い | 備考 |
|---------|------|------------|------|
| `MIGRATION_STATUS.md` | API移行の進捗 | ADR-0001に統合後、アーカイブ | 一時的 |

### ルール

1. **完了後は必ずアーカイブ**
   - `docs/archive/completed/` に移動
   - ファイル名を `YYYYMMDD-original-name.md` にリネーム

2. **恒久的な決定は ADR に抽出**
   - 一時文書から重要な決定を ADR に転記
   - ADR の Related に一時文書へのリンクを記載

3. **長期化する場合は Tier 1 に昇格**
   - 1ヶ月以上続く場合は `project-status.ja.md` に統合検討

---

## 🚫 自動生成ファイル（編集禁止）

### 役割
CI/CDが自動生成するファイル。**絶対に直接編集しない**。

### ファイル一覧

| ファイル | Source | 生成タイミング | 備考 |
|---------|--------|--------------|------|
| `AGENT.md` | `content/AGENT.ja.md` | CI実行時 | 英語版仕様書 |
| `spec/agent.spec.yaml` | `content/AGENT.ja.md` | CI実行時 | YAML構造化仕様 |

### ルール

1. **編集したい場合は Source を変更**
   - `content/AGENT.ja.md` を編集
   - CI が自動的に `AGENT.md` と `spec/agent.spec.yaml` を生成

2. **自動生成ファイルへの直接編集を検出**
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
vim docs/decisions/ADR-0001-ci-cd-pause.md

# 3. 関連ドキュメントを更新
vim docs/project-status.ja.md  # 現在の状態を記録
vim CHANGELOG.md               # [Unreleased] に追記（必要なら）

# 4. コミット
git add docs/decisions/ADR-0001-ci-cd-pause.md \
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
vim docs/operations/NOTE_SYNC_MANUAL.ja.md

# 3. 古い手順をアーカイブ
mkdir -p docs/archive/deprecated
git mv docs/operations/NOTE_SYNC_MANUAL.ja.md \
       docs/archive/deprecated/20251028-NOTE_SYNC_MANUAL.ja.md

# 4. 新しい手順を作成
vim docs/operations/NOTE_SYNC_MANUAL.ja.md

# 5. コミット
git add docs/decisions/ADR-*.md \
        docs/operations/NOTE_SYNC_MANUAL.ja.md \
        docs/archive/deprecated/20251028-NOTE_SYNC_MANUAL.ja.md
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
- [docs/prd_DOCUMENTATION_GOVERNANCE.ja.md](../documentation-governance.ja.md) - 本ガバナンス体系のPRD
- [Architecture Decision Records (ADR)](https://adr.github.io/) - ADR公式サイト

---

## 🔄 次のステップ

1. [ ] 本ドキュメントをレビュー
2. [ ] Phase 1 の成果物を作成（ADRテンプレート等）
3. [ ] 既存ドキュメントの棚卸し（Phase 2）

---

**最終更新**: 2025-10-28  
**次回レビュー**: 2025-11-28  
**バージョン**: 1.0.0
