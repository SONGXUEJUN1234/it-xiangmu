---
title: glass-price-monitor
date: 2026-05-09
updated: 2026-05-09
tags:
  - Tool
  - Monitoring
  - Next.js
  - Dashboard
categories:
  - Projects
repo: "https://github.com/SONGXUEJUN1234/glass-price-monitor"
download: ""
demo: "/apps/glass-price-monitor/"
platform: Web
version: 1.0.0
---

## Overview

玻璃原料价格监控系统是一款实时监控玻璃生产主要原料（纯碱、天然气、电力、锂长石、方解石等）价格变动的专业工具，帮助玻璃制造企业及时掌握原料市场动态。

## Features

- **多原料价格监控**：覆盖玻璃生产主要原料（纯碱、天然气、电力、锂长石、方解石等）
- **实时数据展示**：卡片式布局清晰展示各原料当前价格和涨跌幅
- **行业资讯信息流**：集成相关行业新闻和市场动态
- **本地数据存储**：基于 JSON 文件的数据存储（可扩展至 Supabase）
- **响应式设计**：支持桌面和移动设备访问

## Use Cases

- 玻璃制造企业原料采购决策
- 原料价格趋势分析
- 行业市场动态监控
- 成本控制与预算规划

## Technical Details

- **前端框架**：Next.js 15 + React 19 + TypeScript
- **UI组件**：Tailwind CSS + shadcn/ui
- **数据存储**：本地 JSON 文件（可扩展至 Supabase）
- **部署方式**：Vercel（免费托管）

## Data Sources

系统支持多种数据来源：

| 类型 | 来源 | 覆盖原料 |
|------|------|----------|
| 期货交易所 | 郑商所、上期所 | 纯碱、天然气 |
| 行业网站 | 百川盈孚、卓创资讯 | 全部 |
| B2B平台 | 1688、慧聪网 | 全部 |
| 政府机构 | 发改委 | 能源价格 |

## Demo

[在线体验](/apps/glass-price-monitor/)

## Source Code

源码已托管在 GitHub：[glass-price-monitor](https://github.com/SONGXUEJUN1234/glass-price-monitor)

## Installation & Usage

1. 解压下载的源码包
2. 安装依赖：`npm install`
3. 启动开发服务器：`npm run dev`
4. 访问 http://localhost:3000

## Development Status

### 已实现
- ✅ 原料价格展示卡片
- ✅ 行业资讯信息流
- ✅ 数据存储和读取

### 待实现
- ⏳ 数据抓取器（期货交易所、行业网站）
- ⏳ 供应商管理
- ⏳ 价格告警
- ⏳ 数据可视化图表
- ⏳ 定时任务

## License

MIT
