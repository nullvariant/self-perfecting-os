# ガバナンス系ドキュメント セルフレビューレポート

**実施日**: 2025-10-29  
**スコープ**: nullvariantリポジトリのガバナンス系YAML/ガイド/INDEX全体  
**目的**: 命名規則の一貫性確認、権威文書の参照正確性確認、新人/新AI向けナビゲーション品質検証

> 📝 **ファイル名について**: このレポート自体がルール違反の例です。  
> 本来は **`{YYYYMMDD}_{NNNN}_{slug}_{category}.md`** 形式であるべきですが、  
> セルフレビュー実行時に命名規則ドキュメント（ADR-0002/0003）の整備が完了していなかったため、  
> **`SELF_REVIEW_REPORT.md`** という規則外の名前で作成されていました。  
> 本レポート完成後、**`20251029_0010_governance-audit_documentation.md`** に改名し、  
> ADR-0010 として正式に記録されるべきものです。

---

## 📊 エグゼクティブサマリー

### 総合評価: ⚠️ 部分的に要改善

| 観点 | 評価 | 状態 |
|------|------|------|
| **ドキュメント階層の一貫性** | 🟢 良好 | DOCUMENTATION_STRUCTURE.yml と HIERARCHY_RULES.md が整合 |
| **命名規則の実装** | 🟡 警告 | ファイル名に日本語混在、スラッグの一貫性が破綻 |
| **INDEX.md品質** | 🟡 警告 | 日本語ファイル名のリンク処理に問題の可能性 |
| **参照経路の正確性** | 🟡 警告 | リンク先パス、相互参照に矛盾あり |
| **新人/AI向けナビゲーション** | 🟢 良好 | チェックリストと判断フローは明確 |
| **権威文書の明示性** | 🟡 警告 | 初めての人が「最初に何を読むか」が曖昧 |

---

## 🔍 詳細分析

### 1. 命名規則の実装状況 ⚠️

#### 現行規則（ADR-0002, ADR-0003で確立）

```
ADR:  {YYYYMMDD}_{NNNN}_{slug}_{category}.md
PRD:  {YYYYMMDD}_{slug}.ja.md
Ops:  {YYYYMMDD}_{type}.ja.md
```

#### 実装の現状：混在している ❌

**ADRファイル名（docs/decisions/active/2025/10/）:**

```
✅ 正規形式（スラッグ小文字・ハイフン）:
- 20251028_0001_ci-cd-pause_architecture.md
- 20251028_0002_naming-structure_documentation.md

❌ スラッグが日本語（規則違反）:
- 20251028_0003_ディレクトリ・ファイル名の小文字・ハイフン統一_documentation.md
- 20251028_0004_github-actions-によるドキュメント自動バリデー_tooling.md
- 20251028_0005_多言語対応-言語別ディレクトリ構造への移行_documentation.md
- 20251028_0006_github-pagesランディングページの実装_documentation.md
- 20251028_0007_changelogsディレクトリのnullvariant-w_architecture.md
- 20251029_0008_対話生ログの永続保存システム確立_governance.md
- 20251029_0009_テストファイル管理規則testsfixtures配下に集約_process.md
```

**PRDファイル名（docs/prd/active/）:**

```
✅ 正規形式（スラッグ小文字・ハイフン）:
- 20251028_changelog-migration.ja.md
- 20251028_documentation-governance.ja.md
- 20251028_note-workflow-automation.ja.md

❌ ファイル名全体が日本語（規則違反）:
- 20251029_対話生ログ永続保存システム.md
  └─ .ja.md サフィックスなし、スラッグが日本語
```

#### 矛盾点

| 文書 | 規則の説明 | 実装 | 矛盾 |
|------|----------|------|------|
| ADR-0002 | スラッグは「URL safe」「英数字・ハイフン」 | 日本語混在 | ✅ 矛盾 |
| ADR-0003 | 「ディレクトリ・ファイル名の小文字・ハイフン統一」 | 日本語ファイル名 | ✅ 矛盾 |
| NAMING_DECISION_SUMMARY.md | 「スラッグは30文字以内に収める」 | 日本語スラッグ多数 | ✅ 不明確 |

