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
20251028_0001_ci-cd-pause_architecture.md
20251028_documentation-governance.ja.md
20251028_OPERATIONS.ja.md

❌ 悪い例（旧形式）:
0001-ci-cd-pause.md              # 日付なし
documentation-governance.md  # 日付なし、種類ベース
OPERATIONS.ja.md                 # 日付なし
```

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
docs/operations/OPERATIONS.ja.md      ← 実行必須の手順書
docs/governance/NAMING_DECISION_SUMMARY.md ← メタドキュメント
```
理由: 業界標準、参照対象としての固定性、可視性

**小文字 + ハイフン（流動ドキュメント・URLフレンドリー）:**
```
20251028_0001_ci-cd-pause_architecture.md    ← ADR
20251028_documentation-governance.ja.md      ← PRD
```
理由: URLフレンドリー、プログラマティック処理対応、将来変更可能性

→ 詳細は [ADR-0011](./decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md) 参照

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

→ 詳細は [ADR-0012](./decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) 参照

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

## 🚀 次のステップ

### Phase 2: 既存ファイルのリネーム

```bash
# ADR-0001 のリネーム
mkdir -p docs/decisions/active/2025/10
mv docs/decisions/0001-ci-cd-pause.md \
   docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md

# ADR-0002 のリネーム（本ADR）
mv docs/decisions/0002-naming-and-directory-structure.md \
   docs/decisions/active/2025/10/20251028_0002_naming-structure_documentation.md

# PRDのリネーム
mkdir -p docs/prd/active
mv docs/prd_DOCUMENTATION_GOVERNANCE.ja.md \
   docs/prd/active/20251028_documentation-governance.ja.md
```

### scripts/record_decision.py の更新

新しい命名規則に対応する必要がある：

```python
# 新しいファイル名生成ロジック
def generate_filename(title, category, date):
    number = get_next_number()
    slug = sanitize_slug(title)
    return f"{date.strftime('%Y%m%d')}_{number:04d}_{slug}_{category}.md"

# 月別ディレクトリ自動作成
def get_output_dir(decisions_dir, date, status="active"):
    year_month_dir = decisions_dir / status / date.strftime("%Y") / date.strftime("%m")
    year_month_dir.mkdir(parents=True, exist_ok=True)
    return year_month_dir
```

### validate_docs.py の更新

命名規則チェックを追加：

```python
def check_naming_convention():
    """ファイル名が命名規則に従っているかチェック"""
    # YYYYMMDD_NNNN_slug_category.md 形式かどうか
    # カテゴリタグが定義済みのものか確認
```

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
**最終更新**: 2025-10-28  
**次回更新**: Phase 2（既存ファイルリネーム時）
