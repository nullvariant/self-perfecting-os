---
category: documentation
date: 2025-10-29
number: 0013
status: Accepted
author: GitHub Copilot (with human validation)
---

# ADR-0013: AI Entry Point Documentation as Reference-Only

**Status**: Accepted  
**Decision Date**: 2025-10-29  
**Author**: GitHub Copilot (with human validation)  
**Related**: ADR-0002 (naming structure), ADR-0011 (filename case)

---

## Context

`.github/copilot-instructions.md` が権威文書（`docs/governance/`配下）と内容を重複し、常に同期遅れが発生していた。

### 発見された問題

ユーザーの指摘：「この文書のヒエラルキーがすでに古いんですが、ここってAIが権威文書のまえに最初に見ますよね？毎回ここの更新が忘れられてしまうのはなぜですか？」

**具体的な症状:**
- `.github/copilot-instructions.md` の L82-121（プロジェクト構造セクション）が古い
- 最近追加された `docs/log/`（Tier 4.5）が記載されていない
- INDEX.md の自動生成警告が記載されていない
- ガバナンス体系の変更が反映されていない

**重大性:**
- GitHub Copilot は権威文書（HIERARCHY_RULES.md等）を読む**前に** copilot-instructions.md を読む
- つまり、古い情報が「最初の印象」として刷り込まれる
- AIエージェントが誤った構造理解で作業を開始するリスク

### 根本原因分析

#### 1. 物理的・論理的分離
```
.github/copilot-instructions.md       （AI エントリーポイント）
docs/governance/HIERARCHY_RULES.md   （権威文書）
```
- 物理的に異なるディレクトリ
- メンタルモデル上も「別カテゴリ」として認識されやすい

#### 2. ワークフロー外
- ADR作成時のチェックリストに含まれていない
- `scripts/record_decision.py` も copilot-instructions を考慮しない
- `docs/operations/DOCUMENTATION_UPDATE_CHECKLIST.md` にも記載なし

#### 3. DRY原則違反（Don't Repeat Yourself）
- プロジェクト構造を複数ファイルで重複記述
- 同期機構なし
- 変更時に「全ての重複箇所」を思い出す必要がある（人間の記憶に依存）

---

## Decision

`.github/copilot-instructions.md` を**参照型（Reference-Only）**に変更する。

### 新しい設計原則

**DRY（Don't Repeat Yourself）の徹底:**
```
❌ 詳細を重複記述 → 同期漏れ必然
✅ 概要 + 権威文書への参照 → Single Source of Truth
```

**実装方針:**
1. **概要のみ記載** - 最低限の構造理解（数行程度）
2. **権威文書への明示的参照** - HIERARCHY_RULES.md, DOCUMENTATION_STRUCTURE.yml, AI_GUIDELINES.md
3. **警告文の追加** - 「⚠️ 重要: この構造図は概要のみです。最新の詳細は必ず上記権威文書を参照してください。」

### 変更内容

**Before（L82-121）:**
```markdown
### 4. プロジェクト構造の理解

```
nullvariant/
├── docs/
│   ├── decisions/                    # 🏆 ADR（全ての重要な決定）
（中略：40行の詳細な構造図）
```

詳細は以下を参照：
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 機械可読形式の階層定義
（以下略）
```

**After:**
```markdown
### 4. プロジェクト構造の理解

**📚 詳細は権威文書を参照してください:**

- **[docs/governance/HIERARCHY_RULES.md](../docs/governance/HIERARCHY_RULES.md)** - 人間向け階層ルール説明（最新の構造図あり）
- **[docs/governance/DOCUMENTATION_STRUCTURE.yml](../docs/governance/DOCUMENTATION_STRUCTURE.yml)** - 機械可読形式の階層定義
- **[docs/governance/AI_GUIDELINES.md](../docs/governance/AI_GUIDELINES.md)** - AI向けドキュメント記録ガイドライン

**クイックリファレンス（概要のみ・詳細は上記権威文書を参照）:**

```
nullvariant/
├── docs/
│   ├── decisions/         # 🏆 Tier 0: ADR（全ての重要な決定）
（中略：簡潔な構造図、重要な警告のみ含む）
```

**⚠️ 重要**: この構造図は概要のみです。最新の詳細は必ず上記権威文書を参照してください。
```

---

## Consequences

### ✅ Positive

1. **同期漏れの根絶**
   - 詳細は1箇所（HIERARCHY_RULES.md）のみ
   - copilot-instructions.md は参照するのみ
   - 更新忘れが構造的に不可能