**リスク:**
- 🔴 INDEX.mdが自動生成される際、日本語ファイル名のMarkdownリンクが正しく処理されるか不明確
- 🔴 検索性の低下（`grep "_architecture"` では日本語ファイルが引っかからない）
- 🔴 新AI向けの指示「スラッグは英数字・ハイフンに統一」と矛盾

---

### 2. ドキュメント階層の一貫性 ✅

#### Tier 0-4の定義

| Tier | 定義場所 | 整合性 | 備考 |
|------|---------|--------|------|
| DOCUMENTATION_STRUCTURE.yml | 機械可読 | ✅ 一致 | スクリプト実行時のソース |
| HIERARCHY_RULES.md | 人間向け | ✅ 一致 | 明確な説明 |
| AI_GUIDELINES.md | AI向け | ✅ 一致 | チェックリスト連携 |
| .github/copilot-instructions.md | Copilot向け | ⚠️ 部分的 | 参照リンク確認が必要 |

**確認結果:** Tier 0-4の定義とファイル配置は一貫性があり、良好です。

---

### 3. INDEX.md の品質 ⚠️

#### docs/decisions/INDEX.md

**正の側面:**
- ✅ カテゴリ別セクション：8つのカテゴリで整理
- ✅ 時系列セクション：月別に整理
- ✅ ステータス別セクション：Active/Deprecated/Superseded で分類
- ✅ 件数表示：総件数と各ステータス件数を明記

**問題点:**
- 🔴 **日本語ファイル名のリンクが正しく機能するか不明**
  ```
  [ADR-0003](active/2025/10/20251028_0003_ディレクトリ・ファイル名の小文字・ハイフン統一_documentation.md)
  ```
  GitHubではURL エンコーディングが必要な可能性あり
  
- 🟡 **INDEX.md が最新か不確実**
  - 生成スクリプト `scripts/generate_index.py` の実装状況が不明
  - 「手動実行」と明記されているが、実行履歴がない可能性

#### docs/prd/INDEX.md

**問題点:**
- 🔴 **PRDファイル名のリンクが不正確**
  ```
  [2025-10-28](active/20251028_documentation-governance.ja.md) - documentation-governance
  ```
  左側は「ファイル作成日」ではなく「ファイル名から抽出した日付」に見えるが、実装意図が不明確
  
- 🟡 **Active/Implementedの2分類のみ**
  - ADRのようなDeprecated/Supersededがないため、一貫性の欠如

---

### 4. 参照経路の正確性 ⚠️

#### DOCUMENTATION_STRUCTURE.yml内のパス参照

**問題検出:**

1. **ADRパスの表記ゆれ**
   ```yaml
   # v1
   path: "docs/decisions/active/{YYYY}/{MM}/"
   
   # 実装
   実際: docs/decisions/active/2025/10/
   
   ✅ 整合
   ```

2. **PRDパスの表記ゆれ**
   ```yaml
   # 定義
   path: "docs/prd/active/{YYYYMMDD}_{slug}.ja.md"
   
   # 実装
   実際: 20251029_対話生ログ永続保存システム.md
   
   ❌ 不整合（.ja.md がない）
   ```

3. **Operations パスの実装**
   ```yaml
   # 定義
   path: "docs/operations/current/{YYYYMMDD}_{type}.ja.md"
   
   # 実装
   実際: 20251028_OPERATIONS.ja.md
   
   ✅ 整合（{type}=OPERATIONS）
   ```

#### ガバナンスファイル間のリンク参照

