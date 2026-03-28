# 任务看板系统 - 数据库设计

## 概述

本文档描述任务看板系统的完整数据库设计，包括所有表结构、字段定义、约束条件和表之间的关系。

## ER 关系图

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │───┐   │   Board     │───┐   │    List     │
├─────────────┤   │   ├─────────────┤   │   ├─────────────┤
│ id          │   │   │ id          │   │   │ id          │
│ email       │   │   │ title       │   │   │ title       │
│ username    │───┘   │ owner_id    │───┘   │ board_id    │
│ password    │       │ description │       │ position    │
│ ...         │       │ ...         │       │ ...         │
└─────────────┘       └─────────────┘       └─────────────┘
       │                     │                     │
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│BoardMember  │       │    Card     │       │   Comment   │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ board_id    │       │ list_id     │◄──────│ card_id     │
│ user_id     │       │ title       │       │ user_id     │
│ role        │       │ description │       │ content     │
│ ...         │       │ assignee_id │       │ created_at  │
└─────────────┘       │ ...         │       └─────────────┘
                      └─────────────┘
                             │
                             ▼
                      ┌─────────────┐       ┌─────────────┐
                      │  CardLabel  │───┐   │   Label     │
                      ├─────────────┤   │   ├─────────────┤
                      │ card_id     │   │   │ id          │
                      │ label_id    │───┘   │ board_id    │
                      └─────────────┘       │ name        │
                                            │ color       │
