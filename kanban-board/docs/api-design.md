# 任务看板系统 - API 设计

## 概述

本文档描述任务看板系统的 REST API 接口设计。

## 基础信息

- **Base URL**: `https://api.kanban.example.com/v1`
- **认证方式**: JWT Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

## 通用响应格式

### 成功响应
```json
{
  "success": true,
  "data": { ... }
}
```

### 错误响应
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "错误描述信息",
    "details": { ... }
  }
}
```

### 分页响应
```json
{
  "success": true,
  "data": { ... },
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 100,
    "total_pages": 5
  }
}
```

## 认证接口

### 1. 用户注册

```
POST /auth/register
```

**请求体：**
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "user@example.com",
      "username": "johndoe",
      "full_name": "John Doe",
      "avatar_url": null,
      "created_at": "2024-01-15T10:30:00Z"
    },
    "tokens": {
      "access": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "expires_in": 900
      },
      "refresh": {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "expires_in": 604800
      }
    }
  }
}
```

---

### 2. 用户登录

```
POST /auth/login
```

**请求体：**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "tokens": { ... }
  }
}
```

---

### 3. 刷新令牌

```
POST /auth/refresh
```

**请求体：**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "access": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 900
    }
  }
}
```

---

### 4. 用户登出

```
POST /auth/logout
```

**请求头：**
```
Authorization: Bearer {access_token}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Successfully logged out"
  }
}
```

---

## 用户接口

### 1. 获取当前用户信息

```
GET /users/me
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "username": "johndoe",
    "full_name": "John Doe",
    "avatar_url": null,
    "is_active": true,
    "is_verified": false,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### 2. 更新用户信息

```
PATCH /users/me
```

**请求体：**
```json
{
  "full_name": "John Smith",
  "avatar_url": "https://example.com/avatar.jpg"
}
```

**响应：**
```json
{
  "success": true,
  "data": { ... }
}
```

---

### 3. 修改密码

```
POST /users/me/change-password
```

**请求体：**
```json
{
  "old_password": "OldPass123!",
  "new_password": "NewPass456!"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Password changed successfully"
  }
}
```

---

## 看板接口

### 1. 创建看板

```
POST /boards
```

**请求体：**
```json
{
  "title": "产品开发看板",
  "description": "追踪产品开发进度",
  "background_color": "#0079BF"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "title": "产品开发看板",
    "description": "追踪产品开发进度",
    "owner": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "username": "johndoe",
      "avatar_url": null
    },
    "background_color": "#0079BF",
    "background_url": null,
    "is_public": false,
    "is_archived": false,
    "member_count": 1,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### 2. 获取看板列表

```
GET /boards
```

**查询参数：**
- `page`: 页码（默认：1）
- `page_size`: 每页数量（默认：20，最大：100）
- `archived`: 是否包含归档看板（默认：false）

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "title": "产品开发看板",
      "description": "...",
      "owner": { ... },
      "background_color": "#0079BF",
      "member_count": 5,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

### 3. 获取看板详情

```
GET /boards/{board_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "title": "产品开发看板",
    "description": "追踪产品开发进度",
    "owner": { ... },
    "background_color": "#0079BF",
    "is_public": false,
    "is_archived": false,
    "members": [
      {
        "user": {
          "id": "...",
          "username": "johndoe",
          "full_name": "John Doe",
          "avatar_url": null
        },
        "role": "owner"
      }
    ],
    "lists": [
      {
        "id": "...",
        "title": "待办",
        "position": 0,
        "card_count": 5
      }
    ],
    "labels": [
      {
        "id": "...",
        "name": "紧急",
        "color": "#EB5A46"
      }
    ],
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

---

### 4. 更新看板

```
PATCH /boards/{board_id}
```

**请求体：**
```json
{
  "title": "新标题",
  "description": "更新后的描述",
  "background_color": "#61BD4F",
  "is_public": true
}
```

**响应：**
```json
{
  "success": true,
  "data": { ... }
}
```

---

### 5. 删除看板

```
DELETE /boards/{board_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Board deleted successfully"
  }
}
```

---

### 6. 归档/取消归档看板

```
POST /boards/{board_id}/archive
POST /boards/{board_id}/unarchive
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "is_archived": true
  }
}
```

---

## 看板成员接口

### 1. 添加成员

```
POST /boards/{board_id}/members
```

**请求体：**
```json
{
  "username": "janedoe",
  "role": "admin"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "...",
      "username": "janedoe",
      "full_name": "Jane Doe",
      "avatar_url": null
    },
    "role": "admin",
    "joined_at": "2024-01-15T11:00:00Z"
  }
}
```

---

### 2. 更新成员角色

```
PATCH /boards/{board_id}/members/{user_id}
```

**请求体：**
```json
{
  "role": "member"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "user": { ... },
    "role": "member"
  }
}
```

---

### 3. 移除成员

```
DELETE /boards/{board_id}/members/{user_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Member removed successfully"
  }
}
```

---

## 列表接口

### 1. 创建列表

```
POST /boards/{board_id}/lists
```

**请求体：**
```json
{
  "title": "进行中",
  "position": 1
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "title": "进行中",
    "position": 1,
    "card_count": 0,
    "created_at": "2024-01-15T10:35:00Z"
  }
}
```

---

### 2. 更新列表

```
PATCH /lists/{list_id}
```

**请求体：**
```json
{
  "title": "开发中",
  "position": 2
}
```

**响应：**
```json
{
  "success": true,
  "data": { ... }
}
```

---

### 3. 删除列表

```
DELETE /lists/{list_id}
```

**查询参数：**
- `move_cards_to`: 目标列表ID（可选，用于移动该列表下的卡片）

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "List deleted successfully"
  }
}
```

