---
title: SCM 睡眠巩固记忆
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: ChatGPT对话引用（2026-07-06）
related:
- '[[记忆巩固 Consolidation]]'
- '[[Memory as Metabolism 记忆代谢]]'
- '[[FadeMem 生物启发遗忘]]'
- '[[AI记忆的遗忘曲线]]'
tags:
- Agent记忆
- 睡眠巩固
- SCM
- 记忆衰减
- 学术论文
description: Sleep-Consolidated Memory，模拟人脑睡眠阶段的记忆巩固与主动遗忘机制。在保持高召回率的同时，将记忆噪声降低了90.9%。
---

# SCM 睡眠巩固记忆

> 来源：ChatGPT 对话引用（2026-07-06 会话）
> 定位：借鉴人脑睡眠机制的记忆巩固方案
> 关键数据：保持高召回率，记忆噪声降低 90.9%

## 核心概念

SCM（Sleep-Consolidated Memory）模拟了人脑在睡眠期间的两项核心记忆功能：

1. **记忆巩固（Consolidation）**：将白天的重要经历从海马体转移到皮层，形成长期记忆
2. **主动遗忘（Active Forgetting）**：清除不重要的细节和噪声，为新的学习腾出空间

## 90.9% 噪声降低的意义

这个数字说明 SCM 不是简单地"多存"或"少存"，而是"聪明地存"。它维持了高召回率（该记住的都记住了），同时大幅削减了噪声（不该记的都清理了）。这恰恰是当前大多数 Agent 记忆系统做不到的——它们要么全存导致噪声淹没信号，要么简单按时间淘汰导致丢失重要信息。

## 与 Wiki 的关联

当前 Wiki 的 check-protocol 有基于时间的衰老检测（90 天无更新 → stale），但这是"一刀切"的粗粒度遗忘。SCM 展示了一条更智能的路径：基于记忆内容的实际价值而非存储时间来决定保留/遗忘。

## 状态

> 原文已入库：源/原文/SCM Sleep-Consolidated Memory (2604.20943).md。论文 PDF: https://arxiv.org/pdf/2604.20943

## 相关页面

- [[记忆巩固 Consolidation]] — SCM 的理论基础
- [[Memory as Metabolism 记忆代谢]] — 同一方向的理论框架
- [[AI记忆的遗忘曲线]] — 祥瑞的热度衰减机制
