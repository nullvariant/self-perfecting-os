# ADR-0000: テンプレート

> **注意**: これはテンプレートファイルです。実際のADRを作成する際は、ADR番号を連番で採番してください。

## Status
- **提案日**: YYYY-MM-DD
- **状態**: [Draft | Accepted | Deprecated | Superseded]
- **決定者**: [human | GitHub Copilot | Claude Code | Claude Web UI]

## Context

### 背景
なぜこの決定が必要だったのか？

- 現在の状況
- 問題点
- 解決すべき課題

### 検討した選択肢（任意）
1. **選択肢A**: 説明
2. **選択肢B**: 説明
3. **選択肢C**: 説明

## Decision

何を決めたのか？

- 決定内容を明確に記述
- 具体的な実装方針
- 影響範囲

## Consequences

この決定によって何が変わるのか？

### ✅ メリット
- （具体的なメリット1）
- （具体的なメリット2）

### ⚠️ デメリット
- （具体的なデメリット1）
- （具体的なデメリット2）

### 📋 TODO
- [ ] （必要なタスク1）
- [ ] （必要なタスク2）

## Related

### 関連するファイル
- （影響を受けるファイル）

### 関連する ADR
- ADR-XXXX: （関連するADRがあれば）

### 関連する Issue/PR
- （GitHubのIssue/PRがあれば）

### 関連する Commit
- （主要なコミットSHA）

---

## 使用方法

### 自動生成（推奨）

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "GitHub Copilot"  # or "Claude Code", "human"
```

### 手動作成

1. このテンプレートをコピー
2. ファイル名を `ADR-XXXX-タイトル.md` に変更（XXXX = 連番）
3. 各セクションを埋める
4. Status を `Draft` → `Accepted` に変更
5. `docs/decisions/` に配置

### Status の意味

| Status | 説明 |
|--------|------|
| **Draft** | 提案段階。レビュー待ち。 |
| **Accepted** | 承認済み。実装可能。 |
| **Deprecated** | 非推奨。新しいADRで置き換え推奨。 |
| **Superseded** | 別のADRに置き換えられた。Related に新ADR番号を記載。 |

---

**このテンプレートは削除・編集禁止です。新しいADRを作成する際はコピーして使用してください。**
