---
title: 暖心桌面精灵
date: 2026-08-19
updated: 2026-08-19
tags:
  - 桌面应用
  - Electron
  - 桌宠
  - 工具
categories:
  - 项目
repo: ""
download: /downloads/desktop-sprite.zip
demo: /apps/desktop-sprite/
platform: Windows
version: 1.0.0
---

## 项目简介

暖心桌面精灵是一个基于 Electron 的 Windows 桌面精灵。它以无边框透明窗口悬浮在桌面右下角，能够随机显示关心金句，使用系统中文语音播报，并通过轻微浮动、闪烁和弹出动画营造桌宠陪伴效果。

## 技术栈

- Electron 31 — 无边框透明置顶窗口、系统托盘、开机自启（`setLoginItemSettings`）
- 原生 HTML / CSS / JavaScript — 渲染进程界面与纯 CSS 手绘精灵形象
- Web Speech API — 中文语音合成播报
- contextIsolation + preload 安全桥接 — 主进程与渲染进程 IPC 通信

## 功能特点

- **桌面悬浮**：无边框、透明、置顶显示，不占用任务栏位置
- **关心金句**：内置多条中文暖心金句，支持「再说一句」立即触发
- **随机提醒**：可设置 15 分钟 / 30 分钟 / 1 小时 / 2 小时提醒间隔
- **语音播报**：使用 Windows 系统语音合成播报中文金句
- **动画效果**：桌宠浮动、金句弹出、星光闪烁和按钮交互效果
- **安静时段**：默认 22:00—07:00 免打扰，可在设置面板调整
- **开机启动**：可在设置中启用 Windows 开机自动启动
- **系统托盘**：支持显示精灵、立即发送一句和退出应用

## 本地运行

在 Windows 上进入源码目录，执行：

```bash
npm install
npm start
```

首次安装 Electron 需要网络连接；如下载较慢，可配置可用的 npm 镜像源后重试。配置保存在 Electron 用户数据目录中，不写入项目源码目录。

## 下载

[下载源码](/downloads/desktop-sprite.zip)

## 说明

该项目为 Windows 桌面工程，不提供网页在线演示；[项目介绍页](/apps/desktop-sprite/) 内含精灵形象与功能预览。
