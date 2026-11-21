# Uris Hall：可编辑源文件贴图修复

这是 Uris Hall 的独立、可重建的 Blender 源文件候选，不是游戏导入包。原 Blender 源的 8 张已挂接烘焙图指向旧电脑的绝对地址，复制到云电脑后不会加载。从固定的仓库 LFS 原件取 8 张 PNG，把候选源文件引用改为 ./textures 下的相对路径；PNG 字节不变。Blender 4.3.2 用不同目录重开后，8 张图均实际解码：近/中共享图为 4096×4096，远档为 1024×1024。颜色/发光图为 sRGB，法线和 MaskMap 为 Non-Color；7 个网格对象的坐标、面拓扑、UV、材质绑定及节点连线均无变化。未挂到当前网格材质的旧图路径原样保留；ControlMask 不在这两组 Blender 节点绑定范围。报告不等于贴图内容、重烘或游戏材质验收。

从此仓库取得已拉取 LFS 的 UrisHall 目录，在仓库外新建候选：

```sh
blender -b -t 2 --disable-autoexec --python-exit-code 1 \
  --python candidates/20261120-uris-source-portability/relink_uris_source.py -- \
  --source UrisHall/NA_UrisHall_6x9.blend --output /path/to/fresh/uris-source-candidate
```

这一步不修改任何 FBX。近档 584 (A,B,C) 与 1224 (D,B,C)，中档 290 与 492 的第一版精确切分仍不合格：保留 (D,B,C)、将大面改为 (A,B,D)、并沿 D 切开 A–C 的侧面，会把原三面共边 B–C 降为两面，但 B–D、C–D 会从两面变三面。近档侧邻 1223、4148、4788 已互相覆盖，584、4149 与 4789 亦有重合。不能只切目标两面或把反向支撑一起移除。源文件已回读：各档 Base 已合为同一主体网格，没有独立零件对象可直接判断归属。下一步应按前/侧面构件的完整重叠范围处理，并独立验证双向覆盖、逐角属性和边界后再产出 FBX。

本轮峰值采样约 691 MiB；Blender 退出后核对可用内存 8759 MiB，无本批 Blender 进程残留。CS2 Editor 尚未实测。
