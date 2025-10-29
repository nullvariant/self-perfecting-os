# ガバナンス系ドキュメント セルフレビュー報告書

**実施日**: 2025年10月29日  
**実施者**: GitHub Copilot  
**検査対象**: nullvariant リポジトリ全体  
**検査視点**: 命名規則一貫性・参照正確性・新規訪問者の混乱排除・権威文書明確性

---

## ✅ 検査結果のサマリー

| 項目 | 評価 | 説明 |
|------|------|------|
| **命名規則の一貫性** | ⚠️ 部分的 | YAML・INDEX は正しい。Markdown に古い形式が残存 |
| **参照の正確性** | ❌ 矛盾あり | AI_GUIDELINES.md, HIERARCHY_RULES.md に古いパス参照が多数 |
| **新規訪問者の明確性** | ❌ 混乱リスク | 複数文書で異なる形式が記載 → どれが正しいか不明 |
| **権威文書の階層** | ❌ 不明確 | SSOT の優先順位が明記されていない |
| **ADR・INDEX の整合性** | ✅ 優良 | ADR-0011, 0012 と INDEX.md は完全一致 |

---

## 🚨 重大な問題（修正必須）

### 問題 #1: AI_GUIDELINES.md の古いパス参照

**ファイル**: `docs/governance/AI_GUIDELINES.md`  
**影響度**: ⚠️ **高**（Tier 0 権威文書）

#### 詳細

**Tier 2 セクション（Line 209-211）**:
```markdown
- `docs/operations/OPERATIONS.ja.md` - 運用手順
- `docs/operations/NOTE_SYNC_MANUAL.ja.md` - note公開手順
```

✅ **正しい形式**:
```markdown
- `docs/operations/current/20251028_OPERATIONS.ja.md` - 運用手順
- `docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md` - note公開手順
```

**Tier 3 セクション（Line 213-215）**:
```markdown
- `docs/prd_*.md` - 各機能のPRD
```

✅ **正しい形式**:
```markdown
- `docs/prd/active/{YYYYMMDD}_{slug}.ja.md` - 各機能のPRD
```

#### 発見根拠

- DOCUMENTATION_STRUCTURE.yml では正しい形式で定義されている
- NAMING_DECISION_SUMMARY.md では正しい形式で記載されている
- INDEX.md では正しく参照されている
- 実際のファイルシステムに古い形式のファイルは存在しない

#### 影響

```
新規AI: 「AI_GUIDELINES.md に書いてある」と信じる
    ↓
docs/operations/OPERATIONS.ja.md にADRを置く
    ↓
❌ 命名規則違反・ディレクトリ構造違反
    ↓
🚀 ガバナンス体系の混乱
```

#### 修正方法

Tier 2・Tier 3 セクションの具体例を、新しい命名規則に統一

---

### 問題 #2: HIERARCHY_RULES.md のテーブル内容が実装と乖離

**ファイル**: `docs/governance/HIERARCHY_RULES.md`  
**影響度**: ⚠️ **高**（人間向けドキュメント）

#### 詳細

**Tier 2 テーブル（Line 158-159）**:
```markdown
| `docs/operations/OPERATIONS.ja.md` | 運用手順書 | ✅ | ...
| `docs/operations/NOTE_SYNC_MANUAL.ja.md` | note公開手順 | ✅ | ...
```

✅ **正しい形式**:
```markdown
| `docs/operations/current/20251028_OPERATIONS.ja.md` | 運用手順書 | ✅ | ...
| `docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md` | note公開手順 | ✅ | ...
```

**Tier 3 テーブル（Line 192-194）**:
```markdown
| `docs/prd_CHANGELOG_MIGRATION.ja.md` | ...
| `docs/prd_NOTE_WORKFLOW_AUTOMATION.ja.md` | ...
| `docs/prd_DOCUMENTATION_GOVERNANCE.ja.md` | ...
```

✅ **正しい形式**:
```markdown
| `docs/prd/active/20251028_changelog-migration.ja.md` | ...
| `docs/prd/active/20251028_note-workflow-automation.ja.md` | ...
| `docs/prd/active/20251028_documentation-governance.ja.md` | ...
```

#### 発見根拠

- DOCUMENTATION_STRUCTURE.yml で正しい形式が定義されている
- 実際のファイルシステムに古い形式のファイルは存在しない
- ADR-0002, ADR-0003 で新しい命名規則が確立されている

#### 影響

```
人間: 「ここが現行の例」と思う
    ↓
❌ 古い形式で新しいPRDを作成
    ↓
🚀 命名規則違反
```

#### 修正方法

テーブルの「ファイル」列をすべて新形式に統一

---

### 問題 #3: 複数のガバナンス文書における一貫性の欠如と優先順位の不明確さ

**影響度**: ⚠️ **中-高**

#### 詳細

**症状**:
- AI_GUIDELINES.md（Tier 0）で古い形式が記載されている
- HIERARCHY_RULES.md（Tier 0 補足）で古い形式が記載されている
- 一方、DOCUMENTATION_STRUCTURE.yml では正しい形式が定義されている

