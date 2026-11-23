# 哥大 Kent Hall｜近中景 UV 修复整栋试放

解压后将 KentHallTrial/ 整个文件夹导入；不要覆盖旧版。保留旧枢轴，先用 8×4 地块（64×32 m）试放。近、中外缘 x=±32.35 m，东西各伸出 0.35 m；远景是 ±32.00 m。三档高 25.60 m。若与相邻资产冲突，先检查枢轴并对比 9×4 地块，不要无记录地缩放模型。

- 近、中主体的 26,536 / 13,288 个零面积 UV 三角重新映射到 448 个隔离色块，回读为 0。五张共用贴图只修改三角 UV 不使用的区域：每块 64×64 px，距旧图 UV 包围盒另有至少 12 px，重新取样保留旧常量色值，并重建受影响三角的切线和副切线。原主体几何、法线、索引和未折叠 UV 不变。
- 分件保留每档 505 个 Win、112 个 Gls 三角。沿用原 Win/Gls 游戏导入候选，去掉 Blender 预览材质链接；Gls 每档 80 个零面积 UV 一并修复。全分件的 Blender 预览窗样式与旧版不同，无法据此判断游戏窗色或发光。Editor 需确认 Win/Gls 分配，检查昼夜、反射和换档。
- 远景沿用既有的侧边接缝补丁，108→104 三角，原五张远景贴图数据不变。八组纯主体同机位无灯光回读中，近、中景 RGB 单通道最大差 1/255，远景两视角像素一致。附件 JPG 是不含 Win/Gls 的 Blender 主体对照，不是游戏截图。
- 尚未运行 CS2 Editor、完成碰撞/道路验收、推送 Git LFS 资源或导出 pmod。

## 离线核验
- Original main: 98587eeddab6ddf83a0c562efbf449207d633582. The legacy side-seam and Win/Gls patches resolve at cd2610d9c77fb4917f320598d420264da52c548b. Reimport: 53,876/30,956/104 Base faces, 7 FBX and 10 PBR PNG. Model count +1 (Columbia 9 + Penn 8); Editor, LFS, pmod 0.
- ZIP: 哥大-Kent-Hall-三档及近中景UV修复-未游戏验收.zip, 10889832 bytes. SHA-256: c292a939fef30d3f49f97d228d963ee8203023c329f636cdf866be1cccb238a8. CRC and every offline file SHA passed. Binary assets not included with this record.
