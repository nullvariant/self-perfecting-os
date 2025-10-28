# Architecture Decision Records (ADR)

このディレクトリには、Null;Variant プロジェクトにおける**全ての重要な決定**を時系列で記録します。

---

## 📋 ADRとは？

**Architecture Decision Records (ADR)** は、ソフトウェア開発における重要な決定を記録するための軽量なドキュメント形式です。

### なぜ必要なのか？

- ✅ **決定の理由を後から追跡できる**
- ✅ **AI環境（Claude Code, GitHub Copilot等）を跨いでも文脈が途切れない**
- ✅ **新しい貢献者（AI/人間）が過去の経緯を理解できる**
- ✅ **ドキュメント間の矛盾を防ぐ**

---

## 📂 ADR一覧

| ADR番号 | タイトル | 日付 | Status |
|---------|---------|------|--------|
| [0000](0000-adr-template.md) | テンプレート | - | Template |
| [0001](0001-ci-cd-pause.md) | Claude API レート制限対応によるCI/CD一時停止 | 2025-10-28 | Accepted |

---

## 🛠️ ADRの作成方法

### 方法1: 自動生成（推奨）

```bash
python scripts/record_decision.py \
  --title "決定のタイトル" \
  --context "背景・理由" \
  --author "GitHub Copilot"  # or "Claude Code", "human"
```

### 方法2: 手動作成

1. [`0000-adr-template.md`](0000-adr-template.md) をコピー
2. ファイル名を `ADR-XXXX-タイトル.md` に変更（XXXX = 連番）
3. 各セクションを埋める
4. Status を `Draft` → `Accepted` に変更
5. このディレクトリに配置

---

## 📝 ADRが必要な場合

以下のいずれかに該当する場合、**必ずADRを作成**してください：

- ✅ API の変更・移行
- ✅ アーキテクチャの変更
- ✅ CI/CD パイプラインの停止・変更
- ✅ ドキュメント構造の大幅な変更
- ✅ 重要な依存関係の追加・削除
- ✅ プロセス・手順の変更
- ✅ 破壊的変更 (Breaking Changes)
- ✅ セキュリティ関連の決定
- ✅ パフォーマンス最適化の方針決定

詳細は [docs/governance/AI_GUIDELINES.md](../GOVERNANCE/AI_GUIDELINES.md) を参照。

---

## 🔄 ADRのライフサイクル

```
Draft → Accepted → (Deprecated or Superseded)
```

### Status の意味

| Status | 説明 | 次のアクション |
|--------|------|--------------|
| **Draft** | 提案段階。レビュー待ち。 | human によるレビュー・承認 |
| **Accepted** | 承認済み。実装可能。 | 実装・運用 |
| **Deprecated** | 非推奨。新しいADRで置き換え推奨。 | 新ADR作成 |
| **Superseded** | 別のADRに置き換えられた。 | Related に新ADR番号を記載 |

---

## 🚫 禁止事項

### ❌ 絶対にやってはいけないこと

1. **ADRの削除**
   - 古くなった ADR は削除せず、Status を `Deprecated` に変更
   - 新しい ADR で上書きする場合は、Related に旧ADR番号を記載

2. **ADR番号の欠番**
   - ADR番号は連番（0001, 0002, 0003...）
   - 欠番があると `scripts/validate_docs.py` がエラー

3. **勝手な Status 変更**
   - `Draft` → `Accepted` は human のみ
   - `Accepted` → `Deprecated` は新ADR作成時のみ

---

## 📚 関連ドキュメント

- [docs/governance/AI_GUIDELINES.md](../GOVERNANCE/AI_GUIDELINES.md) - AI向けADR作成ガイド
- [docs/governance/HIERARCHY_RULES.md](../GOVERNANCE/HIERARCHY_RULES.md) - ドキュメント階層ルール
- [docs/governance/DOCUMENTATION_STRUCTURE.yml](../GOVERNANCE/DOCUMENTATION_STRUCTURE.yml) - 機械可読形式の定義
- [Architecture Decision Records (ADR)](https://adr.github.io/) - ADR公式サイト

---

## 🔍 検索のヒント

### タイトルで検索

```bash
ls -1 docs/decisions/ | grep "api"
# ADR-0001-ci-cd-pause.md
```

### 内容で検索

```bash
grep -r "Claude API" docs/decisions/
# docs/decisions/ADR-0001-ci-cd-pause.md:Claude Sonnet 4.5 の出力レート制限が...
```

### Status で検索

```bash
grep -l "Status.*Accepted" docs/decisions/*.md
# docs/decisions/ADR-0001-ci-cd-pause.md
```

---

## 🤖 AI向けの注意

**このディレクトリは Tier 0: Single Source of Truth (SSOT) です。**

- 重要な決定は**必ず**ここに記録してください
- 迷ったら ADR を作成してください
- 人間に確認を求めることを躊躇しないでください

詳細は [docs/governance/AI_GUIDELINES.md](../GOVERNANCE/AI_GUIDELINES.md) を参照。

---

**最終更新**: 2025-10-28  
**次回レビュー**: 2025-11-28
