# Changelog / ????

All notable changes / ?????? to this project will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased] — develop 分支

### Added (v0.2.0 计划)

- Knowledge Engine（knowledge/ + source/）
- 四种 Graph（Knowledge/Capability/Workflow/Dependency）
- Protocol 从 Markdown 升级为 YAML
- Memory 五层架构（Working/Session/Project/Semantic/Archive）

### Added — 2026-07-17 Phase 2
- knowledge/：81 篇知识页的 metadata JSON sidecar（schema: metadata-schema.json）
- source/：源材料归档目录（original/ + summaries/ + codebases/）
- graphs/：四种 Graph 的 schema 定义（dependency-graph-schema.json + graph-index.json）
- protocol/：4 个核心协议从 Markdown 升级为 JSON（check/ingest/wrapup/context-budget）+ 1 个 stub（capability-map）
- executor/executor.py：Protocol Executor v0.1（4 个 handler，smoke test 通过）

### Changed — 2026-07-17 Review 修正
- ontology.md v0.2：Memory Owner 更正、Session/State 边界明确、Protocol 当前位置如实反映、Event 定位升级为核心组件、Graph 新增为第 9 号预留对象
- manager.py：merge() 加 _version 乐观锁冲突检测、新增 batch_write() 和 health_check()
- AGENTS.md：State 层进站协议增加 下次工作计划.md 回退规则

### Added — 2026-07-17 Phase 3
- event-bus/event_bus.py：15 种事件类型的 pub/sub 总线 + history + persist
- memory/memory_store.py：五层记忆 L0-L4（Working/Session/Project/Semantic/Archive）
- planner/planner.py：动态编排引擎（dequeue → match → execute → archive）
- graphs/dependency.json：81 节点 380 边的实际依赖图数据
- agents/wiki-agent.py：首个通用 Wiki 维护 Agent（check + ingest）

### Added — 2026-07-17 v1.0 收尾
- executor v0.2：模板变量解析 + 10 个 handler（fetch_url/generate_summary/create_knowledge_page/generate_sidecar/update_index/emit_event 等）
- ingest 协议完整实现（5 步全链路：抓取→存档→摘要→知识页→索引）
- protocol/TEMPLATE.json：新用户自定义协议模板
- migration/migrate.py：旧目录→新结构迁移脚本
- README.md：重写为通用工具上手文档
- 全链路集成测试：6 项全部通过

---

## [0.1.0] — 2026-07-16

### Added

- `ontology/` 目录：Perspective + Object Rule + Ontology v0.1（7 个一等对象定义）
- `state/` 目录：4 个 JSON 文件（schema + session + task-queue + current-task）
- `state-manager/manager.py`：多 Agent 状态协调器（lock/validate/merge/history/recover）
- `policy.md`：Agent 权限矩阵 v0.1
- `CHANGELOG.md`：本文件

### Changed

- hot.md：TODO/进度迁移到 state/，hot.md 只保留不可变 Memory
- AGENTS.md：新增 State 层读取说明（进站先读 state 文件）

### 目录结构变化

```
新增：
  ontology/    ← Phase 0 产物
  state/       ← Phase 1 产物
  state-manager/ ← Phase 1 产物
  policy.md    ← Phase 1 产物

保留（Phase 2 迁移）：
  知识库/       → 将迁至 knowledge/
  源/           → 将迁至 source/
  agents/       → 将迁至 protocol/

旧版可用 git checkout v0.0-wiki 恢复。
```

---

## [0.0.0] — 2026-07-10

### Added

- 初始 Wiki 快照：80 篇知识页，3 域 7 子 MOC
- 54 篇源原文 + 51 篇源摘要
- 7 个 Agent 协议文件（agents/）
- 基础设施：AGENTS.md、hot.md、index.md、log.md
- README.md：AI 助手快速说明书
- GitHub 仓库创建：[ruiyaoe-hash/my-wiki](https://github.com/ruiyaoe-hash/my-wiki)

### Changed

- 系统定位从"AI Wiki"升级为"Agent Runtime v0.1"

---

## [0.0.0-wiki] — 2026-06-24 ~ 2026-07-08

原始 Wiki 阶段。标签：`v0.0-wiki`

- 69 篇知识页，3 域 MOC 架构
- 完整会话归档（2026-06-24 ~ 2026-07-08）
- MOC 架构重构、五层 index 角色定义、Harness 工程入库
- 知识生命周期引擎首次实验运行
