# テキスト資産管理ワークフロー

## 概要

本プロジェクト（nullvariant）では、テキスト資産をGitHub（公開・共有可能）とObsidian（プライベート・未成熟）で分散管理しています。

この文書では、両者の役割分担と、テキスト資産の作成から公開までのワークフローを定義します。

## 管理原則

### GitHub管理対象

以下のテキスト資産はGitHubで管理します：

- ✅ **公開版コンテンツ**（`content/`）
  - AGENT.md、EmotionMood_Dictionary.md 等
  
- ✅ **公開可能な対話ログ**（`conversations/`）
  - AIとの対話記録
  
- ✅ **ドキュメント**（`docs/`）
  - マニュアル・解説文書
  
- ✅ **バージョン履歴**（`changelogs/`）
  - 思考記録・note-archives

### Obsidian管理対象

以下のテキスト資産はObsidian（ローカル）で管理します：

- 📝 **プライベートな思考の断片**
  - 日次メモ・アイデアの走り書き
  
- 📝 **未成熟な下書き**
  - 構造化されていないテキスト
  
- 📝 **参考資料の個人的整理**
  - 読書メモ・リサーチノート
  
- 📝 **公開済みコンテンツの複製**（参照用）
  - note記事のローカルバックアップ

## ワークフロー

### Phase 1: 創造フェーズ（Obsidian）

**場所:** Obsidian（ローカル）

**活動:**
- 自由に書く（構造・品質不問）
- 双方向リンク・タグを活用
- 思考の流れを妨げない
- アイデアの探索・実験

**成果物:** 
- 思考の断片
- 未成熟な下書き

---

### Phase 2: 選別フェーズ

**判断基準:** 「これは公開価値があるか？」

#### ✅ YES（公開価値あり）
→ Phase 3へ進む

**判断材料:**
- 他者に役立つ可能性がある
- 自己の思考を体系化・記録する価値がある
- note記事・ブログ記事として成立する
- AGENT.mdの補足・解説として機能する

#### ❌ NO（プライベート）
→ Obsidianに残す

**判断材料:**
- 個人的なメモ・走り書き
- センシティブな内容
- 未成熟で整理が必要
- 公開する意義が不明確

**迷った場合:** Obsidianに残す。成熟してから再判断。

---

### Phase 3: 整形フェーズ（Obsidian → GitHub）

**場所:** Obsidian（作業）→ GitHub（最終配置）

**活動:**
1. **構造化**
   - 見出し・段落を整理
   - 論理的な流れを確保
   
2. **品質向上**
   - 誤字・脱字の修正
   - 曖昧な表現の明確化
   
3. **公開前レビュー**
   - センシティブ情報の削除
   - 外部リンクの確認
   
4. **適切なディレクトリへ配置**
   - `conversations/` : AI対話ログ
   - `content/` : 完成版コンテンツ
   - `docs/` : ドキュメント・マニュアル
   - `changelogs/note-archives/` : 思考記録

**成果物:**
- 公開可能な品質のMarkdownファイル

---

### Phase 4: コミット（GitHub）

**場所:** GitHub

**活動:**

```bash
# ファイルをステージング
git add [ファイルパス]

# コミットメッセージの作成
git commit -m "[種別]: [内容の簡潔な説明]"

# プッシュ
git push origin main
```

**コミットメッセージの種別:**
- `feat:` 新機能・新コンテンツ
- `docs:` ドキュメント追加・更新
- `fix:` 修正
- `refactor:` リファクタリング
- `chore:` その他の変更

**例:**
```bash
git commit -m "feat: Add conversation log about AI model compatibility"
git commit -m "docs: Update workflow for text asset management"
```

---

### Phase 5: 公開フェーズ（note等）

**場所:** note / ブログ等の外部プラットフォーム

**活動:**
1. GitHubからコンテンツをコピー
2. プラットフォームに合わせた調整
   - 画像の埋め込み
   - リンクの調整
   - フォーマットの微調整
3. 公開
4. （オプション）公開後、Obsidianに公開版の複製を保存

**note記事転用の判断基準:**
- 対話ログ（`conversations/`）の「note転用候補」フラグ
- 単独記事として成立する（3,000字以上推奨）
- 明確なターゲット読者層がある

---

## ディレクトリ構造

### GitHub（nullvariant repo）

