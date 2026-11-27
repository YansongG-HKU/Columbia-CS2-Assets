# Lewisohn Hall 整栋试放（未在 Editor 运行）

Dot 云电脑从固定 main `98587eeddab6ddf83a0c562efbf449207d633582` 的真实 LFS 文件恢复近档主体和十图，按前序 draft manifest 验证 SHA-256、重建 2 Win/2 Gls 和远档旁壳补丁；回收已验证的中档试件（精确原有 LOD1 补丁，候选 SHA `b9635c70bffa8530c5ad3f74490f73fe465cc9039ae12341075918b0121deb3d`）。中档 16,932 三角完整导入，恢复八组立面饰件而不是直接删片。远档去掉四片同位反向内部面，外形仍不动。

合入较早的试验性远档正门贴图。2,085 像素（x516–573/y379–414）只影响原来两片正面三角，以 UV/坐标签名及一像素防串色核对前后不变。旧 Normal 和夜间图沿用。主体三档 37682/16932/92 三角，近和中独立 Win 431、Gls 112，Gls UV 无退化。孤立目录关自动搜图复验 7 FBX 身份/三角数/边界/可见纹理；十 PNG 及五共享设置齐全。保留 48×32m 名义地块和 25.8m 高度。

试包 SHA-256 `a8ed6508002b217e56eb870d7709dc2f08edafc78e1efc3378b0cb675f10d162`，CRC 通过。试放名称 `NA_LewisohnHallTrial_6x4`，选择 `LewisohnHallTrial/`。真实换档时须看窗，因为 Blender 预览表明远档窗偏暗，近中窗格也简化；再测入口坡道、夜景和保存重开。预览不能代表引擎着色。未发布、未推二进制、不覆盖原资产、不是 pmod。校方参考 [Lewisohn Hall](https://operations.cufo.columbia.edu/content/lewisohn-hall)。