# ADR-0012: ハイフン vs アンダースコア使い分けルール

**Status**: Accepted  
**Decision Date**: 2025-10-29  
**Author**: GitHub Copilot (with human validation)  
**Related**: ADR-0011 (filename case convention)

---

## Context

ファイル名規則の標準化に伴い、**ハイフン（-）とアンダースコア（_）の使い分けが曖昧**であることが判明。

### 現在の状況

```
✅ 明確な部分:
  - 日付とシーケンス番号: アンダースコア区切り（20251029_0001_）
  - 言語コード: ドット区切り（.ja.md）

❓ 曖昧な部分:
  - slug内の単語区切り: ハイフン使用？アンダースコア使用？
    例: ci-cd-pause vs ci_cd_pause
    例: naming-structure vs naming_structure
```

### パターン観察

**URLフレンドリーな小文字ファイル群：**
```
20251028_0001_ci-cd-pause_architecture.md         ← ハイフン
20251028_0003_lowercase-hyphen-unification_documentation.md  ← ハイフン
20251028_0004_github-actions-doc-validation_tooling.md        ← ハイフン
20251029_0011_filename-case-convention_documentation.md       ← ハイフン
```

**観察**: ADRやPRDのslugにはハイフンが統一されている（実装済み）

**しかし疑問**:
- なぜハイフンなのか？（根拠がドキュメント化されていない）
- アンダースコアを使う場面はあるのか？

---

## Decision

ハイフン（-）とアンダースコア（_）の使い分けを、**機能別**に明確に定義する：

### 🔹 アンダースコア（_）：構造区切り

**用途**: ファイル名の**主要なセクション区切り**

| 位置 | 例 | 役割 |
|------|-----|------|
| 日付とシーケンス | `20251029_0011` | タイムスタンプと通し番号の区切り |
| シーケンスとslug | `0011_filename-case` | 番号とコンテンツの区切り |
| slugとカテゴリ | `filename-case_documentation` | 内容とドキュメント種別の区切り |

**理由**:
- ✅ **構造的区別**: 視覚的に「ここで大きく区切られている」が明確
- ✅ **読みやすさ**: アンダースコアは区切り感が強い
- ✅ **パーサビリティ**: スクリプト処理で「主要フィールド」を抽出しやすい

**例**:
```
20251029_0012_hyphen-underscore-convention_documentation.md
           ↑                                 ↑
      主要区切り                       主要区切り
```

---

### 🔸 ハイフン（-）：意味内の単語区切り

**用途**: **slug内の複数単語を繋ぐ**（URLフレンドリー）

| 位置 | 例 | 理由 |
|------|-----|------|
| slug内 | `ci-cd-pause` | 単語 + 単語の繋ぎ（URLフレンドリー） |
| slug内 | `filename-case-convention` | 複合概念を表現 |
| オペレーション名 | `NOTE-SYNC-MANUAL` | ？（未決定） |

**理由**:
- ✅ **URLフレンドリー**: ハイフンはURLで問題なし、アンダースコアは時に問題（言語/サーバー依存）
- ✅ **標準慣習**: REST API, URL, ケバブケースはハイフンが業界標準
- ✅ **検索性**: ハイフン区切りは検索エンジンで単語認識される
- ✅ **可読性**: slug内の複数単語はハイフンで結合が最も読みやすい

**例**:
```
20251029_0012_hyphen-underscore-convention_documentation.md
                └─ slug内はハイフン ─┘
```

---

## Visual Rule Table

```
ファイル名構造:

{YYYYMMDD} _ {NNNN} _ {slug} _ {category} . {ext}
     ↓        ↓         ↓        ↓
   日付    アンダー   ハイフン   アンダー
   (数字)   スコア    (複合概念)  スコア
          ====== 主要区切り ======
                    └──── URLフレンドリー ────┘


具体例:

20251029_0012_hyphen-underscore-convention_documentation.md
├─ 20251029      : 日付（アンダースコア後に続く）
├─ 0012          : シーケンス番号
├─ hyphen-underscore-convention : slug（単語はハイフン繋ぎ）
├─ documentation : カテゴリ
└─ .md           : 拡張子
```

---

## Reference Implementation

### ✅ 正しいパターン（従うべき）

```markdown
### ADR・PRDファイル
20251028_0001_ci-cd-pause_architecture.md
20251028_0002_naming-structure_documentation.md
20251028_0003_lowercase-hyphen-unification_documentation.md
20251028_0004_github-actions-doc-validation_tooling.md
20251028_0005_multilingual-directory-structure_documentation.md
20251029_0011_filename-case-convention_documentation.md
20251029_0012_hyphen-underscore-convention_documentation.md

### 内部ファイル名（推奨ただし必須ではない）
generate-index.py      ← slug内は ハイフン
record-decision.py     ← slug内は ハイフン
validate-docs.py       ← slug内は ハイフン

### メタドキュメント（大文字、アンダースコア可）
NAMING_DECISION_SUMMARY.md     ← 大文字なのでアンダースコア
DOCUMENTATION_STRUCTURE.yml    ← 大文字なのでアンダースコア
HIERARCHY_RULES.md             ← ケバブケース（ハイフン）が標準
```

