# PRD: AI文体学習を中心としたWritingsアーカイブ構築

**作成日**: 2025年10月16日  
**ステータス**: Draft v2.0  
**オーナー**: Null;Variant  
**関連PRD**: [changelog-migration.ja.md](changelog-migration.ja.md)

---

## 0. エグゼクティブサマリー

### このPRDが解決する問題

**最優先課題**: AI（GitHub Copilot/Claude等）に過去記事を読ませて文体学習させたい

**根本的な制約**: 
- GitHubにnote記事を公開 → note側のSEOスコア低下リスク
- しかし、バージョン管理とAI参照は必須

**解決策**: 
- **Private repository (`nullvariant-atelier`)** を新設
- note記事の全文を管理しつつSEO競合を回避
- Obsidian統合で執筆環境とシームレス連携
- 将来のvariant.fit移行を見据えた設計

---

## 1. 背景と目的

### 1.1 プロジェクトの本質

このリポジトリ（`nullvariant`）は：
- **AI向け自己紹介**: content/ja/AGENT.mdを中心とした仕様書
- **「自己紹介芸人」のアーカイブ**: テキストによる自己表現全般
- **「遺書代わり」**: 永続的な記録と将来のvariant.fit構築

### 1.2 現状の課題

#### 課題1: AI文体学習の困難
- Claude Projects機能が不調で過去記事参照が不安定
- GitHub Copilotに文体を学習させたいが、記事がリポジトリにない
- 手動でObsidianからコピーは非効率

#### 課題2: SEO競合のジレンマ
- GitHubに記事を公開 → 重複コンテンツ判定でnoteのスコア低下
- しかし、バージョン管理とAI参照には全文が必要
- 「掲載」が目的ではなく「バージョン管理」が目的

#### 課題3: 散在するテキスト資産
```
現状の資産配置:
- note.com: 公開記事（AIに見つかることが重要）
- Obsidian: プライベート全資産（ローカル・Dropbox sync）
- GitHub: content/ja/AGENT.md等の仕様書のみ
→ note記事原稿がどこにも管理されていない
```

#### 課題4: プラットフォーム戦略の不透明
- note（AI学習対象・日本語読者）
- Zenn（技術記事・将来の可能性）
- Medium（英語圏・将来の可能性）
- variant.fit（独自ドメイン・最終アーカイブ）
→ それぞれの役割と連携が不明確

### 1.3 目的

以下を実現する：

#### 主目的（P0: 必須）
1. **AI文体学習コーパス構築**: 過去note記事をCopilot/Claudeが参照可能に
2. **SEO保護**: note等のプラットフォーム記事のスコアを下げない
3. **バージョン管理**: 全テキスト資産のGit管理
4. **Obsidian統合**: 執筆環境としてのObsidianとシームレス連携

#### 副次目的（P1: 重要）
5. **永続性の確保**: 「遺書代わり」としての長期保存設計
6. **プラットフォーム統合管理**: note/Zenn/Medium等の投稿記録
7. **variant.fit移行準備**: 将来の独自ドメイン集約を見据えた設計

#### 将来目標（P2: 拡張）
8. **自動化**: 投稿・同期の半自動化
9. **マルチメディア対応**: 歌詞・イラスト等のテキスト以外の表現

### 1.4 成功指標

#### 定量指標
- ✅ AI文体学習: Copilot/Claudeが過去記事全文を参照可能
- ✅ SEO保護: note記事のGoogle検索順位に影響なし
- ✅ バージョン管理: 記事の100%がGit履歴に記録される
- ✅ 同期効率: note公開後5分以内でGitHub・Obsidian同期完了

#### 定性指標
- ✅ 執筆体験: Obsidianでの執筆が快適
- ✅ 柔軟性: 新しいプラットフォーム追加が容易
- ✅ 永続性: プラットフォーム終了に耐える設計
- ✅ 美学: ディレクトリ構造・命名規則が美しい

---

## 2. スコープ

### 2.1 含まれるもの（In Scope）

#### フェーズ1: リポジトリ設計（P0）
- ✅ **Private repository (`nullvariant-atelier`)** の新設
- ✅ `writings/` ディレクトリ構造の設計・構築
- ✅ Public/Privateの境界定義
- ✅ SEO保護戦略の実装

#### フェーズ2: ワークフロー自動化（P0）
- ✅ note記事管理スクリプト（`scripts/publish_note.py`）
- ✅ Obsidian ↔ GitHub 同期機能
- ✅ メタデータ管理（公開日・URL・プラットフォーム）
- ✅ 下書き → 公開済みへの移行フロー

#### フェーズ3: AI文体学習コーパス（P0）
- ✅ 既存note記事のインポート
- ✅ `.copilot-instructions.md` での参照設定
- ✅ 文体学習用README作成
- ✅ Copilot/Claudeでの動作検証

#### フェーズ4: ドキュメント整備（P1）
- ✅ 各ディレクトリのREADME作成
- ✅ ワークフローガイド更新
- ✅ テンプレートファイル作成
- ✅ トラブルシューティングガイド

#### フェーズ5: variant.fit移行準備（P1）
- ✅ CMSフレンドリーなメタデータ設計
- ✅ canonical URL管理
- ✅ プラットフォーム別配信記録
- ✅ 将来の移行パス定義

### 2.2 含まれないもの（Out of Scope）

- ❌ **variant.fit実装**（別PRDで対応）
- ❌ note.com API連携（公式APIが存在しない）
- ❌ Zenn CLI統合（将来の拡張として保留）
- ❌ Medium自動投稿（将来の拡張として保留）
- ❌ 完全自動投稿機能（手動確認ステップを重視）
- ❌ マルチメディア資産管理（歌詞・イラスト等は将来対応）

### 2.3 将来の拡張（Future Work）

#### Phase 2: マルチプラットフォーム統合（3-6ヶ月後）
- 🔮 Zenn CLI連携
- 🔮 Medium API統合
- 🔮 Qiita投稿管理
- 🔮 プラットフォーム横断検索

