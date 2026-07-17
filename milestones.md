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
| 2026-07-10 | 定位升级为 Agent Runtime，确立 EVR 方法论 | 从"管理知识"转向"管理 AI 如何利用知识" |
| 2026-07-16 | Ontology 先行 + State/Memory 分离 | Phase 0/1 落地 |
| 2026-07-17 | Protocol 格式定稿 JSON（弃 YAML） | 零依赖原则，标准库即可解析 |
| 2026-07-17 | Planner 归 Layer 2 执行引擎 | 终局对抗性审查 #2 收口，消除文档内部矛盾 |
| 2026-07-17 | md frontmatter 为 sidecar 唯一事实源 | 终结 frontmatter/sidecar/schema 三方词汇漂移 |
| 2026-07-17 | Executor 缺失 handler 改 fail-fast | 杜绝协议假成功 |
| 2026-07-17 | 确认通用定位：无行业锁定，文旅 Agent 仅为历史提法 | 项目面向通用市场化 |

## 阶段性里程碑

| 日期 | 里程碑 |
|------|--------|
| 2026-06-24 | 知识库初始化，首批 5 篇知识页 |
| 2026-06-27 | 外部记忆行业全景入库，知识库扩展至 21 篇 |
| 2026-06-28 | 祥瑞三部曲入库（遗忘曲线 / KEA / Vault六件事） |
| 2026-06-28 | FadeMem + Stanford Generative Agents + MemGPT 三篇论文入库 |
| 2026-06-28 | AGENTS.md 拆分：启动只加载引导文件 + 按需激活协议 |
| 2026-07-10 | Agent Runtime v0.1 概念确立，GitHub 仓库建立 |
| 2026-07-16 | Phase 0+1 完成（Ontology + State Runtime） |
| 2026-07-17 | Phase 2+3 代码完成，v1.0.1 开源发布（38 文件纯运行时） |
| 2026-07-17 | v1.1.0：乱码修复 + 29 项测试全绿 + sidecar 统一重建 + 依赖图落盘（113 节点 286 边）+ 真实 ingest 端到端 + 多轮运行与恢复演示 |

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
