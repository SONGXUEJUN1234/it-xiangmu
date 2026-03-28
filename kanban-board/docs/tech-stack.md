# 任务看板系统 - 技术选型文档

## 概述

本文档说明任务看板系统的技术选型决策和理由。

---

## 后端技术栈

### 1. Web 框架: FastAPI

**选择理由：**

- **现代化设计**：基于 Python 3.8+ 类型提示，提供优秀的编辑器支持和自动补全
- **高性能**：基于 Starlette 和 Pydantic，异步性能接近 NodeJS 和 Go
- **自动文档**：自动生成交互式 API 文档（Swagger UI 和 ReDoc）
- **验证**：Pydantic 提供强大的请求/响应数据验证
- **异步支持**：原生支持 async/await，适合高并发场景
- **标准兼容**：完全遵循 OpenAPI 3.0 规范

**替代方案对比：**

| 框架 | 优点 | 缺点 | 选择理由 |
|------|------|------|----------|
| Flask | 轻量、灵活 | 需要手动集成很多组件 | FastAPI 提供更现代的开发体验 |
| Django | 功能完整、ORM强大 | 过于重量级，模板引擎用不上 | 看板系统是 API 项目，不需要 Django 的全栈功能 |
| FastAPI | 异步、自动文档、类型提示 | 相对较新 | **最佳选择** |

---

### 2. ORM: SQLAlchemy 2.0

**选择理由：**

- **成熟稳定**：Python 生态最成熟的 ORM
- **2.0 版本**：支持异步操作，语法更简洁
- **灵活性**：支持 Core 和 ORM 两种模式，可根据需求选择
- **数据库无关**：支持 PostgreSQL, MySQL, SQLite 等多种数据库
- **强大查询**：支持复杂查询、关系加载、事务管理等

**替代方案对比：**

| ORM | 优点 | 缺点 | 选择理由 |
|-----|------|------|----------|
| Tortoise ORM | 异步原生、类似 Django ORM | 生态较小、文档较少 | SQLAlchemy 2.0 已支持异步 |
| SQLModel | 基于 Pydantic、类型友好 | 功能不如 SQLAlchemy 完整 | **选择 SQLAlchemy** |

---

### 3. 数据库: PostgreSQL

**选择理由：**

- **JSONB 支持**：原生支持 JSON 类型，适合存储活动日志的 changes 字段
- **全文搜索**：内置全文搜索功能
- **数据完整性**：严格的数据类型和约束
- **并发性能**：MVCC 机制支持高并发
- **扩展性**：支持丰富的扩展（如 PostGIS、pg_trgm）
- **可靠性**：ACID 完全支持，适合企业级应用

**替代方案对比：**

| 数据库 | 优点 | 缺点 | 选择理由 |
|--------|------|------|----------|
| MySQL | 广泛使用 | JSON 功能较弱 | PostgreSQL 的 JSONB 更适合 |
| MongoDB | 灵活的 Schema | 缺乏事务一致性 | 看板系统需要严格的关系模型 |
| SQLite | 零配置 | 不支持高并发 | **选择 PostgreSQL** |

---

### 4. 认证: JWT (JSON Web Tokens)

**选择理由：**

- **无状态**：服务器不需要存储会话，便于水平扩展
- **跨域友好**：适合前后端分离架构
- **安全性**：可以设置过期时间，支持刷新令牌机制
- **标准**：广泛使用的行业标准

**实现库：**
- `python-jose[cryptography]`: JWT 编解码
- `passlib[bcrypt]`: 密码哈希
- `bcrypt`: 加密算法

---

### 5. 数据验证: Pydantic

**选择理由：**

- **类型安全**：基于 Python 类型提示
- **自动验证**：自动验证请求体和响应
- **清晰错误**：提供详细的验证错误信息
- **与 FastAPI 深度集成**：FastAPI 内置使用

---

### 6. 数据库迁移: Alembic

**选择理由：**

- **SQLAlchemy 官方工具**：完美集成
- **版本控制**：完整的迁移历史管理
- **自动生成**：可自动从模型生成迁移脚本
- **回滚支持**：支持迁移回滚

---

### 7. CORS 处理: python-multipart

**选择理由：**
- FastAPI 官方推荐
- 支持文件上传
- 表单数据处理

---

### 8. 开发工具