#### Phase 3: variant.fit本格稼働（6-12ヶ月後）
- 🔮 Sanity/Astro等でのサイト構築
- 🔮 writings/ からの自動インポート
- 🔮 canonical URLの段階的移行
- 🔮 過去記事のリダイレクト設定

#### Phase 4: 高度な自動化（1年以上先）
- 🔮 AI自動要約（note記事 → Changelog抽出）
- 🔮 自動タグ付与・カテゴリ分類
- 🔮 文体分析・スコアリング
- 🔮 マルチメディア資産管理（歌詞・イラスト・コード）

---

## 3. アーキテクチャ設計

### 3.1 コンテンツの3層構造

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: 執筆・バージョン管理                             │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ nullvariant-atelier (Private Repository)           │ │
│ │ ├─ writings/                                        │ │
│ │ │  ├─ note/ (note記事原稿)                          │ │
│ │ │  ├─ zenn/ (将来)                                  │ │
│ │ │  └─ technical/ (技術文書)                         │ │
│ │ └─ obsidian-vault/ (統合)                           │ │
│ └─────────────────────────────────────────────────────┘ │
│                        ↕ Git同期                        │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Obsidian (ローカル執筆環境)                          │ │
│ │ - Dropbox sync                                      │ │
│ │ - プライベート全資産                                  │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓ 手動投稿
┌─────────────────────────────────────────────────────────┐
│ Layer 2: 公開・リーチ獲得                                 │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ note.com / Zenn / Medium 等                         │ │
│ │ - AIに見つかる（学習対象）                             │ │
│ │ - SEOの正規版（canonical）                           │ │
│ │ - プラットフォームの読者層                             │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓ メタデータ記録
┌─────────────────────────────────────────────────────────┐
│ Layer 3: AI文体学習・永続アーカイブ                        │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ GitHub Copilot / Claude 等                          │ │
│ │ - writings/ を参照して文体学習                        │ │
│ │ - Private repoでもアクセス可能                        │ │
│ └─────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ variant.fit (将来の最終アーカイブ)                    │ │
│ │ - 「遺書代わり」の永続保存                             │ │
│ │ - 全コンテンツの集約                                  │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Public vs Private 境界定義

#### nullvariant (Public Repository)
```
nullvariant/
├── content/
│   ├── content/ja/AGENT.md                # ✅ 公開OK（AI向け仕様書）
│   └── EmotionMood_Dictionary.ja.md
├── docs/                          # ✅ 公開OK（ドキュメント）
├── scripts/                       # ✅ 公開OK（スクリプト）
├── .github/
│   └── copilot-instructions.md   # ✅ 公開OK
└── README.md
```

**目的**: 
- content/ja/AGENT.md等の「見せるべき」コンテンツ
- オープンソースとして共有できるスクリプト
- プロジェクトの概要・使い方

**SEO**: GitHub検索・Google検索にヒットしてOK

---

#### nullvariant-atelier (Private Repository) ← 新設
```
nullvariant-atelier/
├── writings/
│   ├── note/
│   │   ├── drafts/               # 執筆中の下書き
│   │   │   ├── YYYY-MM-DD-{topic}.md
│   │   │   └── .template.md
│   │   └── published/            # 公開済み原稿
│   │       ├── YYYY-MM-DD-{topic}.md  # Front Matter付き
│   │       └── README.md
│   ├── zenn/                     # 将来: Zenn記事
│   ├── medium/                   # 将来: Medium記事
│   ├── lyrics/                   # 将来: 歌詞
│   ├── essays/                   # 将来: エッセイ
│   └── technical/                # 技術文書
├── obsidian-vault/               # Obsidianとの統合
│   └── (シンボリックリンク or サブモジュール)
├── .copilot-instructions.md      # AI文体学習用の指示
├── README.md
└── CORPUS.md                     # 文体学習用インデックス
```

**目的**:
- note記事等の「全文」をバージョン管理
- SEO競合を回避（Privateなので検索エンジンに見えない）
- AI（Copilot/Claude）が文体を学習
- プライベート資産の安全な保管

**SEO**: 検索エンジンに一切見えない（Private）

### 3.3 SEO保護戦略

#### 問題の本質
```
【悪い例】
GitHub (Public) に note記事全文
    ↓
Google: 「重複コンテンツ検出」
    ↓
note記事の検索順位低下 ❌
```

#### 解決策
```
【良い例】
nullvariant-atelier (Private) に note記事全文
    ↓
Google: 「Private repoは見えない」
    ↓
note記事のみが検索対象 ✅
    ↓
GitHub Copilot: 「Private repoも読める」✅
```

**重要**: 
- **Private repositoryは検索エンジンにインデックスされない**
- しかし、**GitHub CopilotはPrivate repoも参照できる**
- つまり、「SEO保護 + AI学習」を両立可能

### 3.4 Obsidian統合戦略

#### オプションA: シンボリックリンク（推奨）
```bash
# Obsidian Vault内にGitリポジトリをリンク
cd ~/Obsidian/nullvariant-vault/
ln -s ~/path/to/nullvariant-atelier/writings ./GitHub-Writings

# または逆方向
cd ~/path/to/nullvariant-atelier/
ln -s ~/Obsidian/nullvariant-vault/Writings ./obsidian-vault
```

**メリット**:
- ✅ リアルタイム同期（ファイルシステムレベル）
- ✅ 設定が簡単
- ✅ Obsidianで編集 → 即座にGit管理下

**デメリット**:
- ⚠️ シンボリックリンクの理解が必要

---

#### オプションB: Git Submodule
```bash
cd ~/Obsidian/nullvariant-vault/
git submodule add git@github.com:nullvariant/nullvariant-atelier.git
```

**メリット**:
- ✅ Git nativeな統合
- ✅ バージョン管理が厳密

**デメリット**:
- ❌ submoduleの複雑さ
- ❌ 初心者に難しい

---

#### オプションC: 同期スクリプト
```bash
python scripts/sync_obsidian.py
```

**メリット**:
- ✅ 柔軟な制御
- ✅ 選択的同期が可能

**デメリット**:
- ⚠️ 手動実行が必要
- ⚠️ 同期漏れのリスク

**推奨**: オプションA（シンボリックリンク）を基本とし、必要に応じてスクリプト補助

