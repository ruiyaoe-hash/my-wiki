---
type: source
title: "Claude Code Loop 循环机制完全指南"
source: "https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ"
source_type: wechat
source_label: "微信公众号：Claude Code 团队对 Loop 机制的四种分类及实践指南"
author: "你说的完全正确（YAR师）"
domain: ai-engineering
date_retrieved: "2026-07-08"
status: raw
tags: ["Claude Code", "Agent Loop", "循环机制", "Token管理"]
---

# Claude Code Loop 循环机制完全指南

> 原文链接：[微信公众号](https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ)

## 核心内容

Claude Code 团队对循环（Loop）的定义：Agent 重复执行工作周期，直到满足特定的停止条件。

### 四种循环类型

1. **轮次循环（Turn-based）** - 用户每次发提示词启动，Claude 自行判断何时完成。适合短任务。
2. **目标循环（/goal）** - 设定可验证的完成条件，评估模型判定是否达标。适合有明确标准的任务。
3. **时间循环（/loop, /schedule）** - 时间间隔触发，适合定期重复工作。本地用 /loop，云端用 /schedule。
4. **主动循环（Proactive）** - 事件/计划触发，组合 schedule + goal + workflow + auto mode。适合长期运行的流水线。

### 代码质量保障

- 保持代码库干净，Claude 会遵循已有模式
- 通过 Skill 文件记录团队认可的标准
- 让框架和库文档易于获取
- 使用第二个 Agent 做代码审查（偏见更少）
- 把单次失败纳入系统改进

### Token 管理

- 选合适的基础组件和模型
- 定义清晰的成功/停止标准
- 大规模前先试点
- 确定性工作用脚本而非推理
- 别太频繁运行例行程序
- /usage 查看详细用量

## 相关官方文档

- https://code.claude.com/docs/en/agents
- https://code.claude.com/docs/en/goal
- https://code.claude.com/docs/en/routines
- https://code.claude.com/docs/en/workflows
