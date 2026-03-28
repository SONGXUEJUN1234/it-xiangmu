.PHONY: help install dev test lint format clean migrate shell db-up db-down

# ============================================
# 默认目标 - 显示帮助
# ============================================
help:
	@echo "任务看板系统 - 可用命令:"
	@echo ""
	@echo "  install     - 安装依赖"
	@echo "  dev         - 启动开发服务器"
	@echo "  test        - 运行测试"
	@echo "  test-cov    - 运行测试并生成覆盖率报告"
	@echo "  lint        - 代码检查"
	@echo "  format      - 格式化代码"
	@echo "  clean       - 清理临时文件"
	@echo "  migrate     - 运行数据库迁移"
	@echo "  migration   - 创建新的数据库迁移 (需要 MSG 参数)"
	@echo "  shell       - 进入 Python shell"
	@echo "  db-up       - 启动数据库 (Docker)"
	@echo "  db-down     - 停止数据库 (Docker)"
	@echo ""
	@echo "示例:"
	@echo "  make install"
	@echo "  make dev"
	@echo "  make migration MSG=add_user_table"

# ============================================
# 安装
# ============================================
install:
	@echo "安装 Python 依赖..."
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "安装 pre-commit 钩子..."
	. venv/bin/activate && pre-commit install
	@echo "完成！"

# ============================================
# 开发
# ============================================
dev:
	@echo "启动开发服务器..."
	. venv/bin/activate && uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

# ============================================
# 测试
# ============================================
test:
	@echo "运行测试..."
	. venv/bin/activate && pytest backend/tests -v

test-cov:
	@echo "运行测试并生成覆盖率报告..."
	. venv/bin/activate && pytest backend/tests --cov=backend/app --cov-report=html --cov-report=term
	@echo "覆盖率报告: htmlcov/index.html"

# ============================================
# 代码质量
# ============================================
lint:
	@echo "运行代码检查..."
	. venv/bin/activate && ruff check backend/
	. venv/bin/activate && mypy backend/app

format:
	@echo "格式化代码..."
	. venv/bin/activate && ruff format backend/
	. venv/bin/activate && ruff check --fix backend/

# ============================================
# 数据库
# ============================================
migrate:
	@echo "运行数据库迁移..."
	. venv/bin/activate && alembic upgrade head

migration:
	@echo "创建新的数据库迁移..."
	. venv/bin/activate && alembic revision --autogenerate -m "$(MSG)"

rollback:
	@echo "回滚最后一次迁移..."
	. venv/bin/activate && alembic downgrade -1

# ============================================
# 工具
# ============================================
shell:
	@echo "启动 Python shell..."
	. venv/bin/activate && python -i -c "from backend.app.core.database import SessionLocal; from backend.app.models import *; db = SessionLocal(); print('Database session: db')"

clean:
	@echo "清理临时文件..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*.pyd' -delete
	find . -type f -name '.DS_Store' -delete
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage .mypy_cache .ruff_cache
	@echo "清理完成"

# ============================================
# Docker 数据库
# ============================================
db-up:
	@echo "启动 PostgreSQL 和 Redis..."
	docker-compose -f docker-compose.dev.yml up -d postgres redis

db-down:
	@echo "停止数据库服务..."
	docker-compose -f docker-compose.dev.yml down

db-logs:
	docker-compose -f docker-compose.dev.yml logs -f postgres redis

# ============================================
# 生产构建
# ============================================
build:
	@echo "构建 Docker 镜像..."
	docker build -t kanban-backend:latest -f backend/Dockerfile backend/
