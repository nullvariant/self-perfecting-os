# ADR-0011: ファイル名ケース規則の明確化（大文字 vs 小文字）

**Status**: Accepted  
**Decision Date**: 2025-10-29  
**Author**: GitHub Copilot (with human validation)  
**Supersedes**: Clarifies ambiguity in ADR-0002/0003  
**Related**: ADR-0002 (naming structure), ADR-0003 (lowercase-hyphen unification)

---

## Context

ガバナンス監査（ADR-0010）の過程で、命名規則に**矛盾**が発見された：

- **ADRファイル**: 全て小文字 + ハイフン（`20251028_0001_ci-cd-pause_architecture.md`）
- **PRDファイル**: 全て小文字 + ハイフン（`20251028_documentation-governance.ja.md`）
- **運用手順書**: 大文字のまま（`20251028_OPERATIONS.ja.md`）

なぜこの差別化が存在するのか、**根拠がドキュメントに記載されていなかった**。

### 観察：業界慣習パターン

プロジェクト直下の「標準ファイル」は全て大文字：

```
README.md           ← 業界標準
CHANGELOG.md        ← 業界標準
AGENT.md            ← 仕様書（重要メタ）
CONTRIBUTING.md     ← 業界標準
LICENSE             ← 業界標準
Makefile            ← 業界標準
```

**パターン認識**: 「プロジェクト説明・参照対象のメタドキュメント」は慣習的に大文字

---

## Decision

ファイル名のケースを、**ドキュメント性質による二軸**で明確に定義する：

### 大文字（慣習的メタドキュメント）

**適用対象**:
- プロジェクト/docs ルート直下の「参照基準ドキュメント」
- 「このプロジェクトについて説明するドキュメント」
- 業界で確立された標準命名
- **固定的・参照対象・業務重要度が高い** 運用手順書

**具体例**:
```
プロジェクトルート:
  README.md              ← プロジェクト概要
  CHANGELOG.md           ← バージョン履歴
  AGENT.md               ← 仕様書（最重要メタ）
  CONTRIBUTING.md        ← 貢献ガイド
  LICENSE                ← ライセンス
  Makefile               ← ビルドスクリプト

docs/ 配下（メタドキュメント）:
  docs/README.md
  docs/governance/README.md
  docs/governance/NAMING_DECISION_SUMMARY.md
  docs/governance/DOCUMENTATION_STRUCTURE.yml
  docs/governance/HIERARCHY_RULES.md
  docs/governance/AI_GUIDELINES.md
  docs/operations/current/OPERATIONS.ja.md         ← 実行必須
  docs/operations/current/NOTE_SYNC_MANUAL.ja.md   ← 手順参照
  docs/operations/current/WORKFLOW_TEXT_ASSETS.ja.md
```

**理由**:
- ✅ 業界標準慣習による直感的認識（README は誰もが大文字で探す）
- ✅ ファイル一覧表示時に「重要度」が視覚的に区別
- ✅ 「固定的・参照対象・不変性」をケースで表現
- ✅ 運用上の重要な参照資料であることを示す

---

### 小文字 + ハイフン（URLフレンドリー・流動的）

**適用対象**:
- 日付付きドキュメント（**流動する履歴**）
- 意思決定記録（ADR）、要件定義（PRD）
- プログラマティック処理対象（スクリプト生成）
- 将来変更・更新される可能性のあるドキュメント

**具体例**:
```
docs/decisions/active/2025/10/:
  20251028_0001_ci-cd-pause_architecture.md
  20251028_0002_naming-structure_documentation.md
  20251028_0003_lowercase-hyphen-unification_documentation.md
  20251029_0011_filename-case-convention_documentation.md

docs/prd/active/:
  20251028_documentation-governance.ja.md
  20251029_dialogue-log-persistence.ja.md
```

**理由**:
- ✅ URLフレンドリー（ハイフン使用時はスラッシュと混同しない）
- ✅ プログラマティック処理に適合（正規表現: `\d{8}_\d{4}_[a-z0-9-]+_[a-z]+\.md`）
- ✅ セマンティック一貫性（日付順ソート = タイムラインとして解釈可能）
- ✅ grep/find/スクリプト処理が簡単
- ✅ 「流動的・変更可能・歴史的記録」をケースで表現

---

## Consequences

### ✅ Positive

1. **明確な視覚的区別** - メタ（大文字）vs 流動（小文字）が一目瞭然
2. **プログラマティック処理** - 小文字ファイルは正規表現で統一パターン
3. **業界慣習との調和** - README, CHANGELOG など既存慣習を尊重
4. **スケーラビリティ** - 50個以上のADRが増えても処理ルール統一
5. **直感性** - ファイル一覧で「重要度」が把握可能

