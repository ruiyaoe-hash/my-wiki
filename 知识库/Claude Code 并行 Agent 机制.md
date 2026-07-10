---
type: concept
title: "Claude Code 并行 Agent 机制"
description: "Claude Code 四种并行工作方式的本质区别、何时选用哪个"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["Claude Code", "Agent", "并行计算", "工作流"]
status: draft
domain: ai-engineering
related: ["Claude Code 动态工作流", "Claude Code 目标循环"]
source: "https://code.claude.com/docs/en/agents"
source_label: "Claude Code 官方文档：并行 Agent 机制对比"
---

# Claude Code 并行 Agent 机制

## 一句话概括

Claude Code 提供了四种让多个 Agent 同时干活的方法。区别在于谁当指挥、工人之间要不要交流、会不会改到同一个文件。

## 二八定理：核心 20%

### 四个方法的本质区别

| 方法 | 谁来指挥 | 工人之间交流吗 | 什么时候用 |
|------|----------|----------------|------------|
| 子代理 | Claude 在对话里分配 | 不交流，各自干完汇报 | 搜索日志、读大文件——活儿太大，塞不进主对话 |
| Agent 视图 | 你指挥，后台盯着 | 不交流，各自向你汇报 | 好几个独立任务，想批量派出去再回头看 |
| Agent 团队 | 一个队长 Claude 分配 | 共享任务清单互相发消息 | 一个项目要拆成多块、互相配合干 |
| 动态工作流 | 脚本（代码）指挥 | 可以不交流，也可以对抗审查 | 几百个文件要审计、大规模迁移、交叉验证研究 |

### 选哪个？问三个问题

第一问：谁当指挥？
- 让 Claude 在对话里分配和收结果 -> 子代理
- 你自己派活、回头看 -> Agent 视图
- Claude 当队长统一调度 -> Agent 团队
- 一段代码脚本当指挥 -> 动态工作流

第二问：工人需要互相说话吗？
- 不需要 -> 子代理 或 Agent 视图
- 需要 -> Agent 团队
- 需要对抗审查（互相找茬）-> 动态工作流

第三问：会改到同一个文件吗？
- 用 worktree（独立 git 工作区）隔离。Agent 视图自动隔离。子代理可以开。Agent 团队不自动隔离，需要自己分好文件领域。

### 怎么查看进度

- 后台 Agent -> claude agents 命令打开总控面板
- 当前会话的子代理 -> 输入 @ 可以看到状态
- 所有后台任务 -> /tasks
- 动态工作流 -> /workflows

### 容易被忽略但重要

- 所有的工人都是 Claude 会话。想用别的工具就给它配个 MCP Server。
- /batch 是打包好的一个技能，把大变更拆成 5-30 个隔离子代理各提一个 PR。它不算独立的协调方式。
- 后台 bash 命令 != Agent，fork 子代理 != 新机制，云端例程 != 本地并行。这些各是别的东西，别搞混。

> 原文：[Run agents in parallel - Claude Code Docs](https://code.claude.com/docs/en/agents)
> 说明：Claude Code 官方文档，详解四种并行机制的选择逻辑。
