---
title: 自我演化记忆 Self-Evolving Memory
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: ChatGPT对话（2026-07-06），八个研究热点之一（五星）
related:
- '[[AutoGenetic记忆引擎]]'
- '[[记忆巩固 Consolidation]]'
- '[[Ralph Loop]]'
- '[[Letta 状态化Agent]]'
tags:
- Agent记忆
- 自我演化
- 自进化
- 主动学习
- Agent
description: AI记忆领域八个前沿热点之一。记忆系统不应被动存储，而应主动从交互中提取模式、优化结构、生成新知识。
---

# 自我演化记忆 Self-Evolving Memory

> 来源：ChatGPT 对话（2026-07-06），八个研究热点中五星级重要
> 核心理念：记忆不是被动存储，而是主动生长

## 核心概念

自我演化记忆（Self-Evolving Memory）的核心主张是：AI Agent 的记忆系统不应该只是"存了什么就有什么"，而应该像生物记忆一样具有自组织、自优化、自生长的能力。

## 六个维度

1. **自主提取**：从交互中自动识别值得保留的模式，不需要人工标注
2. **自主组织**：根据使用模式自动调整记忆结构（分类、层级、关联）
3. **自主抽象**：从具体经历中提炼通用规则和策略
4. **自主矛盾消解**：识别新旧记忆之间的冲突并自行裁决
5. **自主遗忘**：基于价值判断而非简单的时间阈值决定保留/遗忘
6. **自主生长**：在不增加存储成本的前提下，让理解的深度和广度持续增长

## 与 AutoGenetic 的关联

华为 JiuwenMemory 的 [[AutoGenetic记忆引擎]] 是目前最接近"自我演化"理念的开源实现。它的基因式分层记忆（L0-L3）+ 交叉繁殖 + 群体记忆共享，本质上是给记忆装上了"演化"能力，而不仅是"存储"能力。

## 与 Memory as Metabolism 的关联

Memory as Metabolism 提供了实现自我演化的操作框架（TRIAGE → CONTEXTUALIZE → DECAY → CONSOLIDATE → AUDIT），而自我演化是这套框架在长期运行时涌现的高阶行为。

## 状态

> AutoGenetic记忆引擎（华为 JiuwenMemory）概念页已有覆盖。Memory as Metabolism 原文已入库。

## 相关页面

- [[AutoGenetic记忆引擎]] — 最接近的开源实现
- [[Memory as Metabolism 记忆代谢]] — 代谢框架
- [[记忆巩固 Consolidation]] — 自我演化的关键步骤
