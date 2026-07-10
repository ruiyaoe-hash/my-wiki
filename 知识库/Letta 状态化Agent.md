---
title: Letta 状态化Agent
created: '2026-06-27'
updated: '2026-06-27'
type: note
domain: ''
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Mem0 记忆层]]'
- '[[Session管理]]'
- '[[OpenRath]]'
tags:
- Agent记忆
- Letta
- MemGPT
- 状态化Agent
- 自我编辑
description: 前 MemGPT 团队，2.8k stars。状态化 Agent——Agent 有记忆、有身份、有经验、能自我编辑上下文。MemFS 用
  Git 管理所有 Agent 状态。
---
# Letta 状态化 Agent

> 来源：letta-ai/letta-code (2,768 stars) · 前身为 MemGPT

Letta Code 是一个**状态化 Agent 框架**。核心理念：Agent 应该更像人而不是工具——有记忆、有身份、有随着时间积累的经验感知。

---

## 关键特性

### 自我编辑记忆（Memory Blocks）
- Agent **编程式地重写自己的上下文**,随时间和经验持续优化
- 不只是"存下来",而是"主动整理自己的记忆"
- `/doctor` 命令审计记忆质量,`/palace` 命令可视化记忆结构
- 支持定期"做梦"（`/sleeptime`）：Agent 在空闲时主动整理和优化记忆

### MemFS：Git 管理 Agent 状态
- **所有上下文（包括记忆块）通过 Git 追踪**
- 可以同步到自定义 GitHub 仓库
- 有 commit 历史、可以 diff、可以回滚
- **这与 OKF 的 "知识即 Git 仓库" 完全同构**

### 技能学习
- Agent 能自己创造新技能并持久化
- 全局技能（`~/.letta`）、项目技能（`.agents/skills`）、Agent 专属技能（存 MemFS）

### 多 Agent + 子 Agent
- 内置通用子 Agent、fork Agent、recall Agent、history-analyzer
- Agent 可以调用任何其他 Agent（包括自己）作为子 Agent

### 全渠道接入
- CLI、桌面 App、浏览器（含移动端）、Telegram、Slack、Discord、自定义渠道

---

## 与你 Wiki 的关联

- **MemFS + Git** 和 OKF 的理念完全一致：知识/记忆应该像代码一样版本管理。
- **自我编辑记忆** 是"第四次解耦"的工程化参考——Agent 不只产出知识,还主动优化自己已有的知识结构。
- **定期做梦** 是 Wiki 自动化 lint 的参照——Agent 在空闲时主动检查断链、矛盾、过时内容。
