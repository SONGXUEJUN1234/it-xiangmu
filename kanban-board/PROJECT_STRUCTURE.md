# 项目结构说明

## 目录树

```
kanban-board/
├── backend/                          # 后端代码
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI 应用入口
│   │   │
│   │   ├── api/                      # API 层
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # 依赖注入 (数据库、认证)
│   │   │   └── endpoints/            # API 路由模块
│   │   │       ├── __init__.py
│   │   │       ├── auth.py           # 认证相关
│   │   │       ├── users.py          # 用户管理
│   │   │       ├── boards.py         # 看板管理
│   │   │       ├── lists.py          # 列表管理
│   │   │       ├── cards.py          # 卡片管理
│   │   │       ├── comments.py       # 评论管理
│   │   │       ├── labels.py         # 标签管理
│   │   │       └── activities.py     # 活动日志
│   │   │
│   │   ├── core/                     # 核心配置
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # 配置管理 (Pydantic Settings)
│   │   │   ├── security.py           # JWT、密码处理
│   │   │   ├── database.py           # 数据库连接
│   │   │   └── logger.py             # 日志配置
│   │   │
│   │   ├── models/                   # SQLAlchemy ORM 模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── board.py
│   │   │   ├── list.py
│   │   │   ├── card.py
│   │   │   ├── label.py
│   │   │   ├── comment.py
│   │   │   └── activity.py
│   │   │
│   │   ├── schemas/                  # Pydantic 模式 (请求/响应)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── board.py
│   │   │   ├── list.py
│   │   │   ├── card.py
│   │   │   ├── label.py
│   │   │   ├── comment.py
│   │   │   ├── activity.py
│   │   │   └── common.py             # 通用响应模式
│   │   │
│   │   ├── services/                 # 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── board_service.py
│   │   │   ├── card_service.py
│   │   │   └── activity_service.py
│   │   │
│   │   └── utils/                    # 工具函数
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── tests/                        # 测试代码
│   │   ├── __init__.py
│   │   ├── conftest.py               # pytest 配置和 fixtures
│   │   ├── unit/                     # 单元测试
│   │   └── integration/              # 集成测试
│   │
│   ├── alembic/                      # 数据库迁移
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/                 # 迁移版本文件
│   │
│   ├── Dockerfile                    # 生产环境 Docker 镜像
│   └── pyproject.toml                # Python 项目配置
│
├── frontend/                         # 前端代码
│   ├── src/
│   │   ├── components/               # React 组件
│   │   │   ├── common/               # 通用组件
│   │   │   ├── board/                # 看板相关组件
│   │   │   ├── card/                 # 卡片相关组件
│   │   │   └── auth/                 # 认证相关组件
│   │   │
│   │   ├── pages/                    # 页面组件
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── BoardPage.tsx
│   │   │   └── CardDetailModal.tsx
│   │   │
│   │   ├── services/                 # API 服务
│   │   │   ├── api.ts                # API 客户端配置
│   │   │   ├── auth.ts
│   │   │   ├── boards.ts
│   │   │   ├── cards.ts
│   │   │   └── socket.ts             # WebSocket 连接
│   │   │
│   │   ├── hooks/                    # 自定义 Hooks
│   │   │   ├── useAuth.ts
│   │   │   ├── useBoard.ts
│   │   │   └── useWebSocket.ts
│   │   │
│   │   ├── store/                    # 状态管理 (Zustand)
│   │   │   ├── authStore.ts
│   │   │   ├── boardStore.ts
│   │   │   └── uiStore.ts
│   │   │
│   │   ├── types/                    # TypeScript 类型
│   │   │   ├── models.ts
│   │   │   └── api.ts
│   │   │
│   │   ├── styles/                   # 样式文件
│   │   ├── utils/                    # 工具函数
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── public/                       # 静态资源
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── docs/                             # 文档
│   ├── database-design.md            # 数据库设计
│   ├── api-design.md                 # API 设计
│   └── tech-stack.md                 # 技术选型
│
├── scripts/                          # 脚本工具
│   ├── init_db.py                    # 初始化数据库
│   └── seed_data.py                  # 填充测试数据
│
├── .env.example                      # 环境变量示例
├── .gitignore                        # Git 忽略文件
├── .pre-commit-config.yaml           # Pre-commit 钩子配置
├── docker-compose.dev.yml            # 开发环境 Docker Compose
├── Makefile                          # 开发命令快捷方式
├── pyproject.toml                    # 项目配置 (ruff, mypy, pytest)
├── requirements.txt                  # Python 依赖
└── README.md                         # 项目说明
```

