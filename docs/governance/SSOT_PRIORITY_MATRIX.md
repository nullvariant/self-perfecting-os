# SSOT Priority Matrix: 複数ガバナンス文書の権威性と優先順位

**Status**: Reference  
**Last Updated**: 2025-10-29  
**Purpose**: 複数のガバナンス文書が存在する場合、どの文書が「真実の源（SSOT: Single Source of Truth）」であるかを明確に定義する

---

## 概要

nullvariant リポジトリのガバナンス体系には、複数の権威文書が存在する：

- YAML形式（機械可読）: `docs/governance/DOCUMENTATION_STRUCTURE.yml`
- Markdown形式（人間向け）: `docs/governance/AI_GUIDELINES.md`, `HIERARCHY_RULES.md`
- ADR（決定記録）: `docs/decisions/active/`
- スクリプト仕様: `scripts/record_decision.py`, `validate_docs.py`

これらが **矛盾する場合の優先順位** を定義するドキュメント。

---

## 権威性レベルの定義

### 🥇 Level 1: YAML スペック（最高権威）

| 文書 | URL | 役割 | 対象システム | 更新責任 |
|-----|-----|------|------------|---------|
| `DOCUMENTATION_STRUCTURE.yml` | `docs/governance/DOCUMENTATION_STRUCTURE.yml` | 機械可読型のドキュメント構造定義 | スクリプト・CI/CD | validation scripts |
| `agent.schema.json` | `spec/agent.schema.json` | Agentシステムのスキーマ | 仕様検証 | structure change ADR |

**特性**:
- ✅ バージョン管理が厳密（Git履歴で追跡可能）
- ✅ スクリプト処理による一貫性強制
- ✅ 破壊的変更の検知が容易
- ❌ 人間が直接参照しづらい

**矛盾時の対応**:
→ YAML/JSON が正しい。Markdown ドキュメントは同期がズレている

---

### 🥈 Level 2: ADR（アーキテクチャ決定記録）

| ADR | 対象 | 優先度 | 更新頻度 |
|-----|------|--------|---------|
| ADR-0002 | 命名規則とディレクトリ構造 | ⭐⭐⭐⭐ | 確定 |
| ADR-0003 | lowercase-hyphen 統一化 | ⭐⭐⭐⭐ | 確定 |
| ADR-0005 | ドキュメント階層・ポリシー | ⭐⭐⭐⭐ | 確定 |
| ADR-0011 | ファイル名ケース規則（大文字 vs 小文字） | ⭐⭐⭐ | 確定 |
| ADR-0012 | ハイフン vs アンダースコア | ⭐⭐⭐ | 確定 |

**特性**:
- ✅ 決定の背景・理由が明記
- ✅ 超越（supersede）/非推奨（deprecated）の明示
- ✅ 人間にとって読みやすい
- ❌ YAML より更新が遅れる可能性あり

**矛盾時の対応**:
→ 最新の ADR が正しい。古い ADR は確認してから参照

---

### 🥉 Level 3: Markdown ガイド（補足資料）

| 文書 | 役割 | 信頼度 | 同期状態 |
|-----|------|--------|---------|
| `AI_GUIDELINES.md` | AI向けドキュメント記録ルール | ⭐⭐⭐⭐ | ✅ 2025-10-29 で同期完了 |
| `HIERARCHY_RULES.md` | ドキュメント階層の人間向け説明 | ⭐⭐⭐ | ✅ 2025-10-29 で同期完了 |
| `README.md` | ディレクトリ概要 | ⭐⭐⭐ | ⏳ 定期確認推奨 |

**特性**:
- ✅ 人間にとって最も読みやすい
- ✅ 文脈・背景の説明が豊富
- ❌ YAML と同期が漏れやすい（手動同期のため）

**矛盾時の対応**:
→ YAML/ADR が正しい。Markdown は参考資料として扱う
→ 矛盾を発見したら [Issue/PR](../operations/current/20251029_DOCUMENTATION_UPDATE_CHECKLIST.md) を作成

