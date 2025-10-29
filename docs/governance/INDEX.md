# Governance & Documentation Rules

**最終更新**: 2025-10-29
**ドキュメント数**: 5個

ドキュメント管理とガバナンスの基準ドキュメント一覧です。

---

## 📚 参照ドキュメント

### 権威文書（SSOT）

- [AI向けドキュメント記録ガイドライン](AI_GUIDELINES.md)
- [ドキュメント構造定義（機械可読形式）](DOCUMENTATION_STRUCTURE.yml)
- [SSOT Priority Matrix: 複数ガバナンス文書の権威性と優先順位](SSOT_PRIORITY_MATRIX.md)

### 説明・ガイド文書

- [ドキュメント階層ルール（人間向け説明）](HIERARCHY_RULES.md)
- [命名規則とディレクトリ構造の決定 - サマリー](NAMING_DECISION_SUMMARY.md)


---

## 🗺️ 初めての方へ

このディレクトリに初めて来た方は、[README.md](README.md) から始めてください。
ユースケース別の導線が記載されています。

---

## ⚠️ 自動生成ファイルについて

以下のファイルは **CI/CD または scripts により自動生成** されます。**直接編集禁止**です。

### リポジトリルートレベル
- `AGENT.md` - `content/ja/AGENT.md` から自動生成（英語版仕様書）
- `spec/agent.spec.yaml` - `content/ja/AGENT.md` から自動生成（YAML構造化仕様）

### INDEX.md ファイル群
- `docs/decisions/INDEX.md`
- `docs/prd/INDEX.md`
- `docs/operations/INDEX.md`
- `docs/governance/INDEX.md`（このファイル）

**修正方法**: スクリプトを修正してから再生成
```bash
python scripts/generate_index.py --target [adr|prd|operations|governance|all]
```

詳細は [AI_GUIDELINES.md](AI_GUIDELINES.md) の「禁止事項」セクションを参照してください。

---

**注記**: このディレクトリは大文字メタドキュメント専用です。
時系列記録は `docs/log/` に管理されます。