**新規AIの困惑パターン**:
```
AI: 「どの文書が正しいのか？」
  │
  ├─ AI_GUIDELINES.md → 「操作/OPERATIONS.ja.md」と記載
  ├─ HIERARCHY_RULES.md → 「操作/OPERATIONS.ja.md」と記載
  └─ DOCUMENTATION_STRUCTURE.yml → 「操作/current/20251028_OPERATIONS.ja.md」と記載
  
AI: 「YAMLが正しい？それともマークダウンが正しい？」
    「この矛盾は ADR が必要では？」
```

#### 発見根拠

実際の検査から：

| ドキュメント | Tier 2 形式 | Tier 3 形式 | 一貫性 |
|------------|-----------|-----------|--------|
| AI_GUIDELINES.md | 古い | 古い | 矛盾 |
| HIERARCHY_RULES.md | 古い | 古い | 矛盾 |
| DOCUMENTATION_STRUCTURE.yml | ✅ 新しい | ✅ 新しい | OK |
| NAMING_DECISION_SUMMARY.md | ✅ 新しい | ✅ 新しい | OK |
| INDEX.md | ✅ 新しい | ✅ 新しい | OK |

#### 影響

```
新規AI・人間: 「どれが権威か？」と混乱
    ↓
❌ 判断停止・確認要求増加
    ↓
🚀 効率低下・ガバナンス信用低下
```

#### 修正方法

1. マークダウン文書を YAML と同期
2. 「権威性マトリクス」を新規作成し、複数文書の優先順位を明記

---

## ⚠️ 中程度の問題

### 問題 #4: 新規訪問者向けの「最初に読むべき順序」が不明確

**ファイル**: `.github/copilot-instructions.md` / `docs/governance/README.md`  
**影響度**: ⚠️ 中

#### 詳細

`.github/copilot-instructions.md` には相対パスで複数のドキュメントが参照されているが、「最初に何を読むべきか」の指示が不十分：

```markdown
- `docs/governance/AI_GUIDELINES.md`      ← AI向け？
- `content/ja/AGENT.md`                   ← 仕様書？
- `docs/decisions/active/2025/10/...`    ← ADR？
```

#### 新規訪問者のシナリオ

```
初来訪者: 「このリポジトリのガイドを読みたい」
    │
    ├─ → README.md へ
    ├─ → .github/copilot-instructions.md へ
    └─ → 「複数のドキュメントが参照されている」
    
❓ 「どれから読めばいいのか？」
```

#### 修正方法

- Tier 0（Tier）ドキュメントの明確な列挙
- 新規訪問者向けの「読む順序チェックリスト」を作成

---

### 問題 #5: .github/copilot-instructions.md のプロジェクト構造が部分的に古い

**ファイル**: `.github/copilot-instructions.md` (Line 73 以降)  
**影響度**: ⚠️ 低-中

#### 詳細

プロジェクト構造図に以下の古い参照が残存：

```markdown
├── operations/                   # 📋 運用手順書
│   ├── DOCUMENTATION_UPDATE_CHECKLIST.md  # 構造変更時のチェックリスト
│   └── current/                  # 現行版手順書
├── prd/                          # 💡 要件定義
```

新しい形式では `docs/operations/current/` に日付付きファイルが配置される。

#### 修正方法

プロジェクト構造図を更新し、新しい命名規則を反映させる

---

## ✅ 優良な実装（参考）

### ADR インデックスの完全性

**ファイル**: `docs/decisions/INDEX.md`

✅ **優れている点**:
1. カテゴリ別・時系列・ステータス別の 3 視点で分類
2. ADR-0011, 0012 による命名規則を完全に反映
3. 全12件のADRを漏れなく掲載
4. 相対パスが正確

### DOCUMENTATION_STRUCTURE.yml の精度

✅ **優れている点**:
1. 機械可読形式で正確に定義
2. ファイルパスが新命名規則に統一
3. AI判定用ロジックが明確に記述
4. バリデーションルールが充実

---

## 🎯 修正の優先順位

| 優先度 | 問題 | 対象 | 難度 |
|--------|------|------|------|
| 🔴 **1番目** | #1 古いパス参照 | AI_GUIDELINES.md | 低 |
| 🔴 **2番目** | #2 テーブル乖離 | HIERARCHY_RULES.md | 低 |
| 🟠 **3番目** | #3 複数文書の優先順位不明 | 新規セクション追加 | 中 |
| 🟡 **4番目** | #4 読む順序不明 | .github/copilot-instructions.md | 低 |
| 🟡 **5番目** | #5 プロジェクト構造図 | .github/copilot-instructions.md | 低 |

---

## 📋 修正アクション計画

### Action-1: AI_GUIDELINES.md 修正（優先度🔴）

**修正内容**:
1. Tier 2 セクション：`docs/operations/OPERATIONS.ja.md` → `docs/operations/current/20251028_OPERATIONS.ja.md`
2. Tier 2 セクション：`docs/operations/NOTE_SYNC_MANUAL.ja.md` → `docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md`
3. Tier 3 セクション：`docs/prd_*.md` → `docs/prd/active/{YYYYMMDD}_{slug}.ja.md`