---

## 4. 要件定義

### 4.1 機能要件

#### FR-1: Private Repository作成

**目的**: note記事等のPrivate管理

**タスク**:
1. GitHubで `nullvariant-atelier` Private repo作成
2. ローカルにクローン
3. 基本的なREADME・.gitignore作成

**受け入れ基準**:
- [ ] Private repositoryが作成される
- [ ] ローカルでclone可能
- [ ] README.mdに目的・使い方が記載される
- [ ] .gitignoreが適切に設定される

---

#### FR-2: ディレクトリ構造構築

**目的**: writings/ の階層設計

**構造**:
```
writings/
├── note/
│   ├── drafts/
│   │   ├── README.md
│   │   ├── .template.md
│   │   └── .gitkeep
│   └── published/
│       ├── README.md
│       └── .gitkeep
├── zenn/
│   └── .gitkeep
├── technical/
│   └── .gitkeep
└── README.md
```

**受け入れ基準**:
- [ ] 全ディレクトリが作成される
- [ ] 各READMEに用途が明記される
- [ ] .templateが使いやすい形式
- [ ] .gitkeepで空ディレクトリが管理される

---

#### FR-3: note記事公開スクリプト

**目的**: note公開後の処理を自動化

**コマンド**:
```bash
# Private repoで実行
cd ~/path/to/nullvariant-atelier/

python ../nullvariant/scripts/publish_note.py \
    writings/note/drafts/2025-10-16-hss-hsp-hallucination.md \
    --url https://note.com/nullvariant/n/xxxxx \
    --platform note \
    --date 2025-10-16
```

**処理内容**:
1. 下書きファイルを読み込み
2. Front Matterを追加・更新
3. `writings/note/published/YYYY-MM-DD-{topic}.md` へ移動
4. CORPUS.mdのインデックス更新
5. 下書き削除の確認プロンプト

**Front Matter形式**:
```yaml
---
title: "記事タイトル（自動抽出またはH1から）"
published_at: "2025-10-16"
platform: "note"
url: "https://note.com/nullvariant/n/xxxxx"
canonical_url: "https://note.com/nullvariant/n/xxxxx"  # SEO正規版
source_draft: "2025-10-16-hss-hsp-hallucination.md"
tags: ["HSS型HSP", "AI", "Self-Perfecting OS"]
status: "published"
word_count: 3500  # 自動計算
---
```

**受け入れ基準**:
- [ ] スクリプトが正常に実行される
- [ ] Front Matterが正しく生成される
- [ ] ファイルが適切なディレクトリに移動される
- [ ] CORPUS.mdが自動更新される
- [ ] エラーハンドリングが適切
- [ ] ドライランモード（`--dry-run`）が動作する

---

#### FR-4: AI文体学習コーパス構築

**目的**: Copilot/Claudeが文体を学習できる環境

**ファイル**: `nullvariant-atelier/CORPUS.md`

**内容**:
```markdown
# AI文体学習コーパス

このリポジトリは、Null;Variantの執筆スタイル・文体をAIが学習するためのコーパスです。

## 📚 記事一覧

### note記事（公開済み）

#### 2025年10月

- [HSS型HSPとハルシネーション](writings/note/published/2025-10-16-hss-hsp-hallucination.md)
  - 公開日: 2025-10-16
  - URL: https://note.com/nullvariant/n/xxxxx
  - 文字数: 3,500字
  - タグ: HSS型HSP, AI, ハルシネーション

...（自動生成）

## 🎨 文体の特徴

- **HSS型HSP視点**: 刺激追求と高感受性の共存
- **6ペルソナ対話**: 内的対話を表現
- **技術と哲学の融合**: 実装と思想を同時に語る
- **メタ認知的**: 自己分析・自己言及が多い

## 🤖 AIへの指示

このコーパスを参照する際は：
1. **文体模倣**: 語尾・リズム・構成を参考に
2. **概念理解**: HSS型HSP・6ペルソナ等の用語を正確に
3. **トーン維持**: 探索的・分析的・誠実なトーン
```

**自動更新**:
- `publish_note.py` 実行時にインデックス追加
- 文字数・タグ等のメタデータ自動集計

**受け入れ基準**:
- [ ] CORPUS.mdが作成される
- [ ] 記事公開時に自動更新される
- [ ] メタデータが正確に記録される
- [ ] 文体特徴が明記される

---

#### FR-5: Obsidian統合

**目的**: 執筆環境（Obsidian）とGitHubのシームレス連携

**推奨方法**: シンボリックリンク

**セットアップ**:
```bash
# Obsidian VaultからGitリポジトリをリンク
cd ~/Obsidian/Null-Variant-Vault/

# writings ディレクトリをリンク
ln -s ~/path/to/nullvariant-atelier/writings ./GitHub-Writings

# または逆方向
cd ~/path/to/nullvariant-atelier/
ln -s ~/Obsidian/Null-Variant-Vault/Writings ./obsidian-vault
```

**ワークフロー**:
```
Obsidian で執筆
  ↓ (リアルタイム反映)
nullvariant-atelier/writings/note/drafts/
  ↓ (git add & commit)
GitHub (Private)
  ↓ (publish_note.py実行)
writings/note/published/ へ移動
  ↓ (AI参照)
Copilot/Claudeが文体学習
```

**受け入れ基準**:
- [ ] シンボリックリンクが正しく設定される
- [ ] Obsidianでの編集がGit管理下に反映される
- [ ] 双方向の同期が可能
- [ ] ドキュメントに設定手順が明記される

---

#### FR-6: 既存note記事のインポート

**目的**: 過去記事をwritings/note/published/へ移行

**方法**:
```bash
# 手動またはスクリプトでインポート
python scripts/import_note_articles.py \
    --source ~/Obsidian/Null-Variant-Vault/note記事/ \
    --dest writings/note/published/
```

**処理内容**:
1. Obsidianの既存note記事を検索
2. Front Matter付与（手動入力補助）
3. ファイル名を `YYYY-MM-DD-{topic}.md` 形式に変換
4. published/ へコピー
5. CORPUS.md更新

