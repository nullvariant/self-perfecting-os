# PRD: ドキュメント管理ガバナンス体系の確立

**ドキュメントID**: PRD-DOC-001  
**作成日**: 2025-10-28  
**ステータス**: Draft → Review → Approved  
**優先度**: P0（最高）  
**担当**: nullvariant (human) + AI assistants

---

## 📋 Executive Summary

### 課題
- AI環境（Claude Code, GitHub Copilot, Chat UI）を跨ぐと文脈が途切れる
- 「ドキュメントを残す」指示が曖昧で、記録場所が不統一
- 既存ドキュメントが散在し、Single Source of Truth (SSOT) が不明確
- CI/CD停止などの重要な決定が記録されず、矛盾が蓄積

### ゴール
- **Phase 1**: ADR (Architecture Decision Records) 導入による決定記録の標準化
- **Phase 2**: 既存ドキュメントの整理統合・階層化
- **Phase 3**: AI が自動的に正しい場所に記録する仕組みの確立

### 期待される成果
- ✅ 環境を跨いでも一貫した記録が残る
- ✅ 過去の決定理由が追跡可能
- ✅ 新しいAI/人間の貢献者が迷わない
- ✅ HSP特性（完璧主義・認知負荷への配慮）に適合

---

## 🎯 Phase 1: ADR導入とドキュメント階層の確立

### 1.1 新規ディレクトリ構造

```
nullvariant/
├── docs/
│   ├── DECISIONS/              # 🆕 ADR保管庫（最優先参照）
│   │   ├── 0000-adr-template.md
│   │   ├── 0001-ci-cd-pause.md
│   │   └── README.md
│   ├── GOVERNANCE/             # 🆕 ガバナンス文書
│   │   ├── DOCUMENTATION_STRUCTURE.yml
│   │   ├── AI_GUIDELINES.md
│   │   └── HIERARCHY_RULES.md
│   ├── operations/             # 🔄 既存を整理
│   │   ├── OPERATIONS.ja.md
│   │   └── NOTE_SYNC_MANUAL.ja.md
│   └── archive/                # 🆕 古いドキュメント退避先
│       └── deprecated/
├── content/                     # 変更なし（一次情報）
│   ├── content/ja/AGENT.md
│   └── EmotionMood_Dictionary.ja.md
├── changelogs/                  # 変更なし
└── scripts/                     # 🆕 ADR生成スクリプト追加
    ├── record_decision.py       # ADR自動生成
    └── validate_docs.py         # ドキュメント整合性チェック
```

### 1.2 成果物リスト

| ファイル | 目的 | 状態 |
|---------|------|------|
| `docs/decisions/0000-adr-template.md` | ADRテンプレート | 🆕 作成 |
| `docs/decisions/0001-ci-cd-pause.md` | 初回ADR（API移行記録） | 🆕 作成 |
| `docs/decisions/README.md` | ADR使用ガイド | 🆕 作成 |
| `docs/governance/DOCUMENTATION_STRUCTURE.yml` | ドキュメント階層定義（機械可読） | 🆕 作成 |
| `docs/governance/AI_GUIDELINES.md` | AI向け記録ルール | 🆕 作成 |
| `docs/governance/HIERARCHY_RULES.md` | 階層ルール説明（人間向け） | 🆕 作成 |
| `scripts/record_decision.py` | ADR生成スクリプト | 🆕 作成 |
| `scripts/validate_docs.py` | ドキュメント検証スクリプト | 🆕 作成 |
| `.github/copilot-instructions.md` | AI向けルール追記 | 🔄 更新 |

### 1.3 受け入れ基準

- [ ] ADRテンプレートが作成され、使用方法がドキュメント化されている
- [ ] CI/CD停止の決定が ADR-0001 として記録されている
- [ ] `DOCUMENTATION_STRUCTURE.yml` が機械可読形式で存在する
- [ ] AI向けガイドラインが `.github/copilot-instructions.md` に統合されている
- [ ] `scripts/record_decision.py` が動作し、ADRを自動生成できる
- [ ] `scripts/validate_docs.py` がドキュメント間の矛盾を検出できる

---

## 🗂️ Phase 2: 既存ドキュメントの整理統合

### 2.1 現状分析

#### 散在しているドキュメント

| ファイル | 役割 | 問題点 | 対応方針 |
|---------|------|--------|---------|
| `README.md` | 概要 | 一部古い情報 | Phase 2で整理 |
| `docs/project-status.ja.md` | 移行状況 | 一時的（完了後削除予定） | ADR-0001に統合検討 |
| `docs/project-status.ja.md` | プロジェクト状態 | 更新日未記載 | Phase 2で強化 |
| `docs/operations/current/` | 運用手順 | 一部古い | Phase 2で精査 |
| `docs/operations/current/` | note公開手順 | 比較的最新 | Phase 2で検証 |
| `docs/prd_CHANGELOG_MIGRATION.ja.md` | Changelog分離PRD | 実装状況不明 | Phase 2で確認 |
| `docs/prd_NOTE_WORKFLOW_AUTOMATION.ja.md` | note自動化PRD | 実装状況不明 | Phase 2で確認 |
| `docs/WORKFLOW_TEXT_ASSETS.ja.md` | テキスト資産管理 | 役割不明確 | Phase 2で整理 |

