# 命名規則とディレクトリ構造の決定 - サマリー

**決定日**: 2025-10-28  
**ADR**: ADR-0002  
**ステータス**: Accepted

---

## 🎯 決定内容

### 1. 命名規則

#### ✅ 採用形式

```
ADR: {YYYYMMDD}_{NNNN}_{slug}_{category}.md
PRD: {YYYYMMDD}_{slug}.ja.md
Ops: {YYYYMMDD}_{type}.ja.md
```

#### 📋 具体例

```
✅ 良い例:
20251028_0001_ci-cd-pause_architecture.md       # ADR（小文字）
20251028_documentation-governance.ja.md         # PRD（小文字）
20251028_OPERATIONS.ja.md                        # Ops（type部分は大文字）
20251028_NOTE_SYNC_MANUAL.ja.md                  # Ops（type部分は大文字）

❌ 悪い例（旧形式）:
0001-ci-cd-pause.md              # 日付なし
documentation-governance.md      # 日付なし
OPERATIONS.ja.md                 # 日付なし
```

**運用手順書のtype部分が大文字である理由**:
- 運用手順書は「実行必須の参照資料」として、メタドキュメント性が高い
- ADR-0011の「大文字メタドキュメント」原則に準拠
- 例: `OPERATIONS`, `NOTE_SYNC_MANUAL`, `WORKFLOW_TEXT_ASSETS`

---

## 📂 ディレクトリ構造

### ADR（月別 + ステータス別）

```
docs/decisions/
├── active/2025/10/
│   ├── 20251028_0001_ci-cd-pause_architecture.md
│   └── 20251028_0002_naming-structure_documentation.md
├── active/2025/11/         # 空 = 更新なし（美学）
├── deprecated/2025/10/
└── superseded/2025/10/
```

### PRD（ステータス別のみ）

```
docs/prd/
├── active/
│   └── 20251028_documentation-governance.ja.md
└── implemented/
```

### 運用手順書（最新版 + アーカイブ）

```
docs/operations/
├── current/
│   └── 20251028_OPERATIONS.ja.md
└── archive/2025/10/
```

---

## 🤖 INDEX.md 管理

### 生成方法

```bash
# 全INDEX生成
python scripts/generate_index.py

# プレビュー
python scripts/generate_index.py --dry-run

# 手動編集を上書き
python scripts/generate_index.py --force
```

### 更新タイミング

- **推奨**: ADR追加・変更時に手動実行
- **手動上書き**: スクリプト生成後、美学的調整が可能
- **Git Hooks**: 採用しない（HSP特性への配慮）

---

## 💡 設計思想

### ケース規則（大文字 vs 小文字）【ADR-0011】

**大文字（メタドキュメント・業界慣習）:**
```
README.md, CHANGELOG.md, AGENT.md
docs/operations/current/20251028_OPERATIONS.ja.md      ← 実行必須の手順書
docs/governance/NAMING_DECISION_SUMMARY.md ← メタドキュメント
```
理由: 業界標準、参照対象としての固定性、可視性

**小文字 + ハイフン（流動ドキュメント・URLフレンドリー）:**
```
20251028_0001_ci-cd-pause_architecture.md    ← ADR
20251028_documentation-governance.ja.md      ← PRD
```
理由: URLフレンドリー、プログラマティック処理対応、将来変更可能性

→ 詳細は [ADR-0011](../decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md) 参照

---

### ハイフン vs アンダースコア【ADR-0012】

ファイル名の構造例:
```
{YYYYMMDD} _ {NNNN} _ {slug} _ {category} . {ext}
     ↓        ↓         ↓        ↓
   日付    アンダー   ハイフン   アンダー
          スコア     (複合概念)  スコア
```

**🔹 アンダースコア（_）= 構造区切り**
- 日付とシーケンスの区切り: `20251029_0011_`
- slugとカテゴリの区切り: `_documentation`
- 理由: 視覚的に「ここで大きく区切られている」が明確

**🔸 ハイフン（-）= 意味内の単語区切り**
- slug内の複数単語: `ci-cd-pause`, `filename-case-convention`
- 理由: URLフレンドリー、SEO最適化、標準慣習（ケバブケース）