---

## 卡片接口

### 1. 创建卡片

```
POST /lists/{list_id}/cards
```

**请求体：**
```json
{
  "title": "实现用户认证功能",
  "description": "使用JWT实现用户认证",
  "position": 0,
  "priority": "high",
  "due_date": "2024-02-01T18:00:00Z",
  "label_ids": ["label-id-1", "label-id-2"]
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "title": "实现用户认证功能",
    "description": "使用JWT实现用户认证",
    "list_id": "...",
    "position": 0,
    "assignee": null,
    "priority": "high",
    "due_date": "2024-02-01T18:00:00Z",
    "labels": [
      {
        "id": "...",
        "name": "紧急",
        "color": "#EB5A46"
      }
    ],
    "comment_count": 0,
    "attachment_count": 0,
    "is_completed": false,
    "created_at": "2024-01-15T10:40:00Z"
  }
}
```

---

### 2. 获取卡片详情

```
GET /cards/{card_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "title": "实现用户认证功能",
    "description": "使用JWT实现用户认证",
    "list": {
      "id": "...",
      "title": "待办"
    },
    "board": {
      "id": "...",
      "title": "产品开发看板"
    },
    "position": 0,
    "assignee": {
      "id": "...",
      "username": "johndoe",
      "avatar_url": null
    },
    "priority": "high",
    "due_date": "2024-02-01T18:00:00Z",
    "labels": [ ... ],
    "is_completed": false,
    "created_at": "2024-01-15T10:40:00Z",
    "updated_at": "2024-01-15T10:40:00Z"
  }
}
```

---

### 3. 更新卡片

```
PATCH /cards/{card_id}
```

**请求体：**
```json
{
  "title": "实现JWT用户认证",
  "description": "新的描述",
  "priority": "critical",
  "assignee_id": "...",
  "due_date": "2024-02-05T18:00:00Z",
  "is_completed": false
}
```

**响应：**
```json
{
  "success": true,
  "data": { ... }
}
```

---

### 4. 移动卡片

```
POST /cards/{card_id}/move
```

**请求体：**
```json
{
  "list_id": "target-list-id",
  "position": 0
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "list_id": "target-list-id",
    "position": 0
  }
}
```

---

### 5. 删除卡片

```
DELETE /cards/{card_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Card deleted successfully"
  }
}
```

---

## 标签接口

### 1. 创建标签

```
POST /boards/{board_id}/labels
```

**请求体：**
```json
{
  "name": "前端",
  "color": "#0079BF"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "name": "前端",
    "color": "#0079BF"
  }
}
```

---

### 2. 更新标签

```
PATCH /labels/{label_id}
```

**请求体：**
```json
{
  "name": "后端开发",
  "color": "#61BD4F"
}
```

**响应：**
```json
{
  "success": true,
  "data": { ... }
}
```

---

### 3. 删除标签

```
DELETE /labels/{label_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Label deleted successfully"
  }
}
```

---

### 4. 为卡片添加标签

```
POST /cards/{card_id}/labels
```

**请求体：**
```json
{
  "label_id": "label-id-1"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "card_id": "...",
    "label": { ... }
  }
}
```

---

### 5. 从卡片移除标签

```
DELETE /cards/{card_id}/labels/{label_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Label removed from card"
  }
}
```

---

## 评论接口

### 1. 获取卡片评论

```
GET /cards/{card_id}/comments
```

