---
category: documentation
date: 2025-10-28
number: 0006
status: Accepted
---

# ADR-0006: GitHub Pagesランディングページの実装

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: GitHub Copilot + human

## Context

### 背景
index.htmlがW3.CSSテンプレートのまま放置されていた。2025年6月21日に`static.yml`と同時に作成されたが、内容は「My Logo」というプレースホルダーのままで、実際のコンテンツが設定されていなかった。

nullvariant.github.ioは別リポジトリ（ユーザーサイト）として存在するため、本リポジトリのGitHub Pages（`https://nullvariant.github.io/nullvariant/`）は**プロジェクトサイト**として機能する。

### 検討した選択肢
1. **最小限リダイレクト**: noteへの即リダイレクトまたはGitHub案内のみ（🦥スロウ推奨）
2. **ランディングページ**: プロジェクト紹介とナビゲーション（👮ジャスティス推奨）
3. **ドキュメントポータル**: 各種ドキュメントへの整理されたリンク集
4. **完全削除**: GitHub Pagesを無効化

## Decision

**選択肢2：ランディングページ**を実装

### 実装内容
- **デザイン**: ミニマル・清潔感重視
- **フォント**: システムフォント使用（`-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP"`）
- **構成**: 3セクション
  - 📖 Documentation（AGENT.md、感情辞書、Governance Docs）
  - 📝 Articles（note、Changelog Magazine）
  - 🔧 Development（GitHub Repository、CHANGELOG.md）
- **カラースキーム**: 背景`#fafafa`、テキスト`#1a1a1a`、アクセント`#3b82f6`
- **インタラクション**: ホバー時の`→`アニメーション
- **レスポンシブ**: モバイル対応（640px以下でレイアウト調整）

### 採用理由
- プロジェクトの顔として意味のあるコンテンツを提供
- 外部フォント読み込みなし（システムフォント）でページ速度を維持
- 6ペルソナ全員の美学に適合：
  - 👮ジャスティス: シンプルで整った構造
  - 👧ルナ: 絵文字で視覚的な楽しさ
  - 🦥スロウ: 軽量・高速（追加リソースなし）
  - 🐗ブレイズ: 本質的な情報のみ
  - 🕊️シエル: 柔らかい色味・受容的デザイン
  - 🐰ミミ: 外部評価に耐える洗練度

## Consequences

### ✅ メリット
- プロジェクトの第一印象が向上
- 主要ドキュメント・記事への明確なナビゲーション
- システムフォント使用で追加読み込みなし（高速）
- GitHub Actionsで自動デプロイ（`.github/workflows/static.yml`）
- レスポンシブ対応でモバイルでも閲覧可能

### ⚠️ デメリット
- メンテナンスコストの増加（リンク更新など）
- Figmaなどでの作り込みをしていないため、将来的な洗練度向上の余地あり

### 📋 TODO
- [x] index.html実装
- [x] GitHub Pagesへのデプロイ確認
- [x] ADR記録
- [ ] 将来的なデザイン改善（必要に応じて）

## Related

### 関連するファイル
- `index.html` - ランディングページ本体
- `.github/workflows/static.yml` - GitHub Pages デプロイワークフロー
- `content/ja/AGENT.md` - システム仕様書（リンク先）
- `content/ja/EmotionMood_Dictionary.md` - 感情辞書（リンク先）

### 関連する Commit
- `841d9f9` - Create index.html（2025-06-21：W3.CSSテンプレート作成）
- `6efc723` - feat: Replace W3.CSS template with clean landing page（2025-10-28：本実装）

---

**Status**: Accepted  
**実装完了**: 2025-10-28
