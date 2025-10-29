# GitHub Copilot Instructions for Self-Perfecting OS

このリポジトリは **Self-Perfecting OS (Null;Variant)** の仕様書およびドキュメント管理プロジェクトです。

## プロジェクト概要

- **目的**: 6ペルソナ協調型OS仕様書の管理と公開
- **主要言語**: 日本語（一次情報）、英語（自動翻訳）
- **技術スタック**: Python, Markdown, YAML, JSON
- **ドキュメント駆動**: 主にMarkdownファイルで構成されています

## 重要な原則

### 0. ドキュメント記録ルール（最優先）

**🏆 全ての重要な決定は ADR (Architecture Decision Records) に記録**

詳細は [docs/governance/AI_GUIDELINES.md](../docs/governance/AI_GUIDELINES.md) を参照してください。

#### クイックチェック

コード変更を提案する前に、以下を確認：

1. **[ ] この変更は ADR が必要か？**
   - API変更、アーキテクチャ変更、CI/CD変更 → **Yes**
   - タイポ修正、軽微なバグ修正 → **No**

2. **[ ] 既存の ADR/ドキュメントと矛盾しないか？**
   - `docs/decisions/` を確認
   - 矛盾する場合は新ADRで上書き

3. **[ ] 記録場所は適切か？**
   - 重要な決定 → `docs/decisions/ADR-*.md`
   - 一時的な状態 → `docs/project-status.ja.md`
   - バージョンリリース → `CHANGELOG.md`

#### ADR作成方法

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "GitHub Copilot"  # or "Claude Code", "human"
```

### 1. 編集対象ファイルの優先順位

**✅ 積極的に編集すべきファイル:**
- `docs/decisions/` - **ADR（全ての重要な決定を記録）**
- `content/ja/AGENT.md` - **日本語一次仕様書（最重要）**
- `content/ja/EmotionMood_Dictionary.md` - 感情辞書
- `CHANGELOG.md` - バージョン履歴（Keep a Changelog形式・技術的差分）
- `docs/` - ドキュメント類（階層ルールに従う）

**📝 note記事関連:**
- [nullvariant-writings/changelogs/](https://github.com/nullvariant/nullvariant-writings/tree/main/changelogs) - note記事原稿管理（ADR-0007により移行）
- `scripts/prepare_note_article.py` - note記事生成スクリプト（このリポジトリに残存、出力先は nullvariant-writings）

**❌ 直接編集禁止:**
- `AGENT.md` - CI自動生成（現在未稼働、手動更新も避ける）
- `spec/agent.spec.yaml` - CI自動生成（現在未稼働）
- `docs/decisions/0000-adr-template.md` - テンプレート（コピーして使用）

### 2. 言語・翻訳ポリシー

- **一次情報**: 日本語（`content/ja/AGENT.md`）
- **英語版**: 自動翻訳を想定（現在CI未稼働、`content/en/AGENT.md`）
- コード提案時は日本語コメントを推奨（プロジェクトオーナーの母語）
- ドキュメント執筆時は日本語優先、必要に応じて英語併記

### 3. コミットメッセージとChangelog

- 全ての変更は `CHANGELOG.md` の `[Unreleased]` セクションに記録
- Keep a Changelog形式に従う
- バージョニングはセマンティックバージョニング（SemVer）

### 4. プロジェクト構造の理解

```
nullvariant/
├── docs/
│   ├── decisions/                    # 🏆 ADR（全ての重要な決定）
│   ├── governance/                   # 🏛️ ドキュメント管理ルール
│   │   ├── AI_GUIDELINES.md
│   │   ├── DOCUMENTATION_STRUCTURE.yml
│   │   └── HIERARCHY_RULES.md
│   ├── operations/                   # 📋 運用手順書
│   │   ├── DOCUMENTATION_UPDATE_CHECKLIST.md  # 構造変更時のチェックリスト
│   │   └── current/                  # 現行版手順書
│   ├── prd/                          # 💡 要件定義
│   └── project-status.ja.md          # プロジェクト状況
├── content/                           # ✅ 一次情報
│   ├── ja/                           # 🇯🇵 日本語（編集対象）
│   └── en/                           # 🇬🇧 英語（CI自動生成）
├── AGENT.md                          # ⚠️ 自動生成（編集禁止）
├── CHANGELOG.md                      # ✅ バージョン履歴（技術的差分）
├── scripts/                          # Python自動化スクリプト
│   ├── check_path_references.py      # パス参照チェック・自動修正
│   ├── validate_docs.py              # ドキュメント整合性検証
│   ├── record_decision.py            # ADR作成支援
│   ├── archive_conversation.py       # 対話ログ保存（nullvariant-writings）
│   ├── check_token_usage.py          # トークン使用量監視
│   └── prepare_note_article.py       # note記事生成（出力先: nullvariant-writings）
├── tests/                            # 🧪 テストファイル管理（ADR-0009）
│   ├── README.md                     # テストファイル配置ガイド
│   └── fixtures/
│       ├── permanent/                # Git管理（単体テスト用・回帰テスト用）
│       └── temporary/                # .gitignore（一時的な動作確認用）
├── spec/                             # ⚠️ 自動生成（編集禁止）
└── i18n/                             # 翻訳用語集・スタイルガイド
```

詳細は以下を参照：
- `docs/governance/DOCUMENTATION_STRUCTURE.yml` - 機械可読形式の階層定義
- `docs/governance/HIERARCHY_RULES.md` - 人間向け階層ルール説明
- `docs/governance/AI_GUIDELINES.md` - AI向けドキュメント記録ガイドライン
- `docs/project-status.ja.md` - プロジェクト状況
- `tests/README.md` - テストファイル配置ガイド（ADR-0009）

### 5. テストファイル配置ルール（ADR-0009）

**基本原則**: すべてのテストファイルは `tests/fixtures/` 配下に集約

#### 配置先の判断

| 配置先 | 用途 | Git管理 | 例 |
|--------|------|---------|-----|
| `tests/fixtures/permanent/` | 単体テスト、回帰テスト、継続的に使用 | ✅ する | `sample_agent.md`, `expected_output.yaml` |
| `tests/fixtures/temporary/` | 一時的な動作確認、デバッグ | ❌ しない | `test_conversation.txt`, `debug_output.json` |

#### 判断基準（6つの質問）

1. **再現性**: 他の開発者が同じテストを実行できるべきか？ → Yes: permanent
2. **バージョン管理**: 将来のコード変更でこのデータが必要か？ → Yes: permanent
3. **一時性**: このファイルは今回限りの確認用か？ → Yes: temporary
4. **共有**: 他の開発者やCIでも使用するか？ → Yes: permanent
5. **削除**: テスト完了後に削除してよいか？ → Yes: temporary
6. **回帰**: 将来のバグ検出に役立つか？ → Yes: permanent

詳細: `tests/README.md`

## コーディング規約

### Python

- **スタイル**: PEP 8準拠
- **docstring**: Google Style推奨
- **型ヒント**: 可能な限り使用
- **エラーハンドリング**: 適切な例外処理を含める
- **スクリプト用途**: ビルド自動化、翻訳処理、目次生成

### Markdown

- **見出し**: ATX形式（`#`）を使用
- **リンク**: 相対パスで記述
- **コードブロック**: 言語指定を必ず含める
- **目次**: `scripts/gen_toc.py`で自動生成可能
- **数式**: KaTeX記法（`$...$`または`$$...$$`）

