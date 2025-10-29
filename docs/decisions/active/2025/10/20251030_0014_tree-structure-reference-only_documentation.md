# ADR-0014: Tree Structure Reference-Only Design

**Status**: Active  
**Decision Date**: 2025-10-30  
**Author**: GitHub Copilot (with human validation)  
**Related**: ADR-0013 (copilot-instructions.md reference-only design)

---

## Context

### 問題の発生

ユーザーからの指摘：
> "表玄関README.mdで書かれているツリーが古いじゃん。権威文書にもツリーがあるじゃん。結局、二重管理かよ・・・ツリー構造が書かれているドキュメントが最新になるように部分的に自動化できないものか。構造が変わるたびにドキュメント修正するの鬱陶しい"

### 根本原因

複数のREADMEファイルに重複したツリー構造が記載されており、リポジトリ構造が変更されるたびに手動で同期する必要があった：

1. **README.md (root)** - L50-130
   - 全リポジトリ構造を詳細に記載（絵文字付き）
   - 全サブディレクトリ、個別ファイル名まで列挙
   - operations/current/ の4ファイルを具体的に記載

2. **docs/README.md** - L24-40
   - docs/ サブディレクトリ構造を記載
   - decisions/, governance/, prd/, operations/ の階層を表示

3. **docs/operations/README.md** - L15-25
   - operations/ サブディレクトリ構造を記載
   - current/, archive/ の具体的なファイル一覧を表示

### DRY違反

同じ情報（ツリー構造）が3箇所に重複して記載されており、以下の問題が発生：

- リポジトリ構造変更時、3箇所全てを手動更新する必要がある
- 更新漏れにより不整合が発生するリスク
- メンテナンス負荷の増大

### 既存の権威文書

ユーザーの重要な指摘：
> "権威文書がすでに複数あるのでまたREADMEを権威文書として指定したら今度はあなたたちAIが判断ミスをする。せっかくヒエラルキーについての権威文書があるんだからREADMEからは全部見せる必要なく参照でいいのでは"

既に以下の権威文書が存在：
- `docs/governance/HIERARCHY_RULES.md` - 人間向け階層ルール説明
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 機械可読形式の構造定義

---

## Decision

**参照専用（Reference-Only）デザインを採用**

### 実装内容

1. **全てのREADMEから詳細なツリー構造を削除**
   - 最小限の概要情報のみ残す
   - ディレクトリの目的説明は保持

2. **権威文書への参照を追加**
   - README.md (root): `docs/governance/HIERARCHY_RULES.md` への参照
   - docs/README.md: `./governance/HIERARCHY_RULES.md` および `./governance/DOCUMENTATION_STRUCTURE.yml` への参照
   - docs/operations/README.md: `../../governance/HIERARCHY_RULES.md` への参照

3. **権威文書は変更しない**
   - `HIERARCHY_RULES.md` と `DOCUMENTATION_STRUCTURE.yml` が唯一の権威
   - READMEは「ナビゲーション」の役割に徹する

### 採用理由

1. **Phase 7 ADR-0013と同じパターン**
   - copilot-instructions.md で既に成功した参照専用デザイン
   - ユーザーフィードバック: "参照型がいいです。権威文書があちこち分散するのが嫌です"

2. **AI混乱の防止**
   - READMEを新たな権威文書として扱わない
   - AIエージェントが参照すべき文書が明確になる

3. **既存インフラの活用**
   - governance/ ディレクトリは既に権威文書として機能している
   - 新たな自動化システムは不要

4. **保守性の向上**
   - リポジトリ構造変更時、1箇所（HIERARCHY_RULES.md）のみ更新
   - 手動同期作業の完全廃止

---

## Alternatives Considered

### A案: 自動生成スクリプト

**案**: READMEのツリー構造を自動生成するスクリプトを作成

**却下理由**:
- 新たな自動化システムの実装・保守コストが発生
- READMEを権威文書として扱うことになり、AI混乱のリスク
- ユーザーの望む「参照型」ではない

### B案: READMEを権威文書として指定

**案**: READMEを新たな権威文書として `docs/governance/` に位置づける

**却下理由**:
- ユーザーの明示的な拒否: "またREADMEを権威文書として指定したら今度はあなたたちAIが判断ミスをする"
- 権威文書の分散化（governance/ と README の二重管理）
- 既に HIERARCHY_RULES.md が存在するため冗長

### C案: ハイブリッド（簡略版ツリー + 参照）

**案**: READMEに簡略版ツリーを残しつつ、詳細は参照

**却下理由**:
- 結局「どこまで簡略化するか」の判断が必要
- 簡略版でも同期コストが残る
- ユーザーの希望: "READMEからは全部見せる必要なく参照でいいのでは"

---

## Consequences

### ✅ Positive

1. **メンテナンス負荷の劇的削減**
   - リポジトリ構造変更時、HIERARCHY_RULES.md のみ更新
   - 3箇所の手動同期作業が不要に

