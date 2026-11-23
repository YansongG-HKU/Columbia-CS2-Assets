# 哥大 Schermerhorn Hall｜钟面山花、双柱铭牌与三阶入口

解压后从 SchermerhornHallTrial/ 作为独立候选导入；保留原枢轴和 8×6（64×48 米）名义地块，面向校园的一侧为模型 −Y。近/中檐口仍各超出地块宽约 0.30 米，先检查摆放后是否侵入相邻资产。

- 用矩形双门、双圆柱、刻有楼名的门楣和上方四行铭牌替掉旧半圆门头。门前三级短台阶由一体闭合网格形成，三档同为模型 z6.54 / 6.68 / 6.82 米。旧远景门口平台顶部由 z7.40 调到 z6.40 米，与旧近、中档的校园台基对齐。近、中原路灯分件保留；这里没有可进入的室内。
- 三档加了正立面的三角山花、圆钟与铜饰；山花局部模型最高约 31.24 米，非实测楼高。远档对原本 160 个三角的平面改用面法线，屋顶与墙的大片圆状高光在 Blender 同镜回读消失。三档主体 48,424 / 26,714 / 498 三角，近、中各另有 628 三角窗和 112 三角玻璃灯罩；近中五张共用图、远景五张图。新增部分的贴图只写向未被原三档使用的图集区域；原 UV 映射未重绘，近/中遗留的大量塌缩 UV 未在本包统一修复。
- 依据[哥大现状照片](https://neuropsychopharmacologylab.psychology.columbia.edu/research-projects/interested-being-research-participant-one-our-studies)、[院系入口照片](https://eesc.columbia.edu/content/undergraduate-program-overview)和[哥大铭牌特写](https://news.columbia.edu/news/6-iconic-inscriptions-columbias-morningside-campus-you-should-know)制作图案和几何。照片仅为参考，未复制进图集。原资产的较大台基/外侧场地关系仍是简化；照片中的侧向栏杆、门厅内改坡（[哥大 2023 工程说明](https://designconstruct.cufo.columbia.edu/news/summer-2023-construction-projects)）以及 [Extension 的六层连通](https://operations.cufo.columbia.edu/content/schermerhorn-extension) 未建模。
- 游戏中需先核校园台基标高和街道摆放，再看外门台阶、地形接触、三档切换、材质、光照、碰撞和有效路径。附件预览来自 Blender；不是 Editor 实测、不是 pmod，也没有模型推送或发布。

三档 Blender/FBX 回读共通过 60 个台阶、84 个门面与山花、15 个屋面探针；短台阶每档 42 条边均两面相接。


## 核对与交付

源仓固定 `98587eeddab6ddf83a0c562efbf449207d633582`，验证全部 FBX 和 10 PNG 的 Git/LFS 对象。原远档 `6b30f8e42a6ccf29783af67f33a97e8fc8f3659d66f2446c6eff97e461d74dd0`，旧 160 面矩形门色图试验与本轮几何版不混用。近/中各移除 326/254 个旧门相关三角。便携 ZIP 10,142,098 bytes，SHA-256 `e819b9bcf2899f7fd3194e0a3108dbf33cbdefb4e203e7b0ff3463739cd5b8e9`，CRC 与 23 份解压内容 SHA-256 通过。仅这条证据写入本草稿 PR；未改 main、未推送模型 LFS、未游戏验收或发布。
