# 哥大 Philosophy Hall｜西入口六阶与双铜灯三档整栋

解压后独立导入 PhilosophyHallTrial/。6×4（48×32 米）地块和原枢轴不变，模型顶 29.0 米。这是离线整栋候选，不是已发布资产或实景测绘。

- 参考[国家史迹资料第 4 页](https://npgallery.nps.gov/NRHP/GetAsset/NHLS/03001046_text)，西侧校园入口应有六级花岗岩台阶，两侧是约 12 英尺的铜灯。近、中档原来六块相互重叠的阶梯箱体、远档原实心挡板都替换为一件闭合六阶楼梯；旧灯组件改为三档统一的双灯轮廓。灯位沿用建模位置，简化灯罩及装饰。
- 三档九组位置验证共 54 个阶面命中，三个横向采样位置均读到 6.56／6.72／6.88／7.04／7.20／7.36 米；左右灯各为高出露台 3.6576 米（按史料 12 英尺，不是实测精度）。三件新部件各自闭合，新面无折叠 UV。两份旧玻璃分件只包含原灯泡，已去除；新版灯罩为实色不发光试件，未验真实玻璃和夜景。
- 楼体保留已复验的中档八柱补件和远档侧边接缝补丁。主体三档 43,622 / 19,608 / 408 三角，5 件 FBX。原部位的几何和 UV 不改；近中共用和远档贴图各只使用四块原图集空位新增颜色和 PBR 参数，未使用参考照片像素。
- 实际放置时西入口朝 Buell 和校园，不能把此六阶当成街道入口。[哥大建筑资料](https://operations.cufo.columbia.edu/content/philosophy-hall)另有 Amsterdam Avenue 无障碍门，以及 Kent 二层连通关系。这一包未修正街侧高差、Kent 连廊、Revson 平台、扶手或游戏行走路径。
- Editor 优先看两灯及六阶换档、与大露台衔接、入口路径、材质昼夜和保存重开。截图仅 Blender 回读；无游戏、LFS 或 pmod 验收。

- Inputs: offline eight-pillar trial and exact prior LOD2 seam delta; no import of the incompatible half-atlas standalone lamp experiment. Package: 9,624,182 bytes, SHA-256 `a0e232d90061da9d66c64e79d480da354578282a8310925cbc89df842d34787c`. ZIP and all expanded file SHA entries passed. Offline whole count 22 (Columbia 12, Penn 10); Editor, LFS, pmod 0. No binary resources added to this PR.
