---
title: Cognee 知识图谱记忆
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: ChatGPT对话推荐（2026-07-06 会话），知识图谱Memory代表项目
related:
- '[[Mem0 记忆层]]'
- '[[Zep 开源记忆平台]]'
- '[[HippoRAG 记忆框架]]'
- '[[外部记忆-行业全景]]'
tags:
- Agent记忆
- 知识图谱
- 开源
- graph-memory
- Cognee
description: ChatGPT对话推荐的开源项目第五名。以知识图谱为核心的Agent记忆方案，强调结构化关系而非向量相似度。
---

# Cognee 知识图谱记忆

> 来源：ChatGPT 对话推荐（2026-07-06 会话）
> 定位：知识图谱 Memory 代表
> 技术路线：以图结构为核心组织 Agent 记忆

## 核心定位

Cognee 是专门面向 AI Agent 的知识图谱记忆方案。与 Mem0 的多信号混合检索不同，Cognee 的核心竞争力在于结构化关系的表达和推理。

## 与 Mem0 / Zep 的关键差异

- **Mem0**：ADD-only + 多信号混合检索，强调通用性和低耦合
- **Zep**：图结构 + 企业级，强调可追溯和治理
- **Cognee**：纯知识图谱路线，强调结构化推理和关系发现

## 适用场景

适合需要复杂关系推理的 Agent 场景——例如多实体关联分析、因果链追溯、层级知识组织。在简单的对话记忆场景下可能是 overkill，但在专业领域 Agent（如文旅策划的多维度分析）中有独特价值。

## 状态

> README 已入库：源/原文/Cognee README.md。GitHub: https://github.com/topoteretes/cognee。研究论文: https://arxiv.org/abs/2505.24478

## 相关页面

- [[Mem0 记忆层]] — 通用记忆层的对比参照
- [[HippoRAG 记忆框架]] — 另一个图结构记忆方案
- [[外部记忆-行业全景]] — wiki 自建的行业扫描
