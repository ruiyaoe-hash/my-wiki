---
type: summary
title: "Claude Code 循环机制（微信文章）"
source: "https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ"
source_type: wechat
source_label: "微信公众号：Claude Code 团队对 Loop 机制的四种分类及实践指南"
domain: ai-engineering
date_retrieved: "2026-07-08"
tags: ['Claude Code', 'Loop', '循环']
status: draft
---

# Claude Code 循环机制（微信文章） - 源摘要

## 来源
- URL: https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ
- 类型: 微信公众号文章
- 作者: 你说的完全正确（YAR师）
- 抓取日期: 2026-07-08
- 说明: 基于 Claude Code 团队对 Agent Loop 官方分类的微信解读文章。文章末尾引用了四篇 Claude Code 官方文档。

## 核心要点（80/20）

Claude Code 团队定义 Loop = Agent 重复执行工作周期直到满足停止条件。分为四大类：

1. 轮次循环：用户每次发提示词启动，Claude 自行判断完成。适合短任务。
2. 目标循环（/goal）：设可验证条件，评估模型判定。适合有明确标准的任务。
3. 时间循环（/loop /schedule）：定时触发。本地用 /loop 云端用 /schedule。
4. 主动循环：事件/计划驱动，组合 schedule + goal + workflow + auto mode。

文章还涵盖了代码质量保障和 Token 管理策略。

## 引用文档
- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/goal
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/workflows