| 工具 | 用途 | 说明 |
|------|------|------|
| pytest | 测试框架 | 异步测试支持 |
| pytest-asyncio | 异步测试 | pytest 插件 |
| httpx | HTTP 客户端 | 异步请求，用于测试 |
| ruff | 代码检查 | 快速的 Python linter |
| mypy | 类型检查 | 静态类型检查 |
| black | 代码格式化 | 统一代码风格 |
| pre-commit | Git 钩子 | 提交前自动检查 |

---

## 前端技术栈建议

### 1. 框架: React 18

**选择理由：**

- **生态成熟**：组件库丰富
- **TypeScript 支持**：优秀的类型推导
- **Concurrent Mode**：更好的性能和用户体验
- **Hooks**：简洁的状态管理

**替代方案：**
- **Vue 3**：更简单易学，但生态略逊于 React
- **Svelte**：编译时框架，但生态较小

---

### 2. 状态管理: Zustand

**选择理由：**

- **轻量简洁**：相比 Redux 更简单
- **TypeScript 友好**：无需额外配置
- **无样板代码**：直接编写状态逻辑

---

### 3. 数据请求: TanStack Query (React Query)

**选择理由：**

- **缓存管理**：自动缓存和重新验证
- **乐观更新**：更好的用户体验
- **分页支持**：内置分页功能

---

### 4. UI 组件库: shadcn/ui

**选择理由：**

- **可定制**：组件代码复制到项目中，完全控制
- **基于 Radix UI**：无障碍访问支持
- **Tailwind CSS**：样式一致性好

**替代方案：**
- **Material-UI**：功能完整但定制困难
- **Ant Design**：企业级但设计语言固定

---

### 5. 拖拽库: dnd-kit

**选择理由：**

- **现代化**：基于 React Hooks
- **性能优秀**：比 react-dnd 更轻量
- **无障碍访问**：内置支持
- **移动端友好**：支持触摸操作

---

### 6. 路由: React Router v6

**选择理由：**

- **标准方案**：React 路由事实标准
- **嵌套路由**：支持布局嵌套
- **数据加载**：内置 loader/action 模式

---

### 7. 实时通信: Socket.IO

**选择理由：**

- **自动重连**：断线自动重连
- **房间机制**：方便实现多看板订阅
- **跨浏览器**：降级支持

**后端对应：** `python-socketio`

---

## DevOps 建议

### 1. 容器化: Docker

```dockerfile
# 多阶段构建
FROM python:3.11-slim as builder
...

# 运行时镜像
FROM python:3.11-slim
...
```

### 2. 容器编排: Docker Compose

```yaml
services:
  app:
    build: ./backend
  postgres:
    image: postgres:16-alpine
  redis:
    image: redis:7-alpine
```

### 3. CI/CD: GitHub Actions

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest
```

### 4. 监控: Prometheus + Grafana

- **Prometheus**：指标收集
- **Grafana**：可视化仪表盘

### 5. 日志: 结构化日志

```python
import structlog

logger = structlog.get_logger()
logger.info("card_created", card_id=card.id, user_id=user.id)
```

---

## 部署建议

### 1. 反向代理: Nginx

```nginx
location /api {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

location /ws {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### 2. 应用服务器: Uvicorn + Gunicorn

```bash
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

### 3. 云服务选项

| 提供商 | 服务 | 说明 |
|--------|------|------|
| AWS | ECS + RDS | 企业级解决方案 |
| Railway | 全栈托管 | 快速部署，适合小团队 |
| Fly.io | 边缘部署 | 全球分布 |
| DigitalOcean | App Platform | 简单易用 |

---

## 安全建议

1. **HTTPS 强制**：生产环境必须使用 HTTPS
2. **CORS 限制**：仅允许可信域名
3. **速率限制**：防止 API 滥用
4. **输入验证**：所有输入必须验证
5. **SQL 注入防护**：使用参数化查询
6. **XSS 防护**：前端输出转义
7. **CSRF 保护**：状态变更操作验证
8. **密钥管理**：使用环境变量或密钥管理服务

---

## 性能优化

1. **数据库索引**：为常用查询添加索引
2. **查询优化**：使用 select_related/prefetch_related
3. **缓存**：Redis 缓存热点数据
4. **分页**：大量数据使用游标分页
5. **CDN**：静态资源使用 CDN
6. **前端代码分割**：路由级别懒加载