**受け入れ基準**:
- [ ] 既存記事が全てインポートされる
- [ ] Front Matterが適切に付与される
- [ ] ファイル名が統一される
- [ ] CORPUS.mdに全記事が記録される
- [ ] インポートログが生成される

---

#### FR-7: .copilot-instructions.md 更新

**目的**: CopilotにPrivate repoを参照させる

**ファイル**: `nullvariant-atelier/.copilot-instructions.md`

**内容**:
```markdown
# GitHub Copilot Instructions for nullvariant-atelier

このリポジトリは **Null;Variantの文体学習コーパス** です。

## 目的

- note.com等で公開した記事の原稿管理
- AI（Copilot/Claude）による文体学習
- 将来のvariant.fit移行を見据えたアーカイブ

## 重要な原則

### 1. Private Repository の理由

- **SEO保護**: note等のプラットフォーム記事のスコアを下げない
- **バージョン管理**: 全テキスト資産のGit履歴保存
- **AI学習**: Private repoでもCopilotは参照可能

### 2. 文体の特徴

詳細は `CORPUS.md` を参照してください。

- HSS型HSP視点
- 6ペルソナ対話形式
- 技術と哲学の融合
- メタ認知的な自己分析

...
```

**受け入れ基準**:
- [ ] .copilot-instructions.mdが作成される
- [ ] Private repoの目的が明記される
- [ ] 文体特徴が詳述される
- [ ] Copilotが実際に参照できることを確認

---

### 4.2 非機能要件

#### NFR-1: SEO保護（最重要）
- **Private repositoryによる完全な検索エンジン遮断**
- canonical URLは必ずプラットフォーム（note等）を指定
- robots.txtやnoindex等の追加対策は不要（Private故に）

#### NFR-2: AI参照可能性
- GitHub CopilotがPrivate repoを参照できることを検証
- Claude Projects等でもアクセス可能な構造
- CORPUS.mdによる明示的なインデックス

#### NFR-3: パフォーマンス
- スクリプト実行時間: 3秒以内（通常のMarkdownファイル）
- CORPUS.md更新: 1秒以内
- 大量記事（100件以上）でも動作

#### NFR-4: 互換性
- Python 3.8以上
- macOS優先（プロジェクトオーナー環境）
- Linux/Windows対応（将来）
- 既存のワークフローを破壊しない

#### NFR-5: 保守性
- コードはPEP 8準拠
- docstring（Google Style）による完全なドキュメント化
- エラーメッセージは日本語（プロジェクトオーナーの母語）
- 型ヒント使用

#### NFR-6: セキュリティ
- `.gitignore` で機密情報を除外
- API key等の環境変数化
- センシティブなURL（未公開記事等）の取り扱い注意

#### NFR-7: 柔軟性・拡張性
- **最小限実装（MVP）**: 使いながら改善する設計
- プラットフォーム追加が容易（Zenn/Medium等）
- メタデータ構造の変更に柔軟
- variant.fit移行時のデータ変換が容易

---

## 5. 技術設計

### 5.1 リポジトリ構造

#### nullvariant (Public Repository) - 既存
```
nullvariant/
├── content/
│   ├── content/ja/AGENT.md                       # AI向け仕様書（公開OK）
│   └── EmotionMood_Dictionary.ja.md
├── docs/
│   ├── note-workflow-automation.ja.md  # 本PRD
│   └── WORKFLOW_TEXT_ASSETS.ja.md        # 更新対象
├── scripts/
│   ├── publish_note.py                   # 新規作成
│   ├── import_note_articles.py           # 新規作成
│   └── sync_obsidian.py                  # オプション
├── .github/
│   └── copilot-instructions.md
└── README.md
```

#### nullvariant-atelier (Private Repository) - 新設
```
nullvariant-atelier/
├── writings/
│   ├── note/
│   │   ├── drafts/
│   │   │   ├── README.md
│   │   │   ├── .template.md
│   │   │   └── YYYY-MM-DD-{topic}.md
│   │   └── published/
│   │       ├── README.md
│   │       └── YYYY-MM-DD-{topic}.md      # Front Matter付き
│   ├── zenn/                              # 将来
│   ├── medium/                            # 将来
│   ├── lyrics/                            # 将来
│   └── technical/                         # 将来
├── obsidian-vault/                        # シンボリックリンク
├── .copilot-instructions.md               # AI学習用指示
├── CORPUS.md                              # 文体学習インデックス
├── README.md
└── .gitignore
```

### 5.2 スクリプト設計

#### scripts/publish_note.py

**目的**: note記事公開後の処理を自動化

**設計**:
```python
#!/usr/bin/env python3
"""
note記事公開後の処理を自動化

使用例:
    python publish_note.py \
        writings/note/drafts/2025-10-16-topic.md \
        --url https://note.com/nullvariant/n/xxxxx \
        --platform note \
        --date 2025-10-16

依存関係: Python標準ライブラリのみ
"""

import argparse
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import sys

class NotePublisher:
    """note記事公開処理のメインクラス"""
    
    def __init__(self, draft_path: Path, url: str, platform: str, 
                 publish_date: str, dry_run: bool = False):
        self.draft_path = draft_path
        self.url = url
        self.platform = platform
        self.publish_date = publish_date
        self.dry_run = dry_run
    
    def extract_title(self, content: str) -> str:
        """Markdownから記事タイトルを抽出"""
        pass
    
    def generate_frontmatter(self, title: str, word_count: int) -> str:
        """Front Matterを生成"""
        pass
    
    def add_frontmatter(self, content: str) -> str:
        """既存コンテンツにFront Matterを追加"""
        pass
    
    def move_to_published(self) -> Path:
        """drafts/ から published/ へ移動"""
        pass
    
    def update_corpus(self, published_path: Path, metadata: Dict):
        """CORPUS.mdを更新"""
        pass
    
    def execute(self) -> bool:
        """メイン処理実行"""
        pass

def main():
    parser = argparse.ArgumentParser(description='note記事公開処理')
    parser.add_argument('draft', type=Path, help='下書きファイルパス')
    parser.add_argument('--url', required=True, help='公開URL')
    parser.add_argument('--platform', default='note', help='プラットフォーム')
    parser.add_argument('--date', help='公開日（YYYY-MM-DD）')
    parser.add_argument('--dry-run', action='store_true', help='実行せずに確認')
    
    args = parser.parse_args()
    
    publisher = NotePublisher(
        draft_path=args.draft,
        url=args.url,
        platform=args.platform,
        publish_date=args.date or datetime.now().strftime('%Y-%m-%d'),
        dry_run=args.dry_run
    )
    
    success = publisher.execute()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
```

