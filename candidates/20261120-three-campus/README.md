# 哥大 19 件建筑的导入包复核

取回并验证 main `98587eeddab6ddf83a0c562efbf449207d633582` 的实际 Git LFS 数据。逐件核对 19 份 Blend 和 133 个分拆 FBX，三角数一致。以仓库可取得的主分支为本轮基线。之前私有精修 ZIP 下载返回 HTTP 403，该 ZIP 的内容未纳入这版候选。

## 几何和交付

Butler Library 10 面、Low Memorial Library 8 面、Mathematics Hall 4 面、St. Paul’s Chapel 近中各 2 面。仅移除源 FBX 中精确为零面积的三角。剩余顶点、面序、角点 UV、法线、材质、图像和边界通过 Blender 4.3.2 回导核对。每个修改过的 FBX 有五个固定角度的前后图，图像差异为 0。上下分别为修改前后，证据在 `same-view/`。用 `model_delta.py apply` 可从实际 LFS 原件重放79 个最终 FBX，包含这五份几何修补以及 74 份窗面/玻璃分拆修补。输入、差量和结果各有 SHA 核对。

当前候选的分拆 FBX 统一为二进制 7500、相对纹理名及一套可导入贴图。74 个特殊网格解除预览材质绑定。22 个玻璃 FBX 共修复 1,000 个塌缩 UV 面，只把这些面展开到空白区域，原有效 UV、几何和有效角点保持。36 个非空玻璃 FBX 全部通过最终 UV 回读。原主支同一项目的备用整组导出和编辑源档单存。`asset-audit.csv` 逐件给出实际大小，`asset-hashes.json` 给出每个文件的最终散列。PNG 存储减重保留原像素和其他数据块。

Lerner Hall 是建筑部位仍需处理的案例。近中档两份零顶点玻璃占位已从候选导入目录剔除，实景的玻璃与支撑仍待建模和验收。既有逐栋的尺寸、坡道和建筑形态疑点见 [逐栋复核](../../docs/building-by-building-review-20261119.md)。FBX 7500 已用 Blender 回读，CS2 Editor 与游戏内仍为 0/19。

[共同的重放工具及技术验收](https://github.com/YansongG-HKU/UChicago-Campus-CS2-Assets/tree/codex/full-source-technical-audit-20261118/candidates/20261120-three-campus)

从校验过的原克隆重放模型差量，请运行 `python model_delta.py apply /path/to/columbia-repo /new/replay-dir fbx-delta`。完整导入目录需要使用体积审计中所列的贴图、设置和其他网格。
