# Lerner Hall 校园侧幕墙定位

以哥大草稿 `de9422e5084bfe7a5589ed8e062222db619edecf` 的 LernerHall 离线候选为基线，用 Blender 4.3.2 回导近、中档 Base 和 Win，按世界法线、共平面位置与三角面积分组。原始测表见 `lerner-planes.json`，模型单位为米，校园侧朝 −Y。

- 近、中档 Base 在 Y −31.60 m 各有一组中央上横构件，范围 X −6.10…21.10 m、Z 17.85…18.10 m。近档 Y −31.66 m 的中央横构件也可定位。
- 近、中档 Win 的一组地面窗墙面在 Y −32.54 m，四个三角总面积 161.7 m²，合并包围盒横跨左右翼。它不能用来代指中央通高幕墙。候选里的近、中档专用 Gls 仍未建成。
- 校方说明校园侧幕墙面积约 5,600 ft²（约 520 m²），并以档案记录点支玻璃与可见坡道。设计方确认两翼由连续坡道连接。监测面积包含的具体面和竣工控制位置仍待核，不能单凭总面积确定宽和高。原仓说明也记录了内部坡道未做。[校方建筑档案](https://www.columbia.edu/cu/lernerhall/docs/History_and_Architecture/index.html) · [Bernard Tschumi 项目页](https://www.tschumi.com/projects/13)
- 设计方公开项目图的独立下载在当前云环境返回 HTTP 403。图名和模型坐标都不足以核验现状的玻璃头、底、点连接和坡道锚位。中央幕墙候选继续待证，CS2 验收待做。

重放时执行 `blender -b --factory-startup --python-exit-code 1 --python lerner_planes.py -- /path/to/LernerHall /new/lerner-planes.json`。这份证据只定位现有候选的平面，供下一次图纸配准及从外侧验证内部坡道使用。
