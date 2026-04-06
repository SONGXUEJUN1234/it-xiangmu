---
title: maodun-award
date: 2026-04-06
updated: 2026-04-06
tags:
  - Hugo
  - StaticSite
  - ChineseLiterature
categories:
  - 项目
repo: "https://github.com/SONGXUEJUN1234/maodun-award"
download: "/downloads/maodun-award.zip"
demo: "/apps/maodun-award/"
platform: Web
version: 1.0.0
---

## Overview

茅盾文学奖获奖作品展示网站，采用现代卡片式设计风格，深红+金色配色方案。

## Features

- **响应式布局**：移动端/平板/桌面自适应
- **作品展示**：第十届（2019）和第十一届（2023）共11部获奖作品
- **详细信息**：书名、作者、作者简介、出版社、出版年份、作品简介
- **优雅设计**：深红+金色配色，呼应文学庄重感
- **快速加载**：纯静态网站，秒开体验

## Tech Stack

- **静态网站生成器**: Hugo
- **样式**: 原生 CSS3
- **数据格式**: YAML + Markdown
- **部署**: Vercel

## Demo

[在线预览](/apps/maodun-award/)

## Download

[下载源码](/downloads/maodun-award.zip)

## Quick Start

### 环境要求
- Hugo 0.120+
- 任意浏览器

### 安装运行
\`\`\`bash
# 克隆仓库
git clone https://github.com/SONGXUEJUN1234/maodun-award.git
cd maodun-award

# 启动 Hugo 开发服务器
hugo server -D

# 访问 http://localhost:1313
\`\`\`

### 构建部署
\`\`\`bash
# 构建静态文件
hugo

# 输出在 public/ 目录
\`\`\`
