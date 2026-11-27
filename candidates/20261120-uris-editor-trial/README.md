# Uris Hall 合并试验包（未放行）

仅适用于独立 CS2 Editor 试验，不是 pmod，不发布。组合先前确认的可移植主体、专用窗/玻璃层、两处色样切线候选；不将旧和新主体同时装入。保留 10 张原贴图和原共享配置。ZIP 26,579,151 字节，SHA-256 `01c51612d1ddbb23c4b09a192cfa3d3b8d374b90a794f0856b855c2245dd4965`。18 个资产文件均通过哈希校验，ZIP CRC 验证成功。实际解压到另一个目录，在禁用找图设置下独立回导 7 个 FBX、解码 10 张 PNG。三档主体 7210 / 4762 / 72 三角，玻璃层 72/72，窗层 80/80。三档主体最大 Z 47.20 m（相对模型局部零点；不当作实景高度）。

主体底色正侧、俯视两组同镜：近与中二值轮廓没有像素差，远相对中在两个镜头约差 0.14% 和 0.19%（以较细一档遮罩像素数为基数）。远档烘焙里的窗格更暗；此图没混合专用玻璃/窗着色器、法线 PBR 或场景灯光，因此是游戏转场待查信号，不宣称实机也有同样色差。所有画幅留边。仍缺真实场地配准、现存接缝修复及 Editor 各档切换。原资产不覆盖。

用上一份可移植目录和逐字节重现的切线目录，在仓库之外运行 `python assemble_uris_trial.py --portable <portable> --tangents <tangent> --output <fresh-out> --zip <fresh-zip> --extract <fresh-extraction>`。然后用 Blender 的 `verify_uris_trial.py -- <extraction>/UrisHall <fresh-renders> <report.json>` 像本批一样从提取目录独立核验。云电脑 Blender 已结束，可用内存约 8.4 GiB。
