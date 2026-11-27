# 哥大 Uris Hall：独立铺地与地块试放件（离线）

这是原 Uris Hall 三档包的可选补件，不替换任何原建筑、玻璃或窗体。打开 `Uris-Campus-Pavers-OFFLINE.blend` 可编辑；`UrisPavers/` 是独立 FBX 与 5 张 512px 材质图，只做平地视觉试放。放置时对齐建筑原点、朝向与 Z，不要自动用各自包围盒中心对齐。

- 在校园正面和东南边缘补三段铺地。初版与既有低处台阶有相交；缩回后逐个与建筑原包七个 FBX 做表面三角相交检测，全部为零。新铺地 548 三角面，每条边由两面共用。正面在部分位置留有间隔，不把该间隔或铺地视作可以通行的入口。
- 以每格名义 8m 计算，合放时用 10×12，西、东、南、北分别剩 5.70、2.28、1.90、7.50m。10×11 仅适合比较建筑本体；试铺地伸出其南界约 2.1m。地面高度是离线试值，不是校园高程。
- [哥大运营部门](https://operations.cufo.columbia.edu/content/uris-hall)记录东南无障碍坡道，[商学院资料](https://business.columbia.edu/behaviorlab/directions-uris-lab-morningside-campus)另有东侧楼梯下的地下双扇门。本包不合并两者，不猜坡道走向、高差、扶手或门槛，不建立寻路连线。未运行 CS2 Editor，未验证游戏碰撞、地形或自动读取贴图；未发布。

## Audit

{
  "pavers_fbx_triangles": 548,
  "all_mesh_edge_incidence": 2,
  "bounds_with_pavers": [
    [
      -34.29999923706055,
      37.720001220703125
    ],
    [
      -46.099998474121094,
      40.5
    ],
    [
      -0.1000061109662056,
      41.720001220703125
    ]
  ],
  "lot_10_12_actual_margin_W_E_S_N_m": [
    5.7,
    2.28,
    1.9,
    7.5
  ],
  "pavers_vs_seven_asset_fbx": {
    "NA_UrisHall_6x9.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_Gls.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_LOD1.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_LOD1_Gls.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_LOD1_Win.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_LOD2.fbx": {
      "intersection_pairs": 0
    },
    "NA_UrisHall_6x9_Win.fbx": {
      "intersection_pairs": 0
    }
  },
  "limitations": "No Editor, as-built grades, functional paths, collision settings or access certification."
}
a008f3b606f3e39e35d44652b35d92eb17eece278d6892b1d220ee64c3081822  UrisPavers/NA_UrisCampusPavers_Trial.fbx
211846daf5b6b174bafe6ee0a142c53ab91a97309a241dd6a2e939796a8f4fdc  UrisPavers/NA_UrisCampusPavers_Trial_BaseColor.png
074065f07e35265d9695cced0f42844dbb02e5766c4ed185d0a372b2d033b093  UrisPavers/NA_UrisCampusPavers_Trial_ControlMask.png
e9c4a470ad900801f7de4f9402eb27af8a1cc00eac80d618ef16bac39fb27d33  UrisPavers/NA_UrisCampusPavers_Trial_Emissive.png
1967943dfa41db2a89fe712a0e4d1a3ce6180101f3dcf4e5202bd96ad1716e91  UrisPavers/NA_UrisCampusPavers_Trial_MaskMap.png
82f11923d5e92211b66b39625b072ffe33f61bf04f348340efb7cdaf4fe207b4  UrisPavers/NA_UrisCampusPavers_Trial_Normal.png
b801ff9994ab0cb82b9960167690ac14ff3c0ae4828f9ff1f23d5e64744dbd8a  Uris-Campus-Pavers-OFFLINE.blend
8ff1181ecb2f3c305955704e57a0502baef31a5883ae161355443665b21b2715  prop-source.json
b420d58526f95685137e61465992c31c464de3d6309af221489b7e5836229b5b  readback.json
c875b95d3a328b01ac7ba1d7b49ca79a8485ff85a0424fd7258683e819154674  lot-preflight.json

ZIP SHA-256 `8fe9b25d5979d8c3913ccf368d3822f2975a591a7ffde9954237219925465585` (229,066 bytes). Original Uris model unchanged, no game test or publication.