### YAML/JSON

- **インデント**: YAML=2スペース、JSON=2スペース
- **構造化**: `spec/agent.schema.json`のスキーマに準拠

## 開発フロー

### ローカル開発セットアップ

```bash
# 仮想環境構築
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 依存関係インストール
pip install -r requirements.txt

# OpenAI API キー設定（翻訳機能用）
export ANTHROPIC_API_KEY=sk-...
```

### 典型的な編集フロー

1. `content/ja/AGENT.md` を編集
2. 必要に応じて `scripts/gen_toc.py content/ja/AGENT.md` で目次再生成
3. `CHANGELOG.md` の `[Unreleased]` に変更を記録
4. （将来）CI/CDが自動的に英語版・YAML版を生成

**注意**: 現在CI/CDパイプラインは未稼働です。

## AI特有の注意事項

### プロジェクトオーナーの背景

- **経歴**: 心理学系大学を3年終了時点で中退
- **理由**: 「現実世界に出たほうが人間心理を学べる」という判断
- **アプローチ**: 自己を「生きた実験対象」として、心理学理論を実践的に応用

このペルソナシステムは：
- 交流分析・ゲシュタルト療法の理論的基盤
- 実際の自己観察による実践的カスタマイズ
- 理論と実践の統合

として構築されている。特に「FCを2体に分割」は、
教科書的な心理学では得られない実践的洞察である。

### 6ペルソナシステムの理解

このプロジェクトは「脳内珍獣動物園」コンセプトに基づいています:
- 👮 ジャスティス（孤高のユニコーン・完璧主義・秩序と検証・庭園の守護者）
- 👧 ルナ（蝶の群れ・好奇心旺盛・探索と生成）
- 🦥 スロウ（動かないナマケモノ・省エネ主義・リセットと無為）
- 🐗 ブレイズ（突進するイノシシ・情熱的・推進と衝動）
- 🕊️ シエル（森の古木・博愛・受容と安定）
- 🐰 ミミ（巣穴のウサギ・社会適応担当・外面調整）

コード提案時は、これらのペルソナ概念を尊重してください。

### 哲学的基盤

- **Nullvariant思想**: 選択的努力最大化（Selective Effort Maximizer）
- **内側美学最重視**: 自己理解とマスターが第一原則
- **EBI指標**: Ecosystem Balance Index（生態系バランス指標）

### HSS型HSP体質の理解

**重要**: プロジェクトオーナーは単なるHSPではなく、**HSS型HSP（High Sensation Seeking HSP）**です。

