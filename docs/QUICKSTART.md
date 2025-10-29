# 🚀 QUICKSTART - あなたが知りたいこと別ガイド

**対象**: 初めて来たAI / 新しい貢献者  
**バージョン**: 1.0.0  
**最終更新**: 2025-10-29

---

## ❓ まず確認：あなたが知りたいことは？

### 🎯 「このプロジェクトが何か」を知りたい

**→ 読むべき順序:**
1. プロジェクトルート: [`README.md`](../README.md)（1分）
2. Tier 0仕様書: [`content/ja/AGENT.md`](../content/ja/AGENT.md)（30分～）

**目安**:
- プロジェクトの全体像を知りたい → README.md
- システムの詳細構造を理解したい → AGENT.md の「1. System Overview」
- 6ペルソナの仕組みを理解したい → AGENT.md の「2. The Bizarre Beasts」

---

### 🏛️ 「ドキュメント管理ルール」を知りたい

**→ 読むべき順序:**
1. 人間向け: [`docs/governance/HIERARCHY_RULES.md`](governance/HIERARCHY_RULES.md)
2. AI向け: [`docs/governance/AI_GUIDELINES.md`](governance/AI_GUIDELINES.md)
3. 機械可読: [`docs/governance/DOCUMENTATION_STRUCTURE.yml`](governance/DOCUMENTATION_STRUCTURE.yml)

**何を選ぶか**:
- 直感的に理解したい → HIERARCHY_RULES.md
- 自動化・スクリプト処理 → DOCUMENTATION_STRUCTURE.yml
- 意思決定フローを知りたい → AI_GUIDELINES.md

---

### 📂 「ファイル名命名規則」を知りたい

**→ 直接参照:**
- **[ADR-0011: ファイル名ケース規則](decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md)**
  - Q: 大文字にするか小文字にするか？
  - A: メタドキュメント（README, OPERATIONS）= 大文字 / 流動ドキュメント（ADR, PRD）= 小文字

- **[ADR-0012: ハイフン・アンダースコア規則](decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md)**
  - Q: ハイフンとアンダースコアのどちらを使う？
  - A: アンダースコア = 主要セクション区切り（日付・シーケンス）/ ハイフン = slug内の単語繋ぎ

**パターン記憶用**:
```
{YYYYMMDD}_{NNNN}_{lowercase-hyphen-slug}_{category}.md
 └─────┬──────┘ └──┬──┘ └───────────┬─────────┘ └──┬───┘
    日付      シーケンス      意味的単語     カテゴリ
   (下)     (下)            (下-下)        (下)
```

---

### 📊 「過去の決定」を検索したい

**→ 使うべきツール:**
1. **索引**: [`docs/decisions/INDEX.md`](decisions/INDEX.md)（推奨、ブラウザで見やすい）
2. **コマンド検索**:
   ```bash
   # カテゴリで検索
   ls docs/decisions/active/2025/10/*_architecture.md
   
   # タイムラインで検索
   ls docs/decisions/active/2025/10/
   
   # キーワードで検索
   grep -r "ファイル名" docs/decisions/
   ```

**INDEX.mdが提供する検索軸**:
- ✅ タイプ別（アーキテクチャ、ドキュメント、ガバナンスなど）
- ✅ 時系列（2025-10-29のすべての決定）
- ✅ ステータス別（Active/Deprecated/Superseded）
- ✅ 直接リンク

---

### ⚙️ 「新しいADRを作成」したい

**→ 実行:**
```bash
# 1. スクリプト実行（対話的に情報入力）
python scripts/record_decision.py \
  --title "決定のタイトル（日本語OK）" \
  --context "背景・理由・文脈" \
  --author "human"  # or "GitHub Copilot", "Claude Code"

# 2. ファイルが自動生成される
# → docs/decisions/active/2025/10/20251029_XXXX_...

# 3. INDEX.mdを再生成
python scripts/generate_index.py

# 4. コミット
git add docs/decisions/ docs/decisions/INDEX.md
git commit -m "docs(adr): Add ADR-XXXX for [簡潔なタイトル]"
```

**ADRの構造テンプレート** (`docs/decisions/0000_template.md` 参照):
```markdown
# ADR-NNNN: タイトル

## Status
- Proposed | Accepted | Deprecated | Superseded

## Context
背景・問題・トリガー

## Decision
実際の決定内容

## Consequences
メリット / デメリット / TODO

## Related
関連ファイル・Issue・ADR
```

---

### 📋 「運用手順」を知りたい

**→ 参照:**
- [`docs/operations/current/`](operations/current/)
  - `20251028_OPERATIONS.ja.md` - 全体運用マニュアル
  - `20251028_NOTE_SYNC_MANUAL.ja.md` - note公開手順
  - `20251028_WORKFLOW_TEXT_ASSETS.ja.md` - テキスト資産管理

