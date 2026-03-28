# 任务看板系统 (Kanban Board)

一个类似 Trello 的任务看板系统，支持多人协作、任务管理、实时更新等功能。

## 功能特性

- **用户认证**：注册、登录、JWT 令牌认证
- **看板管理**：创建、编辑、删除看板，支持多人协作
- **任务列表**：在看板内创建自定义列表（如：待办、进行中、已完成）
- **任务卡片**：
  - 标题、描述、优先级
  - 截止日期、负责人
  - 标签分类
- **评论系统**：卡片评论、回复
- **活动日志**：追踪所有操作记录
- **实时更新**：WebSocket 支持实时同步
- **搜索功能**：按关键词、标签、负责人等条件搜索

## 技术栈

### 后端
- **框架**：FastAPI
- **数据库**：PostgreSQL
- **ORM**：SQLAlchemy 2.0
- **认证**：JWT (python-jose)
- **WebSocket**：Socket.IO
- **数据验证**：Pydantic

### 前端（建议）
- **框架**：React 18 + TypeScript
- **状态管理**：Zustand
- **UI 组件**：shadcn/ui
- **拖拽**：dnd-kit
- **实时通信**：Socket.IO Client

## 项目结构

```
kanban-board/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py         # 依赖注入
│   │   │   └── endpoints/      # API 路由
│   │   ├── core/
│   │   │   ├── config.py       # 配置管理
│   │   │   ├── security.py     # JWT/密码处理
│   │   │   └── logger.py       # 日志配置
│   │   ├── models/             # SQLAlchemy 模型
│   │   ├── schemas/            # Pydantic 模式
│   │   ├── services/           # 业务逻辑
│   │   └── utils/              # 工具函数
│   ├── tests/                  # 测试文件
│   └── alembic/                # 数据库迁移
├── docs/
│   ├── database-design.md      # 数据库设计
│   ├── api-design.md           # API 设计
│   └── tech-stack.md           # 技术选型
├── frontend/
│   └── src/
│       ├── components/         # React 组件
│       ├── pages/              # 页面组件
│       ├── services/           # API 服务
│       ├── hooks/              # 自定义 Hooks
│       ├── types/              # TypeScript 类型
│       └── store/              # 状态管理
├── scripts/                    # 脚本工具
├── requirements.txt            # Python 依赖
└── README.md
```

## 快速开始

### 环境要求

- Python 3.11+
- PostgreSQL 16+
- Redis 7+ (可选，用于 Socket.IO)

### 后端安装

```bash
# 克隆项目
git clone <repository-url>
cd kanban-board

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp .env.example .env

# 编辑 .env 文件，配置数据库连接
# vim .env

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

### 环境变量

```bash
# 应用配置
APP_NAME=Kanban Board
APP_VERSION=1.0.0
DEBUG=True
API_V1_PREFIX=/api/v1

# 数据库
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/kanban

# JWT 密钥
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Redis (可选)
REDIS_URL=redis://localhost:6379/0
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

详细 API 设计请查看 [docs/api-design.md](docs/api-design.md)

## 数据库设计

完整的数据库设计文档请查看 [docs/database-design.md](docs/database-design.md)

## 开发

### 代码格式化

```bash
# 格式化代码
black backend/
isort backend/

# 代码检查
ruff check backend/
mypy backend/
```

### 运行测试

```bash
# 运行所有测试
pytest

# 带覆盖率报告
pytest --cov=backend/app --cov-report=html
```

### 数据库迁移

```bash
# 创建新迁移
alembic revision --autogenerate -m "描述信息"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t kanban-backend ./backend

# 运行容器
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql+asyncpg://... \
  -e SECRET_KEY=your-secret \
  kanban-backend
```

### 生产环境建议

- 使用 Gunicorn + Uvicorn Workers
- 配置 Nginx 作为反向代理
- 启用 HTTPS
- 配置 Redis 作为会话存储
- 设置定期数据库备份

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

- 项目主页：[GitHub Repository]
- 问题反馈：[Issues]