2. **メンテナンス負荷の削減**
   - 構造変更時の更新箇所が1箇所に
   - 「どこを更新すべきか」を思い出す必要なし

3. **権威の明確化**
   - 「最新情報はどこか」が明白
   - AIエージェントも人間も同じ権威文書を参照

4. **拡張性の向上**
   - 新しい構造追加時も権威文書のみ更新
   - copilot-instructions.md は変更不要

### ⚠️ Negative

1. **間接参照のコスト**
   - AIが2つのファイルを読む必要がある
   - ただし、GitHub Copilot は複数ファイル参照が得意なので影響軽微

2. **クイックリファレンスの陳腐化リスク**
   - 概要図も古くなる可能性
   - 対策：概要を極力簡潔に（Tier構造と主要ディレクトリのみ）

### 📋 Mitigation

- **概要図の最小化**: Tier 0-4.5 の存在と主要ディレクトリ名のみ
- **明示的警告**: 「⚠️ 重要」セクションで権威文書参照を強調
- **リンクの正確性**: 相対パス `../docs/governance/` の検証

---

## Alternatives Considered

### A案: 採択（参照型）
```
概要（数行）+ 権威文書への参照
```
**メリット**: DRY徹底、同期漏れ根絶  
**デメリット**: 間接参照コスト

### B案: 自動同期スクリプト
```
scripts/sync_copilot_instructions.py
HIERARCHY_RULES.md → copilot-instructions.md への自動転記
```
**却下理由**: 
- スクリプト実行を忘れるリスク（人間の記憶依存）
- CI/CDに組み込むとしても、Pre-commit hookは重い
- 本質的にDRY違反を継続

### C案: チェックリスト強化
```
scripts/record_decision.py にcopilot-instructions更新リマインダー追加
```
**却下理由**:
- 人間の記憶・注意力に依存（今回の問題の根本原因）
- ADR作成以外の変更（PRD、運用手順等）でも更新が必要だが、検出不可能

---

## Validation

### 変更前後の比較

| 項目 | Before | After |
|------|--------|-------|
| copilot-instructions.md の行数 | 40行（詳細構造図） | 15行（概要+参照） |
| 同期が必要な箇所 | 2箇所（copilot + HIERARCHY） | 1箇所（HIERARCHY のみ） |
| 更新忘れリスク | 高（人間の記憶依存） | 低（構造的に防止） |
| AIの読み取りコスト | 1ファイル | 2ファイル |

### 実装確認

- ✅ copilot-instructions.md を参照型に変更済み
- ✅ 権威文書へのリンク追加（HIERARCHY_RULES.md, DOCUMENTATION_STRUCTURE.yml, AI_GUIDELINES.md）
- ✅ 明示的警告文追加（「⚠️ 重要」セクション）
- ✅ クイックリファレンスを最小化（Tier 0-4.5 + 主要ディレクトリのみ）

---

## Implementation

### 変更ファイル

1. `.github/copilot-instructions.md`
   - L82-121: 詳細構造図削除 → 参照型に置換
   - 新規: 権威文書への明示的リンク追加
   - 新規: 警告文追加

### 今後の運用

**権威文書更新時（HIERARCHY_RULES.md等）:**
- copilot-instructions.md の更新は**不要**
- ただし、概要図が大幅に変わる場合（新Tier追加等）のみ、概要も調整

**copilot-instructions.md の役割（明確化）:**
- AI エージェントへの「最初の道案内」
- 詳細は権威文書へ誘導
- 概要は「Tierの存在」と「主要ディレクトリ」のみ

---

## Related Decisions

- **ADR-0002**: 命名規則とディレクトリ構造（HIERARCHY_RULES.md が権威）
- **ADR-0011**: ファイル名ケース規則（大文字 vs 小文字）
- **ADR-0012**: ハイフン・アンダースコア規則

---

## Summary

`.github/copilot-instructions.md` を**参照型（Reference-Only）**に変更することで、権威文書の分散を防ぎ、同期漏れを構造的に根絶した。

**核心原則:**
```
詳細を重複させない（DRY）
概要のみ記載 + 権威文書への参照
```

これにより、ユーザーが毎回同期を指摘する負担を解消し、AIエージェントが常に最新の構造を参照できる体制を確立した。

**今後の拡張:**
- 新しい構造追加 → HIERARCHY_RULES.md のみ更新
- copilot-instructions.md は変更不要（参照が自動的に最新を指す）

---

**Status**: ✅ **ACCEPTED**  
**Implementation**: Completed  
**Last Updated**: 2025-10-29
