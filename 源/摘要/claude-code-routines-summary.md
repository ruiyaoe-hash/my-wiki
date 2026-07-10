---
type: summary
title: "Claude Code Routines 云端例程"
source: "https://code.claude.com/docs/en/routines"
source_type: claude-docs
source_label: "Claude Code 官方文档：云端例程自动化调度指南"
domain: ai-engineering
date_retrieved: "2026-07-08"
tags: ['Claude Code', 'Routines', '云端']
status: draft
---

# Claude Code Routines 云端例程 - 源摘要

## 来源
- URL: https://code.claude.com/docs/en/routines
- 类型: Claude Code 官方文档
- 抓取日期: 2026-07-08
- 说明: Claude Code 官方文档，详解云端例程的创建、触发方式和六种典型使用场景。

## 核心要点（80/20）

例程（Routine）是存于 Anthropic 云的 Claude Code 配置，电脑关机也能跑。一个例程 = prompt + 仓库 + 连接器 + 触发器。

三种触发：定时（cron）、API（HTTP POST）、GitHub（PR/Release 等事件）。一个例程可挂多种触发器。

六种典型场景：积压整理、告警响应、定制代码审查、部署验证、文档对齐、跨库同步。

在 claude.ai/code/routines 或 Desktop App 创建。跑的时候全自动无审批。属于个人账号，动作以你的 GitHub 身份出现。

区别于本地定时任务：云端可靠，不依赖本地开机。
