---
title: Zep 开源记忆平台
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: ChatGPT对话推荐（2026-07-06 会话），开源图记忆项目
related:
- '[[Mem0 记忆层]]'
- '[[Letta 状态化Agent]]'
- '[[外部记忆-行业全景]]'
- '[[Agent记忆技术全景]]'
tags:
- Agent记忆
- 开源
- 图记忆
- 企业级
- Zep
description: ChatGPT对话推荐的开源项目第三名，企业级长期记忆平台，基于图结构的记忆组织方案。
---

# Zep 开源记忆平台

> 来源：ChatGPT 对话推荐（2026-07-06 会话）
> 定位：企业级长期记忆平台
> 技术路线：图结构记忆组织

## 核心定位

Zep 是一个面向企业级 AI Agent 的开源长期记忆平台。与 Mem0 的通用记忆层定位不同，Zep 更侧重于图结构的知识组织和企业场景下的记忆管理。

## 与 Mem0 的关键差异

Mem0 采用 ADD-only 策略 + 多信号检索（语义 + BM25 + 实体匹配），而 Zep 以图数据库为核心，强调知识之间的结构化关系。两者的选择取决于场景需求：
- 需要快速、通用、低耦合的记忆层 → Mem0
- 需要结构化、可追溯、关系密集的企业知识 → Zep

## HN 社区数据

HN 评分为 6 分，说明社区认知度相对较低，但在企业级场景中有明确的适用边界。

## 状态

> README 已入库：源/原文/Zep README.md。GitHub: https://github.com/getzep/zep

## 相关页面

- [[Mem0 记忆层]] — 通用记忆层的对比参照
- [[Letta 状态化Agent]] — 另一个企业级 Agent 记忆方案
- [[外部记忆-行业全景]] — wiki 自建的行业扫描
