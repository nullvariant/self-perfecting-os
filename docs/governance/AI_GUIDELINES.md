# AI向けドキュメント記録ガイドライン

**対象**: GitHub Copilot, Claude Code, Claude Web UI, その他のAIアシスタント  
**バージョン**: 1.0.0  
**最終更新**: 2025-10-28

---

## 📋 クイックリファレンス

### 変更タイプ別の記録場所

| 変更タイプ | 記録場所 | ADR必要 | 追加更新 |
|-----------|---------|---------|---------|
| 🔧 API変更・移行 | `docs/decisions/active/{YYYY}/{MM}/` | ✅ | PROJECT_STATUS, CHANGELOG |
| 🏗️ アーキテクチャ変更 | `docs/decisions/active/{YYYY}/{MM}/` | ✅ | PROJECT_STATUS |
| ⚙️ CI/CD変更 | `docs/decisions/active/{YYYY}/{MM}/` | ✅ | PROJECT_STATUS |
| 📂 ドキュメント構造変更 | `docs/decisions/active/{YYYY}/{MM}/` | ✅ | DOCUMENTATION_STRUCTURE.yml |
| 📦 重要な依存関係変更 | `docs/decisions/active/{YYYY}/{MM}/` | ✅ | CHANGELOG |
| 📊 一時的な状態変化 | `docs/project-status.ja.md` | ❌ | - |
| 🎉 バージョンリリース | `CHANGELOG.md` | ❌ | PROJECT_STATUS |
| 📝 プロセス・手順変更 | `docs/operations/current/` | ✅ | - |
| 💡 機能要件定義 | `docs/prd/active/` | ❌ | - |
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

## � 原則3: 一時的ドキュメント vs メタドキュメント

### 判別フロー

```
「このドキュメント、どこに保存する？」

  ├─ 決定したこと（重要事項の記録）?
  │  └─ YES → docs/decisions/active/{YYYY}/{MM}/ (ADR)
  │
  ├─ 要件定義（機能仕様）?
  │  └─ YES → docs/prd/active/ (PRD)
  │
  ├─ 運用手順（実行方法）?
  │  └─ YES → docs/operations/current/ (Operations)
  │
  ├─ ガバナンスルール・定義（参照ドキュメント）?
  │  └─ YES → docs/governance/ (大文字メタドキュメント)
  │
  └─ ガバナンス監査・品質レビュー・デバッグログ（記録・履歴）?
     └─ YES → docs/log/{YYYY}/{MM}/ (作業ログ)
```

### 一時的ドキュメントの特徴

| 特性 | governance/ | log/ |
|------|-----------|------|
| **目的** | ガバナンスルール・定義 | 作業ログ・履歴記録 |
| **参照頻度** | 高（繰り返し参照） | 低（履歴確認用） |
| **ステータス管理** | ✅ あり（active/deprecated） | ❌ 不要（時系列自動管理） |
| **命名** | 大文字、日付なし（恒久的） | 日付付き（時系列） |
| **例** | `AI_GUIDELINES.md`, `DOCUMENTATION_STRUCTURE.yml` | `20251029_governance-self-review.md` |
| **Git管理** | ✅ すべて | ✅ すべて（永続保存、削除ポリシーなし） |

### governance/ に含まれるべきもの

- ✅ `AI_GUIDELINES.md` - AI向けガイドライン（参照対象）
- ✅ `DOCUMENTATION_STRUCTURE.yml` - ドキュメント構造定義（参照対象）
- ✅ `HIERARCHY_RULES.md` - 階層ルール説明（参照対象）
- ✅ `NAMING_DECISION_SUMMARY.md` - 命名規則サマリー（参照対象）

### log/ に含まれるべきもの

- ✅ `20251029_governance-self-review.md` - ガバナンス監査レポート
- ✅ `20251030_quality-check-log.md` - 品質チェック結果
- ✅ `20251101_debug-investigation.md` - デバッグ調査ログ
- ✅ `20251105_performance-test-report.md` - パフォーマンステスト結果

---

## �📂 原則4: ドキュメント階層の理解

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

- `docs/operations/current/{YYYYMMDD}_{type}.ja.md` - 運用手順（最新版）
  - 例: `docs/operations/current/20251028_OPERATIONS.ja.md`
  - 例: `docs/operations/current/20251028_NOTE_SYNC_MANUAL.ja.md`
- 過去版は `docs/operations/archive/{YYYY}/{MM}/` へ移動

### Tier 3: 設計文書（PRD）
**機能開発・改善の要件定義**

- `docs/prd/active/{YYYYMMDD}_{slug}.ja.md` - 各機能のPRD（実装前）
  - 例: `docs/prd/active/20251028_documentation-governance.ja.md`
  - 例: `docs/prd/active/20251028_note-workflow-automation.ja.md`
- 実装完了後は `docs/prd/implemented/` へ移動