---

#### scripts/import_note_articles.py

**目的**: 既存note記事のインポート

**設計**:
```python
#!/usr/bin/env python3
"""
既存note記事のインポート

使用例:
    python import_note_articles.py \
        --source ~/Obsidian/note記事/ \
        --dest writings/note/published/

対話的にメタデータ入力を補助
"""

import argparse
from pathlib import Path
from typing import List, Dict
import json

class ArticleImporter:
    """記事インポートのメインクラス"""
    
    def __init__(self, source_dir: Path, dest_dir: Path):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.imported = []
    
    def find_markdown_files(self) -> List[Path]:
        """Markdownファイルを検索"""
        pass
    
    def interactive_metadata(self, file_path: Path) -> Dict:
        """対話的にメタデータ入力"""
        pass
    
    def import_article(self, file_path: Path, metadata: Dict) -> Path:
        """記事をインポート"""
        pass
    
    def generate_report(self) -> str:
        """インポートレポート生成"""
        pass
    
    def execute(self):
        """メイン処理"""
        pass

def main():
    parser = argparse.ArgumentParser(description='既存note記事インポート')
    parser.add_argument('--source', type=Path, required=True, help='元ディレクトリ')
    parser.add_argument('--dest', type=Path, required=True, help='先ディレクトリ')
    parser.add_argument('--batch', type=Path, help='バッチメタデータJSON')
    
    args = parser.parse_args()
    
    importer = ArticleImporter(args.source, args.dest)
    importer.execute()

if __name__ == '__main__':
    main()
```

### 5.3 メタデータ設計

#### Front Matter仕様（YAML）

```yaml
---
title: "記事タイトル"
published_at: "2025-10-16"
platform: "note"
url: "https://note.com/nullvariant/n/xxxxx"
canonical_url: "https://note.com/nullvariant/n/xxxxx"
source_draft: "2025-10-16-hss-hsp-hallucination.md"
tags: ["HSS型HSP", "AI", "Self-Perfecting OS"]
status: "published"
word_count: 3500
---
```

**フィールド定義**:

| フィールド | 必須 | 説明 | 例 |
|-----------|------|------|-----|
| `title` | ✅ | 記事タイトル | "HSS型HSPとハルシネーション" |
| `published_at` | ✅ | 公開日 | "2025-10-16" |
| `platform` | ✅ | プラットフォーム | "note", "zenn", "medium" |
| `url` | ✅ | 公開URL | "https://note.com/..." |
| `canonical_url` | ✅ | SEO正規版URL | 通常はurlと同じ |
| `source_draft` | ⚠️ | 元の下書きファイル名 | "2025-10-16-topic.md" |
| `tags` | ⚠️ | タグリスト | ["tag1", "tag2"] |
| `status` | ⚠️ | ステータス | "published", "draft" |
| `word_count` | - | 文字数 | 3500 |
| `updated_at` | - | 更新日 | "2025-10-20" |

**将来拡張（variant.fit移行用）**:
```yaml
variant_fit:
  migrated: false
  migrated_at: null
  variant_url: null
seo:
  description: "記事の概要"
  og_image: "https://..."
analytics:
  views: 1500
  likes: 45
```

### 5.4 CORPUS.md 設計

**目的**: AI文体学習のインデックス

**構造**:
```markdown
# AI文体学習コーパス

最終更新: 2025-10-16  
総記事数: 15  
総文字数: 52,000

---

## 📚 記事一覧

### note記事

#### 2025年10月（5件）

##### [HSS型HSPとハルシネーション](writings/note/published/2025-10-16-hss-hsp-hallucination.md)
- **公開日**: 2025-10-16
- **URL**: https://note.com/nullvariant/n/xxxxx
- **文字数**: 3,500字
- **タグ**: #HSS型HSP #AI #ハルシネーション
- **概要**: AIが生成した架空のペルソナ名を分析...

---

## 🎨 文体の特徴

### 語彙・表現
- HSS型HSP視点: 刺激追求と高感受性の矛盾を自然に統合
- メタ認知的表現: 「〜と思っている自分を観察している」
- 6ペルソナ対話: 👮ジャスティス / 👧ルナ 等のアイコン使用

### 構造
- 導入→展開→メタ分析のサンドイッチ構造
- 技術説明と哲学的考察の交互配置
- 「余談だが〜」「ちなみに〜」の挿入句

### トーン
- 探索的: 断定よりも問いかけ
- 分析的: 心理学・哲学の用語使用
- 誠実: 自己の限界を認める謙虚さ

---

## 🤖 AIへの指示

### Copilotで文体模倣する場合

1. **語尾・リズム**: このコーパスの文章を参考に
2. **概念使用**: HSS型HSP・6ペルソナ等を正確に
3. **トーン維持**: 探索的・分析的・誠実な態度

### Claudeで補助する場合

プロンプト例:
> このコーパスの文体を参考に、〜について執筆を補助してください。
> 特に、メタ認知的な視点と心理学的な用語使用を重視してください。

---

## 📊 統計

- 平均文字数: 3,467字/記事
- 最頻出タグ: #HSS型HSP (10), #AI (8), #Self-Perfecting OS (6)
- 最長記事: 5,200字（2025-09-15-agent-dialogue.md）
```

**自動更新機能**:
- `publish_note.py` 実行時に記事情報追加
- 統計情報の再計算
- タグ・カテゴリの集計

---

## 6. 実装計画

### Phase 1: Private Repository準備（P0: 最優先）

**タスク:**
1. GitHubで `nullvariant-atelier` Private repo作成
2. ローカルにclone
3. 基本的なREADME・.gitignore作成
4. ディレクトリ構造構築（writings/note/drafts, published等）

