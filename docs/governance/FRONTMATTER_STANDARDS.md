# YAMLフロントマター標準

**Repository**: nullvariant (Public)  
**Purpose**: 全ドキュメントタイプのYAMLフロントマター標準定義  
**Authority**: この文書が唯一の真実の源泉（SSOT）  
**最終更新**: 2025年11月3日  
**Related ADR**: [ADR-0019](../decisions/active/2025/11/20251103_0019_frontmatter-standards.md)

---

## 📋 ドキュメントタイプ別標準

### 1. ADR (Architecture Decision Records)

#### 必須フィールド

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `category` | string | 許可リスト | architecture, documentation, tooling, process, governance |
| `date` | string | YYYY-MM-DD | 決定日（ISO 8601形式） |
| `number` | string | NNNN | ADR番号（4桁、ゼロパディング） |
| `status` | string | 許可リスト | Accepted, Superseded, Deprecated |

#### 任意フィールド

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `author` | string | 自由形式 | 決定者（人間 or AI名） |
| `supersedes` | array | [NNNN, ...] | 置き換え対象のADR番号 |
| `related` | array | [NNNN, ...] | 関連ADR番号 |
| `tags` | array | [string, ...] | タグ（検索用） |
| `impact` | string | 許可リスト | high, medium, low |

#### テンプレート

```yaml
---
category: architecture
date: 2025-11-03
number: 0019
status: Accepted
author: Claude (Cursor)
related: [0018, 0002]
tags: [frontmatter, metadata, standards]
impact: high
---
```

---

### 2. PRD (Product Requirements Document)

#### 必須フィールド

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `status` | string | 許可リスト | Active, Implemented, Deprecated |
| `date` | string | YYYY-MM-DD | 策定日 |
| `priority` | string | 許可リスト | High, Medium, Low |

#### 任意フィールド

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `author` | string | 自由形式 | 作成者 |
| `assignee` | string | 自由形式 | 担当者 |
| `milestone` | string | 自由形式 | マイルストーン |
| `estimated_tokens` | integer | 数値 | 予想トークン消費量 |
| `actual_tokens` | integer | 数値 | 実際のトークン消費量 |
| `tags` | array | [string, ...] | タグ |
| `related_adr` | array | [NNNN, ...] | 関連ADR番号 |

#### テンプレート

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

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `date` | string | YYYY-MM-DD | 最終更新日 |
| `frequency` | string | 許可リスト | daily, weekly, monthly, yearly, ad-hoc |

#### 任意フィールド

| フィールド | 型 | 形式 | 説明 |
|-----------|-----|------|------|
| `author` | string | 自由形式 | 作成者 |
| `last_updated_by` | string | 自由形式 | 最終更新者 |
| `tags` | array | [string, ...] | タグ |

#### テンプレート

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

## 🔍 バリデーションルール

### 日付形式
```regex
^\d{4}-\d{2}-\d{2}$
```

例: `2025-11-03`

### ADR番号形式
```regex
^\d{4}$
```

例: `0019`, `0001`

### 許可リスト

#### ADR - category
- `architecture`
- `documentation`
- `tooling`
- `process`
- `governance`

#### ADR - status
- `Accepted`
- `Superseded`
- `Deprecated`

#### ADR - impact
- `high`
- `medium`
- `low`

#### PRD - status
- `Active`
- `Implemented`
- `Deprecated`

#### PRD - priority
- `High`
- `Medium`
- `Low`

#### Operations - frequency
- `daily`
- `weekly`
- `monthly`
- `yearly`
- `ad-hoc`

---

## 🔧 実装ガイド

### バリデーションスクリプト

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
    # 実装例は ADR-0019 を参照
    pass
```

### Git Hooks統合

```bash
# .git/hooks/pre-commit
python scripts/validate_frontmatter.py --changed-files
```

---

## 📚 関連文書

- **[ADR-0019](../decisions/active/2025/11/20251103_0019_frontmatter-standards.md)**: この標準を確立した決定記録
- **[ADR-0018](../decisions/active/2025/11/20251103_0018_adr-category-in-frontmatter.md)**: ADRカテゴリのFrontmatter移行
- **[DOCUMENTATION_STRUCTURE.yml](DOCUMENTATION_STRUCTURE.yml)**: ドキュメント構造定義（機械可読形式）

---

**Authority**: この文書が Frontmatter 標準の唯一の真実の源泉（SSOT）です。  
**Updates**: 標準変更時は必ず ADR を作成してください。

