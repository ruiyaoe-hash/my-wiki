---
type: summary
title: "Claude Code 动态工作流"
source: "https://code.claude.com/docs/en/workflows"
source_type: claude-docs
source_label: "Claude Code 官方文档：动态工作流编排子Agent指南"
domain: ai-engineering
date_retrieved: "2026-07-08"
tags: ['Claude Code', '工作流', 'Agent']
status: draft
---

# Claude Code 动态工作流 - 源摘要

## 来源
- URL: https://code.claude.com/docs/en/workflows
- 类型: Claude Code 官方文档
- 抓取日期: 2026-07-08
- 说明: Claude Code 官方文档，详解动态工作流的原理、触发方式和六种典型编排模式。

## 核心要点（80/20）

动态工作流是把编排逻辑写进 JS 脚本，让运行时在后台执行成百上千个子 Agent。核心差异：计划在代码里而非 Claude 的上下文里。

三种启动方式：prompt 中含 ultracode 关键词、/effort ultracode 全局开启、/deep-research 等内置命令。

关键能力：对抗审查（交叉验证）、保存复用（/workflows 界面按 s）、可中断恢复。

六种典型模式：全仓审计、检查-修复循环、大批迁移、分散审查、竞品调研、flaky 测试定位。

限制：16 并发、1000 Agent 上限。比普通对话费 Token，建议小规模试点。可在 /config 设规模偏好。