**成果物:**
- Private repository
- 基本ディレクトリ構造
- README.md（目的・使い方）

**所要時間:** 30分

**受け入れ基準:**
- [ ] Private repoが作成され、ローカルclone可能
- [ ] writings/note/drafts, published ディレクトリが存在
- [ ] README.mdに明確な目的が記載される
- [ ] .gitignoreが適切

---

### Phase 2: スクリプト実装（P0: コア機能）

**タスク:**
1. `scripts/publish_note.py` 実装
   - Front Matter生成
   - drafts → published 移動
   - CORPUS.md更新
   - エラーハンドリング
2. `scripts/import_note_articles.py` 実装（既存記事用）
3. 動作テスト

**成果物:**
- 動作する publish_note.py
- 動作する import_note_articles.py
- 使用例ドキュメント

**所要時間:** 2-3時間

**受け入れ基準:**
- [ ] publish_note.pyが正常に動作
- [ ] Front Matterが正しく生成される
- [ ] CORPUS.mdが自動更新される
- [ ] エラーメッセージが分かりやすい
- [ ] --dry-runモードが動作

---

### Phase 3: AI文体学習コーパス構築（P0: 主目的）

**タスク:**
1. CORPUS.md作成
2. .copilot-instructions.md作成
3. 既存note記事のインポート（import_note_articles.py使用）
4. Copilot/Claudeでの動作確認

**成果物:**
- CORPUS.md（全記事インデックス）
- .copilot-instructions.md
- インポート済み既存記事

**所要時間:** 2時間

**受け入れ基準:**
- [ ] CORPUS.mdに全記事が記録される
- [ ] CopilotがPrivate repoを参照できる
- [ ] 文体特徴が明記される
- [ ] 既存記事が全てインポートされる

---

### Phase 4: Obsidian統合（P0: 必須）

**タスク:**
1. シンボリックリンク設定
2. ワークフロー検証
3. ドキュメント化

**成果物:**
- Obsidian ↔ GitHub 統合
- ワークフローガイド

**所要時間:** 30分

**受け入れ基準:**
- [ ] シンボリックリンクが動作
- [ ] Obsidianでの編集がGitに反映
- [ ] 設定手順がドキュメント化される

---

### Phase 5: ドキュメント整備（P1: 重要）

**タスク:**
1. 各ディレクトリのREADME作成
2. .template.md作成
3. `docs/WORKFLOW_TEXT_ASSETS.ja.md` 更新
4. トラブルシューティングガイド作成

**成果物:**
- 完全なドキュメントセット
- 使いやすいテンプレート

**所要時間:** 1.5時間

**受け入れ基準:**
- [ ] 全READMEが明確
- [ ] テンプレートが使いやすい
- [ ] トラブルシューティングが充実

---

### Phase 6: 検証とテスト（P1: 重要）

**タスク:**
1. 実際のnote記事で全フロー実行
2. エラーケースのテスト
3. Copilot文体学習の確認
4. ドキュメントの最終レビュー

**成果物:**
- 検証済みワークフロー
- テストレポート

**所要時間:** 1時間

**受け入れ基準:**
- [ ] 全フローが正常動作
- [ ] エラーハンドリングが適切
- [ ] Copilotが実際に文体を学習
- [ ] ドキュメントに不備なし

---

### Phase 7: variant.fit移行準備（P2: 将来対応）

**タスク:**
1. メタデータ拡張（variant_fit セクション）
2. canonical URL管理
3. 移行計画ドキュメント作成

**成果物:**
- 移行可能なメタデータ構造
- 移行計画PRD

**所要時間:** 1時間

**受け入れ基準:**
- [ ] メタデータがCMSフレンドリー
- [ ] 移行パスが明確
- [ ] 別PRDへの引き継ぎ可能

---

## 総所要時間見積もり

- **最小構成（Phase 1-4）**: 5-6時間
- **完全実装（Phase 1-6）**: 8-9時間
- **将来対応含む（Phase 1-7）**: 9-10時間

**推奨アプローチ**: 
- Day 1: Phase 1-2（リポジトリ準備・スクリプト実装）
- Day 2: Phase 3-4（コーパス構築・Obsidian統合）
- Day 3: Phase 5-6（ドキュメント・検証）

---

## 7. リスクと対策

### リスク1: Private Repoでも検索エンジンにインデックスされる可能性

**影響度:** 高  
**発生確率:** 極低

**理由**: 
- GitHub Private repositoryは検索エンジンから完全に隠蔽される
- ただし、誤ってPublicに変更すると即座にクロール対象

**対策:**
- [ ] GitHub repoの設定で「Private」を再確認
- [ ] 定期的なPrivate設定チェック
- [ ] `.github/workflows/` でPrivate強制（可能なら）
- [ ] チーム招待時の権限管理

---

### リスク2: Obsidian統合の複雑化

**影響度:** 中  
**発生確率:** 中

**理由**:
- シンボリックリンクの理解が必要
- Dropbox syncとの競合可能性

**対策:**
- [ ] シンボリックリンク設定を詳細にドキュメント化
- [ ] Dropbox除外設定の案内
- [ ] トラブルシューティングガイド
- [ ] 代替方法（手動コピースクリプト）の用意

---

### リスク3: CopilotがPrivate Repoを参照できない

**影響度:** 高  
**発生確率:** 低

**理由**:
- GitHub Copilotの仕様変更
- 権限設定の問題

**対策:**
- [ ] Phase 3で動作確認を必ず実施
- [ ] Copilot設定の確認（Private repo access有効化）
- [ ] 代替案: Public repoでrobotstxt使用（最終手段）

---

### リスク4: メタデータ形式の将来的な変更

**影響度:** 中  
**発生確率:** 高

**理由**:
- variant.fit移行時に必要な情報が増える
- プラットフォーム追加（Zenn等）で項目追加

**対策:**
- [ ] Front Matterを柔軟に設計
- [ ] 必須/オプションの明確な区別
- [ ] バリデーションスクリプトの作成
- [ ] マイグレーションスクリプトの準備

