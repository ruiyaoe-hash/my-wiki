---
type: source
title: "FadeMem：生物启发遗忘的 Agent 记忆架构"
description: "arXiv 2601.18642 论文摘要。双重记忆层级 + 自适应指数衰减 + LLM 记忆融合，45% 存储缩减。"
timestamp: "2026-06-28T12:00:00Z"
created: 2026-06-28
tags: [FadeMem, Agent记忆, 遗忘机制, 生物启发, 论文]
status: seed
related:
  - "[[FadeMem 生物启发遗忘]]"
  - "[[AI记忆的遗忘曲线]]"
  - "[[Agent记忆技术全景]]"
domain: ai-engineering
---

# FadeMem: Biologically-Inspired Forgetting for Efficient Agent Memory

**arXiv:** [2601.18642v2](https://arxiv.org/abs/2601.18642) | **发布:** 2026-01-26
**作者:** Lei Wei, Xiao Peng, Xu Dong, Niantao Xie, Bin Wang
**分类:** cs.AI, cs.CL

## 核心主张

当前 LLM Agent 面临关键的记忆瓶颈——缺乏选择性遗忘机制，导致要么在上下文边界处灾难性遗忘，要么在上下文内部信息过载。人类记忆通过自适应衰减过程自然地平衡保留和遗忘，而 AI 系统目前采用的是「要么全留、要么全丢」的二元策略。

## 方法

FadeMem 提出：
1. **双重记忆层级** — 快层（临时信息，高衰减）+ 慢层（长期知识，低衰减）
2. **自适应指数衰减** — 保留程度 = f(语义相关性 × 访问频率 × 时间模式)
3. **LLM 驱动的冲突消解** — 语义级判断，合并相关信息、丢弃冗余

## 实验

在 Multi-Session Chat、LoCoMo、LTI-Bench 三个基准上验证，实现 **45% 存储缩减** 同时保持或提升多跳推理和检索性能。
