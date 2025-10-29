# docs/log/ - 作業ログ・記録

このディレクトリは、ガバナンス監査、品質レビュー、デバッグログなど、
**作業の時系列記録** を管理します。

## 配置ルール

```
docs/log/
├── {YYYY}/
│   └── {MM}/
│       └── {YYYYMMDD}_{slug}.md  ← 例: 20251029_governance-self-review.md
```

### 命名規則

| 要素 | 形式 | 例 | 説明 |
|------|-----|----|----|
| 年 | `YYYY` | `2025` | ログ作成年 |
| 月 | `MM` | `10` | ログ作成月 |
| 日付 | `YYYYMMDD` | `20251029` | ログ作成日 |
| スラッグ | `kebab-case` | `governance-self-review` | ログの簡潔な説明 |

## 検索方法

### 月別に検索
```bash
# 2025年10月のすべてのログを表示
ls -la docs/log/2025/10/

# 2025年9月のログを表示
ls -la docs/log/2025/09/
```

### キーワード別に検索
```bash
# governance に関するログをすべて検索
grep -r "governance" docs/log/ --include="*.md"

# 複数キーワードで検索
grep -r "review.*governance" docs/log/ --include="*.md"
```

### 最新のログを表示
```bash
# 最新10個のログ
find docs/log -name "*.md" -type f | sort | tail -10

# 特定月の最新ログ
find docs/log/2025/10 -name "*.md" -type f | sort | tail -5
```

---

## vs governance/ ディレクトリ

| 観点 | `governance/` | `log/` |
|------|-----------|------|
| **目的** | ガバナンスルール・定義（参照対象） | 作業記録・履歴（参照対象外） |
| **典型例** | `AI_GUIDELINES.md`, `DOCUMENTATION_STRUCTURE.yml` | `20251029_governance-self-review.md` |
| **ステータス管理** | ✅ active/deprecated/superseded | ❌ 不要（時系列で自動管理） |
| **ファイル命名** | 大文字、日付なし（恒久的） | 日付付き（時系列） |
| **参照頻度** | 高（頻繁に参照される） | 低（過去検証・履歴確認用） |
| **変更頻度** | 低（ルール変更時のみ） | 高（作業のたびに記録） |

---

## ライフサイクル

### 記録作成
- 作業完了時に `docs/log/{YYYY}/{MM}/{YYYYMMDD}_{slug}.md` として記録
- 例: `docs/log/2025/10/20251029_governance-self-review.md`

### 検索・参照
- 「2025年10月の記録を見たい」→ `docs/log/2025/10/` を参照
- 「governance に関する過去ログ」→ grep で検索

### 削除・アーカイブ
- 削除ポリシーは運用判断で決定
- 現在: 永続保存（特別な指示がない限り）

---

## GitHub Copilot 向けガイド

### ログファイルを作成するタイミング

以下の場合、作業記録をログとして保存してください：

- ✅ **ガバナンス監査・セルフレビュー** を実施した時
- ✅ **品質チェック・バリデーション** の結果
- ✅ **デバッグ・調査ログ** を記録する場合
- ✅ **実験的な試行・プロトタイピング** の記録

### ログファイルを作成してはいけない場合

以下は `log/` ではなく、他のディレクトリに記録してください：

- ❌ **決定事項** → `docs/decisions/active/{YYYY}/{MM}/` (ADR)
- ❌ **実装完了した要件定義** → `docs/prd/implemented/` (PRD)
- ❌ **恒久的な運用手順** → `docs/operations/current/` (Operations)
- ❌ **ガバナンスルール・定義** → `docs/governance/` (Governance)

### 判定フロー

```
「このドキュメント、どこに保存する？」

1. 決定したこと? → ADR (docs/decisions/)
2. 要件定義? → PRD (docs/prd/)
3. 運用手順? → Operations (docs/operations/current/)
4. ガバナンスルール・定義? → Governance (docs/governance/)
5. 上記以外で、作業の「記録」? → ✅ Log (docs/log/)
```

---

**最終更新**: 2025-10-29
