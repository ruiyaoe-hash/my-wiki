---
type: summary
title: "Claude Code Goal 目标循环"
source: "https://code.claude.com/docs/en/goal"
source_type: claude-docs
source_label: "Claude Code 官方文档：/goal 目标循环机制详解"
domain: ai-engineering
date_retrieved: "2026-07-08"
tags: ['Claude Code', '/goal', '目标循环']
status: draft
---

# Claude Code Goal 目标循环 - 源摘要

## 来源
- URL: https://code.claude.com/docs/en/goal
- 类型: Claude Code 官方文档
- 抓取日期: 2026-07-08
- 说明: Claude Code 官方文档，详解 /goal 目标循环的设定、裁判机制和条件编写指南。

## 核心要点（80/20）

/goal 命令让 Claude 反复迭代直到指定条件满足。每轮结束后，一个小模型（Haiku）作为裁判检查条件是否达标。裁判只看对话记录，不自己跑命令。

好条件的三要素：可测量的终点 + 怎么证明 + 不能碰的底线。建议加轮次上限（如"最多 20 轮"）防止死循环。

黄金搭档：auto mode（单轮不打断）+ /goal（多轮不停）= 全自动。区别于 /loop（时间触发）和 Stop hook（自定义逻辑）。

会话可断点续传但计数归零。非交互模式也能跑：claude -p "/goal ..."
