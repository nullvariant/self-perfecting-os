---
category: documentation
date: 2025-11-03
number: 0019
status: Accepted
author: Claude (Cursor)
related: [ADR-0018]
---

# ADR-0019: YAMLフロントマター標準の確立

**Status**: Accepted  
**Decision Date**: 2025-11-03  
**Author**: Claude (Cursor)  
**Category**: documentation  
**Related**: ADR-0018 (ADRカテゴリのFrontmatter移行)

---

## Context

ADR-0018で「カテゴリをFrontmatterに移行」を決定したが、**Frontmatter自体の標準が未定義**だった。

### 現在の問題点

1. **Frontmatter定義が分散**
   - ADR-0018: ADR用Frontmatterを定義
   - DOCUMENTATION_STRUCTURE.yml: ファイル名形式のみ定義
   - **統一された権威文書が存在しない**

2. **ドキュメントタイプごとに異なるFrontmatter**
   - ADR用
   - PRD用
   - operations用
   - 将来的に他のドキュメントタイプも増える可能性

3. **バリデーションルールの欠如**
   - 必須フィールドの定義なし
   - フォーマット検証なし
   - 拡張性の考慮なし

4. **メタレベルの矛盾**
   - ADR-0018で「Frontmatterに移行」と決定
   - しかし「Frontmatterとは何か」が未定義
   - 実装不可能な状態

---

## Decision

**ドキュメントタイプごとのYAMLフロントマター標準を確立する**

### 基本原則

1. **ドキュメントタイプごとに必須フィールドを定義**
2. **拡張可能性を保持**（将来のフィールド追加）
3. **機械的バリデーション可能**（YAMLスキーマ）
4. **人間にも読みやすい**（コメント推奨）

---

## Frontmatter Standards

### 1. ADR (Architecture Decision Records)

#### 必須フィールド
```yaml
---
category: string          # architecture, documentation, tooling, process, governance
date: YYYY-MM-DD         # 決定日（ISO 8601形式）
number: NNNN             # ADR番号（4桁、ゼロパディング）
status: string           # Accepted, Superseded, Deprecated
---
```

#### 任意フィールド
```yaml
author: string           # 決定者（人間 or AI名）
supersedes: [NNNN, ...]  # 置き換え対象のADR番号（配列）
related: [NNNN, ...]     # 関連ADR番号（配列）
tags: [string, ...]      # タグ（検索用）
impact: string           # high, medium, low
```

#### 完全な例
```yaml
---
category: architecture
date: 2025-11-03
number: 0019
status: Accepted
author: Claude (Cursor)
related: [0018, 0002, 0011]
tags: [frontmatter, metadata, standards]
impact: high
---
```

---

### 2. PRD (Product Requirements Document)

#### 必須フィールド
```yaml
---
status: string           # Active, Implemented, Deprecated
date: YYYY-MM-DD         # 策定日
priority: string         # High, Medium, Low
---
```

#### 任意フィールド
```yaml
author: string           # 作成者
assignee: string         # 担当者
milestone: string        # マイルストーン
estimated_tokens: int    # 予想トークン消費量
actual_tokens: int       # 実際のトークン消費量
tags: [string, ...]      # タグ
related_adr: [NNNN, ...] # 関連ADR番号
---
```

#### 完全な例
```yaml
---
status: Active
date: 2025-11-03
priority: High
author: Human
assignee: Claude (Cursor)
milestone: Phase 7
estimated_tokens: 20000
tags: [frontmatter, migration, automation]
related_adr: [0018, 0019]
---
```

---

### 3. Operations (運用手順書)

#### 必須フィールド
```yaml
---
date: YYYY-MM-DD         # 最終更新日
frequency: string        # daily, weekly, monthly, yearly, ad-hoc
---
```

#### 任意フィールド
```yaml
author: string           # 作成者
last_updated_by: string  # 最終更新者
tags: [string, ...]      # タグ
---
```

#### 完全な例
```yaml
---
date: 2025-11-03
frequency: monthly
author: Human
last_updated_by: Claude (Cursor)
tags: [workflow, automation, ai-dialogue]
---
```

---

## Validation Rules

### 1. 必須フィールドチェック

```python
# ADR
required_fields_adr = ['category', 'date', 'number', 'status']

# PRD
required_fields_prd = ['status', 'date', 'priority']

# Operations
required_fields_ops = ['date', 'frequency']
```

### 2. フォーマット検証

```python
# 日付: ISO 8601形式
date_pattern = r'^\d{4}-\d{2}-\d{2}$'

# ADR番号: 4桁ゼロパディング
number_pattern = r'^\d{4}$'

# カテゴリ: 許可リスト
categories_adr = ['architecture', 'documentation', 'tooling', 
                  'process', 'governance']

# ステータス: 許可リスト（ADR）
status_adr = ['Accepted', 'Superseded', 'Deprecated']

# ステータス: 許可リスト（PRD）
status_prd = ['Active', 'Implemented', 'Deprecated']

# 優先度: 許可リスト（PRD）
priority_prd = ['High', 'Medium', 'Low']

# 頻度: 許可リスト（Operations）
frequency_ops = ['daily', 'weekly', 'monthly', 'yearly', 'ad-hoc']
```