**查询参数：**
- `page`: 页码（默认：1）
- `page_size`: 每页数量（默认：20）

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "content": "这个任务进展如何？",
      "user": {
        "id": "...",
        "username": "johndoe",
        "avatar_url": null
      },
      "parent_id": null,
      "is_edited": false,
      "created_at": "2024-01-15T11:00:00Z",
      "updated_at": "2024-01-15T11:00:00Z",
      "replies": []
    }
  ],
  "pagination": { ... }
}
```

---

### 2. 创建评论

```
POST /cards/{card_id}/comments
```

**请求体：**
```json
{
  "content": "这个任务进展如何？",
  "parent_id": null
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "content": "这个任务进展如何？",
    "user": { ... },
    "parent_id": null,
    "is_edited": false,
    "created_at": "2024-01-15T11:00:00Z"
  }
}
```

---

### 3. 更新评论

```
PATCH /comments/{comment_id}
```

**请求体：**
```json
{
  "content": "更新后的评论内容"
}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "...",
    "content": "更新后的评论内容",
    "is_edited": true,
    "updated_at": "2024-01-15T11:30:00Z"
  }
}
```

---

### 4. 删除评论

```
DELETE /comments/{comment_id}
```

**响应：**
```json
{
  "success": true,
  "data": {
    "message": "Comment deleted successfully"
  }
}
```

---

## 活动日志接口

### 1. 获取看板活动

```
GET /boards/{board_id}/activities
```

**查询参数：**
- `page`: 页码（默认：1）
- `page_size`: 每页数量（默认：20）

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "user": {
        "id": "...",
        "username": "johndoe",
        "avatar_url": null
      },
      "action": "created",
      "entity_type": "card",
      "entity_id": "...",
      "entity_title": "实现用户认证功能",
      "changes": null,
      "created_at": "2024-01-15T11:00:00Z"
    },
    {
      "id": "...",
      "user": { ... },
      "action": "assigned",
      "entity_type": "card",
      "entity_id": "...",
      "entity_title": "实现用户认证功能",
      "changes": {
        "assignee": {
          "from": null,
          "to": {
            "id": "...",
            "username": "janedoe"
          }
        }
      },
      "created_at": "2024-01-15T11:05:00Z"
    }
  ],
  "pagination": { ... }
}
```

---

## 搜索接口

### 1. 搜索卡片

```
GET /boards/{board_id}/search
```

**查询参数：**
- `q`: 搜索关键词
- `labels`: 标签ID列表（逗号分隔）
- `assignee`: 负责人ID
- `priority`: 优先级（low/medium/high/critical）
- `due_before`: 截止日期之前（ISO 8601）
- `is_completed`: 是否完成

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "...",
      "title": "实现用户认证功能",
      "list": {
        "id": "...",
        "title": "待办"
      },
      "assignee": { ... },
      "priority": "high",
      "due_date": "2024-02-01T18:00:00Z",
      "labels": [ ... ],
      "is_completed": false
    }
  ]
}
```

---

## 错误码参考

| 错误码 | HTTP状态 | 说明 |
|--------|----------|------|
| AUTH_INVALID_CREDENTIALS | 401 | 无效的登录凭据 |
| AUTH_TOKEN_EXPIRED | 401 | 令牌已过期 |
| AUTH_INVALID_TOKEN | 401 | 无效的令牌 |
| PERMISSION_DENIED | 403 | 权限不足 |
| RESOURCE_NOT_FOUND | 404 | 资源不存在 |
| VALIDATION_ERROR | 400 | 请求参数验证失败 |
| DUPLICATE_RESOURCE | 409 | 资源重复（如邮箱已注册） |
| INTERNAL_SERVER_ERROR | 500 | 服务器内部错误 |

---

## WebSocket 接口（可选）

### 连接

```
wss://api.kanban.example.com/v1/ws?token={jwt_token}
```

### 事件类型

**客户端 → 服务器：**
- `subscribe:board` - 订阅看板更新
- `unsubscribe:board` - 取消订阅

**服务器 → 客户端：**
- `card:created` - 卡片创建
- `card:updated` - 卡片更新
- `card:moved` - 卡片移动
- `card:deleted` - 卡片删除
- `comment:created` - 评论创建
- `member:added` - 成员加入
- `activity:logged` - 新活动记录

### 事件示例

```json
{
  "type": "card:updated",
  "board_id": "...",
  "data": {
    "card": { ... },
    "changes": {
      "title": {
        "from": "旧标题",
        "to": "新标题"
      }
    }
  }
}
```
