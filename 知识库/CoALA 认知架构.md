---
title: CoALA 认知架构
created: '2026-06-27'
updated: '2026-06-27'
type: note
domain: ''
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Agent记忆技术全景]]'
tags:
- 认知架构
- Agent设计
- 记忆模块
- 学术论文
description: 普林斯顿等团队提出：Cognitive Architectures for Language Agents。将模块化记忆组件定义为语言 Agent
  架构的核心要件——记忆是第一公民。
---
# CoALA 认知架构

> 来源：arXiv · "Cognitive Architectures for Language Agents" · 普林斯顿等团队

## 核心框架

CoALA 借鉴认知科学和符号 AI 的丰富历史,为语言 Agent 提出了一套系统框架：

```
Agent = 记忆模块 + 行动空间 + 决策过程
```

- **记忆模块**：不是可选附加功能,而是架构的核心要件
- **行动空间**：与内部记忆和外部环境交互的结构化操作
- **决策过程**：选择行动的通用决策机制

## 与 Wiki 范式的关系

CoALA 的框架可以从架构层面解释"为什么 Wiki 比 RAG 更根本"：

- RAG 只解决了行动空间中的"检索外部信息"这一步
- Wiki + Agent 记忆则覆盖了记忆模块的全部生命周期：存储 → 更新 → 链接 → 检索 → 推理
- CoALA 把"记忆"定位为与"决策"并列的架构支柱——这从理论上支撑了"记忆即基础设施"的判断
