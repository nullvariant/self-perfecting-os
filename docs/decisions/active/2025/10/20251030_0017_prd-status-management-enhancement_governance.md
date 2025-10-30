# ADR-0017: PRDステータス管理の拡張（deprecated対応）

## Status
- **提案日**: 2025-10-30
- **状態**: Accepted
- **決定者**: human + Claude Code

## Context

### 背景

PRD（Product Requirement Document）のステータス管理において、ルールの不備が発見されました。

**発覚した問題**:
- `docs/prd/active/20251030_copilot-agent-acceleration-phase2.ja.md` に Status: Deprecated を記載
- しかし、ファイルは `active/` ディレクトリに残ったまま
- **理由**: PRDディレクトリ構造に `deprecated/` が定義されていない

### 現在の構造（DOCUMENTATION_STRUCTURE.yml）

```yaml
prd:
  pattern: "docs/prd/{status}/"
  status_dirs:
    - active      # 策定中・未実装
    - implemented # 実装完了
  monthly_archive: false
```

### 不足しているケース

| ケース | 現状 | 問題 |
|--------|------|------|
| PRDが実装完了 | `implemented/` に移動 | ✅ 対応済み |
| PRDが中止・不要に | **未定義** | ❌ ルール不備 |

**実際の事例**:
- Cursor移行により、Copilot高速化PRDが不要に（ADR-0016）
- Status: Deprecated と記載したが、`active/` に残存
- ディレクトリ構造とStatus記載が矛盾

### 検討した選択肢

1. **選択肢A**: `deprecated/` ディレクトリを追加
   - メリット: ADRと同様の構造、一貫性が高い
   - デメリット: ディレクトリが増える

2. **選択肢B**: `active/` にそのまま残し、Statusのみ変更
   - メリット: シンプル
   - デメリット: ディレクトリ構造とStatusが矛盾、検索時に混乱

3. **選択肢C**: `archive/` にまとめて配置
   - メリット: PRD専用のアーカイブ
   - デメリット: ADRの `deprecated/` `superseded/` との一貫性がない

## Decision

**選択肢A を採用: PRDディレクトリ構造に `deprecated/` を追加**

### 新しいディレクトリ構造

```yaml
prd:
  pattern: "docs/prd/{status}/"
  status_dirs:
    - active       # 策定中・未実装
    - implemented  # 実装完了
    - deprecated   # 不要になった（中止・方針転換・環境変化等）
  monthly_archive: false
```

### Status定義

| Status | 意味 | 配置先 |
|--------|------|--------|
| **Active** | 策定中・未実装 | `docs/prd/active/` |
| **Implemented** | 実装完了 | `docs/prd/implemented/` |
| **Deprecated** | 不要になった | `docs/prd/deprecated/` |

### Deprecated の定義

以下の場合に PRD は Deprecated となる：
- プロジェクト方針転換により不要に
- 実装前に要件が変更され、新PRDに置き換え
- 外部環境変化（ツール移行等）により無効化
- 実装コストが高すぎて中止

### AI向けチェックリスト（追加）

```yaml
ai_checklist:
  after_prd_status_change:
    - question: "PRD の Status が変更されたか？"
      check: "Status: フィールドの変更を検知"
      action_map:
        "Active → Implemented":
          - "mv docs/prd/active/{file} docs/prd/implemented/{file}"
          - "INDEX.md は Git Hooks で自動再生成"
        "Active → Deprecated":
          - "mv docs/prd/active/{file} docs/prd/deprecated/{file}"
          - "INDEX.md は Git Hooks で自動再生成"
          - "CHANGELOG.md に記録"
```

## Consequences

### ✅ メリット

1. **一貫性**: ADRと同様のステータス管理構造
2. **明確化**: ディレクトリ構造とStatus記載が一致
3. **検索効率**: `active/` は本当に現行のPRDのみ
4. **履歴保持**: Deprecated PRDも履歴として残る

### ⚠️ デメリット

1. **ディレクトリ増加**: 3つのステータスディレクトリを管理
   - 対策: PRDは件数が少ないため、管理負担は軽微
2. **既存ファイルの移動**: 該当PRDを手動移動が必要
   - 対策: 今回のADR実装時に対応

### 📋 TODO

- [x] `docs/prd/deprecated/` ディレクトリ作成
- [x] `DOCUMENTATION_STRUCTURE.yml` 更新
- [x] `20251030_copilot-agent-acceleration-phase2.ja.md` を `deprecated/` に移動
- [x] `.cursor/rules/project.mdc` に Status変更チェックリスト追記
- [x] `CHANGELOG.md` に記録
- [ ] Git Hooks 動作確認（INDEX.md 自動再生成）

## Related

### 関連するファイル

- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - PRD構造定義を更新
- `.cursor/rules/project.mdc` - AIチェックリストを追記
- `docs/prd/deprecated/` - 新規作成
- `docs/prd/active/20251030_copilot-agent-acceleration-phase2.ja.md` - 移動対象

### 関連する ADR

- ADR-0002: 命名規則とディレクトリ構造の確立
- ADR-0016: VSCode/Copilot → Cursor 移行（本PRDが不要になった理由）

### 関連する Issue/PR

該当なし

### 今回の対象ファイル

| ファイル | Status | 移動先 | 理由 |
|---------|--------|--------|------|
| `20251030_copilot-agent-acceleration-phase2.ja.md` | Deprecated | `docs/prd/deprecated/` | Cursor移行により不要（ADR-0016） |

---

**実装者**: Claude Code  
**レビュアー**: nullvariant (approved)