#### HSS型HSPの特性
- **刺激追求性（HSS）**と**高感受性（HSP）**の共存
- 新しい経験・冒険・探索への強い欲求
- 同時に、過剰刺激への脆弱性と緻密な誤差検知能力
- **退屈を嫌う**/**変化を求める** ← 防衛的引きこもり型ではない
- 「アクセルとブレーキを同時に踏む」矛盾した体質

#### ペルソナ構成への影響
- 👧ルナ / 🐗ブレイズ = **HSSのアクセル**（刺激追求・探索欲）
- 👮ジャスティス / 🦥スロウ = **HSPのブレーキ**（緻密性・疲弊対策）
- 🕊️シエル = この矛盾を統合する超越層

#### 誤解しやすいポイント
- ❌ 「HSP = 防衛的・慎重」というステレオタイプ
- ✅ 実際は**攻撃的・探索的・刺激追求型** + 緻密完遂傾向
- 「保護的観察」= 刺激遮断ではなく、**刺激を安全に取り込む技術**
- 「庭園」= 避難所ではなく、**実験と回復が両立する空間**

#### コード提案時の注意
- 「安全優先」「防衛的」な提案は適合しない可能性が高い
- 「探索的」「実験的」「刺激的」な提案を推奨
- ただし「緻密さ」「美学」「誤差最小化」は常に重視
- 刺激が**少なすぎても多すぎても**疲弊することに注意

### 心理学的背景

このペルソナシステムは以下の心理学理論から影響を受けています：

- **交流分析（TA）**: CP/NP/A/FC/ACの5要素モデル
- **ゲシュタルト療法**: エンプティチェア技法
- **独自アレンジ**: HSS型HSP特有の要請により、FC（自由な子ども）を2体に分割

#### 交流分析との対応

| TA要素 | ペルソナ | 備考 |
|-------|---------|------|
| CP（批判的な親） | 👮ジャスティス | 完璧主義・規律 |
| NP（養育的な親） | 🕊️シエル | 受容・安定 |
| A（大人） | 🦥スロウ | 現実的判断・省エネ |
| FC（自由な子ども） | 👧ルナ + 🐗ブレイズ | **2体に分割**（重要） |
| AC（順応した子ども） | 🐰ミミ | 社会適応 |

#### FCを2体に分割した理由

HSS型HSPの特性により、「自由な子ども」が2つの矛盾した形で現れます：

- 👧**ルナ**: 知的好奇心・探索・緻密な観察（HSS+HSP）
- 🐗**ブレイズ**: 情熱・衝動・推進力（HSS純粋型）

この分離により、「刺激追求」と「緻密性」の両立が可能になります。

#### エンプティチェア技法

6ペルソナ間の対話は、ゲシュタルト療法の「エンプティチェア」を常時稼働させたものと解釈できます。
[`content/ja/AGENT.md`](../content/ja/AGENT.md)の「6.2 事例集」は、この内的対話のログです。

#### AI向けの注意

- 標準的な心理学モデル（5要素・8要素など）に当てはめようとしないこと
- 特に「FCの2体分割」は、HSS型HSP特有の構造的必然性
- 交流分析ベースだが、独自のカスタマイズが施されている
- エンプティチェア的な対話形式を尊重すること

### 用語の一貫性

- 専門用語は `i18n/glossary.yml` を参照
- 日英スタイルガイドは `i18n/style/` を参照
- 感情関連用語は `content/ja/EmotionMood_Dictionary.md` を参照

## スクリプトの使用

```bash
# 目次自動生成
python scripts/gen_toc.py content/ja/AGENT.md

# note記事準備（プレビュー・コピー）
python scripts/prepare_note_article.py

# レビュー実行（LLMによる品質チェック）
python scripts/review.py

# ビルド実行（翻訳・YAML生成）
python scripts/build.py  # 現在未稼働

# ドキュメント整合性チェック
python scripts/validate_docs.py
```

## テスト

```bash
# 目次生成テスト
python scripts/test_toc.py
```

## コントリビューション

詳細は `CONTRIBUTING.md` を参照してください。

## 関連リンク

- **note**: https://note.com/nullvariant
- **GitHub**: https://github.com/nullvariant/nullvariant
- **Changelog Magazine**: https://note.com/nullvariant/m/m0d682a2ae34d

## コード提案時のベストプラクティス

1. **日本語コメント**: コードには日本語コメントを含める
2. **文脈理解**: 6ペルソナシステムの概念を尊重
3. **ドキュメント優先**: コードよりもMarkdown編集が多い
4. **自動化重視**: 繰り返しタスクはスクリプト化を提案
5. **品質維持**: HSP特性に配慮した緻密な実装を推奨
6. **Changelog更新**: 変更時は必ず `CHANGELOG.md` への記載を促す

## その他の注意事項

- このプロジェクトは **個人プロジェクト** です
- **美学と哲学** が設計の中心にあります
- **完璧主義傾向** があるため、段階的な改善を推奨します
- **自己実験ログ** としての側面も持つため、非標準的なアプローチも許容されます

---

**最終更新**: 2025年10月14日  
**バージョン**: 1.0.0
