---
title: inventory-tool
date: 2026-04-25
updated: 2026-04-25
tags:
  - Tool
  - 3D
  - Calculation
categories:
  - Projects
repo: ""
download: ""
demo: "/apps/inventory-tool/"
platform: Web
version: 1.0.0
---

## Overview

散装物料盘点工具是一款基于空置体积法的专业盘点计算工具，用于精确计算仓库中散装砂石等物料的体积与重量。

## Features

- **空置体积法计算**：采用棱台公式精确计算散装物料体积
- **3D立体可视化**：基于Three.js实现物料堆的3D交互展示
- **多物料支持**：内置多种工业物料密度数据（瓶料碎玻璃、玻璃砂、锂长石等）
- **测量动画演示**：直观展示空置体积法测量流程
- **灵活测量**：支持任意高度层测量，自动分层计算

## Use Cases

- 砂石料场盘点
- 玻璃原料库存统计
- 散装物料仓储管理
- 工业原料计量核算

## Technical Details

- 纯前端实现，无需后端服务
- 使用原生 JavaScript + Three.js 开发
- 棱台体积公式：V = h × (A₁ + A₂ + √(A₁×A₂)) / 3
- 响应式设计，支持桌面和移动设备

## Demo

[在线体验](/apps/inventory-tool/)

## Usage

1. 输入仓库尺寸（长×宽×高）
2. 选择物料类型或自定义密度
3. 在不同高度水平测量空置长度
4. 系统自动计算物料体积和重量
5. 查看3D可视化结果和详细计算数据
