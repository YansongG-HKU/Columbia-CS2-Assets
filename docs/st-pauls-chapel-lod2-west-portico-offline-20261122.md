# 哥大圣保罗礼拜堂：西门廊远景修整（离线 LOD2）

在上版单材质远景基础上，移除西侧不准确的实心假坡顶门廊。恢复四根浅石柱、三段开间、平檐和栏杆式矮栏，在后方独立山墙补简化圆饰；保留原来的砖墙和唯一正门，并加少量简化台阶。门廊铭文自行制作，不复制文档照片。模型只还原游戏里容易辨识的尺度与构成，不将柱宽、栏板或圆饰视作测绘成果。

- **检查**：关闭自动搜图后用 Blender 4.3.2 回读 FBX，仍是单材质；744 顶点、1,340 个有效三角面，总范围 32×48m（含底板）、最高 33m，和上版一致。只移除了原西侧占位的 16 面；其余 544 面的位置最大差约 5.4µm、UV 完全相同，最大法线向量差约 0.00012。新增组件检查分别为闭壳且共享边的朝向一致；组件之间接合未做整体布尔或碰撞认证。
- **贴图**：暗绿釉瓦、东侧铜屋顶和旧场景纹理完全保留。只用了已有 atlas 右下闲置区，仍为 2048×2048 BaseColor 和 Normal 一套；Normal 文件逐字节相同。地图材质、碰撞、贴图过滤和游戏内换档未测；未提供新版 UV 对应的 MaskMap、ControlMask 或 Emissive。近/中景源模型没找到，因此本包不冒充三档交付。
- **看模型**：打开 `candidate/StPaulsChapel-LOD2-West-Portico-OFFLINE.blend`，材质已打包。FBX 可和同名贴图离线独立查看；生产源未覆盖。前后对照为离线渲染，不是 CS2 游戏截图。
- **参考**：[纽约市 LPC 第 19 页（图纸 18）照片与提案](https://www.nyc.gov/assets/lpc/downloads/pdf/presentation-materials/20260714/140-West-Street.pdf#page=19)；[哥大入口资料](https://operations.cufo.columbia.edu/content/st-pauls-chapel)。照片与改造示意分别使用；当前精确坡道样式未确认，因此不重做坡道、栏杆或铺地。
- **复核**：`sha256sum -c SHA256SUMS.txt`；`python guard.py verify.py -- "$PWD"` 可从 FBX 核实。修改前验证数据随包，重建脚本需上版单材质源及原屋面计划，未附第三方照片。

## Audit

{
  "vertices": 744,
  "triangles": 1340,
  "removed_proxy_triangles": 16,
  "retained_triangles": 544,
  "new_triangles": 796,
  "closed_components_added": 34,
  "bounds_m": [
    [
      -16.0,
      16.0
    ],
    [
      -24.0,
      24.0
    ],
    [
      -0.05000181123614311,
      33.0
    ]
  ],
  "readback_vertices": 744,
  "matched_triangles": 544,
  "max_xyz_uv_normal_error": [
    5.364418029785156e-06,
    0.0,
    0.00011649968738119043
  ],
  "min_triangle_area_m2": 0.004660815867881013,
  "materials": 1
}
9d34b463d18d5cbb83846fdadf6d2506aef4fd0d8cdca4f1ac159e69e391995b  candidate/NA_StPaulsChapel_4x6_LOD2.fbx
09bfc4698307af9a5962dff4e11a6822fa01f2a449cb4fcac17b3e4642234834  candidate/NA_StPaulsChapel_4x6_LOD2_BaseColor.png
2354924fc8d6246dcbd463990f85f8961ba90d9886d05fe2487d9c713e1b31d3  candidate/NA_StPaulsChapel_4x6_LOD2_Normal.png
54acdf3a0abf85690b985b613ffda651b2554fd12a01deca3466cc08f51ee3c0  candidate/StPaulsChapel-LOD2-West-Portico-OFFLINE.blend
de0fd137a19cfc6ec417ade0105059d64a299bc353792307a6881309ee38a38e  readback.json
8d7b760d8e94ca599518f9e7c584c3bb4d2b91dace2d992991923bce258c078b  retained.json
8b36e9caee36e2db5e79a6b29ffa03627badf990ae5bf79c177ca7ba3b9dfdd4  candidate-spec.json
083e9499216342d8f81557a02f398e842bb09f8fb1f6ee9cf075d4f96db4a2f4  west-atlas.json

ZIP SHA-256 `5d1567a9e3aa6eb8fbdafca35045aadb4d868e0bea09a0bb9fbea5bf8435b04d` (6,487,120 bytes). Documentation only: no binary, publish, collision or game-acceptance claim.
