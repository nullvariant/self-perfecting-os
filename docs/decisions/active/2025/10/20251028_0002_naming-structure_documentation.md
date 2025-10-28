# ADR-0002: ドキュメント命名規則とディレクトリ構造の確立

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: human (nullvariant) + GitHub Copilot

## Context

### 背景

Phase 1 でドキュメント階層（Tier 0-4）を確立したが、以下の課題が残っていた：

1. **命名規則の不統一**: 種類ベース（PRD_*）、日付なし、連番のみなど混在
2. **新旧判別の困難**: ファイルリストで「古い/新しい」が直感的にわからない
3. **ディレクトリ構造の曖昧さ**: 月別アーカイブの有無、タイミングが不明確

### nullvariant の要望（HSS型HSP特性を反映）

1. **日付接頭辞を優先**: 時系列が直感的にわかる
2. **カテゴリタグは必須**: 検索性を確保
3. **最初から月別ディレクトリ**: 空ディレクトリが「更新がない時期」を示す美学
4. **INDEX.md は自動生成**: スクリプト実行 + 手動上書き可能

### 検討した選択肢

#### 命名規則

1. **連番優先**: `0001_20251028_slug_category.md`
2. **日付優先**: `20251028_0001_slug_category.md` ← **採用**
3. **日付のみ**: `20251028_slug_category.md`

#### ディレクトリ構造

1. **フラット**: 全ファイルを1ディレクトリに配置
2. **ステータス別**: `active/`, `deprecated/` のみ
3. **月別 + ステータス**: `active/2025/10/`, `deprecated/2025/10/` ← **採用**

#### INDEX.md 更新方法

1. **手動のみ**: 人間が編集
2. **Git Hooks**: コミット時に自動実行
3. **スクリプト + CI検証**: 手動実行 + CI でチェック ← **採用**

## Decision

### 1. 命名規則の確立

#### ADRファイル名

```
{YYYYMMDD}_{NNNN}_{slug}_{category}.md

例:
20251028_0001_ci-cd-pause_architecture.md
20251115_0002_adr-introduction_process.md
```

| 要素 | 形式 | 例 | 説明 |
|------|-----|----|----|
| 日付 | `YYYYMMDD` | `20251028` | 決定日（人間の直感優先） |
| 連番 | `NNNN` | `0001` | ADRの一意識別子（絶対に変わらない） |
| スラッグ | `kebab-case` | `ci-cd-pause` | 内容の要約（URL safe） |
| カテゴリ | `{tag}` | `architecture` | **必須**（後からの分類・検索用） |

#### カテゴリタグ定義

```yaml
categories:
  architecture: アーキテクチャ変更
  process: プロセス・手順変更
  tooling: ツール・インフラ変更
  documentation: ドキュメント構造変更
  security: セキュリティ関連
  performance: パフォーマンス最適化
  integration: 外部連携
  governance: ガバナンス・ポリシー
```

#### PRDファイル名

```
{YYYYMMDD}_{slug}.ja.md

例:
20251028_documentation-governance.ja.md
```

（連番不要：実装後はアーカイブされるため）

#### 運用手順書ファイル名

```
{YYYYMMDD}_{type}.ja.md

例:
20251028_OPERATIONS.ja.md
20251028_NOTE_SYNC_MANUAL.ja.md
```

（最新版のみ `current/` に配置）

### 2. ディレクトリ構造

#### ADR（月別 + ステータス別）

```
docs/decisions/
├── active/                    # 現行有効
│   ├── 2025/
│   │   ├── 10/
│   │   │   ├── 20251028_0001_ci-cd-pause_architecture.md
│   │   │   └── 20251028_0002_adr-introduction_process.md
│   │   └── 11/
│   │       └── (空ディレクトリ = 更新なし)
│   └── 2026/
│       └── (将来の記録)
├── deprecated/                # 非推奨（Status: Deprecated）
│   └── 2025/
│       └── 10/
├── superseded/                # 上書きされた決定
│   └── (構造は active/ と同じ)
├── INDEX.md                   # 自動生成
└── README.md                  # 使用ガイド（手動管理）
```

#### PRD（ステータス別のみ）

```
docs/prd/
├── active/
│   ├── 20251028_documentation-governance.ja.md
│   └── 20251115_note-workflow-automation.ja.md
├── implemented/
│   └── 20241001_changelog-migration.ja.md
└── INDEX.md                   # 自動生成
```

（PRDは件数が少ないため月別不要）

#### 運用手順書（最新版のみ + アーカイブ）

