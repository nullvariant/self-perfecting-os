# ADR作成ワークフロー

## 対話開始前の準備

### ✅ 開いておくファイル
- [ ] `docs/decisions/0000_template.md` (nullvariant)
- [ ] `docs/governance/AI_GUIDELINES.md` (nullvariant)
- [ ] 直近のADR 2-3件（参考用）

### ✅ 閉じておくファイル
- [ ] スクリプト類
- [ ] ログファイル
- [ ] テストファイル

---

## 新規チャット開始

**推奨**: ADR作成専用の新しいチャットを開始

**理由**: 他の作業のコンテキストが混入しない

---

## 効率的なクエリパターン

### パターン1: テンプレート活用
```markdown
@docs/decisions/0000_template.md
@.cursor/contexts/ADR_GUIDELINES.md

{決定内容の説明}

上記のテンプレートとガイドラインに従って、ADRを作成してください。
```

### パターン2: 過去のADR参考
```markdown
@docs/decisions/0000_template.md
@docs/decisions/active/2025/10/20251029_0011_filename-case-convention_documentation.md

上記のADR-0011と同様の形式で、{決定内容}に関するADRを作成してください。
```

### パターン3: 段階的作成
```markdown
# Step 1: 背景・理由の整理
@.cursor/contexts/ADR_GUIDELINES.md

{決定内容}の背景と理由を整理してください。

（確認後）

# Step 2: ADR本文作成
@docs/decisions/0000_template.md

上記の背景・理由に基づいて、ADR本文を作成してください。
```

---

## ❌ 避けるべきパターン

### 非効率なパターン1: コンテキスト過多
```markdown
❌ @docs/governance/HIERARCHY_RULES.md  # ADR作成には不要
❌ @.cursor/contexts/PERSONA_SYSTEM.md  # ADR作成には不要
❌ @scripts/record_decision.py  # まだ実行段階ではない

ADRを作成してください
```

### 非効率なパターン2: コンテキスト不足
```markdown
❌ ADRを作成してください

→ テンプレートもガイドラインも参照されず、品質が低下
```

---

## 作成後のチェックリスト

- [ ] **Frontmatter**: status, created, updated, author, tags
- [ ] **命名規則**: `{YYYYMMDD}_{NNNN}_{lowercase-hyphen-slug}_{category}.md`
- [ ] **配置**: `docs/decisions/active/{YYYY}/{MM}/`
- [ ] **内容**: 背景、決定内容、理由、影響、関連決定
- [ ] **Git add**: `git add` のみ実行（コミットは承認後）
- [ ] **ユーザー確認**: 「コミットしてもよろしいですか？」と確認

---

## トークン消費の目安

| 項目 | トークン数 | 備考 |
|---|---:|---|
| コアルール | ~500 | 常時読み込み |
| ADR_GUIDELINES.md | ~800 | 必要時のみ |
| テンプレート | ~400 | 必要時のみ |
| 過去のADR 1件 | ~500 | 参考時のみ |
| **合計** | **~2,200** | Phase 1実施前: ~10,000 |

**削減率**: 約78%削減

---

**作成日**: 2025-11-02