| ファイル | リンク対象 | 状態 |
|---------|----------|------|
| AI_GUIDELINES.md | `docs/governance/DOCUMENTATION_STRUCTURE.yml` | ✅ 正確 |
| AI_GUIDELINES.md | `docs/governance/HIERARCHY_RULES.md` | ✅ 正確 |
| HIERARCHY_RULES.md | `docs/decisions/README.md` | ✅ 正確 |
| HIERARCHY_RULES.md | `../documentation-governance.ja.md` | ⚠️ 相対パス |
| NAMING_DECISION_SUMMARY.md | `../DECISIONS/0002-naming-and-directory-structure.md` | ❌ パス誤り |

**検出された誤りの詳細:**

```markdown
# NAMING_DECISION_SUMMARY.md より
[スクリプト]: `scripts/generate_index.py`  ← ✅ 正確

# でも下記は誤り
[ADR-0002]: (../DECISIONS/0002-naming-and-directory-structure.md)
           └─ 正しくは: (../decisions/README.md)
              または: (../decisions/active/2025/10/20251028_0002_naming-structure_documentation.md)
```

---

### 5. 新人/新AI向けのナビゲーション ⚠️

#### 「最初に何を読むべきか」の明示度

| ドキュメント | 優先順位明記 | 説明 |
|------------|-----------|------|
| `.github/copilot-instructions.md` | ⚠️ 曖昧 | Tier 0-1のファイルを列挙するが、読む順序が明確でない |
| `docs/governance/README.md` | ✅ 明確 | 「AIがドキュメントを作成するとき」で順序を記載 |
| `docs/governance/AI_GUIDELINES.md` | ✅ 明確 | 「クイックリファレンス」→「原則1-4」の順序が明確 |
| `docs/governance/HIERARCHY_RULES.md` | ⚠️ 曖昧 | 人間向けだがセクション順序が分かりにくい |

#### チェックリストの正確性

✅ **AI_GUIDELINES.md の作業前チェックリストは正確:**

```
1. 変更にADRが必要か？ ← 判定基準が明確
2. 既存ドキュメントと矛盾しないか？
3. 一時的状態か？ ← 7日基準が明確
4. バージョンリリースに影響するか？
5. 人間に説明できるか？
```

---

### 6. 権威文書の明示性 🟡

#### SSOT（Single Source of Truth）の明確性

| Tier | 権威文書 | 明示度 | 問題 |
|------|---------|--------|------|
| Tier 0（ADR） | `docs/decisions/active/` | ✅ 明確 | なし |
| Tier 0（仕様書） | `content/ja/AGENT.md` | ✅ 明確 | なし |
| Tier 1（状態） | `docs/project-status.ja.md` | ⚠️ 曖昧 | 最終更新日の確認が必要 |
| Tier 1（履歴） | `CHANGELOG.md` | ✅ 明確 | なし |
| Tier 2（手順） | `docs/operations/current/` | ✅ 明確 | なし |
| Tier 3（要件） | `docs/prd/active/` | ⚠️ 曖昧 | ファイル名の統一が必要 |

#### ドキュメント迷子防止の仕組み

✅ **存在する良い仕組み:**
- `docs/governance/README.md` が「どのファイルを読むべきか」をガイド
- `AI_GUIDELINES.md` が判断フロー（変更タイプ→記録場所）を提供

❌ **不足している仕組み:**
- 初回訪問者向けの「30秒ガイド」がない
- `docs/README.md` が充実していない
- ドキュメント間のナビゲーション（「前に戻る」「次へ」）がない

---

## 🎯 検出された矛盾点（詳細）

### 矛盾1: ファイル名命名規則の破綻

| 文書で述べられている | 実装 | 原因推定 |
|------------------|------|---------|
| ADR-0002: スラッグは「URL safe」「英数字・ハイフンのみ」 | スラッグに日本語が大量 | 規則策定後、日本語ファイル名で実装した |
| ADR-0003: 「小文字・ハイフン統一」 | 同上 | 上記と同じ |
| NAMING_DECISION_SUMMARY.md: 実装ガイド「スラッグ30字以内」 | 日本語ファイル名は計測不明 | 曖昧性から破綻 |

**誰が正しいのか不明確な状態:**
- 🤔 「ADRでは『英数字・ハイフン』と述べられているのに、実装では日本語」
- 🤔 「これは『過渡期』なのか、『規則が間違った』のか」