→ 詳細は [ADR-0012](../decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) 参照

---

### なぜ日付を先頭に？

1. **直感的な時系列把握**
   - ファイル名ソートで時系列順に並ぶ
   - 「最近の決定」がすぐわかる

2. **HSS型HSP特性に適合**
   - 緻密な誤差検知能力 → 「新旧が一目でわからない」はストレス
   - 美学重視 → ファイルリストが美しく整列

### なぜ月別ディレクトリを最初から？

1. **空ディレクトリが歴史を示す美学**
   - `2025/11/` が空 = 「この月は更新なし」が可視化される
   - プロジェクトの「呼吸」が見える

2. **後から作るより最初から**
   - 50件を超えてから導入すると移行コストが高い
   - 最初から統一ルールで運用

### なぜカテゴリタグは必須？

1. **検索性の向上**
   - `grep "_architecture"` で関連ADRを一括検索
   - INDEX.md のカテゴリ別セクションで分類

2. **トピック横断の可視化**
   - 「CI/CD関連の全決定」を時系列問わず抽出可能

### 【重要】2つの独立した管理軸：カテゴリ vs ディレクトリ構造

本命名規則は、**コンテンツ分類軸**と**ライフサイクル管理軸**を意図的に分離しています：

#### 軸1: コンテンツ分類軸（Category）
```
ファイル名の _category 部分

例: 20251028_0001_ci-cd-pause_architecture.md
                                  ↑
                        これは「メタデータタグ」
```

**役割**: 「何について決定したのか」を分類・検索
- `_architecture` → アーキテクチャ関連の決定
- `_process` → プロセス・手順関連の決定
- `_governance` → ガバナンス・ポリシー関連の決定

**活用例**:
```bash
# 「governance」カテゴリのすべてのADR
grep -r "_governance.md" docs/decisions/

# INDEX.md でカテゴリ別フィルタリング
python scripts/generate_index.py --group-by-category
```

#### 軸2: ライフサイクル管理軸（Directory）
```
ファイルの保存先

例: docs/decisions/active/2025/10/
                       ↑       ↑  ↑
              ステータス 年    月
```

**役割**: 「いつ、どの状態で、どこにあるのか」を管理
- `active/2025/10/` → 2025年10月の現行有効ADR
- `deprecated/2025/09/` → 2025年9月の非推奨ADR
- `superseded/2025/08/` → 2025年8月の上書きされたADR

**活用例**:
```bash
# 「2025年10月の有効なADR」
ls docs/decisions/active/2025/10/

# ステータス別検索
find docs/decisions/deprecated -name "*.md"
```

#### 2つの軸の独立性

```
シナリオ: 「2025年10月の active かつ architecture 関連」を検索

Step 1: ディレクトリで絞る
        → docs/decisions/active/2025/10/

Step 2: カテゴリで絞る
        → grep "_architecture.md" docs/decisions/active/2025/10/

         ↓

結果: docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md
```

**この2つの軸が直交することで、複雑な検索要求に対応可能**です。

#### なぜ分離したか

❌ **1つの軸だけでは足りない**:
- カテゴリのみ → 古いADRと新しいADRが混在
- ディレクトリのみ → 「architecture 関連の決定」が時系列問わず散在

✅ **2つの軸を独立させると**:
- 各軸を独立して設計・変更可能
- INDEX.md で複数軸の組み合わせ検索が容易
- 新しいカテゴリ追加時にディレクトリ構造は変わらない
- ディレクトリ移動時にカテゴリは変わらない

### なぜGit Hooksを採用しない？

1. **HSP特性との整合性**
   - 「勝手に動く」はストレス源
   - 「自分で制御している感覚」が重要

2. **完璧主義への対応**
   - 手動編集 → スクリプト上書き → 手動微調整のサイクル
   - 「美しいINDEX.md」を追求可能

3. **AI環境との相性**
   - Claude Code/Copilot が「スクリプト実行を提案」できる
   - Hooksは「気づかないうちに実行」されるため説明困難

