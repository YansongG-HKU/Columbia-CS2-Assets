# 哥大 Dodge Hall｜远景闭合与近中贴图修复

解压后导入独立的 DodgeHallTrial/，旧枢轴、9×5 地块（72×40 米），实物放置和寻路未验。不要与旧的单个远景补丁同时导入。三档模型顶 25.60 米，地块表面最低约 −0.05 米。

- 先验证并沿用既有 22.80 米屋顶接缝补丁，再把远景屋顶、主楼、前坡道和底座整合成一个闭合网格。与 main 对照，5→1 个索引外壳、23→0 组正面积共面重叠、29→0 组 BVH 非邻接交错。最终 98 三角、147 条边反向配对，零开边、重叠或退化面（限制于本离线筛查，不等于游戏碰撞测试）。
- 六个方向 21,426 次外表命中，首个交点最大差 0.046 毫米，UV 最大差 8.35e-7；没有丢失或额外的命中。五张远景贴图保持字节级相同。两组无灯光主体对照最大色差 9/255，无像素通道差超过 20。
- 近、中主体共修正 34,720 个零面积 UV 三角；五张共用贴图只在 15 个原 UV 不使用的色块改像素，顶点、三角和原法线不变。回读近、中主体和 Win/Gls 均未检出零面积 UV；保留每档 492 个窗、276 个玻璃分件三角，导入候选已解除旧预览材质绑定。六组近、中无灯光主体回读的最大颜色差 1/255。
- 主体三角 37,936 / 22,408 / 98。JPG 为纯主体 Blender 回读，不是游戏截图。进 Editor 优先看前坡道和地基、玻璃昼夜材质、屋檐/底座换档，再确认保存重开。未运行游戏、未推模型到 Git LFS、未导出 pmod。

- Main `98587eeddab6ddf83a0c562efbf449207d633582`; exact earlier far patch SHA `425f34adf65876779180b1ea0479a6c104cb98381cd03fbe7aa5a54e5576eedb`. Package: 11,274,002 bytes, SHA-256 `fcd5cef96fed17f88237dc2c6cee023f72025b9a80584c536f84ada45a026885`. ZIP CRC and every extracted file SHA verified. Binary assets not added to this PR. Offline whole models: 19 (Columbia 10, Penn 9); actual Editor, Git LFS pushes, pmod 0.