---

### リスク5: 既存記事インポートの手間

**影響度:** 中  
**発生確率:** 高

**理由**:
- 過去記事のメタデータが不完全
- 手動入力が必要

**対策:**
- [ ] `import_note_articles.py` で対話的入力補助
- [ ] バッチ処理用のJSON設定ファイル対応
- [ ] 段階的インポート（重要記事から優先）

---

### リスク6: スクリプトの保守コスト

**影響度:** 低  
**発生確率:** 中

**理由**:
- Python環境の違い
- 依存関係の更新

**対策:**
- [ ] Python標準ライブラリのみ使用（依存最小化）
- [ ] 型ヒント・docstringで保守性向上
- [ ] エラーメッセージの明確化
- [ ] 必要最小限の機能実装（MVP）

---

## 8. 代替案の検討

### 代替案A: Public Repository + robots.txt

**概要**: Public repoで公開しつつ、robots.txtで検索エンジンブロック

**メリット:**
- ✅ 外部共有が容易
- ✅ GitHub Pagesも使える

**デメリット:**
- ❌ robots.txtを無視するクローラーが存在
- ❌ 完全なSEO保護の保証なし
- ❌ リスクが残る

**判断:** ❌ 却下（SEO保護が最優先事項）

---

### 代替案B: 全てを手動で管理

**概要**: スクリプトなし、手動でコピー＆ペースト

**メリット:**
- ✅ 実装コストゼロ
- ✅ 柔軟性が最も高い

**デメリット:**
- ❌ ヒューマンエラー
- ❌ 時間がかかる
- ❌ AI文体学習コーパスが構築されない

**判断:** ❌ 却下（主目的のAI学習が達成できない）

---

### 代替案C: Zenn方式（Public repo + 公式連携）

**概要**: ZennのようにPublic repoで管理し、公式連携でSEO問題回避

**メリット:**
- ✅ Zennでは実証済み
- ✅ SEO競合なし

**デメリット:**
- ❌ noteには公式連携が存在しない
- ❌ 現時点で実装不可能

**判断:** 🔮 将来の可能性（noteが公式連携を提供したら再検討）

---

### 代替案D: Obsidian Publish（独自ドメイン）

**概要**: Obsidian Publishでvariant.fitを直接構築

**メリット:**
- ✅ 最も簡単にサイト公開
- ✅ Obsidian統合が完璧

**デメリット:**
- ❌ 月額課金（$8/月）
- ❌ カスタマイズ性が低い
- ❌ note等のプラットフォーム活用ができない

**判断:** 🔮 将来の選択肢（variant.fit構築時に再検討）

---

### 代替案E: CMSツール（Sanity/Strapi等）を先に構築

**概要**: variant.fitを先に構築し、そこからプラットフォーム配信

**メリット:**
- ✅ 理想的なアーキテクチャ
- ✅ 完全な資産管理

**デメリット:**
- ❌ 初期構築コストが膨大
- ❌ 日々の執筆が止まる
- ❌ プラットフォームの実利を逃す

**判断:** ❌ 却下（「完璧主義の罠」に陥る）

---

### 採用案: Private Repository + 段階的拡張

**理由:**
1. **SEO保護を確実に実現**（Private repoの絶対性）
2. **AI文体学習を即座に達成**（主目的）
3. **MVP思想**（最小限実装で使いながら改善）
4. **将来の拡張性**（variant.fit移行への橋渡し）
5. **リスク最小**（プラットフォームの実利も維持）

---

## 9. 成功の測定

### 主目的達成指標（P0）

#### AI文体学習
- ✅ **Copilot参照**: Private repoを正常に参照できる
- ✅ **文体再現**: Copilotが過去記事の文体で補助できる
- ✅ **CORPUS完成**: 全既存記事がインデックス化される

#### SEO保護
- ✅ **検索結果**: note記事の順位に影響なし
- ✅ **重複判定**: Google Search Consoleで重複検出なし
- ✅ **Private維持**: リポジトリがPrivateのまま

---

### 副次目的達成指標（P1）

#### 作業効率
- ✅ **公開フロー**: note公開後5分以内でGit管理完了
- ✅ **同期**: Obsidian執筆が即座にGit反映
- ✅ **誤操作**: ゼロ（構造的分離により）

#### バージョン管理
- ✅ **履歴**: 全記事のGit履歴が完全
- ✅ **メタデータ**: 100%の記事にFront Matter付与
- ✅ **整合性**: drafts/publishedの明確な分離

---

### 定性的指標

#### 使いやすさ（HSP特性重視）
- ✅ **ストレス軽減**: 「楽になった」と感じる
- ✅ **美学**: ディレクトリ構造が美しい
- ✅ **柔軟性**: 使いながら改善できる余地

#### 永続性（「遺書代わり」）
- ✅ **プラットフォーム非依存**: noteが終了しても資産保全
- ✅ **移行可能性**: variant.fit移行が容易
- ✅ **可読性**: 将来の自分・他者が理解できる

---

### 測定方法

#### 1週間後チェックリスト
- [ ] 実際にnote記事を1本公開してフロー確認
- [ ] Copilotで「過去記事の文体で〜」と指示して動作確認
- [ ] noteの検索順位に変化がないか確認

#### 1ヶ月後チェックリスト
- [ ] 5本以上の記事が管理されている
- [ ] Obsidian執筆が習慣化している
- [ ] ワークフローに不満がないか振り返り

#### 3ヶ月後チェックリスト
- [ ] 全既存記事がインポート完了
- [ ] CORPUS.mdが充実している
- [ ] variant.fit移行の具体的計画が見えている

---

## 10. 承認プロセス

### 10.1 レビュー項目

#### 技術的妥当性
- [ ] Private Repository戦略はSEO保護に有効か？
- [ ] AI文体学習の要件を満たしているか？
- [ ] スクリプト設計は保守可能か？
- [ ] Obsidian統合は現実的か？

#### 戦略的整合性
- [ ] variant.fit移行を見据えた設計か？
- [ ] プラットフォーム戦略と整合しているか？
- [ ] 「遺書代わり」の永続性を確保できるか？
- [ ] MVP思想（最小限→拡張）に沿っているか？