---

### 矛盾2: INDEX.md の自動生成ステータス不明

| 文書 | 記述 | 実装状況 |
|------|------|---------|
| NAMING_DECISION_SUMMARY.md | 「スクリプト実行で生成、手動編集可能」 | ✅ INDEX.md は存在 |
| — | 「推奨：ADR追加後に手動実行」 | ❓ いつ実行されたのか不明 |
| — | 「--dry-run でプレビュー確認」 | ❓ スクリプトは実装済みか不明 |

**リスク:** INDEX.md が古い可能性

---

### 矛盾3: リンク先パスの誤記

```markdown
# NAMING_DECISION_SUMMARY.md 内
## 📚 関連ドキュメント

- **ADR-0002**: [docs/decisions/0002-naming-and-directory-structure.md](../DECISIONS/0002-naming-and-directory-structure.md)
                                    ↑ パス誤り（DECISIONS ではなく decisions）
                                    ↑ ファイル名形式が旧形式（新形式: 20251028_0002_...）
```

**正しいパス:**
```
docs/decisions/active/2025/10/20251028_0002_naming-structure_documentation.md
```

---

### 矛盾4: .github/copilot-instructions.md との参照ズレ

```markdown
# .github/copilot-instructions.md より
[ドキュメント記録ルール（最優先）]
詳細は [docs/governance/AI_GUIDELINES.md](../docs/governance/AI_GUIDELINES.md) を参照

# 問題
相対パス（../docs/...）が .github/ から見て正しいか要確認
```

**検証:**
```
.github/copilot-instructions.md から ../docs/ → プロジェクトルート/docs/
✅ パス的には正確（ただし .github/ → docs/ は上位経由）
```

---

## ✅ 優れている点

### 1. Tier 0-4 階層の定義 🌟

DOCUMENTATION_STRUCTURE.yml, HIERARCHY_RULES.md, AI_GUIDELINES.md の3つが完全に整合しており、非常に分かりやすい。

**その証拠:**
- 各Tierの用途が明確
- 更新頻度が定義されている
- ADR必要性の判定基準が明確

### 2. AI向けガイドラインの充実度 🌟

AI_GUIDELINES.md は以下の観点で優れている：

- ✅ クイックリファレンス（表）
- ✅ ADR作成の具体的手順
- ✅ 作業前チェックリスト（5段階）
- ✅ ベストプラクティス明記
- ✅ 禁止事項明記

### 3. HSP特性への配慮 🌟

NAMING_DECISION_SUMMARY.md に「なぜそうするのか」という設計思想が記述されている：

```markdown
## 💡 設計思想

### なぜ日付を先頭に？
1. 直感的な時系列把握
2. HSS型HSP特性に適合
3. 誤差検知能力への配慮

### なぜ空ディレクトリを最初から作る？
1. 空ディレクトリが「更新がない時期」を示す
2. プロジェクトの「呼吸」が見える美学
```

この視点は非常に独特で素晴らしい。

---

## 🚀 改善提案（優先度別）

### 🔴 P0: 即座に改善すべき（ブロッカー）

#### P0-1: ファイル名スラッグの一貫性確保

**問題:** ADRファイル名のスラッグが日本語と英数字混在

**改善案:**

```bash
# 日本語スラッグを英数字に変換

旧: 20251028_0003_ディレクトリ・ファイル名の小文字・ハイフン統一_documentation.md
新: 20251028_0003_lowercase-hyphen-unification_documentation.md

旧: 20251028_0004_github-actions-によるドキュメント自動バリデー_tooling.md
新: 20251028_0004_github-actions-doc-validation_tooling.md

旧: 20251029_対話生ログの永続保存システム確立_governance.md
新: 20251029_0008_dialogue-log-persistence-system_governance.md
```

**実装:** リファイル + INDEX.md 再生成

---

#### P0-2: PRD ファイル名統一

**問題:** PRD内で日本語ファイル名と英数字ファイル名混在