┌─────────────┐       └─────────────┘
│  Activity   │
├─────────────┤
│ id          │
│ board_id    │
│ user_id     │
│ action      │
│ entity_type │
│ entity_id   │
│ ...         │
└─────────────┘
```

## 数据表设计

### 1. users - 用户表

存储系统用户的基本信息和认证凭据。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 用户唯一标识 |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 用户邮箱 |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希值 |
| full_name | VARCHAR(100) | | 全名 |
| avatar_url | VARCHAR(500) | | 头像URL |
| is_active | BOOLEAN | DEFAULT TRUE | 账户是否激活 |
| is_verified | BOOLEAN | DEFAULT FALSE | 邮箱是否验证 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

**索引：**
- `idx_users_email` ON (email)
- `idx_users_username` ON (username)

---

### 2. boards - 看板表

存储看板的基本信息。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 看板唯一标识 |
| title | VARCHAR(100) | NOT NULL | 看板标题 |
| description | TEXT | | 看板描述 |
| owner_id | UUID | FK(users.id), NOT NULL | 所有者ID |
| background_url | VARCHAR(500) | | 背景图URL |
| background_color | VARCHAR(7) | | 背景色（十六进制） |
| is_public | BOOLEAN | DEFAULT FALSE | 是否公开 |
| is_archived | BOOLEAN | DEFAULT FALSE | 是否归档 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

**索引：**
- `idx_boards_owner` ON (owner_id)
- `idx_boards_created` ON (created_at DESC)

---

### 3. board_members - 看板成员表

存储看板成员关系和权限。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 关系唯一标识 |
| board_id | UUID | FK(boards.id), NOT NULL | 看板ID |
| user_id | UUID | FK(users.id), NOT NULL | 用户ID |
| role | VARCHAR(20) | NOT NULL | 角色: owner/admin/member/viewer |
| joined_at | TIMESTAMP | DEFAULT NOW() | 加入时间 |

**角色权限说明：**
- `owner`: 完全控制，可删除看板
- `admin`: 管理看板，管理成员和标签
- `member`: 可编辑卡片和列表
- `viewer`: 只读权限

**索引：**
- `idx_board_members_board` ON (board_id)
- `idx_board_members_user` ON (user_id)
- `uniq_board_membership` UNIQUE (board_id, user_id)

---

### 4. lists - 任务列表表

存储看板内的列（如：待办、进行中、已完成）。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 列表唯一标识 |
| board_id | UUID | FK(boards.id), NOT NULL | 所属看板ID |
| title | VARCHAR(100) | NOT NULL | 列表标题 |
| position | INTEGER | NOT NULL | 在看板中的位置顺序 |
| is_archived | BOOLEAN | DEFAULT FALSE | 是否归档 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

**索引：**
- `idx_lists_board` ON (board_id)
- `idx_lists_position` ON (board_id, position)

---

### 5. cards - 任务卡片表

存储具体的任务卡片。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 卡片唯一标识 |
| list_id | UUID | FK(lists.id), NOT NULL | 所属列表ID |
| title | VARCHAR(200) | NOT NULL | 卡片标题 |
| description | TEXT | | 卡片描述 |
| position | INTEGER | NOT NULL | 在列表中的位置顺序 |
| assignee_id | UUID | FK(users.id) | 负责人ID |
| priority | VARCHAR(10) | DEFAULT 'medium' | 优先级: low/medium/high/critical |
| due_date | TIMESTAMP | | 截止日期 |
| is_completed | BOOLEAN | DEFAULT FALSE | 是否完成 |
| completed_at | TIMESTAMP | | 完成时间 |
| attachment_count | INTEGER | DEFAULT 0 | 附件数量 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

**索引：**
- `idx_cards_list` ON (list_id)
- `idx_cards_assignee` ON (assignee_id)
- `idx_cards_position` ON (list_id, position)
- `idx_cards_due_date` ON (due_date)
- `idx_cards_board_lookup` ON (id) INCLUDE (list_id) -- 用于快速查找所属看板

---

### 6. labels - 标签表

存储看板的标签定义。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 标签唯一标识 |
| board_id | UUID | FK(boards.id), NOT NULL | 所属看板ID |
| name | VARCHAR(50) | NOT NULL | 标签名称 |
| color | VARCHAR(7) | NOT NULL | 标签颜色（十六进制） |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |

**索引：**
- `idx_labels_board` ON (board_id)
- `uniq_labels_board_name` UNIQUE (board_id, name)

---

### 7. card_labels - 卡片标签关联表

存储卡片与标签的多对多关系。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| card_id | UUID | FK(cards.id), PK, NOT NULL | 卡片ID |
| label_id | UUID | FK(labels.id), PK, NOT NULL | 标签ID |

**索引：**
- `idx_card_labels_card` ON (card_id)
- `idx_card_labels_label` ON (label_id)

---

### 8. comments - 评论表

存储卡片的评论。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 评论唯一标识 |
| card_id | UUID | FK(cards.id), NOT NULL | 所属卡片ID |
| user_id | UUID | FK(users.id), NOT NULL | 评论者ID |
| content | TEXT | NOT NULL | 评论内容 |
| parent_id | UUID | FK(comments.id) | 父评论ID（用于回复） |
| is_edited | BOOLEAN | DEFAULT FALSE | 是否已编辑 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT NOW() | 更新时间 |

**索引：**
- `idx_comments_card` ON (card_id, created_at DESC)
- `idx_comments_user` ON (user_id)

---

### 9. activities - 活动日志表

存储看板内的所有活动记录。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 活动唯一标识 |
| board_id | UUID | FK(boards.id), NOT NULL | 所属看板ID |
| user_id | UUID | FK(users.id), NOT NULL | 操作者ID |
| action | VARCHAR(50) | NOT NULL | 动作类型 |
| entity_type | VARCHAR(20) | NOT NULL | 实体类型: board/list/card/member/label/comment |
| entity_id | UUID | NOT NULL | 实体ID |
| entity_title | VARCHAR(200) | | 实体标题（用于显示） |
| changes | JSONB | | 变更详情 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |

**动作类型 (action)：**
- `created`: 创建实体
- `updated`: 更新实体
- `deleted`: 删除实体
- `moved`: 移动卡片/列表
- `assigned`: 分配负责人
- `commented`: 添加评论
- `labeled`: 添加标签
- `completed`: 完成卡片

**索引：**
- `idx_activities_board` ON (board_id, created_at DESC)
- `idx_activities_entity` ON (entity_type, entity_id)

---

### 10. refresh_tokens - 刷新令牌表

存储JWT刷新令牌。

| 字段名 | 类型 | 约束 | 说明 |
|--------|------|------|------|
| id | UUID | PK, NOT NULL | 令牌唯一标识 |
| token | VARCHAR(500) | UNIQUE, NOT NULL | 刷新令牌 |
| user_id | UUID | FK(users.id), NOT NULL | 用户ID |
| expires_at | TIMESTAMP | NOT NULL | 过期时间 |
| created_at | TIMESTAMP | DEFAULT NOW() | 创建时间 |
| revoked_at | TIMESTAMP | | 撤销时间 |

**索引：**
- `idx_refresh_tokens_user` ON (user_id)
- `idx_refresh_tokens_token` ON (token)
- `idx_refresh_tokens_expires` ON (expires_at)

---

## 数据关系总结

### 一对多关系
- `User` → `Board` (一个用户拥有多个看板)
- `User` → `Card` (一个用户可以被分配多个卡片)
- `Board` → `List` (一个看板包含多个列表)
- `Board` → `Label` (一个看板包含多个标签)
- `Board` → `Activity` (一个看板包含多个活动记录)
- `List` → `Card` (一个列表包含多个卡片)
- `Card` → `Comment` (一个卡片包含多个评论)

### 多对多关系
- `User` ↔ `Board` (通过 `board_members` 表)
- `Card` ↔ `Label` (通过 `card_labels` 表)

### 自引用关系
- `Comment` → `Comment` (通过 `parent_id` 实现评论回复)

## 初始化数据

### 默认标签颜色

看板创建时，建议提供以下默认标签：
- #61BD4F - 绿色
- #F2D600 - 黄色
- #FF9F1A - 橙色
- #EB5A46 - 红色
- #C377E0 - 紫色
- #0079BF - 蓝色

### 默认列表

看板创建时，建议创建以下默认列表：
1. 待办 (To Do)
2. 进行中 (In Progress)
3. 已完成 (Done)
