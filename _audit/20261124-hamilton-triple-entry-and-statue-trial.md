# 哥大 Hamilton Hall｜三扇木门、四柱门廊与汉密尔顿像
在 CS2 Editor 作为独立候选导入 `HamiltonHallTrial/`。保留 8×4（64×32 米）地块、枢轴和原 30.10 米体量；近中檐口各约 0.40 米伸出地块。模型 −Y 是朝校园低区的三门正立面，不是 College Walk 独立进路。

- 按[校方历史导览](https://archive.org/details/officialguidetoc00colu)所记三门和三处学院印记，以及 [Beyond My Ken 的入口照片](https://commons.wikimedia.org/wiki/File:2014_Columbia_University_Hamilton_Hall_entrance_facade.jpg)（仅作参考，不在包内分发），重做一组三扇木双门、四根通高柱、三层窗和 HAMILTON 铭牌。去掉中心两侧错误的外置灯柱和离散模板门，远景用轻量窗面保留识别特征。原两枚玻璃灯罩模型不再随包；新墙灯、窗和门玻璃都是不透明近似，未设置动态发光。
- 以[哥大艺术档案](https://mcid.mcah.columbia.edu/work/w0001281)与[哥大杂志](https://magazine.columbia.edu/article/foundry-father)核对雕像，另建低多边形青铜剪影，保留分脚站姿、抬手及石台。总高模型 4.286 米，基座后缘与台阶留约 0.71 米，均为试放值，不是测绘；不用于判断游戏行人是否能绕行。
- 入口台阶 0.17／0.34／0.51／0.68 米。右侧附坡在模型上跨 7.814 米、升 0.676 米，与同一个门前平台相接。仅属游戏用近似，不代表符合实际无障碍坡度。校方[设施页面](https://operations.cufo.columbia.edu/content/hamilton-hall)另列 College Walk 入口，[Centennial Path 的西侧公共坡道](https://cufo.columbia.edu/news/lower-campus-accessibility-ramp-installation)是另一个连接，两者都未做。
- 三档主体 61,436／32,806／1,402 三角，近中额外各有 738 个原窗三角。用原采样色与材质值建立图集未占用区的色块，先补原近／中 43,226／21,338 个单点 UV。重导入五个 FBX 后主体没有零面积三角或退化 UV；保持原有有效 UV 和未命中部位的原面。不是把平涂重做成实景纹理。远档采用平面法线以去掉原平墙上的高光斑。
- 回读三档合计通过 135 台阶、144 坡面、63 登平台衔接、378 门面、216 柱身、45 铭带、30 雕像几何检查。九扇上部新窗为装饰，不假设可以穿行。附图不是游戏画面。云端编辑器可用后先验 Irvine；轮到 Hamilton 时测实际碰撞、侧坡与步道、雕像绕行、切 LOD、关开重载及夜景。未游戏验收、未推模型或发布 pmod。

## Offline evidence (Dot cloud, 2026-11-24 UTC)

- Input pinned Columbia main `98587eeddab6ddf83a0c562efbf449207d633582`. Verified 19 Git blob hashes and resolved LFS bytes against pinned pointer sizes and SHA-256 values.
- ZIP `哥大-Hamilton-Hall-三门四柱与雕像整栋-未游戏验收.zip`: 9,503,595 bytes, SHA-256 `2f3ab9c4127e4fe813c15897a730c49fc0fc2d5f34a679af44e057bde016e696`. CRC and all 25 extracted SHA-256 entries verified. Three body FBX plus both original Win overlays and ten maps; original geometry and UV on unaffected faces were preserved. No model stored in Git.
- `placement-qa.json` `a3d486b4c9dbcbd4dc37fcdcc56a7d0065d8d4ff64d69424c01d0fcdd62fa264`, `readback.json` `5a1c0001e2c2ec7aaa07c15ccc6d7e345f060bfc0febb18b2d81e5272f2d45ae`, `Hamilton-Hall-Readback.jpg` `b260397c8c7fb4124bf6776d15e3ad79e4ef3ac46592f48178a580214d348ac3`.
- 4,496 / 3,176 old overlap-prone entrance/decorative triangles removed in LOD0/1. Three doors and direct landing separate from the adjacent civic path; no real Editor placement, pedestrian navigation, collision, pmod or release.