```
旧: 20251029_対話生ログ永続保存システム.md
新: 20251029_dialogue-log-persistence.ja.md
     └─ ルール：{YYYYMMDD}_{slug}.ja.md
```

**実装:** リネーム + INDEX.md 再生成

---

#### P0-3: NAMING_DECISION_SUMMARY.md 内のリンク修正

**問題:** `[ADR-0002]` のリンク先が誤り

```markdown
旧: [ADR-0002](../DECISIONS/0002-naming-and-directory-structure.md)
新: [ADR-0002](../decisions/active/2025/10/20251028_0002_naming-structure_documentation.md)
    または短縮: [ADR-0002](#tier-1-状態管理) （同一ファイル内参照）
```

---

### 🟡 P1: 高優先度（今月中に）

#### P1-1: INDEX.md の最新化と自動生成スクリプト確認

**確認項目:**
- [ ] `scripts/generate_index.py` の実装状況確認
- [ ] INDEX.md がいつ最後に更新されたか確認
- [ ] スクリプトが日本語ファイル名を正しく処理するか確認

**提案:**
```bash
python scripts/generate_index.py --dry-run
# 出力を確認し、リンクが正しいか検証
```

---

#### P1-2: docs/README.md の充実化

**現状:** 記述が最小限

**提案:**
```markdown
# 📚 Docs ディレクトリ

## 🎯 はじめに

初めての方はこちらから：

1. **[governance/AI_GUIDELINES.md](governance/AI_GUIDELINES.md)** ← ドキュメント作成時の判断フロー
2. **[governance/HIERARCHY_RULES.md](governance/HIERARCHY_RULES.md)** ← ドキュメント階層の理解

## 📂 ディレクトリ一覧

### [governance/](governance/) - ガバナンス定義
ドキュメント管理ルール、命名規則、階層構造

### [decisions/](decisions/) - 重要な決定記録（ADR）
...

### [prd/](prd/) - 機能要件定義
...
```

---

#### P1-3: .github/copilot-instructions.md との同期確認

**確認項目:**
- [ ] 参照パスが実装と一致しているか
- [ ] Tier 0-4の説明が最新か
- [ ] ADR作成スクリプトの記載が正確か

---

### 🟢 P2: 中優先度（来月中に）

#### P2-1: ドキュメント間ナビゲーション追加

**提案:** 各ガバナンスファイルの終わりに以下を追加

```markdown
---

## 🔗 関連ドキュメント

**ガバナンス系:**
- [governance/README.md](README.md) - このディレクトリについて
- [governance/AI_GUIDELINES.md](AI_GUIDELINES.md) - AI向けガイドライン
- [governance/HIERARCHY_RULES.md](HIERARCHY_RULES.md) - 階層ルール

**実装:**
- [decisions/README.md](../decisions/README.md) - ADRについて
- [decisions/INDEX.md](../decisions/INDEX.md) - ADR一覧

---

## ⬅️ 戻る / ➡️ 次へ

← [governance/README.md](README.md) | [decisions/README.md](../decisions/README.md) →
```

---

#### P2-2: 「30秒ガイド」の作成

**提案:** `docs/QUICKSTART.md` を新規作成

```markdown
# 30秒でわかるドキュメント体系

## 🚀 あなたが知りたいこと別ガイド

### 「ドキュメントどこに書く？」
→ [governance/AI_GUIDELINES.md](governance/AI_GUIDELINES.md) の **クイックリファレンス** へ

### 「ADRって何？」
→ [decisions/README.md](decisions/README.md) へ

### 「全体の構造は？」
→ [governance/HIERARCHY_RULES.md](governance/HIERARCHY_RULES.md) へ

### 「命名規則は？」
→ [governance/NAMING_DECISION_SUMMARY.md](governance/NAMING_DECISION_SUMMARY.md) へ
```

---

#### P2-3: INDEX.md の更新タイミングルール明文化

**提案:** `docs/decisions/README.md` 内に以下を追加