### Tier 4: 一時的文書（廃止、Tier 4.5 に統合）
**【廃止】この定義は Tier 4.5 に統合されました**

- （将来的には、全ての一時的ドキュメントは `docs/log/` で管理）

### Tier 4.5: ログ・記録（作業の時系列記録）
**ガバナンス監査・品質レビュー・デバッグログなど、作業の時系列記録**

- `docs/log/{YYYY}/{MM}/{YYYYMMDD}_{slug}.md` - 作業ログ（永続保存）
  - 例: `docs/log/2025/10/20251029_governance-self-review.md`
  - 例: `docs/log/2025/10/20251030_quality-check-log.md`

**特徴**:
- 参照対象ではなく、単なる「記録」
- ステータス管理（active/deprecated）は不要
- 月別フォルダで時系列整理
- `grep` やファイルシステムで検索可能

---

```

## 🚫 禁止事項

### ❌ 絶対にやってはいけないこと

1. **自動生成ファイルの直接編集**
   - `AGENT.md` - CI/CDが自動生成（編集禁止）
   - `spec/agent.spec.yaml` - CI/CDが自動生成（編集禁止）
   - `docs/decisions/INDEX.md` - `scripts/generate_index.py` が自動生成（編集禁止）
   - `docs/prd/INDEX.md` - `scripts/generate_index.py` が自動生成（編集禁止）
   - `docs/operations/INDEX.md` - `scripts/generate_index.py` が自動生成（編集禁止）
   - `docs/governance/INDEX.md` - `scripts/generate_index.py` が自動生成（編集禁止）

   **修正方法**: スクリプトを修正してから再生成
   ```bash
   # スクリプト修正後
   python scripts/generate_index.py --target [adr|prd|operations|governance|all]
   ```

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

## 🏷️ 補足：カテゴリタグ（category）の活用

### カテゴリタグとは

ADRファイル名の `_{category}` 部分（例：`_architecture`, `_governance`）は、
ADRの**内容分類タグ** です。これはファイル名に付与されるメタデータで、
ADRの保存場所（ディレクトリ構造）とは独立した概念です。

### カテゴリタグの役割

**カテゴリタグによる検索・抽出**:
```bash
# 「architecture」カテゴリのすべてのADRを検索
grep -r "_architecture.md" docs/decisions/

# または find で検索
find docs/decisions -name "*_architecture.md"

# 複数カテゴリで検索
grep -r "_governance.md\|_process.md" docs/decisions/
```

**INDEX.md でのカテゴリ別フィルタリング**:
- `scripts/generate_index.py --group-by-category` でカテゴリ別 INDEX 生成
- `scripts/generate_index.py --category architecture` で特定カテゴリのみ抽出

### カテゴリタグ vs ディレクトリ構造の違い

| 観点 | カテゴリタグ（`_category`） | ディレクトリ構造（`{status}/{YYYY}/{MM}/`） |
|------|---------------------------|----------------------------------------|
| **役割** | 内容分類（コンテンツ軸） | 状態・時期管理（ライフサイクル軸） |
| **用途** | grep検索、INDEX.md フィルタ | ステータス管理、月別整理 |
| **例** | `_architecture`, `_process`, `_governance` | `active/2025/10/`, `deprecated/2025/09/` |
| **独立性** | 独立：新しいカテゴリ追加も可能 | 独立：ディレクトリ階層変更も可能 |

### 検索フロー

```
「architecture に関する、2025年10月の active ADR を見たい」

     ↓
 
Step 1: ディレクトリで絞り込み
        → docs/decisions/active/2025/10/

Step 2: カテゴリで絞り込み
        → find docs/decisions/active/2025/10/ -name "*_architecture.md"

     ↓
結果: docs/decisions/active/2025/10/20251028_0001_ci-cd-pause_architecture.md
```

### AI が判定すべきこと

ADRを新規作成する際、以下を確認：

```
1. 【ディレクトリ】このADRのステータスは?
   → active/deprecated/superseded のいずれか?

2. 【ディレクトリ】対象年月は?
   → {YYYY}/{MM} の形式で正確に指定

3. 【カテゴリタグ】このADRの内容分類は?
   → DOCUMENTATION_STRUCTURE.yml の categories から選択

4. 【ファイル名】最終的なパスは正確か?
   → docs/decisions/{status}/{YYYY}/{MM}/{YYYYMMDD}_{NNNN}_{slug}_{category}.md
```

---

## 📚 参考資料

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [docs/governance/DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml) - 機械可読形式の定義
- [docs/governance/HIERARCHY_RULES.md](HIERARCHY_RULES.md) - 階層ルール詳細
- **[ADR-0011: ファイル名ケース規則](../decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md)** - 大文字/小文字の使い分けルール
- **[ADR-0012: ハイフン・アンダースコア規則](../decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md)** - 区切り文字の使い分けルール

---

**このガイドラインは `.github/copilot-instructions.md` と統合され、全てのAI環境で参照されます。**
