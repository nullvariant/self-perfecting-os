# AI向けドキュメント記録ガイドライン

**対象**: GitHub Copilot, Claude Code, Claude Web UI, その他のAIアシスタント  
**バージョン**: 1.0.0  
**最終更新**: 2025-10-28

---

## 📋 クイックリファレンス

### 変更タイプ別の記録場所

| 変更タイプ | 記録場所 | ADR必要 | 追加更新 |
|-----------|---------|---------|---------|
| 🔧 API変更・移行 | `docs/decisions/ADR-*.md` | ✅ | PROJECT_STATUS, CHANGELOG |
| 🏗️ アーキテクチャ変更 | `docs/decisions/ADR-*.md` | ✅ | PROJECT_STATUS |
| ⚙️ CI/CD変更 | `docs/decisions/ADR-*.md` | ✅ | PROJECT_STATUS |
| 📂 ドキュメント構造変更 | `docs/decisions/ADR-*.md` | ✅ | DOCUMENTATION_STRUCTURE.yml |
| 📦 重要な依存関係変更 | `docs/decisions/ADR-*.md` | ✅ | CHANGELOG |
| 📊 一時的な状態変化 | `docs/project-status.ja.md` | ❌ | - |
| 🎉 バージョンリリース | `CHANGELOG.md` | ❌ | PROJECT_STATUS |
| 📝 プロセス・手順変更 | `docs/operations/*.md` | ✅ | - |
| 💡 機能要件定義 | `docs/prd_*.md` | ❌ | - |
| 🐛 タイポ修正 | コミットメッセージのみ | ❌ | - |
| 🔨 軽微なバグ修正 | コミットメッセージのみ | ❌ | - |

---

## 🎯 原則1: すべての重要な決定は ADR に記録

### ADRが必要な場合

以下のいずれかに該当する場合、**必ず ADR を作成**してください：

- ✅ **API の変更・移行**
  - 例: OpenAI API → Claude API への移行
  - 例: エンドポイントの変更
  - 例: レスポンス形式の変更

- ✅ **アーキテクチャの変更**
  - 例: モノリス → マイクロサービス
  - 例: 新しいデザインパターンの導入
  - 例: データベース設計の変更

- ✅ **CI/CD パイプラインの停止・変更**
  - 例: 自動ビルドの一時停止
  - 例: デプロイ戦略の変更
  - 例: テストフレームワークの変更

- ✅ **ドキュメント構造の大幅な変更**
  - 例: 新しいディレクトリの追加
  - 例: ドキュメント階層の再編成
  - 例: 命名規則の変更

- ✅ **重要な依存関係の追加・削除**
  - 例: 新しいライブラリの導入
  - 例: 既存ライブラリの削除
  - 例: バージョンアップ（破壊的変更を含む）

- ✅ **プロセス・手順の変更**
  - 例: リリースフローの変更
  - 例: レビュープロセスの変更
  - 例: 運用手順の変更

- ✅ **破壊的変更 (Breaking Changes)**
  - 例: 公開APIの仕様変更
  - 例: 設定ファイル形式の変更
  - 例: 互換性のない変更

- ✅ **セキュリティ関連の決定**
  - 例: 認証方式の変更
  - 例: アクセス制御の変更
  - 例: 暗号化方式の変更

- ✅ **パフォーマンス最適化の方針決定**
  - 例: キャッシュ戦略の変更
  - 例: 非同期処理の導入
  - 例: レート制限の設定

### ADRが不要な場合

以下の変更は **ADR不要**（コミットメッセージのみで十分）：

- ❌ タイポ修正
- ❌ コメント追加・修正
- ❌ フォーマット調整（Prettier等）
- ❌ 軽微なバグ修正（ロジック変更なし）
- ❌ リファクタリング（挙動変更なし）
- ❌ テストの追加（既存機能に対して）

---

## 🛠️ 原則2: ADR作成の手順

### ステップ1: ADR生成スクリプトを実行

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "GitHub Copilot"  # or "Claude Code", "human"
```

**例**:
```bash
python scripts/record_decision.py \
  --title "Claude API レート制限対応によるCI/CD一時停止" \
  --context "Claude Sonnet 4.5 の出力レート制限が 8,000 tokens/min と判明。content/ja/AGENT.md 全体の翻訳には数分かかるため、CI での自動実行が不適切と判断" \
  --author "Claude Code"
```

### ステップ2: 生成されたADRを編集

```markdown
# ADR-0001: Claude API レート制限対応によるCI/CD一時停止

## Status
- **提案日**: 2025-10-28
- **状態**: Draft → **Accepted** に変更
- **決定者**: Claude Code + human

## Context
Claude Sonnet 4.5 の出力レート制限が 8,000 tokens/min と判明。
content/ja/AGENT.md 全体の翻訳には数分かかるため、CI での自動実行が不適切と判断。

## Decision
CI/CD パイプラインを一時停止し、手動実行に切り替える。

## Consequences
### ✅ メリット
- レート制限を回避できる
- 翻訳品質を手動で確認できる

### ⚠️ デメリット
- 手動実行の手間が増える
- 自動化のメリットが失われる