**予想修正行数**: 約 10 行

---

### Action-2: HIERARCHY_RULES.md 修正（優先度🔴）

**修正内容**:
1. Tier 2 テーブル（Line 158-159）のファイルパスを新形式に統一
2. Tier 3 テーブル（Line 192-194）のファイルパスを新形式に統一
3. 関連する説明文を更新

**予想修正行数**: 約 15 行

---

### Action-3: 権威性マトリクス作成（優先度🟠）

**新規セクション**: `docs/governance/SSOT_PRIORITY_MATRIX.md` (新規作成)

**内容**:
```markdown
## 複数ガバナンス文書における優先順位

### 原則: YAML > Markdown > その他

| 文書 | Tier | 形式 | 優先度 | 用途 |
|------|------|------|--------|------|
| DOCUMENTATION_STRUCTURE.yml | 0 | YAML | 🥇 1番目 | 機械的判定・スクリプト処理 |
| NAMING_DECISION_SUMMARY.md | 0 | Markdown | 🥈 2番目 | 人間向け説明・決定経緯 |
| HIERARCHY_RULES.md | 0 | Markdown | 🥈 2番目 | 人間向け詳細説明 |
| AI_GUIDELINES.md | 0 | Markdown | 🥈 2番目 | AI向け実装ガイド |
| INDEX.md | 0 | Markdown | 🥉 3番目 | 参考用index |

### 矛盾時の解決フロー

1. DOCUMENTATION_STRUCTURE.yml を確認（正源）
2. 他の文書が古い場合は → ADR作成 → 統一
```

---

### Action-4: 新規訪問者向けガイド作成（優先度🟡）

**新規セクション**: `docs/governance/README.md` に追加

**内容**:
```markdown
## 🚀 初めてここに来た方へ

### 最初に読むべきドキュメント（優先順）

1. **このファイル** (`docs/governance/README.md`) - 2分で全体像
2. **HIERARCHY_RULES.md** - 階層構造を理解
3. **AI_GUIDELINES.md** (AIの場合) / **HIERARCHY_RULES.md** (人間の場合)
4. **DOCUMENTATION_STRUCTURE.yml** (詳細な仕様確認)

### クイック判定フロー

「ドキュメントをどこに置くべき？」
→ DOCUMENTATION_STRUCTURE.yml の `ai_decision_rules` を参照
```

---

## 📊 レビュー メトリクス

### 実装状況

| 項目 | 状態 | 覚書 |
|------|------|------|
| ガバナンス層設計 | ✅ 完全 | ADR-0002, 0011, 0012 で確立 |
| YAML定義精度 | ✅ 完全 | DOCUMENTATION_STRUCTURE.yml は正確 |
| Markdown実装精度 | ⚠️ 部分的 | 古い形式が散在 |
| 権威性の明確化 | ❌ なし | 複数文書の優先順位が不明 |
| 新規訪問者ガイド | ⚠️ 部分的 | フロー図が必要 |

### 新規訪問者の混乱度（推定）

**現状**:
```
100% 確実に混乱する箇所：
  ├─ docs/operations/current/ vs docs/operations/ の違い（複数文書で形式が異なる）
  ├─ docs/prd/active/ vs docs/prd_*.md の違い
  └─ どの文書が権威か不明（複数に矛盾した情報）
```

**修正後（予想）**:
```
混乱リスク: 5% 以下（大幅改善）
```

---

## 🔗 関連ドキュメント

- [ADR-0002: ドキュメント命名規則とディレクトリ構造の確立](../decisions/active/2025/10/20251028_0002_naming-structure_documentation.md)
- [ADR-0011: ファイル名ケース規則の明確化](../decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md)
- [ADR-0012: ハイフン・アンダースコア使い分けルール](../decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md)

---

## 📝 結論

### 総合評価

**ガバナンス体系の設計思想**: ✅ **優良**
- 層構造・命名規則・検証ルールが論理的で美学的

**実装の完全性**: ⚠️ **部分的**
- YAML・INDEX は完璧だが、Markdown に古い形式が残存
- 複数文書間の優先順位が不明確

**新規訪問者への親切度**: ❌ **要改善**
- 古い形式の参照が複数個所 → 誤判断リスク
- 権威文書の読む順序が不明確

### 修正による効果（推定）

| 項目 | 修正前 | 修正後 |
|------|--------|--------|
| コマンド誤実行リスク | ⚠️ 高 | ✅ 低 |
| 新規AI の質問数 | 📈 多い | 📉 少ない |
| 命名規則一貫性 | 70% | 95%+ |
| 新規訪問者の混乱度 | 30% | 5% |

### 推奨: すべてのアクションを実施

修正コストが低く（総修正行数 < 50行）、対効果が高いため、**すべてのアクション（Action-1 ～ Action-4）の実施を強く推奨**。

---

**報告書作成日**: 2025年10月29日  
**次回レビュー推奨日**: 修正完了後 + 3ヶ月

