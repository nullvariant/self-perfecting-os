# リポジトリ横断ワークフロー

## 対話開始前の準備

### ✅ 開いておくファイル
- [ ] 両リポジトリの関連ファイル
- [ ] `scripts/prepare_note_article.py` (nullvariant)
- [ ] `changelogs/` (nullvariant-atelier)

### ✅ 閉じておくファイル
- [ ] 無関係なファイル

---

## 新規チャット開始

**推奨**: リポジトリ横断専用の新しいチャットを開始

**理由**: 単一リポジトリ作業のコンテキストが混入しない

---

## 効率的なクエリパターン

### パターン1: 境界理解
```markdown
@.cursor/contexts/REPOSITORY_BOUNDARIES.md

{作業内容の説明}

このファイルはどちらのリポジトリに配置すべきですか？
```

### パターン2: Changelog記事生成
```markdown
@scripts/prepare_note_article.py
@CHANGELOG.md

最新のChangelogエントリーからnote記事を生成してください。
出力先: nullvariant-atelier/changelogs/
```

---

## ❌ 避けるべきパターン

### 非効率なパターン1: 境界を明示しない
```markdown
❌ ファイルを作成してください

→ どちらのリポジトリか不明、誤配置のリスク
```

### 非効率なパターン2: 過度なコンテキスト
```markdown
❌ @.cursor/contexts/PERSONA_SYSTEM.md  # 横断作業には不要
❌ @.cursor/contexts/ADR_GUIDELINES.md  # 横断作業には不要

Changelog記事を生成してください
```

---

## 作業後のチェックリスト

### ファイル作成時
- [ ] **リポジトリ宣言**: 「このファイルは {nullvariant / nullvariant-atelier} に関するものです」と明示
- [ ] **配置確認**: 適切なリポジトリに配置されている
- [ ] **Git add**: 各リポジトリで `git add` のみ実行
- [ ] **ユーザー確認**: 「コミットしてもよろしいですか？」と確認

### Changelog記事生成時
- [ ] **入力**: `nullvariant/CHANGELOG.md`
- [ ] **出力**: `nullvariant-atelier/changelogs/`
- [ ] **フォーマット**: note.com公開用の物語的フォーマット

---

## トークン消費の目安

| シナリオ | トークン数 | 備考 |
|---|---:|---|
| 境界理解 | ~1,000 | コアルール + REPOSITORY_BOUNDARIES |
| Changelog記事生成 | ~2,000 | コアルール + スクリプト + CHANGELOG |

**Phase 1実施前**: 約10,000トークン

---

**作成日**: 2025-11-02

