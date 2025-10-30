# INDEX.md 自動再生成フック実装計画（Draft）

**Status**: Draft（要承認）  
**Last Updated**: 2025-10-30  
**Owner**: nullvariant（実装担当: GitHub Copilot 想定）  
**Related**: ADR-0015（`docs/decisions/active/2025/10/20251030_0015_git-hooks-index-generation_tooling.md`）

---

## 1. 背景と目的

- 現状、`docs/decisions/`, `docs/prd/`, `docs/operations/`, `docs/governance/` 配下の INDEX.md は `python scripts/generate_index.py` を**手動**で実行して更新している。
- ADR-0015 にて「コミット時に自動再生成する Git pre-commit hook を導入する」方針を決定したが、**実装未着手**のまま Pending。
- 本ドキュメントは、フック実装の仕様を明文化し、承認後に実装へ移行するための作業指針を提供する。

---

## 2. スコープ

対象ディレクトリと生成物:

| 監視対象 | トリガーファイル | 再生成対象 |
|----------|------------------|------------|
| `docs/decisions/active|deprecated|superseded/**` | `.md`（`INDEX.md`除く） | `docs/decisions/INDEX.md` |
| `docs/prd/active|implemented/*.md` | `.md` | `docs/prd/INDEX.md` |
| `docs/operations/current|archive/**` | `.md`（`README.md`除く） | `docs/operations/INDEX.md` |
| `docs/governance/*` | `.md`, `.yml`, `.yaml` （`README.md`, `INDEX.md`除く） | `docs/governance/INDEX.md` |

**非対象**:
- `content/` や `spec/` など INDEX.md を生成しない領域
- `INDEX.md` 単独の編集（手動修正） → フックは発火しない

---

## 3. フック動作仕様

### 3.1 高レベルフロー

```
git commit
  ↳ pre-commit フック呼び出し
      ↳ `git diff --cached --name-only`
      ↳ 対象パスに一致 → 生成対象をキューへ追加
      ↳ キューが空でなければ:
           - python scripts/generate_index.py --target <...>
           - 実行ごとに `git add` で対象 INDEX.md をステージング
      ↳ 生成が失敗した場合 → 標準エラー出力 & コミット中断（終了コード ≠ 0）
```

### 3.2 判定ルール詳細

- `git diff --cached --name-only` の結果に対して `grep` / `python` で正規表現マッチ。
- 各ディレクトリごとに個別トリガーを設け、同一コミットで複数対象が変更された場合でも、生成スクリプトは**対象ごとに一度のみ**実行。
- 生成スクリプトは `python scripts/generate_index.py --target <dir>` を使用。複数ターゲットがある場合は `--target all` ではなく個別実行（必要最小限の再生成 & ログ明確化のため）。

### 3.3 標準出力 / ログ

- 生成開始時: `echo "📋 docs/operations 変更を検知 → INDEX.md 再生成..."` のように簡潔に表示。
- 正常終了時: `generate_index.py` 側のログに加え、フック側で `echo "✅ docs/operations/INDEX.md を更新しました"` を出力。
- 失敗時: エラーメッセージを標準エラーに流し、`exit 1` でコミットを中断。ユーザーに `--no-verify` でスキップ可能である旨を表示する。

### 3.4 スキップ手段

- `git commit --no-verify` によるフック無効化は従来どおり利用可。
- 一時的にフックを無効化したい場合の手順（`chmod -x .git/hooks/pre-commit`）をドキュメント化。

---

## 4. 実装変更差分（予定）

| 変更対象 | 内容 |
|----------|------|
| `scripts/hooks/pre-commit` | 新規追加。フック本体（POSIX シェル / Bash） |
| `scripts/install-hooks.sh` | 新規追加。`scripts/hooks/pre-commit` を `.git/hooks/pre-commit` にコピーし、実行権限を付与 |
| `.gitignore` | 必要に応じて `.git/hooks/pre-commit` を無視リストに追加（既に含まれているか要確認） |
| `README.md` / `CONTRIBUTING.md` | セットアップ手順に `scripts/install-hooks.sh` を追記 |
| `docs/decisions/active/2025/10/20251030_0015_git-hooks-index-generation_tooling.md` | Status を `Accepted` に更新し、実装セクションへリンク |

---

## 5. テスト計画

### 5.1 手動テストシナリオ

1. **単一ディレクトリの変更検知**  
   - 例: `docs/operations/current/TEST.md` を追加  
   - `git add` → `git commit`  
   - フックが発火し、`docs/operations/INDEX.md` が再生成されることを確認。

2. **複数ディレクトリ同時変更**  
   - ADR 追加 + PRD 追加  
   - フックがそれぞれの INDEX を 1 回ずつ生成し、両方がステージされることを確認。

3. **非対象ファイル変更**  
   - `README.md` のみ編集  
   - フックが何も実行しないことを確認。

4. **`--no-verify` スキップ**  
   - `git commit --no-verify` でフックがスキップされることを確認。

5. **エラーハンドリング**  
   - `generate_index.py` を一時的に失敗させる（例: わざと Syntax Error を挿入）  
   - フックがコミットをブロックし、エラーメッセージを表示することを確認。

### 5.2 自動テスト（将来）

- `pytest` などでの Hooks テスト環境は現状未計画。必要に応じて CI 上で `scripts/install-hooks.sh` → 仮コミット → 差分確認の E2E テストを検討。

---

## 6. 導入・ロールアウト手順

1. 本ドキュメントの承認（nullvariant によるレビュー）
2. `scripts/hooks/pre-commit` と `scripts/install-hooks.sh` を実装
3. `README.md` / `CONTRIBUTING.md` / ADR-0015 を更新
4. `scripts/install-hooks.sh` をローカルで実行し、既存メンテナーの環境にフックを導入
5. フック導入後の初回コミットでテストシナリオを走らせ、期待通り動作するか検証
6. 問題なければ ADR-0015 を `Accepted` としてマージ

---

## 7. リスクとオープン事項

| リスク / 未解決事項 | 対応案 |
|----------------------|--------|
| Windows 環境でのシェル互換性 | `#!/usr/bin/env bash` を明示。Windows 開発者がいる場合は PowerShell 版を別途検討 |
| 生成スクリプトの実行時間増大 | 対象ディレクトリ単位で最小限の再生成に留める。処理時間が許容範囲を超える場合は Python 実装での差分検知に移行 |
| Staged 状態とワーキングツリーでの差異 | フック内で `git status --short docs/*/INDEX.md` をチェックし、未ステージ差分が残らないよう注意喚起 |
| `generate_index.py` の将来機能追加 | 新ターゲットが増えた場合はトリガールールの追随が必要。変更時には本ドキュメントも更新する |

---

## 8. 承認ステップ

1. nullvariant が本ドキュメントをレビューし、必要な修正をフィードバック
2. 承認後、実装タスクを起票（Issue or TODO）
3. 実装完了後に再度レビュー（コード + 運用ドキュメント更新）

---

> 承認後、実装に着手します。フィードバックがあればコメントをお願いします。