### 3. バリデーションスクリプト

```python
import yaml
import re

def validate_frontmatter(file_path: str, doc_type: str) -> dict:
    """
    Frontmatterを検証
    
    Args:
        file_path: ファイルパス
        doc_type: 'adr', 'prd', 'operations'
    
    Returns:
        {'valid': bool, 'errors': [str, ...]}
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Frontmatter抽出
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {'valid': False, 'errors': ['Frontmatter not found']}
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        return {'valid': False, 'errors': [f'YAML parse error: {e}']}
    
    errors = []
    
    # 必須フィールドチェック
    required_fields = {
        'adr': ['category', 'date', 'number', 'status'],
        'prd': ['status', 'date', 'priority'],
        'operations': ['date', 'frequency']
    }
    
    for field in required_fields[doc_type]:
        if field not in frontmatter:
            errors.append(f'Missing required field: {field}')
    
    # フォーマット検証
    if 'date' in frontmatter:
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', frontmatter['date']):
            errors.append(f'Invalid date format: {frontmatter["date"]}')
    
    if doc_type == 'adr':
        if 'number' in frontmatter:
            if not re.match(r'^\d{4}$', str(frontmatter['number'])):
                errors.append(f'Invalid number format: {frontmatter["number"]}')
        
        if 'category' in frontmatter:
            valid_categories = ['architecture', 'documentation', 'tooling', 
                                'process', 'governance']
            if frontmatter['category'] not in valid_categories:
                errors.append(f'Invalid category: {frontmatter["category"]}')
    
    return {'valid': len(errors) == 0, 'errors': errors}
```

---

## Implementation

### 1. バリデーションスクリプトの作成

```bash
scripts/validate_frontmatter.py
```

### 2. Git Hooksへの統合

```bash
# pre-commit hook
python scripts/validate_frontmatter.py --changed-files
```

### 3. 既存ドキュメントの更新

- ADR: ADR-0018実装時に一括更新
- PRD: 既存PRDにFrontmatter追加
- Operations: 既存手順書にFrontmatter追加

---

## Consequences

### ✅ Positive

1. **統一された標準**: 全てのドキュメントタイプでFrontmatter形式が明確
2. **機械的バリデーション**: 自動検証が可能
3. **拡張性**: 新しいフィールドを追加しやすい
4. **検索性**: メタデータによる高度な検索が可能
5. **Obsidian連携**: YAMLフロントマターはObsidian標準

---

### ⚠️ Negative

1. **学習コスト**: 各ドキュメントタイプのフィールドを覚える必要
2. **入力負荷**: 手動でFrontmatterを書く場合は手間
3. **移行コスト**: 既存ドキュメントへのFrontmatter追加

---

### 📋 Mitigation

1. **テンプレート提供**: 各ドキュメントタイプのテンプレート
2. **スクリプト自動化**: `record_decision.py`等でFrontmatter自動生成
3. **バリデーション**: Git Hooksで自動検証

---

## Extensibility

### 将来追加される可能性のあるフィールド

#### ADR
```yaml
reviewed_by: [string, ...]  # レビュー者
implemented_date: YYYY-MM-DD  # 実装完了日
deprecated_date: YYYY-MM-DD   # 非推奨日
superseded_by: NNNN           # 上書きされたADR番号
```

#### PRD
```yaml
dependencies: [string, ...]   # 依存関係
blockers: [string, ...]       # ブロッカー
completion_date: YYYY-MM-DD   # 完了日
```

#### Operations
```yaml
dependencies: [string, ...]   # 依存ツール・サービス
estimated_time: string        # 所要時間
```

### フィールド追加時のルール

1. **既存の必須フィールドは変更しない**（後方互換性）
2. **新しいフィールドは任意とする**（段階的導入）
3. **ADRを作成**（フィールド追加の決定を記録）

---

## Related Decisions

- **ADR-0018**: カテゴリをFrontmatterに移行（このADRの前提）
- **ADR-0002**: 命名規則とディレクトリ構造（ファイル名形式）
- **Future ADR**: Obsidian連携時のFrontmatter拡張

---

## Summary

このADRは、**「Frontmatterとは何か」を明確に定義する**ものである。

ADR-0018で「カテゴリをFrontmatterに移行」を決定したが、Frontmatter自体の標準が未定義だった。このメタレベルの矛盾を解消するため、本ADRを作成した。

**定義したもの**:
1. ✅ ADR用Frontmatter（必須・任意フィールド）
2. ✅ PRD用Frontmatter
3. ✅ Operations用Frontmatter
4. ✅ バリデーションルール
5. ✅ 拡張性の指針

これにより：
- ✅ **統一された標準**（権威文書として機能）
- ✅ **機械的バリデーション**（自動検証可能）
- ✅ **拡張可能性**（将来のフィールド追加）
- ✅ **ADR-0018実装の前提条件**を満たす

が実現される。

---

**Status**: ✅ **ACCEPTED**  
**Implementation**: Ready (validation script作成 → 既存ドキュメント更新)  
**Last Updated**: 2025-11-03