```
docs/operations/
├── current/
│   ├── 20251028_OPERATIONS.ja.md
│   └── 20251028_NOTE_SYNC_MANUAL.ja.md
├── archive/
│   └── 2025/
│       └── 10/
│           └── 20251001_old-operations.ja.md
└── INDEX.md                   # 自動生成（将来）
```

### 3. INDEX.md の管理方法

#### 生成方法

```bash
# 全INDEX生成
python scripts/generate_index.py

# ADRのみ
python scripts/generate_index.py --target adr

# プレビュー（ファイル書き込みなし）
python scripts/generate_index.py --dry-run

# 手動編集を上書き
python scripts/generate_index.py --force
```

#### 更新タイミング

- **推奨**: ADR追加・変更時に手動実行
- **CI検証**: PR時に INDEX.md の整合性をチェック（将来実装）
- **手動上書き**: スクリプト生成後、美学的調整が可能

#### INDEX.md の構成

1. **カテゴリ別**: トピック横断検索用
2. **時系列**: 「いつ決定されたか」を可視化
3. **ステータス別**: Active/Deprecated/Superseded を一覧

## Consequences

### ✅ メリット

1. **直感的な時系列把握**
   - ファイル名の先頭が日付 → ソート時に時系列順
   - 「最近の決定」がすぐわかる

2. **美しい空ディレクトリ**
   - 更新がない月も `2025/11/` が存在
   - プロジェクトの「呼吸」が見える

3. **検索性の向上**
   - カテゴリタグで `grep "_architecture"` が可能
   - INDEX.md で複数軸の検索

4. **制御可能な自動化**
   - Git Hooks の「勝手に動く」ストレスなし
   - 手動編集 → スクリプト上書き → 手動微調整のサイクル可能

5. **HSP特性への配慮**
   - 「自分で制御している感覚」を維持
   - 完璧主義を満たす美学的調整が可能

### ⚠️ デメリット

1. **ファイル名が長い**
   - `20251028_0001_ci-cd-pause_architecture.md` は60文字程度
   - タブ補完で緩和可能

2. **月別ディレクトリの管理コスト**
   - 手動で `mkdir -p docs/decisions/active/2025/11/` が必要
   - スクリプトで自動作成可能（将来実装）

3. **INDEX.md 生成の手間**
   - ADR追加のたびにスクリプト実行が必要
   - ただし `--dry-run` でプレビュー可能

### 📋 TODO

- [x] `scripts/generate_index.py` の実装
- [ ] `scripts/record_decision.py` を新命名規則に対応
- [ ] 既存ファイルのリネーム（Phase 2）
- [ ] `DOCUMENTATION_STRUCTURE.yml` に命名規則を追記
- [ ] CI/CD で INDEX.md 整合性チェック（将来）
- [ ] 月別ディレクトリ自動作成機能（将来）

## Related

### 関連するファイル
- `scripts/generate_index.py` - INDEX.md自動生成スクリプト（本ADRで作成）
- `scripts/record_decision.py` - ADR生成スクリプト（要更新）
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 階層定義（要更新）
- `docs/governance/HIERARCHY_RULES.md` - 階層ルール説明（要更新）

### 関連する ADR
- ADR-0001: CI/CD一時停止（本ADRで命名規則を確立）

### 関連する PRD
- `docs/prd_DOCUMENTATION_GOVERNANCE.ja.md` - 本ガバナンス体系のPRD

---

## 補足: Git Hooks vs スクリプトの判断理由

### Git Hooks を採用しなかった理由

1. **HSP特性との不整合**
   - 「勝手に動く」はストレス源になりうる
   - 「自分で制御している感覚」が重要

2. **AI環境との相性**
   - Claude Code/Copilot は「スクリプト実行を提案」できる
   - Hooksは「気づかないうちに実行される」ため、AIが説明しづらい

3. **完璧主義への対応**
   - 手動編集 → スクリプト上書き → 手動微調整 のサイクルが必要
   - Hooksでは「美しいINDEX.md」を追求しづらい

### スクリプト + CI検証を採用した理由

1. **制御可能**: 実行タイミングを選べる
2. **デバッグ容易**: エラーが見える
3. **柔軟性**: 手動編集後にスクリプトで上書きも可能
4. **環境非依存**: Python環境さえあれば動く

---

**Status**: Accepted  
**実装状況**: `generate_index.py` 完成、既存ファイルのリネームは Phase 2  
**次回レビュー**: Phase 2 開始時（既存ドキュメント整理時）
