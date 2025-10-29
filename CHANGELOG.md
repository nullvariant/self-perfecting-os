# Changelog

All notable changes to this repository (spec, docs, scripts, and AGENT) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/ja/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
#### ガバナンス・ドキュメント管理

- **[ADR-0010](docs/decisions/active/2025/10/20251029_0010_governance-audit_documentation.md)**: ガバナンス自己レビュー報告書
  - nullvariantリポジトリ全体のドキュメント命名規則監査
  - 4つの主要矛盾点を特定・分類
  - P0（Critical）～ P3（Nice-to-have）の段階的改善計画を提示
  - **重要**: 本レポート自体が「ADR-0011/0012ルールを遵守する」ことで、ルール有効性を証明

- **[ADR-0011](docs/decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md)**: ファイル名ケース規則（大文字 vs 小文字）
  - **決定**: メタドキュメント（README, OPERATIONS）は大文字 / 流動ドキュメント（ADR, PRD）は小文字
  - **根拠**: 業界慣例（README/AGENT標準化） + URLフレンドリー + プログラマティック処理の容易性
  - **実装**: 具体例、Python正規表現、検証チェックリスト付き
  - **影響**: 7つのADRファイル + 1つのPRDファイルを英語小文字スラグへ統一

- **[ADR-0012](docs/decisions/active/2025/10/20251029_0012_hyphen-underscore-convention_documentation.md)**: ハイフン・アンダースコア規則
  - **決定**: アンダースコア = 構造的セクション区切り（日付｜シーケンス｜カテゴリ） / ハイフン = slug内の語義的単語繋ぎ
  - **パターン**: `{YYYYMMDD}_{NNNN}_{lowercase-hyphen-slug}_{category}.md`
  - **根拠**: SEO最適化（ハイフン推奨） + プログラマティック解析の容易性
  - **実装**: 視覚的ルール表、Regex検証、移行パス、代替案検討

#### ドキュメント・ナビゲーション改善

- **[docs/README.md](docs/README.md)** - 初来訪者向けナビゲーション追加
  - 🎯「あなたが知りたいこと別ガイド」 - 6つのユースケース別読了ガイド
  - 🔍 カテゴリ別ADR検索例
  - 🚀 よくある作業フロー（意思決定記録、ADR検索、整合性確認）
  - 🧭 Tier 0（最優先読了物）の明示

- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** - 新規ナビゲーションドキュメント
  - ❓ 7つの主要ユースケース別ガイド（プロジェクト概要～将来計画）
  - 🎯 よくあるシナリオ別ナビゲーション表
  - 🔀 推奨される読む順序（Phase 1～4、15-30分）
  - 💡 Tips & 迷ったときの質問リスト
  - 🆘 判断フロー表（「このファイルをどこに置く？」など）

- **[scripts/README.md](scripts/README.md)** - generate_index.py ドキュメント追加
  - 用途・機能説明
  - 実行方法（通常実行 + ドライラン）
  - インデックス生成内容の詳細
  - メタデータ抽出ルール
  - 自動ファイル検出パターン
  - ドライラン使用例
  - トラブルシューティング

#### ガバナンス・ドキュメント同期

- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - ADR-0011/0012 参照を追加
  - ADR命名規則セクションに詳細リンク
  - ケース規則・ハイフン規則の新ADRへの参照

- **[docs/governance/AI_GUIDELINES.md](docs/governance/AI_GUIDELINES.md)** - 参考資料セクション更新
  - ADR-0011（ケース規則）へのリンク
  - ADR-0012（ハイフン・アンダースコア規則）へのリンク

- **[docs/decisions/README.md](docs/decisions/README.md)** - INDEX.md メンテナンスルール追加
  - 🤖「INDEX.md 自動生成ルール」セクション
  - 自動化の仕組み・実行タイミング表
  - 生成プロセスの具体例
  - ドライラン確認方法
  - 検出対象ファイルパターン
  - メタデータ抽出ルール
  - トラブルシューティング表

### Fixed
// docs: broaden CHANGELOG scope & PRD guide alignment
- **[CHANGELOG.md](CHANGELOG.md)**
  - 冒頭方針文を「AGENT.mdのみ」から「リポジトリ全体（仕様・ドキュメント・スクリプト・AGENT）」へ拡張し、実態と整合