---

## 優先順位の決定フロー

```
矛盾を発見したか？
  ↓
【質問1】YAML と Markdown が異なる？
  → Yes: YAML が正しい
  → No: 次へ

【質問2】複数の ADR が相互に矛盾？
  → Yes: 最新の ADR（ステータス: Accepted）が正しい
  → No: 次へ

【質問3】複数の Markdown ドキュメントが異なる？
  → Yes: AI_GUIDELINES.md が正しい（最も詳細なため）
  → No: HIERARCHY_RULES.md が補足参照

【質問4】スクリプト実装と文書が矛盾？
  → Yes: スクリプト実装 が正しい
  → No: 問題なし
```

---

## ケース別対応例

### ケース1: 「ファイルは新形式？旧形式？」

| 対象 | YAML に書いてある形式 | ADR | 正しい形式 | 参照先 |
|-----|------|------|---------|--------|
| 運用手順書 | `docs/operations/current/{YYYYMMDD}_{type}.ja.md` | ADR-0002/0005 | ✅ 新形式が正しい | DOCUMENTATION_STRUCTURE.yml |
| PRD | `docs/prd/active/{YYYYMMDD}_{slug}.ja.md` | ADR-0002/0005 | ✅ 新形式が正しい | DOCUMENTATION_STRUCTURE.yml |
| ADR | `docs/decisions/active/{YYYY}/{MM}/{YYYYMMDD}_{NNNN}_{slug}_{category}.md` | ADR-0011/0012 | ✅ 新形式が正しい | DOCUMENTATION_STRUCTURE.yml |

**矛盾のパターン**:
- ❌ Markdown に旧形式（`docs/operations/OPERATIONS.ja.md`）が記載
- → YAML/ADR の新形式が正しい
- → Markdown を修正すること

### ケース2: 「ハイフン vs アンダースコアはどっち？」

| 対象 | 使用箇所 | 正しい形式 | ADR 根拠 |
|-----|----------|---------|---------|
| ファイル名の主要区切り | 日付-シーケンス-slug-カテゴリ | `20251029_0011_filename-case_documentation.md` | ADR-0012 |
| slug 内の単語繋ぎ | 複合単語 | `lowercase-hyphen` | ADR-0012 |

**参照順序**:
1. DOCUMENTATION_STRUCTURE.yml で正規表現確認
2. ADR-0012 で背景理解
3. HIERARCHY_RULES.md で人間向け説明参照

### ケース3: 「この文書は新しく作る必要がある？ADR が必要？」

```
判定フロー（優先順位順）:
1. DOCUMENTATION_STRUCTURE.yml の validation rules を確認
2. AI_GUIDELINES.md の「ADRが必要な場合」セクションを確認
3. 該当する最新 ADR を参照
4. 最後に HIERARCHY_RULES.md で事例を確認
```

---

## 同期メカニズム

### 📋 自動同期（スクリプト処理）

```bash
scripts/validate_docs.py
├─ DOCUMENTATION_STRUCTURE.yml のスキーマ検証
├─ ファイル配置の確認
└─ Markdown との矛盾検出 → レポート生成
```

**実行頻度**: 手動（CI/CDが未稼働のため）

### 🔄 手動同期（開発者による）

**優先順位付き更新フロー**:

1. **Level 1 更新** (YAML/JSON)
   - スクリプト・CI/CD 処理を含むため、まず YAML を更新
   - validation scripts に新ルール追加
   - 影響箇所を特定

2. **Level 2 更新** (ADR 作成)
   - YAML 変更の背景を ADR として記録
   - `scripts/record_decision.py` で自動生成
   - Status: Accepted になるまで待機

3. **Level 3 更新** (Markdown 同期)
   - ADR 確定後、Markdown ドキュメント全体を確認・同期
   - 対象: AI_GUIDELINES.md, HIERARCHY_RULES.md, README.md
   - 検査項目は [DOCUMENTATION_UPDATE_CHECKLIST.md](current/20251029_DOCUMENTATION_UPDATE_CHECKLIST.md) を参照

