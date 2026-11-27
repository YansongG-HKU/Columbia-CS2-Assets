# Uris Hall 分层 FBX：可移植候选，未放行

以哥大草稿同一版本的 LFS 原件为输入，先通过原补丁重建 4 个玻璃和窗户 FBX（移除不适用的预览材质绑定，复验 72/72、80/80 三角，不是本轮新增 UV 修复）。这批在 3 个主体 FBX 中各移除 6 处旧电脑目录，统一为同目录纹理文件名；修复后逐字段回读证明，除明确的路径字段外，几何、UV、材质和 FBX 类型化内容不变。保留 10 张原贴图、原来的 5 项 LOD1 贴图共享设置。独立目录关闭自动找图逐个回导 7 个 FBX，3 档主体均加载应有的三张 FBX 内引用贴图，七件均无零面积几何三角。MaskMap、ControlMask 属于这次包内独立交付，不把 Blender 读不到内联引用当成已实测游戏材质。

**尚未放行：**主体近档 3444 / 7210、中档 2168 / 4762 个三角的三角内 UV 三点完全相同；不是阈值导致的误报。最大两个 UV 采样坐标分别占近档 2672、 中档 1832 个三角，可能包含有意共用色样，不是整批重新展 UV 的授权或证据。下一步先确认面类、源材质和多通道样本是否有意共用，再针对非色样且需要真实纹理的面修补并重烘；保留原 UV 供对照。接缝问题未修复，无游戏实测。

复现：以拉取 LFS 的仓库为 original，使用 `candidates/20261120-three-campus/model_delta.py apply` 先重放仅 `base` 以 `UrisHall/` 开头的 4 条 manifest 及相应补丁。运行 `blender -b -t 2 --disable-autoexec --python-exit-code 1 --python uris_portable_fbx.py -- --original UrisHall --replayed <replay>/UrisHall --textures UrisHall/textures --output <new-output> --clean <new-readback>`。原目录不会被修改；`manifest.json` 的 18 个条目不包含读回报告。此处保存确定性复现工具及证据，不覆盖原建筑资产，也不发布 pmod。
