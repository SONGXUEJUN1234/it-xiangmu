---
title: 猴面包的树 · 作品地点地图
date: 2026-09-12
updated: 2026-09-12
tags:
  - 地图
  - 阅读
  - 旅行
  - 微信读书
categories:
  - 项目
repo: ""
download: "/downloads/baobab-journey.zip"
demo: "https://baobabmap-j2afg9ta.manus.space/"
platform: Web
version: 1.0.0
---

## 项目简介

「猴面包的树 · 作品地点地图」把微信读书作者「猴面包的树」101 部游记作品里写到的地点，放到一张「田野索引」风格的纸质档案册世界地图上。初始收录 136 个地点、153 条作品—地点关联，经书籍简介证据与地理编码双重核验后保留 **88 个地点、99 条关联、0 条坐标错配**；对阿拉斯加、北极圈等易错样本做过逐点人工校验（如"Arctic Circle"曾被错误编码到得州同名道路，已更正为亚马尔萨列哈尔德）。

在线演示由原生成环境（Manus 托管）提供，地图数据与图片素材从其云端下发；[介绍页](/apps/baobab-journey/) 有功能说明与源码本地运行方法。

## 功能特点

- **证据优先**：仅收录「作品简介存在地点证据 + 具备地理编码」的地点，每条关联带证据文字与置信度分级
- **投影对齐**：红点叠加层与 Google Maps 嵌入底图共用同一 Web Mercator 投影与中心缩放，修复"红点漂到海里"类错位
- **作品档案卡**：点击地点展开关联书籍封面轨道，一键跳转微信读书
- **近似定位标注**：地理编码置信不足的地点明确标注，不冒充精确坐标

## 技术栈

- React + Vite + Tailwind + shadcn/ui；Google Maps 官方嵌入底图
- 坐标一次性来自 OpenStreetMap Nominatim（单线程限速 + 本地缓存）

## 在线体验

[在线演示（manus.space）](https://baobabmap-j2afg9ta.manus.space/) · [项目介绍页](/apps/baobab-journey/)

## 下载

[下载源码](/downloads/baobab-journey.zip)