### ⚠️ Negative

1. **複雑さ増加** - ルールが「二段階判定」になる
2. **学習コスト** - 新規貢献者が「どちらのルール適用？」で迷う可能性
3. **実装負荷** - スクリプト `record_decision.py` に判定ロジック追加が必要

### 📋 Mitigation

- `docs/governance/NAMING_DECISION_SUMMARY.md` に判定フローチャート記載
- スクリプト `scripts/record_decision.py` に判定ロジック実装
- `.github/copilot-instructions.md` に詳細例示
- このADR-0011を「判定基準」として参照

---

## Alternatives Considered

### A案: 全部小文字に統一
```
20251028_operations.ja.md
20251028_note-sync-manual.ja.md
```
**却下理由**: README.md, AGENT.md との業界標準慣習齟齬が発生

### B案: 全部大文字に統一
```
OPERATIONS.ja.md
NOTE_SYNC_MANUAL.ja.md
20251028_0001_CI_CD_PAUSE_ARCHITECTURE.md
```
**却下理由**: 
- URLフレンドリー性喪失
- スクリプト処理複雑化
- 検索サーチングで誤検出増加

### C案: 採択（本ADR）
業界慣習（大文字メタドキュメント）+ URLフレンドリー（小文字流動ドキュメント）

---

## Validation

### 現在の適合状況

**✅ 既に遵守している場所**:
```
README.md, CHANGELOG.md, AGENT.md      ← 大文字（慣習）OK
docs/decisions/20251028_000X_*.md      ← 小文字（流動）OK
docs/prd/active/20251028_*.ja.md       ← 小文字（流動）OK
docs/operations/OPERATIONS.ja.md       ← 大文字（メタ）OK
```

**⚠️ 確認・調整が必要な場所**:
```
docs/governance/README.md              ← 大文字で OK（メタドキュメント）
docs/governance/NAMING_DECISION_SUMMARY.md ← 大文字で OK（メタドキュメント）
docs/governance/HIERARCHY_RULES.md     ← 大文字で OK（メタドキュメント）
docs/governance/AI_GUIDELINES.md       ← 大文字で OK（メタドキュメント）
docs/operations/README.md              ← 大文字で OK（メタドキュメント）
```

結論: **既にほぼ従っている。このADRは「根拠の明示」が主目的**

---

## Implementation

### スクリプト実装（scripts/record_decision.py）

```python
def determine_filename_casing(doc_type, is_dated=False):
    """
    判定ロジック：
    - doc_type: 'adr', 'prd', 'ops', 'readme', 'governance'
    - is_dated: 日付付きか（流動ドキュメント）
    
    Returns: casing rule ('UPPERCASE' or 'lowercase')
    """
    # メタドキュメント（大文字）
    META_DOCS = ['ops', 'readme', 'governance', 'handbook', 'manual']
    if doc_type in META_DOCS:
        return 'UPPERCASE'
    
    # 流動ドキュメント（小文字 + ハイフン）
    if is_dated and doc_type in ['adr', 'prd']:
        return 'lowercase-hyphen'
    
    # デフォルト（業界慣習に合わせて大文字）
    return 'UPPERCASE'
```

### ドキュメント更新

1. `docs/governance/NAMING_DECISION_SUMMARY.md` に判定フローチャート追加
2. `.github/copilot-instructions.md` に例示テーブル追加
3. `scripts/README.md` に実装ノート追加

---

## Related Decisions

- **ADR-0002**: 命名規則とディレクトリ構造（このADRで補足）
- **ADR-0003**: lowercase-hyphen 統一（流動ドキュメント対象を明確化）
- **ADR-0010**: ガバナンス監査報告（このADRの発端）

---

## Summary

このADRは、**ルール自体の根拠が不在だった欠陥を正す「メタレベルの決定」**である。

ガバナンス監査を通じて発見された矛盾「なぜ OPERATIONS は大文字か？」→ **業界慣習 + URLフレンドリーの両立**という原則に至った。

これにより、将来のAIやコントリビューターが以下を実現できる：

✅ 「迷わず、根拠を持ってファイル名を決定できるメタレベルの指針」  
✅ 「メタドキュメント（大文字） vs 流動ドキュメント（小文字）の視覚的区別」  
✅ 「プログラマティック処理の統一性」

**このADR-0011は、ADR-0002/0003 の "なぜ" の部分を埋める補足決定である。**

---

**Status**: ✅ **ACCEPTED**  
**Implementation**: In Progress (scripts/record_decision.py update pending)  
**Last Updated**: 2025-10-29
