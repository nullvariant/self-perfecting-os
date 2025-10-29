# ADR-0007: changelogsディレクトリのnullvariant-writingsへの移行

## Status
- **提案日**: 2025-10-28
- **状態**: Accepted
- **決定者**: 園長 + Claude Code

## Context

### 背景

2025-10-28の対話で「提案D（SEO最適化・完全分離案）」が正式採用された（`nullvariant-writings/docs/log/2025/10/2025-10-28_changelog-workflow-dilemma.md`参照）。

**提案Dの核心:**
- GitHub公開リポジトリとnote.comに同じコンテンツを置くと、SEOペナルティのリスク
- 技術記録（CHANGELOG.md）と人間読者向け物語（note記事）は、別プラットフォームで最適化すべき

**構造:**
```
nullvariant/
  └─ CHANGELOG.md              ← 技術的記録のみ（Keep a Changelog形式）

nullvariant-writings/
  └─ changelogs/               ← note記事の原稿・アーカイブ
      ├─ drafts/
      └─ note-archives/
```

### 問題

`changelogs/`ディレクトリはnullvariantリポジトリに存在するが、note記事はnullvariant-writingsで管理すべき。

しかし、`scripts/prepare_note_article.py`は`content/ja/AGENT.md`に依存しているため、スクリプトまで移動すると複雑化する。

### 検討した選択肢

1. **選択肢A: changelogsとスクリプトを両方移動**
   - メリット: note関連の完全一元管理
   - デメリット: リポジトリ間パス参照が複雑化、`content/ja/AGENT.md`への依存を解決困難

2. **選択肢B: スクリプトはnullvariantに残し、出力先のみ変更** ✅ 採用
   - メリット: `AGENT.md`への依存を維持、シンプルなパス修正のみ
   - デメリット: note関連がわずかに分散（スクリプト vs データ）

3. **選択肢C: すべてnullvariantに残す**
   - メリット: 何も変更しなくてよい
   - デメリット: 提案D（SEO最適化）の目的を達成できない

## Decision

**選択肢Bを採用: changelogsディレクトリのみnullvariant-writingsへ移行し、スクリプトはnullvariantに残す**

**実装:**
1. `nullvariant/changelogs/` → `nullvariant-writings/changelogs/` へ物理移動
2. `scripts/prepare_note_article.py` の出力先パスを `../nullvariant-writings/changelogs/` に変更
3. スクリプトの入力元（`content/ja/AGENT.md`）はnullvariantに残る

**ディレクトリ構造（移行後）:**
```
nullvariant/
  ├── content/ja/AGENT.md           ← スクリプトが読み込む
  ├── scripts/
  │   └── prepare_note_article.py  ← nullvariantに残す
  └── CHANGELOG.md                  ← 技術記録のみ

nullvariant-writings/
  └── changelogs/                   ← スクリプトが出力
      ├── drafts/
      └── note-archives/
```

## Consequences

### ✅ メリット

1. **SEO最適化の実現**
   - note記事がGitHub公開リポジトリに存在しない
   - Google検索での重複コンテンツペナルティを回避

2. **note記事の一元管理**
   - すべてのnote関連原稿がnullvariant-writingsに集約
   - Private repositoryでSEO影響なし、AI学習は可能

3. **シンプルな実装**
   - スクリプト修正は出力先パスのみ（数行の変更）
   - `content/ja/AGENT.md`への依存を維持（複雑なリポジトリ間参照不要）

4. **責務の明確化**
   - nullvariant: 技術仕様書・開発ツール
   - nullvariant-writings: コンテンツ原稿・アーカイブ

### ⚠️ デメリット

1. **わずかな分散**
   - note関連のスクリプトと データが別リポジトリ
   - ただし、明確な理由（AGENT.md依存）があるため許容範囲

2. **リポジトリ間の依存**
   - `prepare_note_article.py` が `../nullvariant-writings/` を前提
   - ディレクトリ構造が変わると動かなくなる可能性
   - 対策: ドキュメント化・エラーメッセージ改善

3. **初回実行時の注意**
   - nullvariant-writingsリポジトリが存在しない環境ではエラー
   - 対策: README.mdに前提条件を記載

### 📋 TODO

- [x] `scripts/prepare_note_article.py` の出力先パス修正
- [ ] `nullvariant/changelogs/` を `nullvariant-writings/changelogs/` へ移動
- [ ] nullvariant側のREADME.md更新（changelogsの移行先を明記）
- [ ] nullvariant側のCHANGELOG.md更新（`[Unreleased]`に記録）
- [ ] nullvariant-writings側のREADME.md更新（changelogsの受け入れを明記）
- [ ] nullvariant-writings側の移行記録ドキュメント作成
- [ ] スクリプト動作確認
- [ ] パス参照の全体チェック（`grep -r "changelogs/"` in nullvariant）
- [ ] リンク切れチェック（`scripts/check_path_references.py`）

## Related

### 関連するファイル

**nullvariant:**
- `scripts/prepare_note_article.py` - 出力先パス修正済み
- `CHANGELOG.md` - 技術記録のみ（Keep a Changelog形式）
- `changelogs/` - 移行対象（移行後は削除）

**nullvariant-writings:**
- `changelogs/` - 移行先（受け入れ先）
- `docs/log/2025/10/2025-10-28_changelog-workflow-dilemma.md` - 提案D決定の経緯

### 関連する ADR

- ADR-0006: GitHub Pagesランディングページの実装 - 同じセッションでの設計決定

### 関連するドキュメント

- `nullvariant-writings/docs/log/2025/10/2025-10-28_changelog-workflow-dilemma.md` - 提案D採用の対話ログ
- `nullvariant-writings/docs/log/2025/10/2025-10-28_散漫メモ.md` - 設計検討の散漫メモ

### 関連する Commit

- （移行実施後に記録）

---

**Status**: Accepted  
**実施日**: 2025-10-28  
**次のアクション**: TODOリストの実施