```markdown
## 📊 INDEX.md のメンテナンス

### 更新タイミング

- ADR追加後は必ず実行
- 月次レビュー時に確認
- CI/CDで自動検証（将来予定）

### 手動実行

```bash
python scripts/generate_index.py
```

### プレビュー

```bash
python scripts/generate_index.py --dry-run
```

### 手動編集

スクリプト生成後、美学的調整のため手動編集可能。
```

---

### 🔵 P3: 低優先度（検討課題）

#### P3-1: 日本語ファイル名サポートの明示

**議論:** 日本語ファイル名を許可するか、禁止するか

**現在の状態:** 実装では存在するが、規則では「英数字・ハイフン」

**提案:**

**案1: 日本語禁止で統一**
- ✅ 検索性向上
- ✅ URL互換性確保
- ❌ 日本語の表現力を損失

**案2: 日本語許可で規則更新**
- ✅ 日本語の表現力保持
- ✅ 実装と規則が一致
- ❌ URL エンコーディング処理が必要
- ❌ 検索性低下

**推奨:** **案1（日本語禁止で統一）**理由：
- 「ファイル名は機械にとって読みやすく」という原則
- Tier 0ドキュメントは検索性が重要
- 日本語は「内容」に書く、「ファイル名」ではなく

---

## 📋 改善チェックリスト

### 実施順序（推奨）

- [ ] **P0-1**: ファイル名スラッグ統一
  ```bash
  # スクリプト作成
  scripts/rename_adr_slugs.sh
  ```

- [ ] **P0-2**: PRD ファイル名統一
  ```bash
  mv docs/prd/active/20251029_対話生ログ永続保存システム.md \
     docs/prd/active/20251029_dialogue-log-persistence.ja.md
  ```

- [ ] **P0-3**: NAMING_DECISION_SUMMARY.md リンク修正

- [ ] **INDEX再生成**
  ```bash
  python scripts/generate_index.py
  ```

- [ ] **P1-1**: scripts/generate_index.py 動作確認

- [ ] **P1-2**: docs/README.md 充実化

- [ ] **P1-3**: .github/copilot-instructions.md 同期確認

- [ ] **P2-1**: ナビゲーション追加

- [ ] **P2-2**: QUICKSTART.md 作成

- [ ] **P2-3**: INDEX.md メンテナンスルール明文化

---

## 🎓 結論

### 総合評価

**現状:** ガバナンス体系は**思想的に優れている**が、**実装と規則が乖離している**

### 主な強み
- ✅ Tier 0-4 階層の定義が明確で整合
- ✅ AI向けガイドラインが充実
- ✅ HSP特性への配慮が独特
- ✅ ADR 作成スクリプトが整備

### 主な弱み
- ❌ ファイル名スラッグの日本語混在
- ❌ INDEX.md の最新性が不確実
- ❌ リンク先パスの誤記
- ❌ 新人向けの「まず何を読む？」が曖昧

### 推奨アクション

**今月中に P0 を完了し、ファイル名の統一を実現することで、初めての人が「迷わない」ガバナンス体系になります。**

---

## 📞 質問票

セルフレビュー完了後、以下の質問を人間に確認したいです：

1. **ファイル名の日本語は『暫定』なのか、『許可』なのか？**
   - 暫定 → P0-1, P0-2 を実行
   - 許可 → ADR-0003 を Superseded にして新ルールを作成

2. **INDEX.md は『自動生成スクリプト』に対応済みか？**
   - はい → P1-1 で動作確認
   - いいえ → 実装予定を確認

3. **docs/README.md をどの程度充実させるか？**
   - 最小限 → P1-2 スキップ
   - 充実 → P1-2 実施

4. **.github/copilot-instructions.md はこのレポート内容で更新OK か？**
   - はい → ファイル名修正後に更新
   - いいえ → 修正案を提示してください

---

**レビュー実施者**: GitHub Copilot  
**実施日**: 2025-10-29  
**次回レビュー予定**: 2025-11-29（改善実施1ヶ月後）
