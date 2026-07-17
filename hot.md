## v1.1.0 验收完成（2026-07-17）

### 当前状态（每条均有运行证据）
- 测试：tests/ unittest 29 用例全绿（`python -m unittest discover tests`）
- 编码：protocol/、graphs/、migration/、CHANGELOG、log.md 乱码全部修复，migrate.py 恢复可运行
- Executor：15 个 handler，缺失 handler 改为 fail-fast；摘要支持可插拔 LLM（AGENT_RUNTIME_LLM_* 环境变量，默认提取式）
- Memory：record_type 丢失与 metadata 嵌套 bug 已修，L0-L4 落盘验证通过
- Observability：events.jsonl 追加式持久化 + state/execution-status.json 实时状态
- 多轮运行：wiki-agent `--loop 10` 无人工干预完成；kill → `--recover` 恢复演示 PASS
- 依赖图：graphs/dependency.json 真实落盘（113 节点 / 286 边 / 9 条断链待修）
- 真实 ingest：Engram 企业级记忆层 端到端入库（原文→摘要→知识页→sidecar→index）
- Schema：84 个 sidecar 按"md frontmatter 唯一事实源"重建，metadata-schema 对齐真实词汇
- P2 裁决收口：Planner 归 Layer 2 执行引擎、Protocol 定稿 JSON、5 个 INTERFACE.md、policy 覆盖全组件、ontology/catalog.json（Graph 激活）

### 项目定位
- Agent Runtime（主）/ Agent OS（愿景）：通用、无行业锁定、任何人 clone 即可用
- 文旅 Agent 为历史提法，非项目组成部分（2026-07-17 裁决）

### 旧目录（本地保留，不入仓库）
- 知识库/ — 82 篇个人知识页（.gitignore 排除）
- 源/ — 原始资料
- 工作台/ — 工作产出
- 归档/ — 历史会话
- agents/ — 旧 Markdown 协议（已迁移到 protocol/*.json）

## 最近会话

- 会话: 2026-07-17-003
- 状态: ended
- 任务: (无) — Phase 3 complete + v1.0.1 released
- 更新时间: 2026-07-17T14:16:44.096111+00:00