### ⏰ 同期スケジュール

| タイミング | 対象 | チェック項目 |
|-----------|------|------------|
| **即時** | YAML, スクリプト | validation 実行 |
| **24時間以内** | ADR 作成 | Status: Accepted 確認 |
| **1週間以内** | Markdown 同期 | AI_GUIDELINES.md / HIERARCHY_RULES.md 更新 |
| **月次** | 統合チェック | 全文書間の一貫性確認 |

---

## 矛盾・曖昧さの報告フロー

矛盾を発見した場合、以下の手順に従う：

### ステップ1: 優先順位確認
```
本 SSOT_PRIORITY_MATRIX の「優先順位の決定フロー」に基づき、
どちらが正しいかを判定
```

### ステップ2: 原因特定
```
- YAML/スクリプトが更新されたが Markdown が古い？
- 古い ADR があり、新しい ADR が supersede している？
- 複数 Markdown 間でのみ矛盾？
```

### ステップ3: 修正実施
```
優先順位に基づき修正
- YAML/スクリプト修正 → ADR 作成 → Markdown 同期
```

### ステップ4: 検証
```
- scripts/validate_docs.py で検証
- 全文書間の整合性確認
```

---

## FAQ

### Q: 複数の Markdown が異なることを書いている。どれを信じる？

**A**: 優先順位に基づき：
1. YAML/ADR で正規形式を確認
2. AI_GUIDELINES.md を信じる（最も詳細）
3. 他の Markdown は補助参照資料
4. 矛盾は Issue 作成

### Q: ADR がまだ Draft だが、すでに実装されている。どうする？

**A**:
- **短期**: 現在の実装が正しいと見なす
- **中期**: ADR を Accepted に昇格させる
- **長期**: 矛盾がある場合は新 ADR で supersede

### Q: スクリプトと Markdown が異なる。どちらが正しい？

**A**: スクリプト（YAML）が正しい。  
Markdown は参考資料。矛盾は Issue 作成。

### Q: 「YAML も Markdown も古い」ことに気づいた。どうする？

**A**: 以下の順序で対応：
1. 本来あるべき形式を決定（SSOT_PRIORITY_MATRIX に基づき）
2. YAML → ADR → Markdown の順に修正
3. 修正完了後、`docs/operations/current/{YYYYMMDD}_GOVERNANCE_UPDATE.ja.md` として記録

---

## 関連文書

- **決定根拠**: 
  - [ADR-0002](../decisions/active/2025/10/20251029_0002_naming-structure_documentation.md) - 命名規則とディレクトリ構造
  - [ADR-0005](../decisions/active/2025/10/20251029_0005_multilingual-directory-structure_documentation.md) - ドキュメント階層・ポリシー
  - [ADR-0011](../decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md) - ファイル名ケース規則

- **実装ガイド**:
  - [AI_GUIDELINES.md](./AI_GUIDELINES.md) - AI向けドキュメント記録ルール
  - [HIERARCHY_RULES.md](./HIERARCHY_RULES.md) - ドキュメント階層詳細
  - [DOCUMENTATION_STRUCTURE.yml](./DOCUMENTATION_STRUCTURE.yml) - 機械可読定義

- **メンテナンス**:
  - [DOCUMENTATION_UPDATE_CHECKLIST.md](../operations/current/20251029_DOCUMENTATION_UPDATE_CHECKLIST.md) - 構造変更時のチェックリスト

---

## 更新履歴

| 日時 | 変更 | 実施者 |
|------|------|--------|
| 2025-10-29 | 初版作成。5段階の優先順位レベル定義、ケース別対応例、同期メカニズムを記載 | GitHub Copilot |

---

**このドキュメントは [GOVERNANCE_SELF_REVIEW_REPORT.md](../operations/current/20251029_GOVERNANCE_SELF_REVIEW_REPORT.md) の Action-3 として作成されました。**
