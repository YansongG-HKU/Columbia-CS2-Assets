# Uris Hall：2017 地面控制，2024 正射定位

实际读取纽约州 2017 裸地 GeoTIFF 的局部 700×715 英尺片（700×715 像元），不是用仓库估计或地形网上的显示值；原下载服务支持 HTTP byte range。结合纽约市 2024 正射 9 小瓦片，选取 6 处铺装近似中心，剔除 NoData，各取 9 × 9 个 1 ft 单元。地面高程系 NAVD88 / Geoid12B，以美制测量英尺原样取样后换为米。

| 正射判读位置 | 地面中位数（m） |
|---|---:|
| 南侧入口方向西段步道 | 46.400 |
| 南侧入口方向中段步道 | 46.446 |
| 南侧入口方向东段步道 | 46.412 |
| 西侧相邻通道 | 46.257 |
| 东侧相邻铺装 | 47.753 |
| 北侧广场采样 | 47.436 |

这不是门槛/垂直控制点实测；步道位置取自较新的正射，2017 与 2024 之间的可能场地变化未查。相邻东西采样约差 1.50 m，不能把寻址记录的最低地面（139 ft）直接当南入口基准，也不能据此从父级屋高反算各屋顶。地面结果没有为高度缩放提供充分证据。现有模型和试验包保持原样。

已实际看过 GLUCK+ 原始场地平面、楼层平面和剖面。剖面显示中央采光构件、入口内楼梯和多个台阶层次；未找到可读的标高或比例尺，不能据此直接赋给模型尺寸。2024 正射可分辨主平台、六组独立机件、南附楼屋顶和北侧半圆体。下一步用同一基准测各屋面和设备平台，另比对当前室外台阶。云机没有 PDAL/laspy/LAZ 解码工具，本轮无法用已定位 NOAA 点云提取屋顶；纽约州最高回波瓦片常见路径没有可用结果，未安装新软件、没有用裸地栅格伪造屋高。

复现地面裁片：`GDAL_DISABLE_READDIR_ON_OPEN=EMPTY_DIR GDAL_CACHEMAX=64 gdal_translate -projwin 994600 234375 995300 233660 /vsicurl/https://gisdata.ny.gov/elevation/DEM/NYC_TopoBathymetric2017/be_NYC_029.tif uris-ground-crop.tif`。用本目录脚本读取裁片和 JSON。来源：[市 LiDAR 元数据](https://data.cityofnewyork.us/City-Government/Topobathymetric-LiDAR-Data-2017-/7sc8-jtbz/about_data)、[2024 正射](https://tiles.arcgis.com/tiles/yG5s3afENB5iO9fj/arcgis/rest/services/NYC_Orthos_2024/MapServer)、[建筑师项目图](https://gluckplus.com/project/columbia-university-business-school-addition/)。
