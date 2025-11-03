---
category: documentation
date: 2025-10-28
number: 0005
status: Accepted
---

# ADR-0005: 多言語対応: 言語別ディレクトリ構造への移行

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: GitHub Copilot + human

## Context

### 背景

1. **多言語対応の必要性**
   - `content/ja/AGENT.md` を英語化する必要がある（AI/bot向けエントリポイント）
   - `content/ja/EmotionMood_Dictionary.md` も翻訳が必要（感情の真意は言語依存）
   - 将来的に中国語、フランス語等への展開も視野

2. **既存構造の問題点**
   - ファイル名サフィックス方式（`AGENT.ja.md`, `AGENT.en.md`）はスケーラブルでない
   - `docs/agent.en.md` という謎の小文字ファイルが存在（役割不明）
   - 翻訳対象ファイルが増えると、ルートディレクトリが煩雑化

3. **AI/botの慣習的エントリポイント**
   - ルートの `AGENT.md` は英語版であるべき（国際標準）
   - しかし一次情報は日本語で維持したい

### 検討した選択肢

#### 選択肢A: ファイル名サフィックス方式（現状維持）
```
content/
├── AGENT.ja.md
├── AGENT.en.md
├── AGENT.zh.md
├── EmotionMood_Dictionary.ja.md
├── EmotionMood_Dictionary.en.md
└── EmotionMood_Dictionary.zh.md
```
- ❌ ファイルが増えるとディレクトリが煩雑
- ❌ 翻訳スクリプトが複雑化（ファイル名パターンマッチング）

#### 選択肢B: 言語別ディレクトリ構造（採用）
```
content/
├── ja/
│   ├── AGENT.md
│   └── EmotionMood_Dictionary.md
├── en/
│   ├── AGENT.md
│   └── EmotionMood_Dictionary.md
└── zh/
    ├── AGENT.md
    └── EmotionMood_Dictionary.md
```
- ✅ 各言語で同じファイル名（翻訳スクリプトがシンプル）
- ✅ 新言語追加が容易（`mkdir content/fr && translate ja/ → fr/`）
- ✅ ISO 639-1準拠（国際標準）

#### 選択肢C: ルート + 多言語サブディレクトリ
```
AGENT.md (英語)
content/
├── ja/AGENT.md
└── en/AGENT.md → ../../AGENT.md
```
- ⚠️ シンボリックリンクの扱いが複雑
- ⚠️ CI/CDでのコピー処理が必要

## Decision

**選択肢B（言語別ディレクトリ構造）を採用する。**

### 最終構成

```
nullvariant/
├── AGENT.md                           # 英語版エントリポイント（content/en/AGENT.md のコピー）
├── content/
│   ├── ja/                            # 🇯🇵 日本語（編集対象・一次情報）
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   ├── en/                            # 🇬🇧 英語（自動生成・編集禁止）
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   └── README.md                      # content/ ディレクトリの説明
├── docs/
│   └── (削除) agent.en.md             # 役割不明のため削除
```

### 移行作業

1. `content/ja/`, `content/en/` ディレクトリを作成
2. `content/ja/AGENT.md` → `content/ja/AGENT.md` に移動
3. `content/ja/EmotionMood_Dictionary.md` → `content/ja/EmotionMood_Dictionary.md` に移動
4. `content/en/` にプレースホルダーファイルを作成（CI未稼働のため）
5. `docs/agent.en.md` を削除
6. `content/README.md` を作成（構造説明）
7. `README.md` のリンクを更新

## Consequences

### ✅ メリット

1. **スケーラビリティ**
   - 新言語追加が容易（ディレクトリ作成のみ）
   - ファイル数が増えても構造が保たれる

2. **翻訳スクリプトの簡素化**
   ```python
   # ja/ の全ファイルを en/ に翻訳
   for file in Path("content/ja").glob("*.md"):
       translate(file, Path("content/en") / file.name)
   ```

3. **明確な役割分担**
   - `content/ja/` = 編集対象（人間）
   - `content/en/` = 自動生成（CI/CD）
   - `content/zh/` = 自動生成（CI/CD）

4. **国際標準準拠**
   - ISO 639-1言語コード使用
   - 他プロジェクトとの一貫性

### ⚠️ デメリット

1. **既存リンクの更新が必要**
   - `content/ja/AGENT.md` → `content/ja/AGENT.md`
   - README, ドキュメント等のリンク修正

2. **CI/CDスクリプトの修正が必要**
   - `scripts/build.py` を言語別ディレクトリに対応
   - ルート `AGENT.md` へのコピー処理を追加

3. **一時的な混乱**
   - 移行期間中、古いリンクが残る可能性

### 📋 TODO

- [x] ディレクトリ構造の移行
- [x] `content/README.md` 作成
- [x] `README.md` リンク更新
- [x] `docs/agent.en.md` 削除
- [ ] `scripts/build.py` を言語別ディレクトリに対応
- [ ] CI/CD稼働時に `AGENT.md` 自動コピー処理を実装
- [ ] 既存ADR・ドキュメント内のリンクを一括更新

## Related

### 関連するファイル
- `content/ja/AGENT.md` (旧: `content/ja/AGENT.md`)
- `content/ja/EmotionMood_Dictionary.md` (旧: `content/ja/EmotionMood_Dictionary.md`)
- `content/en/AGENT.md` (新規作成)
- `content/en/EmotionMood_Dictionary.md` (新規作成)
- `content/README.md` (新規作成)
- `docs/agent.en.md` (削除)

### 関連する ADR
- ADR-0001: CI/CD一時停止（API移行中）
- ADR-0002: ドキュメント命名規則とディレクトリ構造

### 関連する Issue/PR
- なし

### 関連する Commit
- (このADR作成と同時にコミット予定)

---

**Status**: Accepted  
**次のアクション**: `scripts/build.py` の言語別ディレクトリ対応
