# ai-weekly-site 操作手册（外部项目接入 / 打包 / 推送 / 部署）

## 1. 项目定位
- 仓库目录：`D:\GITHUB\TEST\ai-weekly-site`
- 当前远程：`origin = https://github.com/SONGXUEJUN1234/it-xiangmu.git`
- 站点类型：Hexo（静态站）

## 2. 外部项目接入标准结构
将一个外部项目（例如 `expfood-mvp`）接入本站时，统一放到这 4 个位置：

1. 体验页（可在线打开）：
- `source/apps/<slug>/index.html`

2. 源码压缩包（供下载）：
- `source/downloads/<slug>.zip`（推荐 zip）
- 或 `source/downloads/<slug>.tar.gz`

3. 项目文章（用于分类和归档）：
- `source/_posts/<slug>.md`

4. 项目列表入口（手动加一行链接）：
- `source/projects/index.md`

`<slug>` 示例：`expfood-mvp`

## 3. 从外部目录打包到本站（WSL 推荐）

### 3.1 在 WSL 打包
```bash
cd /home/erp17
# 推荐 zip（Windows 兼容最好）
zip -r /tmp/expfood-mvp.zip expfood-mvp

# 如果没有 zip 命令，可用 tar.gz
# tar -czf /tmp/expfood-mvp.tar.gz expfood-mvp
```

### 3.2 复制到 Windows 后放入站点
```bash
# 复制到 Windows 下载目录
cp /tmp/expfood-mvp.zip /mnt/c/Users/<Windows用户名>/Downloads/
```

然后在 PowerShell 执行：
```powershell
Copy-Item "C:\Users\<Windows用户名>\Downloads\expfood-mvp.zip" \
  "D:\GITHUB\TEST\ai-weekly-site\source\downloads\expfood-mvp.zip" -Force
```

## 4. 接入页面与文章

### 4.1 新增在线体验页
创建文件：`source/apps/expfood-mvp/index.html`
- 放可直接静态打开的前端文件（不要依赖后端私网服务）。

### 4.2 新增项目文章
创建文件：`source/_posts/expfood-mvp.md`

模板：
```md
---
title: expfood-mvp
date: 2026-02-27
updated: 2026-02-27
tags:
  - Tool
categories:
  - Projects
repo: ""
download: "/downloads/expfood-mvp.zip"
demo: "/apps/expfood-mvp/"
platform: Web
version: 1.0.0
---

## Overview
一句话说明项目用途。

## Demo
[在线体验](/apps/expfood-mvp/)

## Download
[下载源码](/downloads/expfood-mvp.zip)
```

### 4.3 更新项目列表
编辑：`source/projects/index.md`
新增一行：
```md
- expfood-mvp：[在线体验](/apps/expfood-mvp/) | [下载源码](/downloads/expfood-mvp.zip)
```

## 5. 本地检查（最快流程）
在仓库根目录 `D:\GITHUB\TEST\ai-weekly-site`：

```powershell
npm run clean
npm run build
```

如需本地预览：
```powershell
npm run server
```
打开 `http://localhost:4000` 检查：
- `/apps/expfood-mvp/` 可访问
- `/downloads/expfood-mvp.zip` 可下载
- `/categories/Projects/` 中可看到文章

## 6. 推送到 Git（固定命令）

```powershell
git -C D:\GITHUB\TEST\ai-weekly-site add .
git -C D:\GITHUB\TEST\ai-weekly-site commit -m "feat: add expfood-mvp project package and pages"
git -C D:\GITHUB\TEST\ai-weekly-site push origin main
```

如果默认分支不是 `main`，先查：
```powershell
git -C D:\GITHUB\TEST\ai-weekly-site branch --show-current
```

## 7. 发布到 Vercel

### 7.1 首次绑定（只需一次）
在仓库目录执行：
```powershell
cd D:\GITHUB\TEST\ai-weekly-site
vercel
```
建议设置：
- Framework Preset: `Other`
- Build Command: `npm run build`
- Output Directory: `public`

### 7.2 后续发布
```powershell
cd D:\GITHUB\TEST\ai-weekly-site
vercel --prod
```

如果你已在 Vercel 控制台绑定 GitHub 仓库，通常 `git push` 后会自动触发部署。

## 8. 提交前检查清单
- 下载包文件名与文章链接一致（如 `expfood-mvp.zip`）。
- `source/apps/<slug>/index.html` 可独立运行。
- `source/projects/index.md` 已增加入口。
- `npm run build` 通过后再 `git push`。

## 9. 常见失败处理
- 复制到 `D:` 权限失败：先复制到 `C:\Users\<Windows用户名>\Downloads` 再移动。
- 大文件拷贝中断：优先 `zip` 后单文件拷贝，避免散文件 99% 失败。
- 页面中文乱码：确保文件保存为 UTF-8。

## 10. 最易遗漏（必须同时完成）
只把压缩包上传到 `source/downloads/` 不算接入完成。必须同时满足：
- `source/downloads/<slug>.zip` 或 `source/downloads/<slug>.tar.gz` 已存在。
- `source/_posts/<slug>.md` 已创建，且 `categories` 包含 `Projects`。
- `source/apps/<slug>/index.html` 已创建且可访问。
- `source/projects/index.md` 已新增该项目入口。

以本次 `expfood-mvp` 为例：
- 下载：`/downloads/expfood-mvp.tar.gz`
- 体验：`/apps/expfood-mvp/`

## 11. 执行纪律（防漏步骤）
- 当用户要求“按前例推送/打包推送”时，默认执行“完整接入流程”，禁止只上传压缩包。
- 完整接入最少包含 4 项：
  1) `source/downloads/<slug>.*`
  2) `source/_posts/<slug>.md`（`categories` 必须含 `项目`）
  3) `source/apps/<slug>/index.html`
  4) `source/projects/index.md` 入口链接
- 若仅完成第 1 项，视为未完成，不得结束任务。
