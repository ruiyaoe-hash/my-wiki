---
title: Mesh Memory Protocol
created: '2026-06-27'
updated: '2026-06-27'
type: note
domain: ai-engineering
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[OpenRath]]'
- '[[Session管理]]'
tags:
- 语义基础设施
- 多Agent
- 跨Session
- 协议
- MMP
description: arXiv:2604.19540。多 Agent 跨 Session 认知状态共享的形式化协议。语义基础设施层——CAT7 七字段 schema
  + SVAF 锚点评估 + 跨 Agent lineage。
---
# Mesh Memory Protocol

> 来源：arXiv:2604.19540 · "Mesh Memory Protocol: Semantic Infrastructure for Multi-Agent Memory"

## 问题定义

MMP 定义了一个新概念：**跨 Session 的 Agent-to-Agent 认知协作**（cross-session agent-to-agent cognitive collaboration）。

传统 Agent 框架要么解决工具调用（function calling）、要么解决任务委派,但缺少一个协议层来处理"Agent A 在昨天 Session 里学到的认知状态,如何被今天的 Agent B 识别、评估、整合"。

## 三个核心问题 + 解决方案

| 问题 | MMP 方案 |
|------|---------|
| P1: Agent 如何逐字段决定接受/拒绝同行的信息 | **SVAF**：每个字段对照接收方角色锚点评估 |
| P2: 每个声明如何追溯到来源 | **跨 Agent lineage**：内容 hash 的 parents/ancestors 链 |
| P3: 记忆如何在 Session 重启后保持相关 | **相关性由存储方式决定,而非检索方式** |

## 四个组合原语

1. **CAT7**：固定的七字段 schema,用于每个 Cognitive Memory Block (CMB)
2. **SVAF**：逐字段评估,对照角色索引锚点
3. **跨 Agent lineage**：通过内容 hash 的父/祖先键追踪
4. **Mesh 拓扑**：记忆在 Agent 之间形成网状共享结构,而非中心化存储

## 核心论断

> "memory that survives session restarts is relevant because of how it was stored, not how it is retrieved."

翻译：跨会话记忆的价值,取决于**存储时有结构**,而非检索算法多好。这是对你 Wiki 的结构化管理最直接的理论背书。

## 与 OpenRath + OKF 的关系

- OpenRath 提供 Session 状态流动
- OKF 提供知识持久化格式
- **MMP 提供两者之间的语义协议**——这正是"第四次解耦"缺少的那层
