---
title: Ralph Loop（Anthropic 内部 Agent 工作模式）
created: '2026-06-28'
updated: '2026-06-28'
type: note
domain: ''
status: seed
related:
- '[[Agent记忆技术全景]]'
- '[[外部记忆-行业全景]]'
tags:
- Agent架构
- Anthropic
- 工作模式
- 未确证
description: 用户提到的 Anthropic 内部 Agent 循环模式。当前公开资料中无法找到确切出处。可能与 Anthropic 五种工作流模式（Prompt
  Chaining / Routing / Parallelization / Orchestrator-Workers / Evaluator-Optimizer）之一或其复合嵌套有关。
---
# Ralph Loop

> 状态：**未确证**。2026-06-28 在 GitHub/arXiv/DuckDuckGo/Anthropic 工程博客上均未找到名为 "Ralph Loop" 的特定模式。标记为待补线索。

## 已知背景

用户提到 Anthropic 内部有一个叫「Ralph Loop」的工作模式。推测属于 Agent 循环执行类模式的内部命名。

## Anthropic 公开的五种 Agent 工作模式

来源：[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) · 2024 年 12 月

| 模式 | 逻辑 |
|------|------|
| **Prompt Chaining** | 多个 LLM 调用顺序执行，前一步输出为后一步输入 |
| **Routing** | 分类输入，路由到专门处理器 |
| **Parallelization** | 多个 LLM 并行调用，汇总结果 |
| **Orchestrator-Workers** | 一个中心 LLM 动态分配任务给多个工人 |
| **Evaluator-Optimizer** | 一个生成，一个评估，反馈循环持续优化 |

Ralph Loop 有可能是这五种之一的内部代号，也可能是其中几种的**复合嵌套模式**（如 Prompt Chaining + Evaluator-Optimizer 的循环），由某位 Anthropic 工程师命名并内部使用。

## 待补线索

- 来自哪篇公众号/播客/分享？
- 具体的循环流程是什么？
- 适用场景是什么？