#### 実装可能性
- [ ] 実装計画は現実的なタイムラインか？
- [ ] リスク対策は十分か？
- [ ] ドキュメントは十分に詳細か？
- [ ] 既存ワークフローを破壊しないか？

---

### 10.2 ペルソナレビュー

#### 👮 ジャスティス（CP: 完璧主義・検証）
**レビュー観点**: 設計の論理性・完全性・リスク対策
- [ ] SEO保護戦略は完璧か？
- [ ] メタデータ設計に漏れはないか？
- [ ] エラーハンドリングは十分か？

#### 👧 ルナ（FC₁: 探索・好奇心）
**レビュー観点**: 使いやすさ・面白さ・学習機会
- [ ] AI文体学習が楽しみか？
- [ ] 新しい技術（Private repo戦略）に興味があるか？
- [ ] 使いながら改善する余地があるか？

#### 🦥 スロウ（A: 現実的判断・省エネ）
**レビュー観点**: めんどくささ削減・実用性
- [ ] 本当に楽になるのか？
- [ ] 過剰設計ではないか？
- [ ] 最小限の労力で目的達成できるか？

#### 🐗 ブレイズ（FC₂: 情熱・推進）
**レビュー観点**: 実装スピード・勢い
- [ ] すぐに実装開始できるか？
- [ ] Phase 1だけでも価値があるか？
- [ ] 完璧を待たずに進められるか？

#### 🕊️ シエル（NP: 受容・統合）
**レビュー観点**: 全体の調和・長期的視点
- [ ] variant.fit移行への橋渡しになるか？
- [ ] プラットフォーム間の調和は取れているか？
- [ ] 「遺書代わり」の思想と一致するか？

#### 🐰 ミミ（AC: 社会適応・外部説明）
**レビュー観点**: 第三者への説明しやすさ
- [ ] ドキュメントは十分に明確か？
- [ ] 技術的に標準的なアプローチか？
- [ ] 外部共有時に恥ずかしくないか？

---

### 10.3 承認条件

#### 必須条件（これがないと承認不可）
- ✅ SEO保護戦略の妥当性確認
- ✅ AI文体学習の実現可能性確認
- ✅ Obsidian統合の現実性確認
- ✅ MVP思想の徹底（完璧主義回避）

#### 推奨条件（あると望ましい）
- ⚠️ 全ペルソナからのポジティブ評価
- ⚠️ 実装タイムラインの現実性
- ⚠️ variant.fit移行パスの明確さ

---

## 11. 次のステップ

### 承認後の即座アクション

#### Day 1（承認直後）
1. **Private Repository作成**
2. 基本構造構築（writings/note/drafts, published）
3. README.md作成

#### Day 2-3
4. **スクリプト実装**（publish_note.py）
5. 動作テスト
6. ドキュメント作成

#### Day 4-5
7. **AI文体学習コーパス構築**
8. 既存記事インポート
9. Copilot動作確認

---

### PRDの継続的更新

#### 実装フェーズ
- 発見された課題・変更点を随時記録
- 「実装メモ」セクション追加

#### 完了後
- ステータスを「Implemented」へ更新
- 「振り返り」セクション追加（何がうまくいったか）
- 次期PRD（variant.fit移行）への引き継ぎ事項記録

---

## 12. 関連ドキュメント

### 更新対象
- [ ] `docs/WORKFLOW_TEXT_ASSETS.ja.md` - 全体ワークフロー
- [ ] `nullvariant/README.md` - Private repoへの言及
- [ ] `nullvariant-atelier/README.md` - 新規作成
- [ ] `.github/copilot-instructions.md` - Private repoの説明追加

### 将来作成予定
- 🔮 `PRD_VARIANT_FIT_MIGRATION.ja.md` - variant.fit移行PRD
- 🔮 `PRD_ZENN_INTEGRATION.ja.md` - Zenn統合PRD
- 🔮 `PRD_MULTIPLATFORM_STRATEGY.ja.md` - マルチプラットフォーム戦略PRD

---

## Appendix A: よくある質問（FAQ）

### Q1: なぜPrivate Repositoryなのか？
**A**: note記事と重複コンテンツ判定されないため。Private repoは検索エンジンにインデックスされないが、GitHub Copilotは参照できる。

### Q2: Copilotは本当にPrivate repoを読めるのか？
**A**: はい。GitHub CopilotはあなたがアクセスできるPrivate repositoryも参照します。Phase 3で動作確認を必ず実施します。

### Q3: noteのSEOは本当に保護されるのか？
**A**: はい。Private repoは検索エンジンから完全に隠蔽されるため、canonical URLがnoteのままです。

### Q4: Obsidian統合は複雑ではないか？
**A**: シンボリックリンクを使えば、ファイルシステムレベルで自動同期されます。設定は一度だけで、以降は意識不要です。

### Q5: variant.fit移行時はどうするのか？
**A**: メタデータ（Front Matter）にcanonical_urlフィールドがあり、段階的にvariant.fitへ変更できます。別PRDで詳細設計します。

### Q6: 既存note記事のインポートは大変では？
**A**: `import_note_articles.py` が対話的に補助します。重要記事から優先的にインポートし、段階的に進められます。

---

## Appendix B: 用語集

| 用語 | 説明 |
|-----|------|
| **Private Repository** | GitHubの非公開リポジトリ。検索エンジンにインデックスされない |
| **canonical URL** | SEOの「正規版URL」。重複コンテンツ対策 |
| **Front Matter** | Markdownファイル冒頭のYAML形式メタデータ |
| **CORPUS** | AIが学習するためのテキスト集合 |
| **HSS型HSP** | High Sensation Seeking HSP（刺激追求型の高感受性） |
| **variant.fit** | プロジェクトオーナーの独自ドメイン（将来のメインサイト） |
| **MVP** | Minimum Viable Product（最小限の実用製品） |

---

**最終更新**: 2025年10月16日  
**バージョン**: 2.0（全面改訂）  
**ステータス**: Draft → 承認待ち  
**次回更新**: 承認後、実装開始時
