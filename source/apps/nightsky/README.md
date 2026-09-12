# 见星 NIGHTSKY · 河北四季交互星图

## 项目介绍

在河北的夜空下探索四季星座。基于 5,044 颗恒星的真实赤经、赤纬和视星等数据，构建承德、张家口、石家庄三地春夏秋冬四季代表夜的交互星图，持续放大可进入真实望远镜巡天影像。

## 功能特点

- 河北承德、张家口、石家庄三地，春夏秋冬四季代表夜（2026 年 1/4/7/10 月 15 日 22:00）
- 5,044 颗恒星真实坐标，星座连线与中文名称
- 拖动转向、点击选星、滚轮/双指缩放、方向键改变视角
- 时间轴 18:00 至次日 06:00，可拖动或播放
- 星图缩放至 14 倍进入实拍：12 个深空目标的 DSS2 巡天照片与 M57 哈勃照片
- 搜索中文名、英文名、星座、HIP 编号、M 天体（按 `/` 聚焦）
- 图层控制：星座连线、标签、赤道网格、银河氛围、1–6 等阈值
- 浏览器本地收藏与观测手记（localStorage）

## 技术栈

- React + Vite 构建的静态网页，无后端、无数据库、无 API 密钥
- Canvas 立体投影星图（仅绘制地平线上方天体）
- 星表数据：D3-Celestial（5,044 颗恒星 J2000 坐标）
- 巡天照片：DSS2 / STScI，CDS HiPS2FITS 服务
- 中文字体 Noto Sans SC / Noto Serif SC 本地打包，离线可用

## 使用说明

### 查看网页

已构建为纯静态网页，可直接部署到任意静态网站根目录。

本地查看需通过 HTTP 启动（星表通过 HTTP 读取，不要直接双击 index.html）：

```sh
# 在含有 index.html 的文件夹中执行
python -m http.server 8080
# 浏览器打开 http://localhost:8080
```

## 注意事项

- 默认是 2026 年夏季代表夜，不是河北此刻的实时观测
- 未校正岁差、自行、大气折射、消光，未模拟太阳、月球、行星与晨昏亮度
- 银河氛围与地景为艺术示意；实拍为历史巡天/空间望远镜照片
- 默认星表、中文字体与精选照片已本地打包，其他恒星的巡天照片需联网
- 请不要用望远镜直视太阳

## 数据与署名

- 星表：[D3-Celestial](https://github.com/ofrohn/d3-celestial)（BSD 许可，见 data/LICENSE.txt）
- 巡天：DSS2 / STScI，[CDS HiPS2FITS](https://alasky.cds.unistra.fr/hips-image-services/hips2fits)
- M57：NASA, ESA, and C. Robert O'Dell (Vanderbilt University)
- 字体：Noto Sans SC / Noto Serif SC，SIL Open Font License

## 创作者

@SONGXUEJUN1234
