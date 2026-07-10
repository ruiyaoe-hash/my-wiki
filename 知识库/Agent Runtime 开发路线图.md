---
title: Agent Runtime 开发路线图
created: "2026-07-10"
updated: "2026-07-10"
type: note
tags: [roadmap, development-plan, phase-planning]
---

# Agent Runtime 开发路线图

## 开发哲学

不用代码行数衡量进度。用四个问题：

1. 抽象是否更稳定？（对象、边界、职责是否更清晰）
2. 系统是否真正跑起来？（哪怕功能很少，但能持续执行）
3. 是否能服务真实工作？（先服务 Wiki 维护 Agent 和文旅策划 Agent）
4. 系统是否因为真实使用而变得更简单，而不是更复杂？

这不是一个产品开发项目，而是一个长期 Research Engineering Project。真正要沉淀的不是某个版本的代码，而是一套能够不断诞生 Agent、不断吸收新模型、不断适应新工具的工程体系。

## Phase 0：Schema Extraction（1小时）

### Step 0a — Perspective + Object Rule
perspective.md：本系统以 Runtime 为观察视角。
object-rule.md：Runtime 能寻址 + 查询状态 + 执行操作 = 一等对象。

### Step 0b — Object Discovery
从现有 75 页 knowledge + 7 个 protocol + hot.md 中发现对象。
不设计，只发现。不定义 Schema，只列出对象。

### Step 0c — Ontology v0.1
每个对象：一句话定义、生命周期、Owner、Consumer。不含 Schema。

## Phase 1：State Runtime（1-2周）

新建：state/ 目录 + JSON schema + state-manager/ + event-bus/ + policy.md
State Manager：lock/validate/merge/history/recover
Exit：脚本创建 Task、更新 State、写入 Memory、发 Event——不需要 AI

## Phase 2：Knowledge + Capability（2-4周）

四种 Graph：Knowledge/Capability/Workflow/Dependency
Memory 五层：Working/Session/Project/Semantic/Archive
Protocol 格式：State->JSON, Protocol->YAML, Config->TOML
Exit：Agent 自主完成 收 URL -> 入库 -> 生成知识页

## Phase 3：Planner + Application（4-6周）

Planner 动态编排，不是固定 YAML 模板
首个 Application：Wiki 维护 Agent
Exit：Agent 生产环境持续运行 7 天无人工干预

## Phase 4：Interface（未来）

Agent Workspace UI：隐藏所有底层细节
Exit：人类可通过 UI 而非文件系统操作系统

总计约 2-3 个月到 Phase 3 完成。