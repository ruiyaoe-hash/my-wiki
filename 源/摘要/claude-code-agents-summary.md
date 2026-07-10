---
type: summary
title: "Claude Code 并行 Agent 机制"
source: "https://code.claude.com/docs/en/agents"
source_type: claude-docs
source_label: "Claude Code 官方文档：并行 Agent 机制对比"
domain: ai-engineering
date_retrieved: "2026-07-08"
tags: ['Claude Code', 'Agent', '并行']
status: draft
---

# Claude Code 并行 Agent 机制 - 源摘要

## 来源
- URL: https://code.claude.com/docs/en/agents
- 类型: Claude Code 官方文档
- 抓取日期: 2026-07-08
- 说明: Claude Code 官方文档，详解子代理/Agent视图/Agent团队/动态工作流四种并行机制的选择逻辑。

## 核心要点（80/20）

该文档对比了 Claude Code 中四种并行工作方式：
1. 子代理（Subagents）：Claude 在对话中派出的工人，干完汇报。适合搜索、读文件等侧任务。
2. Agent 视图（Agent View）：用户批量派出独立任务、后台监控的仪表盘。
3. Agent 团队（Agent Teams）：队长 Claude 协调多个对等 Agent，共享任务清单互发消息。
4. 动态工作流（Dynamic Workflows）：JS 脚本编排成百上千 Agent，可做对抗审查。

选择取决于三个问题：谁指挥、工人交流吗、会改同一文件吗。Worktree 机制为并行会话隔离 git 工作区。

## 关联知识页
- [[Claude Code 并行 Agent 机制]]
- [[Claude Code 动态工作流]]
- [[Claude Code Agent 循环机制]]