### 📋 TODO
- [ ] レート制限に適合した分割翻訳の実装
- [ ] CI再開の判断基準を決定

## Related
- `scripts/build.py`
- `docs/project-status.ja.md`
```

### ステップ3: 関連ドキュメントを更新

ADR作成後、必要に応じて以下も更新：

```bash
# project-status.ja.md に状態を記録
# CHANGELOG.md の [Unreleased] に追記（必要なら）
# docs/project-status.ja.md に進捗を記録（一時文書の場合）
```

---

## 🧭 原則3: 作業前チェックリスト

コード変更を提案する前に、以下を必ず確認してください：

### ✅ Checklist

1. **[ ] この変更は ADR が必要か？**
   - 「ADRが必要な場合」のリストを確認
   - **Yes** → `python scripts/record_decision.py` を実行
   - **No** → 次へ

2. **[ ] 既存の ADR/ドキュメントと矛盾しないか？**
   - `docs/decisions/` 配下を確認
   - **矛盾あり** → 新ADRで上書き（Status: Superseded）
   - **矛盾なし** → 次へ

3. **[ ] 一時的な状態変化か？（7日以内に完了する見込み）**
   - **Yes** → `docs/project-status.ja.md` に記録
   - **No** → 次へ

4. **[ ] バージョンリリースに影響するか？**
   - 公開API・仕様書・ユーザー向け機能に影響があるか確認
   - **Yes** → `CHANGELOG.md` の `[Unreleased]` に追記
   - **No** → 次へ

5. **[ ] 変更内容を人間に説明できるか？**
   - 変更理由と影響範囲を明確に説明できるか確認
   - **Yes** → 作業実行
   - **No** → 追加情報を人間に質問

---

## 📂 原則4: ドキュメント階層の理解

### Tier 0: Single Source of Truth (SSOT)
**AI/人間が最初に参照すべき真実**

- `docs/decisions/*.md` - ADR（全ての重要な決定）
- `content/ja/AGENT.md` - 仕様書（日本語一次情報）
- `content/ja/EmotionMood_Dictionary.md` - 感情辞書

### Tier 1: 状態管理
**プロジェクトの現在状態を反映**

- `docs/project-status.ja.md` - 現在の状態・優先度
- `CHANGELOG.md` - バージョン履歴

### Tier 2: プロセス・手順書
**運用・実行手順の記録**

- `docs/operations/OPERATIONS.ja.md` - 運用手順
- `docs/operations/NOTE_SYNC_MANUAL.ja.md` - note公開手順

### Tier 3: 設計文書（PRD）
**機能開発・改善の要件定義**

- `docs/prd_*.md` - 各機能のPRD

### Tier 4: 一時的文書
**期限付きの作業記録（完了後アーカイブ）**

- `docs/project-status.ja.md` - 移行作業の進捗

---

## 🚫 禁止事項

### ❌ 絶対にやってはいけないこと

1. **自動生成ファイルの直接編集**
   - `AGENT.md` - CI/CDが自動生成（編集禁止）
   - `spec/agent.spec.yaml` - CI/CDが自動生成（編集禁止）

2. **ADRの削除**
   - 古くなった ADR は削除せず、Status を `Deprecated` に変更
   - 新しい ADR で上書きする場合は、Related に旧ADR番号を記載

3. **ドキュメント間の矛盾の放置**
   - 矛盾を発見したら、必ず ADR で解決
   - 「どちらが正しいか」を明確に記録

4. **勝手なディレクトリ構造の変更**
   - ディレクトリ構造の変更は必ず ADR が必要
   - `DOCUMENTATION_STRUCTURE.yml` を更新

---

## 💡 ベストプラクティス

### ✅ 推奨される行動

1. **迷ったら ADR を作成**
   - 「ADR が必要か？」で迷ったら、作成する
   - 最悪でも記録が残る（後で Deprecated にできる）

2. **人間に確認を求める**
   - 重要な決定は必ず人間に確認
   - 特に破壊的変更の場合

3. **関連ドキュメントへのリンクを明記**
   - ADR に関連ファイル・Issue・Commitを記載
   - トレーサビリティを確保

4. **簡潔かつ明確に記述**
   - ADR は後から読む人（AI含む）のために書く
   - 冗長な説明は避け、要点を明確に

---

## 🔄 フィードバックループ

### ADR作成後の確認

作成した ADR が適切か、以下を確認：

```bash
# ドキュメント整合性チェック
python scripts/validate_docs.py

# エラーがあれば修正
# エラーがなければコミット
git add docs/decisions/ADR-*.md
git commit -m "docs: Add ADR-XXXX for [決定内容]"
```

### 定期レビュー

- **頻度**: 月次
- **確認事項**:
  - 古い ADR の Status を確認（Deprecated にすべきものはないか）
  - `docs/project-status.ja.md` の最終更新日を確認
  - `DOCUMENTATION_STRUCTURE.yml` との整合性を確認

---

## 📚 参考資料

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [docs/governance/DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml) - 機械可読形式の定義
- [docs/governance/HIERARCHY_RULES.md](HIERARCHY_RULES.md) - 階層ルール詳細

---

**このガイドラインは `.github/copilot-instructions.md` と統合され、全てのAI環境で参照されます。**
