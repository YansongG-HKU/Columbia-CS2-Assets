# 哥大 Fayerweather Hall｜矩形门、铭牌与椭圆窗

独立导入 FayerweatherHallTrial/。旧枢轴、6×5（48×40 米）试放地块，三档模型顶约 26.9 米。按[哥大 Operations 的入口照片](https://operations.cufo.columbia.edu/content/fayerweather-hall)和[历史系手册封面](https://history.columbia.edu/wp-content/uploads/sites/29/2026/07/Undergraduate-Handbook-2026-27.pdf)，将旧入口的大半圆窗改为石框矩形门、刻字铭牌和独立竖椭圆窗。颜色与轮廓是游戏尺度近似，未用照片像素烘焙。

- 近、中移除旧门框、半圆扇及局部填件，远景也用实体轮廓而不是只贴一张入口图。门面比两侧框内退约 0.25 米；椭圆有独立窗框和内退窗面。三档用 18 条正向探针验证各部位一致。铭牌使用自绘字样；远处是否能读清取决于显示和贴图级别。
- 原远景门前平台比近、中高 1 米。将远档平台顶从 7.4 米降至 6.4 米；三档 12 次竖向回读均为 6.4 米。只校正模型与模型之间的落点，不代表校方坡道实测或可通行。
- 三档主体 37,874 / 19,322 / 336 三角。七件 FBX，近、中原窗与灯泡分件保留，已去掉分件旧预览材质。旧主体大范围尺寸、屋顶与外墙不改；十图只在各档原图集未采样的小片区绘制新构件。新增入口三角未发现零面积 UV；全楼遗留边界问题不在此次范围。
- 真正的入口坡道、底层接 Avery Plaza 下方、与 Avery 并排摆放、地形高差、昼夜材质与行走未验。模型门面有凹槽而不是可穿行的内通道。图是 Blender 回读；未做 CS2 Editor、Git LFS 或 pmod。

- Main `98587eeddab6ddf83a0c562efbf449207d633582`; earlier single-map ellipse tested only as a reference. New package 10,147,184 bytes, SHA-256 `1b1649756f412403a4275e84a408b86c949917bb1e619bb3d6a1e78c8e96d743`. Archive CRC and all extracted checksums passed. Offline whole totals 24 (Columbia 13, Penn 11); Editor/LFS/pmod 0. Text evidence only.