---

## 📋 カテゴリタグ定義

| タグ | 説明 |
|------|------|
| `architecture` | アーキテクチャ変更 |
| `process` | プロセス・手順変更 |
| `tooling` | ツール・インフラ変更 |
| `documentation` | ドキュメント構造変更 |
| `security` | セキュリティ関連 |
| `performance` | パフォーマンス最適化 |
| `integration` | 外部連携 |
| `governance` | ガバナンス・ポリシー |

---

## ✅ 実装完了状況

### Phase 1: 命名規則の決定・ドキュメント化
**ステータス**: ✅ **完了**（2025-10-28）

- ✅ 命名規則の定義（ADR-0002）
- ✅ ケース規則の明確化（ADR-0011）
- ✅ ハイフン・アンダースコア規則の明確化（ADR-0012）
- ✅ 本ドキュメント（NAMING_DECISION_SUMMARY.md）の作成

### Phase 2: 既存ファイルのリネーム
**ステータス**: ✅ **完了**（2025-10-29）

**実施済みのリネーム:**

| 旧ファイル | 新ファイル | 状態 |
|----------|----------|------|
| `docs/decisions/0001-ci-cd-pause.md` | `docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md` | ✅ 完了 |
| `docs/decisions/0002-naming-and-directory-structure.md` | `docs/decisions/active/2025/10/20251028_0002_naming-structure_documentation.md` | ✅ 完了 |
| `docs/prd_DOCUMENTATION_GOVERNANCE.ja.md` | `docs/prd/active/20251028_documentation-governance.ja.md` | ✅ 完了 |

**ディレクトリ構造の確立:**
- ✅ `docs/decisions/active/2025/10/` ディレクトリ作成
- ✅ `docs/prd/active/` ディレクトリ作成
- ✅ `docs/operations/archive/2025/10/` ディレクトリ作成
- ✅ 月別階層による組織化の実装

### Phase 3: スクリプトの対応
**ステータス**: ⏳ **進行中**（2025-10-29以降）

**scripts/record_decision.py:**
- 新しい命名規則に対応（`{YYYYMMDD}_{NNNN}_{slug}_{category}.md` 形式）
- 月別ディレクトリの自動作成ロジック実装予定
- 実装予定時期: 次のADR作成時

**scripts/validate_docs.py:**
- 命名規則チェック機能の追加予定
- カテゴリタグの検証機能追加予定
- 実装予定時期: ガバナンス検証フェーズ

### Phase 4: INDEX.md 管理の運用化
**ステータス**: ✅ **運用中**

- ✅ 手動実行フロー確立（`python scripts/generate_index.py`）
- ✅ Git Hooks 非採用の決定（HSP特性への配慮）
- ✅ INDEX.md の定期更新手順を確立

---

## 📚 関連ドキュメント

- **ADR-0002**: [docs/decisions/active/2025/10/20251028_0002_naming-structure_documentation.md](../decisions/active/2025/10/20251028_0002_naming-structure_documentation.md)
- **スクリプト**: `scripts/generate_index.py`
- **階層定義**: `docs/governance/DOCUMENTATION_STRUCTURE.yml`

---

## 🎓 ベストプラクティス

### ADR作成時

1. カテゴリを事前に決める（8種類から選択）
2. スラッグは30文字以内に収める（可読性）
3. 月別ディレクトリは自動作成スクリプトに任せる（将来実装）

### INDEX.md 更新時

1. ADR追加後は必ず `python scripts/generate_index.py` を実行
2. `--dry-run` でプレビュー確認
3. スクリプト生成後、美学的調整があれば手動編集

### 美学的ポイント

- ファイルリストをソートしたとき、時系列が美しく並ぶ
- 空ディレクトリが「静寂の期間」を表現
- INDEX.md がプロジェクトの「年表」になる

---

**この命名規則により、nullvariantの「内側美学」と「検索性」が両立します。** 🎨✨

---

**作成日**: 2025-10-28  
**最終更新**: 2025-10-29  
**ステータス**: Phase 2 実装完了、Phase 3 進行中
