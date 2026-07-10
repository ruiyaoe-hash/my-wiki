---
type: source
title: "Generative Agents：交互式人类行为模拟"
description: "arXiv 2304.03442 论文摘要。Stanford 25 个 Agent 的 Sims 沙盒实验，观察→反思→规划记忆架构，涌现社交行为。"
timestamp: "2026-06-28T12:00:00Z"
created: 2026-06-28
tags: [Stanford, 生成式Agent, 记忆架构, 涌现行为, 论文]
status: seed
related:
  - "[[生成式Agent-Stanford小镇]]"
  - "[[Agent记忆技术全景]]"
  - "[[CoALA 认知架构]]"
domain: ai-engineering
---

# Generative Agents: Interactive Simulacra of Human Behavior

**arXiv:** [2304.03442v2](https://arxiv.org/abs/2304.03442) | **发布:** 2023-04-07
**作者:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein (Stanford)
**分类:** cs.HC, cs.AI, cs.LG

## 核心主张

可信的人类行为代理可以赋能从沉浸式环境到人际沟通排练再到原型工具的交互应用。本文提出「生成式 Agent」——模拟可信人类行为的计算软件代理。

## 架构

三个关键组件：
1. **观察 (Observation)** — 事件以自然语言记录为记忆流
2. **反思 (Reflection)** — 定期对记忆做层级抽象，形成高层认知
3. **规划 (Planning)** — 检索相关记忆，生成动态行动计划

## 实验

25 个 Agent 部署在 Sims 风格的沙盒环境 Smallville 中。著名案例：单个 Agent 的「办情人节派对」意图，在两天内自主涌现了邀请传播、约会配对、集体出席等完整社交行为链。

## 影响

Agent 记忆研究领域的奠基之作。公式 Agent = LLM + 记忆流 + 检索 + 反思 + 规划 被后续几乎所有工作继承。