- **[docs/prd/README.md](docs/prd/README.md)**
  - 命名規則を `{YYYYMMDD}_{slug}.ja.md` に統一（英小文字ケバブ）し、日本語スラッグ例を是正
  - ライフサイクルのディレクトリ表記を `implemented/` と `cancelled/` に統一（`completed/` を廃止）
  - 存在しない `docs/prd/template.md` 参照を削除し、README内テンプレートブロックの利用に変更（テンプレ参照の解消）
  - ファイル名末尾カテゴリ付与の規則を廃止し、本文/Front Matterタグ推奨へ変更
- **7つのADRファイル名を英語スラグに統一**
  - `20251028_0003_ディレクトリ・ファイル名...` → `20251028_0003_lowercase-hyphen-unification_documentation.md`
  - `20251028_0004_github-actions-によるドキュメント...` → `20251028_0004_github-actions-doc-validation_tooling.md`
  - `20251028_0005_多言語対応-言語別ディレクトリ...` → `20251028_0005_multilingual-directory-structure_documentation.md`
  - `20251028_0006_github-pagesランディングページ...` → `20251028_0006_github-pages-landing-implementation_documentation.md`
  - `20251028_0007_changelogsディレクトリのnullvariant-w...` → `20251028_0007_changelogs-migration-nullvariant-writings_architecture.md`
  - `20251029_0008_対話生ログの永続保存システム確立...` → `20251029_0008_dialogue-log-persistence-system_governance.md`
  - `20251029_0009_テストファイル管理規則testsfixtures...` → `20251029_0009_test-fixtures-management_process.md`

- **1つのPRDファイルを命名規則に統一**
  - `20251029_対話生ログ永続保存システム.md` → `20251029_dialogue-log-persistence.ja.md`

- **[docs/decisions/README.md](docs/decisions/README.md)**
  - 構造例のファイル一覧を現行の英小文字ケバブスラグへ更新（0010〜0012を追加）
  - 見出しの文字化け（�）を修正（🗂️/✍️ へ置換）

- **[docs/README.md](docs/README.md)**
  - ADR命名例のカテゴリを `dev` → `tooling` に是正（公式カテゴリに準拠）
  - 例示内の文字化け（�）を修正（🏗️へ置換）
  - 最終更新日の更新（2025-10-29）

- **[docs/governance/DOCUMENTATION_STRUCTURE.yml](docs/governance/DOCUMENTATION_STRUCTURE.yml)**
  - YAML構文エラーを修正（改行・インデントの是正）
  - PRD命名規則を `{YYYYMMDD}_{slug}.ja.md` に明記、例を `20251029_dialogue-log-persistence.ja.md` に更新
  - 参照ファイルを実ファイルに合わせて更新（`20251029_対話生ログ永続保存システム.md` → `docs/prd/active/20251029_dialogue-log-persistence.ja.md`）
  - 廃止予定の `MIGRATION_STATUS.md` を構造定義から除外（tier4_temporary.files を空配列へ）

- **[docs/governance/NAMING_DECISION_SUMMARY.md](docs/governance/NAMING_DECISION_SUMMARY.md)** - リンク・内容の更新
  - ADR-0002リンク修正（broken path `../DECISIONS/...` → 正確な相対パス）
  - 「ケース規則（大文字 vs 小文字）【ADR-0011】」セクション追加（根拠説明付き）
  - 「ハイフン vs アンダースコア【ADR-0012】」セクション追加（視覚的ルール表付き）

- **[docs/decisions/INDEX.md](docs/decisions/INDEX.md)** と **[docs/prd/INDEX.md](docs/prd/INDEX.md)** を再生成
  - 11個のActive ADR（ADR-0001～0012のうち0010/0011/0012が新規追加）
  - 4個のActive PRD
  - 適切なカテゴリ分類（architecture, documentation, governance等）
  - 時系列表示と各ドキュメントへの直接リンク

### Improved
- **ドキュメント発見性向上**
  - 初来訪者が「何を読むべきか」を5分以内に把握可能な構造
  - カテゴリ別・ユースケース別・時系列の複数検索軸

