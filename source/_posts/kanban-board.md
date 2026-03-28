---
title: kanban-board
date: 2026-03-28
updated: 2026-03-28
tags:
  - TaskManagement
  - Collaboration
  - FastAPI
  - React
categories:
  - 项目
repo: ""
download: "/downloads/kanban-board.zip"
demo: "/apps/kanban-board/"
platform: Web
version: 1.0.0
---

## Overview

任务看板系统 (Kanban Board) - 一个类似 Trello 的任务看板系统，支持多人协作、任务管理、实时更新等功能。

## Features

- **用户认证**：注册、登录、JWT 令牌认证
- **看板管理**：创建、编辑、删除看板，支持多人协作
- **任务列表**：在看板内创建自定义列表（如：待办、进行中、已完成）
- **任务卡片**：标题、描述、优先级、截止日期、负责人、标签分类
- **评论系统**：卡片评论、回复
- **活动日志**：追踪所有操作记录
- **实时更新**：WebSocket 支持实时同步
- **搜索功能**：按关键词、标签、负责人等条件搜索

## Tech Stack

### 后端
- FastAPI + SQLAlchemy 2.0
- PostgreSQL 数据库
- JWT 认证
- Socket.IO 实时通信

### 前端
- React 18 + TypeScript
- Zustand 状态管理
- shadcn/ui 组件库
- dnd-kit 拖拽功能

## Demo

[项目说明](/apps/kanban-board/)

## Download

[下载源码](/downloads/kanban-board.zip)

## Quick Start

### 环境要求
- Python 3.11+
- PostgreSQL 16+
- Node.js 18+

### 后端安装
\`\`\`bash
cd kanban-board/backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 配置数据库连接
alembic upgrade head
uvicorn app.main:app --reload --port 8000
\`\`\`

### 前端安装
\`\`\`bash
cd kanban-board/frontend
npm install
npm run dev
\`\`\`

## Usage

1. 访问 http://localhost:8000/docs 查看 API 文档
2. 注册账号并登录
3. 创建看板和列表
4. 添加任务卡片并拖拽管理
