---
title: 星空·星座认星镜
date: 2026-09-29
updated: 2026-09-29
tags:
  - 天文
  - 星座
  - Python
  - PDF
  - 手工制作
  - 命令行工具
categories:
  - 项目
repo: "https://github.com/SONGXUEJUN1234/xingkong"
download: /downloads/xingkong.zip
demo: /apps/xingkong/
platform: 跨平台（Python CLI）
version: 1.0.0
---

## 项目简介

星空·星座认星镜是一个眼镜式星座识别装置的打孔图纸生成工具。Python 命令行程序读取精选星表的
J2000 真实坐标（赤经/赤纬/星等），按纸板离眼距离换算孔位，生成可直接打印的打孔图纸 PDF：
硬纸板按图打孔后套在眼镜上，锚点大孔对准易认亮星、歪头旋转锁定第二颗星，其余孔即指向整个星座——
"两星锁定法"让零基础的人也能在晴夜快速套住星座。

## 技术栈

- Python 3 标准库 — 纯命令行实现，仅 reportlab 一个绘图依赖
- reportlab — 生成 100% 实际大小的 PDF 图纸（含 50mm 校准标尺、折翼虚线标记）
- J2000 星表数据 — star_data.py 手工录入北半球首批 5 个星座亮星（精度 0.01–0.05 度）
- pytest — 坐标换算与星表数据不变量的单元测试

## 功能特点

- **真实星位打孔**：孔位按亮星真实相对位置换算，孔位即星位
- **两星锁定法**：锚点 Ø5mm 大孔 + "第二亮"孔双重锁定，其余孔指向全星座
- **可调离眼距离**：`--distance` 支持 80–300mm（默认 100mm）
- **打印校准**：图纸含 50mm 标尺，确保 100% 实际大小打印不出错
- **每孔印星名**：锁定后按孔旁星名逐一认星
- **首批 5 星座**：北斗七星（全年）、猎户座（冬）、仙后座（秋）、天鹅座（夏）、天琴座（夏）
- **可扩展星表**：star_data.py 按格式补星座，跑 pytest 验证即可

## 本地运行

```bash
python -m pip install -r requirements.txt   # 首次
python make_card.py 列表                    # 查看支持的星座
python make_card.py 猎户座 --distance 100   # 生成图纸 PDF
python -m pytest -v                         # 运行单元测试
```

Windows 下建议加 `PYTHONUTF8=1` 前缀运行，避免中文输出乱码。

## 制作与使用

1. 图纸按 **100% 实际大小**打印（关闭"适合页面"缩放），先量标尺确认为 50mm
2. 图纸贴 300g 灰板纸/双层快递纸箱裁切，锚点 Ø5mm、其余 Ø3mm 打孔
3. 左右贴折翼固定在眼镜框；**印刷面必须朝向眼睛**（装反图案会左右镜像）
4. 闭一只眼，锚点大孔套住亮星 → 歪头旋转锁定第二颗 → 其余孔即指向星座各星

## 下载

[下载源码](/downloads/xingkong.zip)

## 说明

该项目为 Python 命令行工具，不提供网页在线演示；[项目介绍页](/apps/xingkong/) 内含北斗七星
打孔面板示意与完整制作说明。源码同步托管于 [GitHub](https://github.com/SONGXUEJUN1234/xingkong)。