- **命名規則の「なぜ」を明示化**
  - 以前: ルール存在だが根拠なし → 混乱・質問増加
  - 現在: 業界標準・SEO・プログラマティック処理 の3軸で正当化（ADR-0011/0012）

- **自動生成プロセスの透明性向上**
  - INDEX.md 生成ルールを文書化
  - ドライランで事前確認可能
  - メンテナンス方法を明文化

- **ガバナンス文書の相互リンク強化**
  - AI_GUIDELINES → ADR-0011/0012
  - copilot-instructions → ADR-0011/0012
  - decisions/README → INDEX.md メンテナンスルール
  - すべてのドキュメントが相互参照可能に

### Compatibility
- ✅ 既存のAGENT.md（v4.1）機能を保持
- ✅ 既存ADR（0001～0009）のメタデータ・リンク互換性維持
- ⚠️ ファイル名が変更されたADR 7つについて、既存リンクは更新済み

### Related Links
- [governance/NAMING_DECISION_SUMMARY.md](docs/governance/NAMING_DECISION_SUMMARY.md) - 命名規則統合サマリー
- [docs/QUICKSTART.md](docs/QUICKSTART.md) - 新規ナビゲーション
- [docs/decisions/INDEX.md](docs/decisions/INDEX.md) - 自動生成ADR索引