### 2.2 整理統合方針

#### Tier 0: Single Source of Truth (SSOT)
- **目的**: AI/人間が最初に参照すべき真実
- **配置**: `docs/decisions/` + `content/`
- **更新頻度**: 重要な決定時のみ
- **ファイル**:
  - `docs/decisions/*.md` (ADR)
  - `content/ja/AGENT.md` (仕様書)
  - `content/ja/EmotionMood_Dictionary.md` (感情辞書)

#### Tier 1: 状態管理
- **目的**: プロジェクトの現在状態を反映
- **配置**: ルートレベル + `docs/`
- **更新頻度**: 週次 or 重要な状態変化時
- **ファイル**:
  - `docs/project-status.ja.md` (最終更新日を強制)
  - `CHANGELOG.md` (Keep a Changelog形式)

#### Tier 2: プロセス・手順書
- **目的**: 運用・実行手順の記録
- **配置**: `docs/operations/`
- **更新頻度**: プロセス変更時
- **ファイル**:
  - `docs/operations/OPERATIONS.ja.md`
  - `docs/operations/NOTE_SYNC_MANUAL.ja.md`

#### Tier 3: 設計文書（PRD）
- **目的**: 機能開発・改善の要件定義
- **配置**: `docs/plans/` (名称変更検討)
- **更新頻度**: 機能開発時
- **ファイル**:
  - `docs/plans/changelog-migration.ja.md`
  - `docs/plans/note-workflow-automation.ja.md`
  - `docs/plans/documentation-governance.ja.md` (本文書)

#### Tier 4: 一時的文書
- **目的**: 期限付きの作業記録（完了後アーカイブ）
- **配置**: `docs/temporary/` (新設)
- **更新頻度**: 適宜（完了後は `docs/archive/` へ）
- **ファイル**:
  - `docs/project-status.ja.md` → ADR化後削除

### 2.3 統合タスク

#### Week 1: 棚卸し・分類
- [ ] 全ドキュメントの最終更新日を記録
- [ ] 各ドキュメントを Tier 0-4 に分類
- [ ] 重複・矛盾を洗い出し

#### Week 2: 移行・統合
- [ ] `docs/operations/` 配下に既存運用文書を整理
- [ ] `docs/plans/` に PRD を集約
- [ ] `docs/temporary/` を新設し、一時文書を移動
- [ ] `docs/project-status.ja.md` → ADR-0001 に統合

#### Week 3: 検証・修正
- [ ] `scripts/validate_docs.py` で矛盾チェック
- [ ] README.md のドキュメント一覧を更新
- [ ] `.github/copilot-instructions.md` に新構造を反映

### 2.4 受け入れ基準

- [ ] 全ドキュメントが Tier 0-4 のいずれかに分類されている
- [ ] 各ドキュメントに「最終更新日」「Tier」「更新ルール」が明記されている
- [ ] `docs/governance/DOCUMENTATION_STRUCTURE.yml` に全ファイルが登録されている
- [ ] `scripts/validate_docs.py` がエラーなく実行できる
- [ ] README.md のドキュメント一覧が最新状態を反映している

---

## 🤖 Phase 3: AI自動記録の仕組み確立

### 3.1 AI向けガイドラインの強化

#### `.github/copilot-instructions.md` に追加すべき内容

```markdown
## 📝 ドキュメント記録ルール（AI必読）

### 原則1: すべての重要な決定は ADR に記録

**判断基準**:
- ✅ API の変更・移行 → ADR
- ✅ アーキテクチャの変更 → ADR
- ✅ CI/CD の停止・変更 → ADR
- ✅ ドキュメント構造の変更 → ADR
- ✅ 重要な依存関係の追加・削除 → ADR
- ❌ タイポ修正 → コミットメッセージのみ
- ❌ 軽微なバグ修正 → コミットメッセージのみ

### 原則2: 記録場所の自動判定

```python
# 疑似コード: AI が実行すべき判断ロジック

def determine_documentation_target(change_type):
    if change_type in ["api_change", "architecture", "cicd", "structure"]:
        return "docs/decisions/ADR-XXXX.md"
    
    elif change_type == "temporary_status":
        return "docs/project-status.ja.md"
    
    elif change_type == "version_release":
        return "CHANGELOG.md"
    
    elif change_type == "process_update":
        return "docs/operations/*.md"
    
    elif change_type == "feature_requirement":
        return "docs/plans/PRD_*.md"
    
    else:
        return "commit message only"
