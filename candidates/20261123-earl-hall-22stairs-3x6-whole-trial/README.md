# 哥大 Earl Hall｜22级入口梯与 3×6 地块试放

把 EarlHallStairsTrial/ 整个文件夹导入独立副本，起始地块为 3×6（24×48 米）。另留原 3×5 资产，不要混导。此套使用已有 22 级阶梯、四柱门廊、砖山花及穹顶方案配套的几何与贴图，没有与另一套旧远景接缝补丁混装。

- 22级版本的旧 FBX 实际长度 46 米（本地 Y −26 至 +20），若仍沿用 3×5，模型前缘越出 6 米。此次把各档主体及窗、玻璃分件相对原枢轴沿 Y 统一移 +3.0 米，再以 3×6 试放，Y 为 −23 至 +23，前后各留 1 米；24 米宽恰在地块两边界，游戏里需检查与邻楼和道路的间隙。没有缩放模型。
- 七件 7500 FBX 均从独立路径回读，三角索引、UV 和原生法线数据没改；按统一位移比较，回读坐标最大差 0.0022 毫米。十张配套 PBR 贴图仅改文件名，内容不改；前两档共用五张。
- 三档分别在左、中央、右三条路径向下探测，均读到全部 22 个阶面高度（0.153 至 3.366 米）；这是几何检查，不等于行人能够上楼梯。柱廊、铜穹顶和顶亭保留；[哥大 University Life](https://universitylife.columbia.edu/book-space) 有建筑材质说明。
- 主体 22,861 / 10,097 / 1,891 三角。为暂时保留阶梯和门廊，远景仍偏重，未称达到约 500 三角的项目目标。模型顶约 34.816 米，是本候选值，不是实测。进入 Editor 后优先验入口方向、坡地衔接、楼梯路径、两侧边界和三档表现。暂无 Editor、LFS 或 pmod。

- Source: prior private `EarlHall_立面及22级台阶校正候选.zip` (not legacy dome-seam model); package: 17,160,006 bytes, SHA-256 `d46fd9bea151014c95bc44eafccc8d034f95a225cea45a4a54db4bebdfb913af`. ZIP CRC and every extracted file SHA verified. No binary models in this PR. Offline whole models: 20 (Columbia 11, Penn 9); actual Editor, LFS, pmod 0.
