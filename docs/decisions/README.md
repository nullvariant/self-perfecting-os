# Decisions ディレクトリ

**ADR（Architecture Decision Records）管理**

---

## 🎯 このディレクトリについて

重要な技術的決定を記録するためのディレクトリです。全ての重要な決定は必ずADRとして記録します。

---

## � 構造

```
decisions/
├── active/                     # 現在有効な決定
│   └── 2025/
│       └── 10/
│           ├── 20251028_0001_ci-cd-pause_architecture.md
│           ├── 20251028_0002_naming-structure_documentation.md
│           ├── 20251028_0003_ディレクトリ・ファイル名の小文字・ハイフン統一_documentation.md
│           ├── 20251028_0004_github-actions-によるドキュメント自動バリデー_tooling.md
│           ├── 20251028_0005_多言語対応-言語別ディレクトリ構造への移行_documentation.md
│           ├── 20251028_0006_github-pagesランディングページの実装_documentation.md
│           ├── 20251028_0007_changelogsディレクトリのnullvariant-w_architecture.md
│           ├── 20251029_0008_対話生ログの永続保存システム確立_governance.md
│           └── 20251029_0009_テストファイル管理規則testsfixtures配下に集約_process.md
├── deprecated/                 # 非推奨（参考のみ）
├── superseded/                 # 上書きされた決定
├── INDEX.md                    # 自動生成索引
└── README.md                   # このファイル
```

---

## 📋 ADR一覧

詳細は [`INDEX.md`](INDEX.md) を参照してください（自動生成）。

---

## 📝 ADRとは

### Architecture Decision Records

以下のいずれかに該当する場合、**必ずADRを作成**してください：

- ✅ API の変更・移行
- ✅ アーキテクチャの変更
- ✅ CI/CD パイプラインの停止・変更
- ✅ ドキュメント構造の大幅な変更
- ✅ 重要な依存関係の追加・削除
- ✅ プロセス・手順の変更
- ✅ 破壊的変更 (Breaking Changes)
- **定義**: 重要な技術的決定とその理由を記録したドキュメント
- **目的**: 「なぜこの決定をしたか」を後から追跡可能にする
- **形式**: 標準テンプレートに従う

---

## ✅ ADRが必要な場合

以下のいずれかに該当する場合、**必ずADRを作成**:

- ✅ API変更・移行
- ✅ アーキテクチャ変更
- ✅ CI/CDパイプラインの停止・変更
- ✅ ドキュメント構造の大幅な変更
- ✅ 重要な依存関係の追加・削除
- ✅ プロセス・手順の変更
- ✅ 破壊的変更 (Breaking Changes)
- ✅ セキュリティ関連の決定
- ✅ パフォーマンス最適化の方針決定

詳細は [`docs/governance/AI_GUIDELINES.md`](../governance/AI_GUIDELINES.md) を参照。

---

## � ADRの作成方法

### 1. スクリプト実行

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "human"  # or "GitHub Copilot", "Claude Code"
```

### 2. 生成されたファイルを編集

テンプレートに従って編集してください。

### 3. INDEX.md更新

```bash
python scripts/generate_index.py
```

---

## 📋 ADRのテンプレート

[`decisions/0000_template.md`](0000_template.md) を参照してください。

---

## 🔄 ADRのライフサイクル

### 1. Draft（草案）

```markdown
## Status
- **状態**: Draft
```

### 2. Accepted（承認）

```markdown
## Status
- **状態**: Accepted
```

### 3. Deprecated（非推奨）

```bash
# deprecated/ に移動
mv docs/decisions/active/2025/10/20251028_0005_*.md \
   docs/decisions/deprecated/
```

### 4. Superseded（上書き）

```markdown
## Status
- **状態**: Superseded by ADR-0007
```

```bash
# superseded/ に移動
mv docs/decisions/active/2025/10/20251028_0005_*.md \
   docs/decisions/superseded/
```

---

## 🚫 禁止事項

### ❌ 絶対にやってはいけないこと

1. **ADRの削除**
   - 古くなった ADR は削除せず、Status を `Deprecated` に変更

2. **ADR番号の欠番**
   - ADR番号は連番（0001, 0002, 0003...）

3. **勝手な Status 変更**
   - `Draft` → `Accepted` は human のみ

---

## 📚 関連ドキュメント

- [`docs/governance/AI_GUIDELINES.md`](../governance/AI_GUIDELINES.md)
- [`docs/governance/HIERARCHY_RULES.md`](../governance/HIERARCHY_RULES.md)
- [ADR GitHub](https://adr.github.io/)

---

**最終更新**: 2025年10月28日