```
nullvariant/
├── content/              # 公開版コンテンツ
│   ├── ja/
│   │   ├── AGENT.md
│   │   └── EmotionMood_Dictionary.md
│   └── en/ (自動生成)
├── conversations/        # AI対話ログ
│   ├── README.md
│   └── 2025-10-13_agent-meta-dialogue.md
├── docs/                 # ドキュメント
│   ├── WORKFLOW_TEXT_ASSETS.ja.md  ← この文書
│   └── ...
├── changelogs/           # バージョン履歴
│   └── note-archives/    # 思考記録
└── scripts/              # スクリプト
```

### Obsidian（ローカル）

```
ObsidianVault/
├── Daily Notes/          # 日次メモ
├── Thoughts/             # 思考の断片
├── Drafts/               # 下書き（未成熟）
├── Published/            # 公開済みの複製（参照用）
└── References/           # 参考資料
```

## トラブルシューティング

### Q: 公開すべきか迷う場合は？

**A:** Obsidianに残す。成熟してから再判断。

無理に公開する必要はありません。時間をおいて読み返し、価値を再評価してください。

---

### Q: 同じ内容がGitHubとObsidianに重複している場合は？

**A:** GitHubを「正」とし、Obsidian版は参照用として保持。

- **更新はGitHub側のみ**で行う
- Obsidian版は「スナップショット」として保持
- 必要に応じてGitHubから最新版をObsidianへコピー

---

### Q: Obsidianで書いた内容をどうGitHubに移すか？

**A:** 手動でコピー&ペースト（当面）。

1. Obsidianで内容を整形
2. 新規Markdownファイルを作成（適切なディレクトリ）
3. 内容をコピー&ペースト
4. Git commit & push

将来的に自動化を検討する可能性があります（Phase 2以降）。

---

### Q: GitHubに配置する際、どのディレクトリが適切か？

**A:** 以下のガイドラインを参照：

| 内容の種類 | 配置先 |
|-----------|--------|
| AI対話ログ | `conversations/` |
| 完成版コンテンツ | `content/` |
| ドキュメント・マニュアル | `docs/` |
| 思考記録・note記事草案 | `changelogs/note-archives/` |
| スクリプト・ツール | `scripts/` |

迷った場合は、`conversations/` または `changelogs/note-archives/` に配置してください。

---

## 将来的な拡張可能性

### Phase 2: 段階的統合（6-12ヶ月後）

**検討事項:**
- Obsidian VaultをGit管理下に置く（ローカルGitリポジトリ）
- プライベート部分は `.gitignore` で除外
- GitHub連携の自動化（スクリプト化）

**移行判断基準（統合移行スコア）:**

```
統合移行スコア = 
  (手動同期頻度 × 3) + 
  (バージョン管理必要性 × 5) + 
  (検索困難度 × 2) + 
  (コラボ機会 × 10)
```

- **< 20**: ハイブリッド管理継続
- **20-40**: Phase 2移行を検討
- **> 40**: Phase 2移行を推奨

**評価サイクル:** 3ヶ月ごと

---

### Phase 3: 完全統合（12ヶ月以降）

**検討事項:**
- プライベートメモの暗号化（Git-crypt等）
- 完全統合（GitHub = Single Source of Truth）
- Obsidianは「ビューアー」として使用

**実施判断:** Phase 2の運用実績に基づいて決定

---

## 評価指標

### 短期（3ヶ月）

- [ ] 手動同期の頻度（週あたり）
- [ ] 「どこに書いたか忘れた」の発生回数
- [ ] Obsidianでのバージョン管理の必要性

### 中期（6-12ヶ月）

- [ ] 統合移行スコア（閾値20以上で検討）
- [ ] note記事転用率（対話ログから）
- [ ] コラボレーション機会の有無

### 長期（12ヶ月以降）

- [ ] 完全統合の必要性
- [ ] ワークフローの満足度
- [ ] テキスト資産の総量・品質

---

## 関連ドキュメント

- [conversations/README.md](../conversations/README.md) - 対話ログの管理方針
- [content/ja/AGENT.md](../../../content/ja/AGENT.md) - 本体仕様書
- [changelogs/README.md](../../../changelogs/README.md) - バージョン履歴

---

**最終更新:** 2025年10月13日  
**次回評価予定:** 2026年1月13日
