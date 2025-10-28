# ADR-0001: Claude API レート制限対応によるCI/CD一時停止

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: Claude Code + human (nullvariant)

## Context

### 背景

`scripts/build.py` は、以下の処理を自動化するために作成されました：

1. **英語翻訳**: `content/ja/AGENT.md` → `AGENT.md`
2. **YAML抽出**: `content/ja/AGENT.md` → `spec/agent.spec.yaml`

当初は OpenAI GPT-4 API を使用していましたが、2025年10月下旬に **Claude Sonnet 4.5 API** への移行を決定しました。

### 問題点

移行後、以下の問題が判明しました：

- **レート制限**: Claude Sonnet 4.5 の出力レート制限は **8,000 tokens/分**
- **処理時間**: `AGENT.ja.md` 全体（約15,000文字）の翻訳には **数分**かかる
- **CI適性**: CI/CDでの自動実行には不向き（タイムアウトリスク・レート制限超過）

### 検討した選択肢

1. **選択肢A: CI/CDを一時停止し、手動実行に切り替える**
   - メリット: レート制限を回避できる
   - デメリット: 自動化のメリットが失われる

2. **選択肢B: ドキュメントを分割翻訳し、レート制限内に収める**
   - メリット: CI/CDを継続できる
   - デメリット: 実装に時間がかかる、翻訳品質の一貫性リスク

3. **選択肢C: 別のLLM APIに再移行する**
   - メリット: レート制限が緩いAPIを選べる
   - デメリット: 再度の移行コスト、品質の不確実性

## Decision

**選択肢A: CI/CDを一時停止し、手動実行に切り替える**

理由：

1. **優先度**: ドキュメント品質 > 自動化の利便性
2. **リスク管理**: レート制限超過によるAPI制限を回避
3. **段階的アプローチ**: まず手動で運用し、必要に応じて選択肢Bを実装

具体的な対応：

- CI/CD パイプライン（`.github/workflows/`）を一時的に無効化
- `scripts/build.py` は手動実行のみ
- `AGENT.md` と `spec/agent.spec.yaml` には「古い・手動更新必要」の警告を追加

## Consequences

### ✅ メリット

1. **レート制限を回避**
   - API制限によるビルド失敗がなくなる
   - 手動実行時に待機時間を設けることで、安全に翻訳可能

2. **翻訳品質の確認**
   - 手動実行時に結果を確認できる
   - 品質問題を早期発見

3. **段階的改善**
   - 選択肢Bの実装を急がず、品質を優先できる

### ⚠️ デメリット

1. **手動実行の手間**
   - `content/ja/AGENT.md` 更新のたびに手動ビルドが必要
   - 忘れると `AGENT.md` が古いまま

2. **自動化のメリット喪失**
   - Pull Request での自動チェックができない
   - リリース時の手作業が増える

3. **ドキュメント間の乖離リスク**
   - `content/ja/AGENT.md` と `AGENT.md` の同期漏れ

### 📋 TODO

- [x] `scripts/build.py` にレート制限対応のコメント追加
- [x] `AGENT.md` に「古い・手動更新必要」の警告追加（検討中）
- [x] `docs/project-status.ja.md` に移行状況を記録
- [ ] `docs/project-status.ja.md` に CI/CD停止中の状態を記録
- [ ] 選択肢B（分割翻訳）の実装を検討（Phase 2 以降）
- [ ] レート制限に適合した実装完成後、CI/CD再開

## Related

### 関連するファイル
- `scripts/build.py` - ビルドスクリプト（レート制限対応コメント追加済み）
- `docs/project-status.ja.md` - API移行状況の記録（一時文書）
- `docs/project-status.ja.md` - プロジェクト状態管理
- `AGENT.md` - 英語版仕様書（自動生成・現在古い）
- `spec/agent.spec.yaml` - YAML仕様（自動生成・現在古い）

### 関連する ADR
- なし（初回ADR）

### 関連する Issue/PR
- なし（GitHub Issues未使用）

### 関連する Commit
- （このADR作成時のコミットSHA）

---

## 補足: レート制限の詳細

```python
# scripts/build.py の現在の実装

MODEL_DEFAULT = "claude-sonnet-4-5-20250929"
MAX_OUTPUT_TOKENS = 5000  # 出力トークン制限
RATE_LIMIT_WAIT = 70      # 60秒 + バッファ

# 問題:
# - AGENT.ja.md 全体の翻訳には約15,000トークン出力が必要
# - 1チャンク5,000トークン × 3回 = 計3分 + バッファ
# - CI/CDのタイムアウト設定との兼ね合い
```

---

**Status**: Accepted  
**実装状況**: 完了（CI/CD停止済み、手動実行に移行済み）  
**次回レビュー**: 2025-11-28（選択肢Bの実装検討）
