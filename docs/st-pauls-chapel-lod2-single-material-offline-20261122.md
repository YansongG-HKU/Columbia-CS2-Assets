# 哥大圣保罗礼拜堂：远景单材质离线候选

把原 Blender 预览里的墙身、绿釉瓦和铜屋面三页整合成一套 UV 和一个材质。保留 130 面暗绿釉瓦和 92 面东侧铜屋面，门廊色彩按原版不改。不是近景重做，不是游戏截图。形体采用已有低模，未声称逐点实测。

- **查看**：打开 `candidate/StPaulsChapel-LOD2-Single-Atlas-OFFLINE.blend`，内嵌 BaseColor 和 Normal。FBX 与两张同名前缀的贴图供单独离线试导入。
- **复核**：新 FBX 在关闭贴图自动搜索的 Blender 4.3.2 中全新回读，为 308 顶点、560 个面积大于零三角面、1 材质。世界顶点位置逐一相同，三角面和面绕序不变；UV 仅按槽做正向缩放和平移，结果最大误差约 3e−8；法线向量最大差约 5.5e−5。网格边界 32×48m 含底板，不是建筑实测开间；总 Z 范围约 −0.05~33m。
- **贴图**：两个 2048×2048 合成贴图各含三页，页边各有 16 像素扩边。为保留边距，每页从 1024 缩至 992，因此不是逐像素不变。三视角 88,095 个可见取样中，铜、瓦两页的逐通道色差 P95 <0.5（8-bit），原砖墙高频纹理约 7.28。原剪影不受影响，深层 mip/游戏材质仍需实测。
- **界限**：无 MaskMap、Emissive 或 ControlMask 的对应新 UV 版本，不可搭配旧 UV 的贴图直接覆盖；这不是完整 CS2 资产包。LOD0/LOD1 未改，换档、碰撞和 CS2 Editor 未验。不覆盖原件，不发布。
- **参考**：[Columbia Facilities 屋面修复](https://cufo.columbia.edu/news/chapelrestoration)；[修复建筑师的绿釉陶瓦记录](https://wbmelvin.com/portfolio-item/st-pauls-chapel/)。

## Audit

{
  "vertices": 308,
  "triangles": 560,
  "slots": 1,
  "max_uv_error": 2.9802322387695312e-08,
  "max_world_movement_m": 0.0,
  "max_world_normal_vector_residual": 5.494650388063974e-05,
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
  "view_tile_hits": [
    {
      "0": 21725,
      "2": 4000,
      "1": 211
    },
    {
      "0": 21652,
      "2": 4425,
      "1": 1045
    },
    {
      "0": 23066,
      "1": 1356,
      "2": 10615
    }
  ]
}
[
  {
    "slot": 0,
    "samples": 66443,
    "mean_abs_error": 1.6246,
    "p95_abs_error": 7.2777,
    "max_abs_error": 58.0785
  },
  {
    "slot": 1,
    "samples": 2612,
    "mean_abs_error": 0.1611,
    "p95_abs_error": 0.4577,
    "max_abs_error": 0.9965
  },
  {
    "slot": 2,
    "samples": 19040,
    "mean_abs_error": 0.1709,
    "p95_abs_error": 0.46,
    "max_abs_error": 1.0031
  }
]

## Candidate Integrity

a6daecc541e79fa86616d00bd1e356c35444c2d24f9dcec8f9dd7f4ba2295f9c  candidate/NA_StPaulsChapel_4x6_LOD2.fbx
628bc7e3fec35adb532ccf3142bb8a6f273120e44a8a6a83089bc292965669bf  candidate/NA_StPaulsChapel_4x6_LOD2_BaseColor.png
2354924fc8d6246dcbd463990f85f8961ba90d9886d05fe2487d9c713e1b31d3  candidate/NA_StPaulsChapel_4x6_LOD2_Normal.png
6022c712b1345b898eb01742de0bda9ecdfca066b1f02e821c68d50812281e71  candidate/StPaulsChapel-LOD2-Single-Atlas-OFFLINE.blend
2b1454ced811792d48a70d816dcad2d88a7f9aaa1017255c66da7a32904b42ad  readback.json
57e8fd99849d30af4c438092890c540b9e99adf9958ddcb349973ba7b33f6dc9  preview-audit.json
922248a762d5ee675c2ccfc48e6937dc73d8fb0bd7b6f6d3d56b6700b592a3ea  atlas.json


Candidate ZIP SHA-256 `90531a56ec89a4747c3dad32092e8fb8cbb49d280652fdf3573543e13bc94b71`; 8,262,203 bytes. Readback performed on cloud. No binary in this draft; no changes to main, game publishing or package claim.