## 开发流程

### 1. 首次设置

```bash
# 启动数据库
make db-up

# 安装依赖
make install

# 复制环境变量
cp .env.example .env

# 运行迁移
make migrate

# 启动开发服务器
make dev
```

### 2. 添加新功能

```bash
# 创建新功能分支
git checkout -b feature/new-feature

# 编辑代码...

# 格式化和检查
make format
make lint

# 运行测试
make test

# 提交代码
git add .
git commit -m "feat: add new feature"
```

### 3. 数据库变更

```bash
# 修改 models/ 中的模型后

# 创建迁移
make migration MSG="add_new_column"

# 检查生成的迁移文件
# 编辑 alembic/versions/xxx_add_new_column.py

# 应用迁移
make migrate
```

### 4. 添加新 API 端点

1. 在 `backend/app/schemas/` 定义请求/响应模式
2. 在 `backend/app/services/` 实现业务逻辑
3. 在 `backend/app/api/endpoints/` 添加路由
4. 在 `backend/app/api/deps.py` 添加依赖（如需要）
5. 在 `backend/app/main.py` 注册路由
6. 编写测试

## 文件说明

### 核心配置文件

| 文件 | 说明 |
|------|------|
| `.env` | 环境变量配置（不提交到版本控制） |
| `pyproject.toml` | Ruff、Black、MyPy、Pytest 配置 |
| `.pre-commit-config.yaml` | Git 提交前自动检查 |
| `Makefile` | 常用开发命令快捷方式 |
| `docker-compose.dev.yml` | 本地开发数据库 |

### 后端关键文件

| 文件 | 说明 |
|------|------|
| `backend/app/main.py` | FastAPI 应用入口、中间件、路由注册 |
| `backend/app/core/config.py` | 从环境变量加载配置 |
| `backend/app/core/security.py` | JWT 和密码处理 |
| `backend/app/core/database.py` | 数据库连接池和 Session |
| `backend/app/api/deps.py` | 依赖注入（获取当前用户、数据库 Session） |
| `backend/alembic/env.py` | Alembic 迁移环境配置 |

### 开发工具命令

| 命令 | 说明 |
|------|------|
| `make dev` | 启动开发服务器 (http://localhost:8000) |
| `make test` | 运行测试 |
| `make lint` | 代码检查 |
| `make format` | 代码格式化 |
| `make migrate` | 应用数据库迁移 |
| `make shell` | Python 交互式 Shell |

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 数据库管理

### 使用 pgAdmin

```bash
# 启动 pgAdmin
docker-compose -f docker-compose.dev.yml --profile tools up -d
```

访问 http://localhost:5050，使用以下凭据：
- Email: admin@kanban.local
- Password: admin

### 使用 Redis Commander

```bash
# 启动 Redis Commander
docker-compose -f docker-compose.dev.yml --profile tools up -d
```

访问 http://localhost:8081

## 下一步

1. **后端开发**
   - 实现认证系统
   - 实现看板 CRUD
   - 实现卡片和列表
   - 实现 WebSocket

2. **前端开发**
   - 搭建 React + Vite 项目
   - 实现认证页面
   - 实现看板拖拽界面
   - 集成 WebSocket

3. **部署**
   - 配置 CI/CD
   - 设置生产数据库
   - 配置 Nginx 反向代理