### ❌ 避けるべきパターン

```markdown
20251028_0001_ci_cd_pause_architecture.md      ← アンダースコアを slug内に使う（NG）
20251028_0002naming-structure-documentation.md ← アンダースコア区切り忘れ（NG）
20251029_hyphen_underscore_convention_docs.md  ← アンダースコアとハイフン混在（NG）
```

---

## Rationale

### なぜ「アンダースコア＝構造」「ハイフン＝意味」か？

#### 1. URLフレンドリー原則

```
URL例:
https://docs.example.com/decisions/20251029_0012_hyphen-underscore-convention/

✅ ハイフン: 検索エンジンが「hyphen」「underscore」「convention」を
           3つの別単語として認識
           
❌ アンダースコア: 「hyphen_underscore_convention」を
                 1つの単語として認識（SEO低下）
```

#### 2. 可読性 + 検索性の両立

```
❌ 全部アンダースコア:
   ci_cd_pause_architecture
   →「記号多く、読みづらい」

✅ 混在（アンダー=構造、ハイフン=意味）:
   ci-cd-pause_architecture
   → 「主構造は明確（アンダースコア）、意味内容は読みやすい（ハイフン）」
```

#### 3. プログラマティック処理

```python
# ハイフン + アンダースコア混在なら、簡単に解析可能
filename = "20251029_0012_hyphen-underscore-convention_documentation.md"

# パターン: YYYYMMDD_NNNN_slug_category.md
import re
pattern = r'(\d{8})_(\d{4})_([a-z0-9-]+)_([a-z]+)\.md'
match = re.match(pattern, filename)

date, seq, slug, category = match.groups()
# date='20251029', seq='0012', slug='hyphen-underscore-convention', category='documentation'

# slug内の単語を抽出
words_in_slug = slug.split('-')  # ← ハイフンで分割
# words_in_slug = ['hyphen', 'underscore', 'convention']
```

---

## Consequences

### ✅ Positive

1. **明確性**: ハイフン＝意味、アンダースコア＝構造が一目瞭然
2. **検索性**: URLフレンドリーでSEO最適化
3. **一貫性**: 全ファイル名が同じルールで予測可能
4. **プログラマティック処理**: スクリプトで容易に解析可能

### ⚠️ Negative

1. **学習コスト**: 「なぜ混在？」という質問が増える可能性
2. **タイピング負荷**: ハイフン↔アンダースコアを使い分ける手間

### 📋 Mitigation

- このADRを権威文書として参照可能にする
- `scripts/record_decision.py` に自動フォーマッティング実装
- `.github/copilot-instructions.md` に具体例を多数記載

---

## Alternatives Considered

### A案: 全部ハイフン
```
20251029-0012-hyphen-underscore-convention-documentation.md
```
**却下理由**: 
- 日付（2025-10-29）とファイル名が混同
- 主要セクション（日付・シーケンス・slug・カテゴリ）の区別が不明確

### B案: 全部アンダースコア
```
20251029_0012_hyphen_underscore_convention_documentation.md
```
**却下理由**:
- URLフレンドリー性が損なわれる
- slug内が長くなると可読性低下

### C案: 採択（本ADR）
```
20251029_0012_hyphen-underscore-convention_documentation.md
```
アンダースコア＝構造区切り、ハイフン＝意味内容 の混在

---

## Implementation Checklist

- [ ] `docs/governance/NAMING_DECISION_SUMMARY.md` にこのルール記載
- [ ] `.github/copilot-instructions.md` に具体例テーブル追加
- [ ] `scripts/record_decision.py` に自動フォーマット実装
- [ ] `scripts/validate_docs.py` に命名検証ロジック追加
- [ ] 既存ファイルが本ルールに適合しているか確認
- [ ] 今後のADR作成時の参考テンプレート更新

---

## Summary

本ADRは、**ハイフン vs アンダースコア**という「技術的」に見える問題の背後にある**「意図の明確化」**を目指すものである。

**ルール**:
- 🔹 **アンダースコア** = ファイル名の主要セクション区切り（日付・シーケンス・slug・カテゴリ）
- 🔸 **ハイフン** = slug内の複数単語繋ぎ（URLフレンドリー・検索最適化）

これにより、ファイル一覧を見ただけで：
1. 「どこまでが日付か」 → アンダースコアで見える
2. 「どこからがslugか」 → アンダースコアで見える
3. 「slug内の単語は何か」 → ハイフンで分割可能
4. 「これはURLとしても使える」 → ハイフンだから安全

という多層的な情報が自動的に読み取れる。

---

**Status**: ✅ **ACCEPTED**  
**Implementation**: Ready for integration into NAMING_DECISION_SUMMARY.md  
**Last Updated**: 2025-10-29