```

### 原則3: 作業前チェックリスト

コード変更を提案する前に、以下を確認:

1. [ ] この変更は ADR が必要か？
   - **Yes** → `python scripts/record_decision.py` を実行
   - **No** → 次へ

2. [ ] 既存の ADR/ドキュメントと矛盾しないか？
   - **矛盾あり** → 新 ADR で上書き（Superseded 記録）
   - **矛盾なし** → 次へ

3. [ ] 一時的な状態変化か？
   - **Yes** → `docs/project-status.ja.md` に記録
   - **No** → 次へ

4. [ ] バージョンリリースに影響するか？
   - **Yes** → `CHANGELOG.md` の `[Unreleased]` に追記
   - **No** → 次へ

5. [ ] 変更内容を人間に説明できるか？
   - **Yes** → 作業実行
   - **No** → 追加情報を人間に質問
```

### 3.2 自動検証スクリプト

#### `scripts/validate_docs.py` の要件

```python
"""
ドキュメント整合性検証スクリプト

チェック項目:
1. ADR 番号の連番チェック
2. DOCUMENTATION_STRUCTURE.yml に記載された全ファイルの存在確認
3. project-status.ja.md の最終更新日チェック（7日以上前なら警告）
4. README.md のドキュメントリンク切れチェック
5. 自動生成ファイル（AGENT.md, spec/agent.spec.yaml）への直接編集チェック
"""
```

### 3.3 Git Hooks の導入（検討）

```bash
# .git/hooks/pre-commit (将来的な検討事項)

#!/bin/bash
# ADR が必要な変更を検出したら警告

CHANGED_FILES=$(git diff --cached --name-only)

# CI/CD 関連ファイルが変更されているか
if echo "$CHANGED_FILES" | grep -q "scripts/build.py\|.github/workflows"; then
    echo "⚠️  WARNING: CI/CD related files changed."
    echo "📝 Did you create an ADR? (docs/decisions/)"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

### 3.4 受け入れ基準

- [ ] `.github/copilot-instructions.md` に詳細な記録ルールが追加されている
- [ ] `scripts/validate_docs.py` が実装され、CI で実行可能
- [ ] AI が変更内容から自動的に記録場所を判断できるガイドラインがある
- [ ] Git Hooks の導入可否が判断されている（Phase 3 完了後に検討でも可）

---

## 📊 成功指標（KPI）

### Phase 1 完了時
- ✅ ADR が 1件以上記録されている
- ✅ `DOCUMENTATION_STRUCTURE.yml` が存在し、機械可読である
- ✅ AI向けガイドラインが `.github/copilot-instructions.md` に統合されている

### Phase 2 完了時
- ✅ 全ドキュメントが Tier 0-4 に分類されている
- ✅ ドキュメント間の矛盾が 0 件
- ✅ `scripts/validate_docs.py` がエラーなく実行できる

### Phase 3 完了時
- ✅ AI が自動的に正しい記録場所を選択できる
- ✅ 新しい貢献者（AI/人間）が迷わずドキュメントを参照できる
- ✅ 環境を跨いでも一貫した記録が残る

---

## 🗓️ タイムライン

| Phase | 期間 | マイルストーン |
|-------|------|--------------|
| Phase 1 | Week 1-2 | ADR導入・ドキュメント階層確立 |
| Phase 2 | Week 3-5 | 既存ドキュメント整理統合 |
| Phase 3 | Week 6-8 | AI自動記録の仕組み確立 |

---

## 🚨 リスクと対策

### リスク1: AI が新ルールを無視する
- **確率**: 中
- **影響度**: 高
- **対策**: 
  - `.github/copilot-instructions.md` の先頭に配置
  - `scripts/validate_docs.py` を CI に組み込み、自動検証

### リスク2: 既存ドキュメントの整理に時間がかかる
- **確率**: 高
- **影響度**: 中
- **対策**:
  - Phase 2 を段階的に実施（優先度付け）
  - 完璧を求めず、80%ルールで進める（HSP対策）

### リスク3: ルールが複雑すぎて運用できない
- **確率**: 中
- **影響度**: 高
- **対策**:
  - シンプルな判断基準を優先
  - `scripts/record_decision.py` で自動化
  - 迷ったら ADR に記録（最悪でも記録は残る）

---

## 📚 参考資料

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Documentation as Code](https://www.writethedocs.org/guide/docs-as-code/)

---

## 🔄 次のアクション

### 人間（nullvariant）が実施
1. [ ] 本PRDをレビューし、Approved に変更
2. [ ] Phase 1 の優先順位を確認

### AI が実施
1. [ ] Phase 1 の成果物を作成（次のステップで実行）
2. [ ] `.github/copilot-instructions.md` を更新

---

**Status**: Draft  
**Next Review**: 2025-10-28（本日中）  
**Approval Needed**: human (nullvariant)
