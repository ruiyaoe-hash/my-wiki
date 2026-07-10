---
title: Memory for Autonomous LLM Agents 综述
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: 2026年综述论文，Pengfei Du 等
related:
- '[[Agent记忆技术全景]]'
- '[[Memory in the Age of AI Agents 综述]]'
- '[[CoALA 认知架构]]'
- '[[外部记忆-行业全景]]'
tags:
- Agent记忆
- 综述
- 学术论文
- Memory Pipeline
- Benchmark
description: ChatGPT对话推荐的必读论文第四名，工程实践总结最好的一篇。重点讲Memory Pipeline、Benchmark、Evaluation、Architecture，覆盖2022到2026年初。
---

# Memory for Autonomous LLM Agents (2026)

> 来源：ChatGPT 对话推荐（2026-07-06 会话）
> 地位：目前工程实践总结最好的一篇综述
> 覆盖时间：2022 年到 2026 年初
> 评价：被 ChatGPT 评为"更适合开发 Agent"

## 核心贡献

这篇综述将 AI Agent 记忆系统按三个维度组织：

1. **Temporal Scope（时间维度）**：工作记忆、情景记忆、语义记忆、程序性记忆
2. **Representational Substrate（表示层）**：上下文文本、向量索引、结构化存储（SQL/KG）、可执行仓库、混合
3. **Control Policy（控制策略）**：启发式规则、提示自控、RL 学习控制

## 工程重点

- Memory Pipeline 的完整设计模式
- Memory Benchmark 的评估体系和对比
- Memory Evaluation 的方法论
- Memory Architecture 的最佳实践

## 对 Wiki 的意义

当前 [[Agent记忆技术全景]] 覆盖了 30 种记忆技术的分类，但主要偏概念分类。这篇综述提供的三维分析框架（时间×表示×控制策略）可以作为更系统化的分析工具。

## 状态

> 原文已入库：源/原文/Memory for Autonomous LLM Agents (2603.07670).md。论文 PDF: https://arxiv.org/pdf/2603.07670

## 相关页面

- [[Agent记忆技术全景]] — 30 种 Agent 记忆技术 Jupyter 分类
- [[Memory in the Age of AI Agents 综述]] — 同级别的全景综述
- [[CoALA 认知架构]] — 三个维度的理论基础
- [[外部记忆-行业全景]] — wiki 自建的行业扫描
