---
title: Agent Runtime 七层架构
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- architecture
- layered-architecture
- runtime-design
---

# Agent Runtime 七层架构

## 总览

Meta: EVR 演化机制（横向贯穿所有层）
Layer 0: Vision（稳定十年，一句定义）
Layer 1: Ontology Core（Perspective + Object Rule，一页锁死）
Layer 2: Runtime Core（State Store + Event Bus + Memory Store + Policy）
Layer 3: Knowledge + Capability（共同演化，不分先后）
Layer 4: Planner（动态编排工作流）
Layer 5: Application（Wiki Agent / 文旅 Agent / 研究 Agent）
Layer 6: Interface（Agent Workspace UI）

## 每层职责与 Exit Criteria

### Layer 0: Vision

永久不变的一句话：模型无关、工具无关、知识驱动、持续演化的 Agent Runtime。

### Layer 1: Ontology Core

产出：perspective.md + object-rule.md（仅一页，Phase 0 锁定）。不定义具体对象，只定义判定标准。

### Layer 2: Runtime Core

模块：State Store（含 lock/recover）+ Event Bus + Memory Store + 最简 Policy。
Exit：一个脚本能创建 Task、更新 State、写入 Memory、发 Event——不需要 AI 参与。

### Layer 3: Knowledge + Capability

模块：Knowledge Store + Source Store + 四种 Graph + Capability Registry + Protocol Executor。
Exit：Agent 自主完成一次 收 URL -> 入库 -> 生成知识页。

### Layer 4: Planner

职责：读 Task -> 查 Capability+Knowledge -> 编排 Workflow -> 调 Protocol -> 更新 State。
Exit：两个不同 Task 由 Planner 自动编排执行。

### Layer 5: Application

模块：Wiki 维护 Agent / 文旅策划 Agent / 研究 Agent。
Exit：至少一个 Agent 在生产环境持续运行 7 天。

### Layer 6: Interface

模块：Agent Workspace UI。
Exit：人类可以通过 UI 而非文件系统操作系统。

## 
## 四个 Primitive

| Primitive | 做什么 | 例子 |
|-----------|--------|------|
| File | 持久化、版本控制、跨工具共享 | Markdown 知识页 |
| State | 瞬时状态、任务队列、执行进度 | current-task.json |
| Graph | 实体间关系、推理路径、冲突检测 | typed relations |
| Execution | 调度、中断、恢复、执行 | Planner 循环 |

Runtime = Execution，不是 File + State + Graph。前三者是数据，Execution 才是 Runtime 本身。

## Graph 不是一种而是四种

| Graph 类型 | 节点是 | 边是 | 谁用 |
|-----------|--------|------|------|
| Knowledge Graph | 概念页 | supports/conflicts/extends | Agent 读知识时 |
| Capability Graph | 系统能力 | composed_of/prerequisite | Planner 选能力时 |
| Workflow Graph | 步骤 | next_success/next_failure | Planner 执行时 |
| Dependency Graph | 产出物 | derived_from/depends_on | 追溯来源 |

## State Manager + Multi-Agent 协调

State Manager 负责：Lock（乐观锁）、Validate（schema 校验）、Merge（冲突解决）、History（变更记录）、Recover（崩溃恢复）。

多 Agent 同时操作同一份 state 时，State Manager 是唯一真相源（single source of truth）。

## Event Bus

不轮询 State，消费 Event：KnowledgeIngested / PlannerCompleted / TaskFailed / NewSourceDetected / ConflictFound。

## Protocol 格式决策

- State：JSON（高频程序读写，需要 schema 校验）
- Protocol：YAML（人+AI 可读，低频修改）
- Config：TOML（可选，生态依赖）
关键设计决策

- Planner 不是 Runtime 的居民，而是 Layer 2 的执行引擎
- EVR 不是第七层，而是横向元过程，贯穿所有层
- Knowledge 和 Capability 共同演化，不分先后
- Ontology 拆成 Stable Core（锁死）+ Dynamic Catalog（持续迭代）