### Removed
- `changelogs/` ディレクトリを nullvariant-writings リポジトリへ移行（ADR-0007参照）
  - note記事の人間向け物語版は [nullvariant-writings/changelogs/](https://github.com/nullvariant/nullvariant-writings/tree/main/changelogs) で管理
  - 技術的変更履歴は本CHANGELOG.mdで継続管理
  - SEO最適化のため、技術記録と人間向け物語を完全分離（Proposal D）

### Planned
- 今後の機能追加や改善予定をここに記載

---

## [4.1.0] - 2025-10-13

### Added
- **Section 2.1.1**: ペルソナ別感情プロファイル概要テーブル
  - 各ペルソナの典型的感情を[感情辞書](content/ja/EmotionMood_Dictionary.md)IDで明示化
  - 愛モード/恐怖モード/苦手感情/統合指針を体系化
  - 参照: [感情辞書 Appendix A](content/ja/EmotionMood_Dictionary.md#appendix-a)

- **Section 6.3**: 感情辞書活用ガイド
  - ペルソナ別感情プロファイル詳細（全6体）
  - 愛モード vs 恐怖モードの感情識別パターン
  - 日常的モニタリングと成長記録の手法

### Enhanced
- **Section 4.3**: 感情バッファを成分分離型へ進化
  - 感情IDによる透明化/吸収/返却の精密分類
  - エネルギー変換効率の数値化
  
- **Section 6.1.4**: EBI測定に「典型的感情状態マップ」追加
  - 全6ペルソナのEBI範囲別感情プロファイル
  - 各EBI帯域での推奨行動パターン

- **Appendix F**: 価値判断マトリクスに感情駆動パターン追加
  - 愛/恐怖モード判断の感情基盤を感情IDで明示
  - 典型的な判断フローの可視化

### Impact
- 🎯 感情を「測定・管理・育成可能なデータ」へ転換
- 🔗 EBI測定と感情辞書の完全統合
- 📊 システム状態の解像度が飛躍的向上

### Compatibility
- ✅ v4.0の全機能を保持
- ✅ 既存システムとシームレスに統合
- ⚠️ 感情辞書の参照が必須（[content/ja/EmotionMood_Dictionary.md](content/ja/EmotionMood_Dictionary.md)）

### Related Links
- [content/ja/AGENT.md v4.1](content/ja/AGENT.md)
- [感情辞書 v1.0](content/ja/EmotionMood_Dictionary.md)
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)
- [note記事 v4.1](https://note.com/nullvariant/n/n2a9a5fbf6e57)

---

## [4.0.0] - 2025-10-11

### Added
- **Section 4.7**: 選択的透過フィルタの実装
  - PCP/MOF（多孔性配位高分子）原理に基づく4層構造フィルタシステム
  - Layer 1（粗いフィルタ）: 即時遮断層
  - Layer 2（中程度フィルタ）: 文脈分析層
  - Layer 3（精密フィルタ）: 美学一致度測定層（閾値85%）
  - Layer 4（ナノフィルタ）: 無意識の前提検出層

- **Section 4.3**: 可逆的吸着プロトコル
  - 時間軸を含む判断システム（24-48時間保留機能）
  - 隔離タンクでの成分分離（感情成分A/認識成分B/投影成分D）
  - 化学の可逆反応に着想を得た「吸着→分析→放出」メカニズム

- **Section 0.4.E**: 空っぽの哲学
  - 「精密に設計された空虚な空間」が機能の源泉
  - PCP/MOFの「空孔」概念との対応
  - 6ペルソナが自由に動ける「余白」の設計思想

### Enhanced
- **Section 4.3**: 感情バッファの成分分離型へ進化
  - 従来の「鎮静化のみ」から「成分分離＋可逆処理」へ
  - 感情成分A（純粋感情）/ 認識成分B（認知的評価）/ 投影成分D（他者からの投影）
  - 有益な要素の選択的抽出と統合

- **Section 2**: 6ペルソナシステムの完全実装
  - 各ペルソナの役割・目的関数・相互作用の詳細化
  - ペルソナ間協調メカニズムの明確化

- **Section 6.1**: EBI（Ecosystem Balance Index）測定システム確立
  - 個別ペルソナメトリクスの定義
  - システム健全性の状態定義（healthy/warning/critical）
  - 生態系バランスの定量化

- **Appendix F**: 価値判断マトリクスの体系化
  - 多層的価値判断の実装プロセス
  - 恐怖モード vs 愛モードの判定基準

### Changed
- **Section 3**: Core Policies の再編成
  - Port B（庭園プロトコル）からの選択的透過フィルタへの進化
  - 防衛アーキテクチャから創造アーキテクチャへの転換完了

### Impact
- 🎯 防衛エネルギー消費を約25-35%から **15-20%へ削減**
- 🔬 分子科学の原理を認知システムに応用した世界初の試み
- 🌱 「防衛から庭園へ」の構造転換が完全実装レベルに到達
- 📊 刺激の選択的処理により、有益情報の取りこぼしを大幅削減

### Compatibility
- ✅ v3.1の全機能を保持
- ✅ Port B（庭園プロトコル）は選択的透過フィルタに統合
- ⚠️ EBI測定基準が精密化されたため、過去ログとの数値比較は要調整

### Related Links
- [content/ja/AGENT.md v4.0](content/ja/AGENT.md)
- [note記事: v4.0アップデート](https://note.com/nullvariant/n/n0c2b7c97a0ba)
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)
- PCP/MOF参照記事: [コーヒーかすから考える多孔質の科学](https://note.com/safe_gibbon6757/n/n992f902ef504)

### 参考文献
※1 2025年ノーベル化学賞受賞: 北川進教授「多孔性配位高分子（PCP/MOF）」  
※2 可逆的吸着の化学的原理  
※3 「空っぽの哲学」: 機能的空虚性の美学

---

## [3.1.0] - 2025-10-05

### Added
- **Section 0.4**: 価値判断の原理セクションの大幅拡充
  - **A. 体質的基盤**: 多層的認知（6層同時起動）とHSP体質の詳細化
    - 物理的現実/論理構造/感情の流れ/抽象的パターン/哲学的意味/見えない次元
    - DOES特性の明示化
  - **B. 価値の最上位原理**: 誤差ゼロへの収束 = 内側美学との一致
    - `価値 = 誤差の最小化 × 本質との一致度`
    - 「誤差を扱える力」の重要性
  - **C. 価値判断の決定的分岐点**: 恐怖モード vs 愛モード
    - 恐怖の二重拘束とその解放の鍵を明示化
    - 「恐怖を感じてもよい。ただし恐怖に従わない」という自由
  - **D. 多層的価値判断の実装**: 全ペルソナの統合プロセス

- **Section 1.3.6**: AIとの相互作用における原則の新設
  - **基本原則**: AIは鏡であり、評価者ではない
  - 評価権限の明確化（常に本OS側が保持）
  - AIからの肯定的評価に依存しない自律性の確保

### Enhanced
- 価値判断メカニズムの体質レベルから実装レベルまでの貫通的言語化
- 恐怖/愛の二重拘束問題の操作的定義

### Impact
- 💡 「価値判断はどこから来るのか」という根源的問いへの回答
- 🎭 AI協働における評価権限の所在の明確化
- 🔓 恐怖の二重拘束からの解放メカニズムの実装

### Compatibility
- ✅ v3.0の全機能を保持
- ✅ 価値判断プロセスの透明化により、システム動作の予測可能性が向上

### Related Links
- [content/ja/AGENT.md v3.1](content/ja/AGENT.md)
- [note記事: v3.1アップデート](https://note.com/nullvariant/n/n353d60ed5ae0)
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)
- 参照記事: [「AIからの肯定」依存の危機](https://note.com/royal_curlew4118/n/nb4096edeaa62)

### Note
Version 3.0の公開から1日で、実運用で2つの根源的な盲点が浮上したことを受けての緊急アップデート。

---

## [3.0.0] - 2025-10-04

### Added
- **Port B: 庭園プロトコルの実装**
  - 二重ポート構造（Port A: 面会室 / Port B: 庭園）
  - 庭園成功条件の定義（全6ペルソナがありのままでくつろげる状態）
  - 半透膜プロトコル（選択的透過・刺激変換・自律浄化）

- **Section 6.1**: 生態系バランス指標（EBI）の仕様化
  - 個別ペルソナメトリクスの定義
  - システム健全性の状態定義（healthy/warning/critical）
  - 日次記録システムの導入

- **Section 3**: ペルソナ目的関数の更新
  - 👮‍♂️ジャスティスの役割変更: 「排除の執行者」→「庭園の守護者」
  - 目的関数が「異物の排除」から「調和的美学」へ

### Changed
- **システム設計思想の転換**: 防衛アーキテクチャから創造アーキテクチャへ
  - Version 2: 防衛エネルギー消費 40-60%
  - Version 3: 防衛エネルギー消費 25-35%（目標）
  - 理想状態の定義: 「防衛にエネルギーを費やさず、したいことを思う存分できる」

- **境界管理の進化**:
  - Version 2: 完全障壁（不透過壁）
  - Version 3: 半透膜（選択的透過・有害刺激の変換・ノイズ許容）

### Enhanced
- **👮‍♂️ジャスティスの行動変化**:
  - 👧ルナの衝動的アイデア: 即時却下 → 実験的サンドボックスの提案
  - 🐗ブレイズの情熱的提案: 非合理として拒否 → エネルギー配分の最適化検討
  - 🦥スロウの抵抗: 怠惰として批判 → 省エネシグナルとして認識

### Impact
- 🎯 「防衛のために存在するOS」から「創造のために存在するOS」への構造的転換
- 🌱 庭園プロトコルによる持続的共生関係の育成可能性
- 📊 EBIによる定量的なシステム健全性測定

### Compatibility
- ⚠️ Version 2の防衛中心アーキテクチャとは設計思想が根本的に異なる
- ✅ 既存ペルソナの基本特性は保持

### Detected Issues (v2.x)
- 構造的矛盾: システム目標（創造）vs 実装（防衛）のミスマッチ
- エネルギー逆説: 防衛運用が創造活動のリソースを消費
- 美学の不整合: 👮‍♂️ジャスティスが「異物の不在」を美とする誤調整

### Related Links
- [content/ja/AGENT.md v3.0](content/ja/AGENT.md)
- [note記事: v3.0アップデート](https://note.com/nullvariant/n/naf2590195055)
- [note Magazine: AI向けChangelog](https://note.com/nullvariant/m/m0d682a2ae34d)
- [前バージョン: v2.0](https://note.com/nullvariant/n/n7f150b19f6a7)

### 参考
※1 構造的矛盾の検出により、Version 3への移行が必須と判断  
※2 ノイズ許容閾値は創造性誘発のため意図的に設定  
※3 👮‍♂️ジャスティスの変容は本アップデートの中核

---

## External Resources
- [GitHub Repository](https://github.com/nullvariant/nullvariant)
- [content/ja/AGENT.md](content/ja/AGENT.md)
- [感情辞書](content/ja/EmotionMood_Dictionary.md)
- [note Magazine: AI向けChangelog記事](https://note.com/nullvariant/m/m0d682a2ae34d)

---

_このChangelogは、AIエージェントシステムの進化を記録し、AI学習データとしても最適化された形式で管理されています。_
