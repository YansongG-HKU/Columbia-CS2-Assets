# 哥大 Butler Library｜北侧中央门、十四柱与东西坡道
从 `ButlerLibraryTrial/` 作为独立候选试放。原枢轴、11×7（88×56 米）地块、31.4 米模型总高保留。模型 −Y 朝校内北侧 Butler Lawn，非西 114 街的背面。

- 按[哥大正立面照片](https://operations.cufo.columbia.edu/content/butler-library)改正原双门和两组挑棚：重建一组中央木双门与两侧壁挂灯。撤下原落在新铺装上的四支独立灯和两只旧玻璃灯罩，不等于删除实景草坪灯。三档保留原 14 柱位置与主檐铭带；柱间 13 开间改为高矩形窗，撤下近中旧半圆窗楣。新窗和灯均为视觉近似，不配置透明玻璃及游戏发光。未拿 19 世纪 University Hall 的尺寸硬套重标 Butler 柱高。
- 按[哥大 2017 年竣工资料](https://cufo.columbia.edu/news/university-officials-join-recognize-butler-plaza-and-lawn-restoration-project-completion)保留东西两进路，在现有地块内做一块闭合平台及双坡，斜面本身使用砖色，无另叠一层。试放坡长各 11 米，模型高差 0.494 米，平台正面标高 0.50 米；用于保留坡面与方向，非测绘或无障碍合规结论。实际独立北向坡道、草坪与铺地范围超出本次模型，不把它们写作已建。
- 三档主体 102,145／64,694／966 三角，近中另各保留 894 窗三角；五个 FBX 和十张 PBR 图。原近中 55,408／30,990 个退化 UV 经采样重投影及删除已替换旧面后均为 0；近档 10 个零面积三角删掉。其余原几何和有效 UV 保留，材质新增色块位于原图集未用区域。原远档平面法线重算，暗斑减少。远档比原 376 面多，实际游戏远景开销待验。
- FBX 回读三档共通过 198 个平台、360 个坡面、126 个门面、54 个灯、936 个窗面、168 个原柱位置采样，每档平台闭合 30 条边。柱位置与原候选一致，不等于柱高已实测。附图是 Blender 对照，不是游戏。
- Editor 可用后先验 Irvine，轮到 Butler 时测东西坡道如何接游戏道路及北向外部坡道接口、门前碰撞与访问标志、三档切换及夜景。未运行游戏、未推模型 LFS 或发布 pmod。

## Offline evidence (Dot cloud, 2026-11-24 UTC)

- Columbia main `98587eeddab6ddf83a0c562efbf449207d633582`; verified 19 input Git blobs and LFS bytes with pinned pointer SHA/size. No binary model stored in this PR.
- ZIP `哥大-Butler-Library-中央门十四柱与双坡整栋-未游戏验收.zip`: 12,914,399 bytes, SHA-256 `a85ca193200844e996094f3546a03147e9cfb6fba8315cc679e75a4a97defe09`. CRC and all 26 extracted hashes passed. Five FBX, ten PBR maps, and five sharedAssets links. No external material references in body readback.
- `placement-qa.json` `3efb0152ff49fb89d8ea63d6c53f475d5822eb9ceb8c3faedc40ae3cba239543`; `readback.json` `ddcd37fcca04d7f68ef2514613788e701573b394585eab186fb583fe436f4230`; `Butler-Library-Readback.jpg` `5f5245941cd5ae9230866dabd3691c9f3039113311aafe8ed8fb4b87780bbc44`. No licensed photo included in ZIP.
- No CS2 Editor/game, LFS model push or pmod release. No claim that all inherited contacts are manifold. No Blender process left after this batch.
