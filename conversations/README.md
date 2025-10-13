# 対話ログ / Conversation Logs

## 概要

このディレクトリには、AGENT.md及び関連トピックに関する、作者とAIとの対話記録を保存します。

これらの対話ログは：
- AGENT.mdの解釈・応用可能性の探索
- 未来の読者への「使用例」ガイド
- note記事等のコンテンツ素材
- 思考プロセスの透明な記録

として機能します。

## 命名規則

```
YYYY-MM-DD_topic-slug.md
```

- **日付:** 対話が行われた日（ISO 8601形式）
- **トピックスラッグ:** 対話の主題（kebab-case）

例：
- `2025-10-13_agent-meta-dialogue.md`
- `2025-11-05_hsp-survival-strategy.md`

## フォーマット

各対話ログは以下の構造を持ちます：

### 1. Frontmatter（YAMLメタデータ）
```yaml
---
title: "対話のタイトル"
date: YYYY-MM-DD
participants:
  - 参加者1
  - 参加者2
topics:
  - トピック1
  - トピック2
primary_language: ja
word_count: 約XX,XXX
status: completed
note_article_candidate: true/false
related_documents:
  - path/to/related/doc.md
tags:
  - tag1
  - tag2
---
```

### 2. 本文構造
- **概要**: 対話の背景・目的・成果
- **対話の文脈**: 日時・参加者・総文字数等
- **主要なテーマ**: トピックごとの要約
- **完全な対話記録**: 時系列での全発言
- **メタ的考察**: 対話自体の意義・価値
- **関連ドキュメント**: 参照リンク

## 対話ログ一覧

### 2025年

| 日付 | タイトル | トピック | 文字数 | note転用 |
|------|---------|---------|--------|----------|
| 2025-10-13 | [AGENT.mdに関するメタ対話](2025-10-13_agent-meta-dialogue.md) | AGENT.md解釈、AIモデル相性、社会システム批判、資本主義攻略、遺書としての価値 | ~50,000 | ✅ 候補 |

## note記事転用候補

以下の対話ログは、note記事として特に価値が高いと判断されています：

### ✅ 2025-10-13: AGENT.mdに関するメタ対話

**転用可能なセクション：**

1. **「AIとの相性：なぜGPT-5は合わないのか」**
   - 対象：AIユーザー全般
   - 推定文字数：3,000-5,000字
   - 優先度：高

2. **「資本主義の攻略法：時間富裕層になる方法」**
   - 対象：働き方に悩む人
   - 推定文字数：5,000-8,000字
   - 優先度：高

3. **「47,000字の遺書を書いた話」**
   - 対象：自己探求に興味がある人
   - 推定文字数：2,000-4,000字
   - 優先度：高

4. **「『めんどくさい』が最強の売りになる理由」**
   - 対象：HSP・ADHD・自己理解に興味がある人
   - 推定文字数：2,000-3,000字
   - 優先度：中

5. **「ジョブ型 vs 存在雇用」**
   - 対象：働き方の哲学に興味がある人
   - 推定文字数：3,000-4,000字
   - 優先度：中

6. **「自己完成が他者を幸せにする逆説」**
   - 対象：利己と利他の統合に興味がある人
   - 推定文字数：3,000-4,000字
   - 優先度：中

## 管理方針

### GitHub管理対象
対話ログは公開価値があるため、GitHubで管理します。

### Obsidianとの連携
必要に応じて、Obsidianにも参照用コピーを作成可能です（手動）。  
「正」の情報源はGitHub版とします。

### 将来的な拡張
- 自動要約システム（AI活用）
- note記事への半自動転換ツール
- トピック別索引の自動生成
- 多言語展開（英語翻訳版）

詳細は [docs/WORKFLOW_TEXT_ASSETS.ja.md](../docs/WORKFLOW_TEXT_ASSETS.ja.md) を参照してください。

## 関連ドキュメント

- [AGENT.ja.md](../content/AGENT.ja.md) - 本体仕様書
- [EmotionMood_Dictionary.ja.md](../content/EmotionMood_Dictionary.ja.md) - 感情辞書
- [changelogs/](../changelogs/) - バージョン履歴・思考記録
- [docs/WORKFLOW_TEXT_ASSETS.ja.md](../docs/WORKFLOW_TEXT_ASSETS.ja.md) - テキスト資産管理ワークフロー