---

### 🎬 「将来の計画」を知りたい

**→ 参照:**
- [`docs/prd/active/`](prd/active/)

各ファイルが実装予定の機能・改善を記述しています。

**INDEX**: [`docs/prd/INDEX.md`](prd/INDEX.md)

---

### 🔧 「スクリプトの使い方」を詳しく知りたい

**→ 参照:**
- [`scripts/README.md`](../scripts/README.md)

**よく使うスクリプト**:
| 用途 | コマンド |
|------|---------|
| 新規ADR | `python scripts/record_decision.py ...` |
| INDEX再生成 | `python scripts/generate_index.py` |
| 整合性確認 | `python scripts/validate_docs.py` |
| 目次生成 | `python scripts/gen_toc.py` |

---

### 📝 「このドキュメント構造を修正」したい

**→ 確認事項:**

1. **小さな修正（タイポ、リンク）**
   - そのまま修正してOK
   - コミットメッセージに記録

2. **大きな修正（カテゴリ追加、構造変更）**
   - ADR作成が必要（ADR-0002 参照）
   - `docs/governance/DOCUMENTATION_STRUCTURE.yml` 更新
   - INDEX.mdを再生成

3. **不明な場合**
   - [`docs/governance/AI_GUIDELINES.md`](governance/AI_GUIDELINES.md) の判定フロー参照

---

## 🎯 よくあるユースケース別ナビゲーション

| ユースケース | 必読ドキュメント | 時間目安 |
|------------|-----------------|--------|
| 「初来訪、全体把握したい」 | README.md → AGENT.md(Sec1) | 5分 |
| 「ADR-0001の内容は？」 | INDEX.md で検索 → 該当ADR開く | 2分 |
| 「新しい決定を記録したい」 | ADR-0000テンプレート → record_decision.py | 10分 |
| 「ハイフンの規則を確認」 | ADR-0012 | 3分 |
| 「note記事を公開したい」 | docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md | 15分 |
| 「ドキュメント構造を修正」 | AI_GUIDELINES.md 判定フロー → ADR | 30分 |

---

## 🔀 推奨される読む順序（新規貢献者向け）

### Phase 1: プロジェクト理解（15分）
1. [`README.md`](../README.md)
2. [`AGENT.md`](../content/ja/AGENT.md) - Sec 0, Sec 1

### Phase 2: 管理ルール理解（10分）
3. [`docs/README.md`](./README.md)
4. [`docs/governance/HIERARCHY_RULES.md`](governance/HIERARCHY_RULES.md)

### Phase 3: 具体的なルール（5分）
5. [`ADR-0011`](decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md) - ケース規則
6. [`ADR-0012`](decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md) - 区切り文字

### Phase 4: 実行（必要に応じて）
7. 各タスクに応じて、specific document を参照

---

## 💡 Tips

### INDEX.md を活用する

```bash
# ブラウザで INDEX.md を開く（最も簡単）
# → カテゴリ別に一覧表示
# → 直接リンク付き

# コマンドで検索
grep "カテゴリ名" docs/decisions/INDEX.md
```

### ファイルフォーマットの確認

不確かな場合は、**テンプレートとすでに存在するファイルを参考に**：

```bash
# テンプレート
cat docs/decisions/0000_template.md

# 実例
cat docs/decisions/active/2025/10/20251029_0011_*.md
```

### 相対パスの確認

リンク参照時は、ファイルの位置を基準に相対パスを計算：

```
docs/README.md からの相対パス:
- decisions/INDEX.md ✅
- ../AGENT.md (プロジェクトルート)
- ../docs/project-status.ja.md (同一ディレクトリ内なら ../ 不要)
```

---

## 🆘 迷ったときの質問リスト

| 質問 | 答える場所 |
|------|----------|
| 「このファイルをどこに置く？」 | DOCUMENTATION_STRUCTURE.yml |
| 「ADRが必要？」 | AI_GUIDELINES.md の判定フロー |
| 「ファイル名は何にする？」 | ADR-0011 + ADR-0012 |
| 「このADRはActive？」 | INDEX.md でステータス確認 |
| 「前の決定との関係は？」 | ADR の "Related" セクション |

---

**質問や不明な点がある場合は、このドキュメントにリンクを追加してください。**

---

**作成**: 2025-10-29  
**バージョン**: 1.0.0  
**関連**: [`docs/README.md`](./README.md), [`docs/governance/HIERARCHY_RULES.md`](governance/HIERARCHY_RULES.md), [`docs/governance/AI_GUIDELINES.md`](governance/AI_GUIDELINES.md)
