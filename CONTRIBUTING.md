# CONTRIBUTING.md

- 編集するのは **`content/AGENT.ja.md`**（日本語・一次情報）だけ。
- CI が **リポジトリ直下の `AGENT.md`（英語標準）** と **`spec/agent.spec.yaml`** を自動生成します。

## セットアップ（ローカル）
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # 生成/レビューに使用
make gen && make val
```

## GitHub Actions
- Secrets に `OPENAI_API_KEY` を登録してください。
- `content/AGENT.ja.md` 変更で **build.yml** が走ります。
- Pull Request では **pr-guard.yml** が厳格チェックを実行します。

## 主要構成
```
AGENT.md                 # ← 英語標準（CI生成）
content/AGENT.ja.md      # ← 日本語一次情報（編集対象）
i18n/glossary.yml        # 語彙固定辞書
spec/{agent.schema.json, agent.spec.yaml}
scripts/{build.py, review.py, prompts/*.txt}
.github/workflows/{build.yml, pr-guard.yml}
```
