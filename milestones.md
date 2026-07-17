# milestones

> 项目决策记录 + 里程碑台账。与 hot.md 分工：hot.md 是运行时快照（每次刷新），milestones.md 是累积历史（只追加不覆盖）。

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-06-24 | Wiki 底座选 Obsidian + Markdown | 本地优先、AI 直接读写、零锁定 |
| 2026-06-27 | 外部记忆纳入 Wiki | Mem0/HippoRAG/Letta/CoALA 等方案验证 Wiki 范式长期成立 |
| 2026-06-28 | AGENTS.md 新增工具能力地图 | 从 祥瑞 Vault 文章中提取，12 条工具链 |
| 2026-06-28 | AGENTS.md 新增上下文用量预警 | 基于 Lost in the Middle 研究的 50K/100K/200K 三级阈值 |
| 2026-06-28 | MEMORY.md 拆分为 hot.md + index.md + log.md 三文件 | 祥瑞三层记忆模式，启动只读索引 |

## 阶段性里程碑

| 日期 | 里程碑 |
|------|--------|
| 2026-06-24 | 知识库初始化，首批 5 篇知识页 |
| 2026-06-27 | 外部记忆行业全景入库，知识库扩展至 21 篇 |
| 2026-06-28 | 祥瑞三部曲入库（遗忘曲线 / KEA / Vault六件事） |
| 2026-06-28 | FadeMem + Stanford Generative Agents + MemGPT 三篇论文入库 |
| 2026-06-28 | AGENTS.md 拆分：启动只加载引导文件 + 按需激活协议 |

## 未决问题

- Wiki 内容价值分类体系（用户说"好好想想"，待定）
- 语义去重 ingest 脚本（待实现）
- vault-gardener 健康巡检（待实现）
- Ralph Loop 确切出处待查（用户线索，公开资料未确证）

## 踩过的坑

| 日期 | 坑 | 解决 |
|------|-----|------|
| 2026-06-24 | 微信公号 HTML 提取只用一种 regex | 升级为三层策略（标准 / content_noencode / 纯 JS） |
| 2026-06-27 | Python -c 多行脚本在 PowerShell 中转义失败 | 改为写 .py 文件再运行 |
| 2026-06-27 | curl.exe 直接调 GitHub API 频繁 403 | 改用 Python urllib + User-Agent header |
| 2026-06-28 | 微信 URL 重新提取返回同一篇文章 | 确认是 URL 映射错误，raw 文件标注来源 |
