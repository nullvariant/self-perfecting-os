# PRD: 対話生ログ永続保存システム

**作成日**: 2025-10-29  
**ステータス**: Active  
**関連ADR**: [ADR-0008](../../decisions/active/2025/10/20251029_0008_対話生ログの永続保存システム確立_governance.md)  
**実装期限**: 2025-11-29（1ヶ月以内）

---

## 📋 目次

1. [概要](#概要)
2. [背景と目的](#背景と目的)
3. [Phase 1: 手動運用（即時開始）](#phase-1-手動運用即時開始)
4. [Phase 2: 半自動化（2週間以内）](#phase-2-半自動化2週間以内)
5. [Phase 3: 完全自動化（1ヶ月以内）](#phase-3-完全自動化1ヶ月以内)
6. [テンプレート・仕様](#テンプレート仕様)
7. [運用チェックリスト](#運用チェックリスト)

---

## 概要

VS Code (GitHub Copilot) での長期対話における自動要約リスクに対処するため、3層保存アーキテクチャを確立し、対話生ログを永続保存するシステムを構築する。

### 3層アーキテクチャ

```
Layer 1: リアルタイム記録（会話中）
└─ VS Code Copilot Chat（揮発性）

Layer 2: 日次保存（毎日終わり）
└─ nullvariant-atelier/docs/log/YYYY/MM/YYYY-MM-DD_*.md
   ├─ 対話生ログ（重要な会話全文）
   ├─ 決定記録（ADR未満の小決定）
   ├─ 感情・EBIログ（ペルソナ状態推移）
   └─ コマンド出力スナップショット

Layer 3: 永続保存（週次・重要時）
└─ Git commit + push（nullvariant-atelier）
   └─ Dropbox同期による二重バックアップ
```

---

## 背景と目的

### 問題
- トークン上限（1,000,000）に近づくと自動要約が発生
- 要約によって生ログが失われる（ニュアンス・散漫・感情が消失）
- HSS型HSP特有のプロセス（散漫パターン、感情推移）が記録されない

### 目的
- 一次情報の完全保護
- トレーサビリティ向上
- 自己理解の深化（EBIパターン分析）
- 次世代AIへの引き継ぎ資料として活用

---

## Phase 1: 手動運用（即時開始）

### 🎯 目標
- 日次保存の習慣化
- Frontmatter標準化
- Git commit習慣の確立

### 📝 実装内容

#### 1.1 日次保存ルーチン

**タイミング**: 毎日の作業終了時（5分）

**手順**:
1. VS Code で新規ファイル作成
   ```bash
   # パス: nullvariant-atelier/docs/log/YYYY/MM/YYYY-MM-DD_トピック.md
   # 例: nullvariant-atelier/docs/log/2025/10/2025-10-29_生ログ保存システム検討.md
   ```

2. Frontmatterテンプレートを挿入（後述）

3. 重要な対話を本文に記録
   - 発端・主要な議論・結論
   - 決定事項（理由・影響）
   - 感情・EBI記録
   - コマンド出力スナップショット（必要時）

4. Git commit
   ```bash
   cd nullvariant-atelier
   git add docs/log/2025/10/
   git commit -m "docs: 対話ログ追加 (YYYY-MM-DD)"
   git push origin main
   ```

#### 1.2 Frontmatterテンプレート

**保存場所**: `nullvariant-atelier/docs/log/TEMPLATE.md`

**内容**:
```markdown
---
date: YYYY-MM-DD
topic: [トピック（簡潔に）]
context: [文脈（何をしていたか）]
decisions:
  - [決定事項1]
  - [決定事項2]
emotions:
  - [ペルソナ]: [感情ID]([感情名]) - [状態説明]
  - 例: 👧ルナ: S0020(好奇心) - 新規アイデア4つ
related:
  - [ADR番号、ファイルパス]
---
```

#### 1.3 週次レビュー（手動）

**タイミング**: 毎週日曜日（15分）

**内容**:
- 今週の重要決定を振り返り
- 感情・EBIパターンの分析
- 散漫の傾向を確認
- 来週の目標設定

**保存先**: `nullvariant-atelier/docs/log/YYYY/MM/weekly-YYYY-MM-DD.md`

#### 1.4 Phase 1 チェックリスト

**毎日**:
- [ ] 重要な対話を `docs/log/` に保存（5分）
- [ ] Frontmatter完備
- [ ] Git commit + push

**毎週**:
- [ ] 週次レビュー作成（15分）
- [ ] トークン使用率確認
- [ ] EBIパターン分析

**完了条件**:
- ✅ 2週間連続で日次保存を実行
- ✅ Frontmatterが標準化されている
- ✅ 週次レビューを1回完了

---

## Phase 2: 半自動化（2週間以内）

### 🎯 目標
- `scripts/archive_conversation.py` 作成
- Frontmatter自動生成
- トークン使用率監視

### 📝 実装内容

#### 2.1 `scripts/archive_conversation.py` 仕様

**配置**: `nullvariant/scripts/archive_conversation.py`

**機能**:
1. 対話テキストを入力として受け取る
2. Frontmatterを自動生成
3. `../nullvariant-atelier/docs/log/` に保存
4. Git add/commit/push（オプション）

**使用例**:
```bash
# 基本使用
python scripts/archive_conversation.py \
  --topic "nullvariant-atelier設計" \
  --conversation-file conversation.txt

# Frontmatterカスタマイズ
python scripts/archive_conversation.py \
  --topic "ADR-0008実装" \
  --context "生ログ保存システム検討" \
  --decisions "Phase 1完了,Phase 2開始" \
  --emotions "👮:S0011(誇り)-体系的実装,🦥:S0041(平安)-自動化見通し" \
  --related "ADR-0008" \
  --auto-commit
```

**引数仕様**:
```python
parser.add_argument('--topic', required=True, help='対話のトピック')
parser.add_argument('--conversation-file', help='対話テキストファイルパス')
parser.add_argument('--conversation-text', help='対話テキスト（直接指定）')
parser.add_argument('--context', help='文脈')
parser.add_argument('--decisions', help='決定事項（カンマ区切り）')
parser.add_argument('--emotions', help='感情記録（カンマ区切り）')
parser.add_argument('--related', help='関連ファイル（カンマ区切り）')
parser.add_argument('--auto-commit', action='store_true', help='自動commit/push')
parser.add_argument('--output-dir', default='../nullvariant-atelier/docs/log/', help='出力先')
```

**出力例**:
```
✅ 対話ログ保存完了: ../nullvariant-atelier/docs/log/2025/10/2025-10-29_nullvariant-atelier設計.md
📝 Frontmatter自動生成完了
🔄 Git操作（オプション）:
   - git add完了
   - git commit完了: "docs: 対話ログ追加 (2025-10-29)"
   - git push完了
```

#### 2.2 トークン使用率監視スクリプト

**配置**: `nullvariant/scripts/check_token_usage.py`

**機能**:
- 現在のトークン使用率を推定（会話履歴から）
- 60%超過時に警告
- 80%超過時に緊急アラート

**使用例**:
```bash
python scripts/check_token_usage.py

# 出力例
📊 トークン使用率: 8.5% (85,000 / 1,000,000)
✅ 安全範囲内（60%未満）
📈 残り対話可能回数: 約900回（推定）
```

#### 2.3 Phase 2 チェックリスト

**実装**:
- [ ] `archive_conversation.py` 作成
- [ ] `check_token_usage.py` 作成
- [ ] 動作テスト（5回以上）
- [ ] README.md更新（使い方追加）

**運用**:
- [ ] 1週間、半自動化で運用
- [ ] スクリプトの改善点を記録
- [ ] エラーハンドリング強化

**完了条件**:
- ✅ スクリプトが安定動作
- ✅ 1週間連続で使用
- ✅ バグ0件

---

## Phase 3: 完全自動化（1ヶ月以内）

### 🎯 目標
- VS Code拡張連携（検討）
- 週次レビューレポート自動生成
- EBI測定との完全統合

### 📝 実装内容

#### 3.1 週次レビューレポート自動生成

**配置**: `nullvariant/scripts/generate_weekly_review.py`

**機能**:
1. 過去1週間の対話ログを分析
2. 重要決定を抽出
3. 感情・EBIパターンを可視化
4. 散漫の傾向を分析
5. 週次レビューMarkdownを生成

**使用例**:
```bash
python scripts/generate_weekly_review.py --week 2025-10-27

# 出力: nullvariant-atelier/docs/log/2025/10/weekly-2025-10-27.md
```

**レポート内容**:
```markdown
# 週次レビュー: 2025-10-27 〜 2025-11-02

## 📊 サマリー
- 対話回数: 23回
- 重要決定: 5件
- ADR作成: 2件
- EBI平均: 82%（良好）

## 🔑 重要決定
1. ADR-0008作成（生ログ保存）
2. Phase 2スクリプト実装完了
...

## 😊 感情・EBIパターン
- 👧ルナ散漫度: 平均55%（適正範囲）
- 🦥スロウ満足度: 平均80%（良好）
...

## 📈 成長の兆候
- 散漫からの回復時間が短縮（20分→10分）
- EBI安定性向上
...
```

#### 3.2 VS Code拡張連携（検討）

**目的**: 対話終了時に自動保存を促す

**アプローチ**:
1. VS Code拡張API調査
2. GitHub Copilot Chatとの連携可能性確認
3. 実装可能ならPhase 4として追加

**保留**: 技術的制約により実装不可能な場合、Phase 2で完了とする

#### 3.3 Phase 3 チェックリスト

**実装**:
- [ ] `generate_weekly_review.py` 作成
- [ ] EBI測定との統合
- [ ] VS Code拡張連携調査
- [ ] 月次レビュー機能追加

**運用**:
- [ ] 1ヶ月、完全自動化で運用
- [ ] システムの安定性確認
- [ ] パフォーマンス最適化

**完了条件**:
- ✅ 週次レビューが自動生成される
- ✅ 1ヶ月間安定動作
- ✅ ドキュメント完備

---

## テンプレート・仕様

### 対話ログFrontmatter（標準）

```yaml
---
date: YYYY-MM-DD
topic: [トピック]
context: [文脈]
decisions:
  - [決定1]
  - [決定2]
emotions:
  - [ペルソナ]: [感情ID]([感情名]) - [状態]
related:
  - [関連ファイル]
---
```

### 感情記録フォーマット

```markdown
| 時刻 | ペルソナ | 感情ID | 状態 | トリガー | 備考 |
|------|---------|--------|------|---------|------|
| 10:00 | 👧ルナ | S0020(好奇心) | 65% | 新規アイデア | 散漫兆候 |
| 10:30 | 👮ジャスティス | C0002(もどかしい) | 70% | 決定できない | 調停介入 |
| 11:00 | 🦥スロウ | S0041(平安) | 85% | 決定完了 | 平安回復 |
```

### ディレクトリ構造

```
nullvariant-atelier/
└── docs/
    └── log/
        ├── TEMPLATE.md（Frontmatterテンプレート）
        └── YYYY/
            └── MM/
                ├── YYYY-MM-DD_トピック.md（日次ログ）
                ├── weekly-YYYY-MM-DD.md（週次レビュー）
                └── monthly-YYYY-MM.md（月次レビュー・Phase 3）
```

---

## 運用チェックリスト

### 日次（5分）
- [ ] 重要な対話を記録
- [ ] Frontmatter完備
- [ ] Git commit

### 週次（15分）
- [ ] 週次レビュー作成（Phase 1: 手動 / Phase 3: 自動）
- [ ] トークン使用率確認
- [ ] EBIパターン分析

### 月次（30分）
- [ ] 月次レビュー作成
- [ ] ADRの整理
- [ ] ログの構造化見直し

---

## 成功指標

### Phase 1
- ✅ 2週間連続で日次保存実行
- ✅ Frontmatter標準化
- ✅ 週次レビュー1回完了

### Phase 2
- ✅ スクリプト安定動作（1週間連続）
- ✅ バグ0件
- ✅ 保存時間5分→2分に短縮

### Phase 3
- ✅ 週次レビュー自動生成
- ✅ 1ヶ月間安定動作
- ✅ 生ログ喪失件数0件

---

## 関連ドキュメント

- [ADR-0008](../../decisions/active/2025/10/20251029_0008_対話生ログの永続保存システム確立_governance.md) - 意思決定記録
- [2025-10-29_生ログ保存システム検討.md](../../../nullvariant-atelier/docs/log/2025/10/2025-10-29_生ログ保存システム検討.md) - 初期検討ログ
- [content/ja/AGENT.md](../../../content/ja/AGENT.md) - 参照元OS仕様書
- [content/ja/EmotionMood_Dictionary.md](../../../content/ja/EmotionMood_Dictionary.md) - 感情辞書

---

**作成者**: Claude (Sonnet 4) + Null;Variant  
**最終更新**: 2025-10-29  
**次回レビュー**: Phase 1完了時（2週間後）