2. **権威の一元化**
   - governance/ ディレクトリが唯一の権威
   - AIエージェントの混乱を防止

3. **実績のあるパターン**
   - ADR-0013 で既に成功
   - ユーザー満足度: "参照型がいいです"

4. **実装コストゼロ**
   - 新たなスクリプトやシステム不要
   - 既存の governance/ インフラを活用

### ⚠️ Negative

1. **ナビゲーションの利便性低下**
   - README から構造全体が一目で見えなくなる
   - 1クリック多く必要（参照先へ移動）

2. **初見ユーザーへの配慮**
   - 構造を知りたい新規ユーザーは governance/ へ誘導される
   - README だけでは全体像が把握しづらい

### 📋 Mitigation

**ナビゲーション性の担保**:
- 主要ディレクトリの目的説明は README に保持
- 絵文字ナビゲーションで視認性維持
- 参照リンクを明確に表示

**初見ユーザー対応**:
- governance/HIERARCHY_RULES.md を「人間向け」に記述
- 図解・例示を含む丁寧な説明
- 「権威文書だが読みやすい」バランス

---

## Implementation

### 変更ファイル

1. **README.md (root)**
   - 詳細ツリー（L50-130）を削除
   - 主要ディレクトリ概要 + 参照リンクへ変更

2. **docs/README.md**
   - ツリー構造（L24-40）を削除
   - 参照リンク + 主要ディレクトリ説明へ変更

3. **docs/operations/README.md**
   - ツリー構造（L15-25）を削除
   - 参照リンク + ディレクトリ概要へ変更

4. **ADR-0014 (このファイル)**
   - 決定の記録

### 実装日

2025-10-30

### コミットメッセージ

```
docs: Eliminate tree structure duplication (ADR-0014)

- Remove detailed trees from README.md, docs/README.md, docs/operations/README.md
- Add references to authoritative governance/HIERARCHY_RULES.md
- Maintain minimal overview for navigation
- Create ADR-0014 documenting reference-only design

Resolves: Tree structure DRY violation
Pattern: Same as ADR-0013 (copilot-instructions.md reference-only)
User request: '構造が変わるたびにドキュメント修正するの鬱陶しい'

Changes:
- README.md: Simplified tree, added reference
- docs/README.md: Removed tree, added reference  
- docs/operations/README.md: Removed tree, added reference
- ADR-0014: Documented decision
```

---

## Validation

### 成功基準

- [ ] 全てのREADMEから詳細ツリーが削除されている
- [ ] 参照リンクが正しく設定されている（相対パス検証）
- [ ] 最小限のナビゲーション情報は保持されている
- [ ] governance/HIERARCHY_RULES.md が存在し、最新である

### テスト方法

```bash
# 参照リンクの検証
ls -la docs/governance/HIERARCHY_RULES.md
ls -la docs/governance/DOCUMENTATION_STRUCTURE.yml

# READMEでツリー構造が残っていないか確認
grep -n "^├──\|^│" README.md docs/README.md docs/operations/README.md

# 参照リンクが含まれているか確認
grep -n "HIERARCHY_RULES.md" README.md docs/README.md docs/operations/README.md
```

---

## Related Decisions

- **ADR-0013**: copilot-instructions.md reference-only design
  - 同じ参照専用パターンを採用
  - ユーザー満足度: "参照型がいいです。権威文書があちこち分散するのが嫌です"

- **ADR-0010**: Governance audit report
  - ドキュメント整合性の重要性を認識
  - DRY原則違反の検出

- **ADR-0011**: Filename case convention
  - governance/ ディレクトリの権威性を確立
  - メタドキュメント vs 流動ドキュメントの区別

---

## Summary

本ADRは、**ツリー構造のDRY違反を解消**するため、**参照専用デザイン**を採用した。

**核心原則**:
- READMEは「ナビゲーション」、governance/ は「権威」
- 権威文書の分散化を避ける（AI混乱防止）
- 既存インフラ（HIERARCHY_RULES.md）を活用

**Phase 7 との類似性**:
| Phase 7 (ADR-0013) | Phase 9 (ADR-0014) |
|-------------------|-------------------|
| copilot-instructions.md 重複 | Tree structure 重複 |
| governance ルール重複 | リポジトリ構造重複 |
| 参照専用デザイン | 参照専用デザイン |
| ユーザー満足 | 期待される満足 |

**ユーザーの言葉**:
- "権威文書があちこち分散するのが嫌です"
- "せっかくヒエラルキーについての権威文書があるんだから"
- "READMEからは全部見せる必要なく参照でいいのでは"

この決定により、リポジトリ構造変更時の手動同期作業が完全に廃止され、保守性が大幅に向上する。

---

**Status**: ✅ **ACTIVE**  
**Implementation**: Complete  
**Last Updated**: 2025-10-30
