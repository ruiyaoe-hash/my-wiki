---
type: concept
title: "Claude Code Agent 循环机制"
description: "Claude Code 四种 Agent 循环（轮次/目标/时间/主动）的触发方式、停止标准和适用场景"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["Claude Code", "Agent Loop", "循环机制", "自动化"]
status: draft
domain: ai-engineering
related: ["Claude Code Goal 目标循环", "Claude Code 动态工作流", "Claude Code Routines 云端例程"]
source: "https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ"
source_label: "微信公众号：Claude Code 团队对 Loop 机制的四种分类及实践指南"
---

# Claude Code Agent 循环机制

## 一句话概括

所谓 Loop 就是 Agent 自己一轮一轮干活，不等人催。Claude Code 团队把循环分成了四种：你每发一句话启动的、你设个目标让 Claude 自己闯关的、定时自动触发的、和全自动流水线式的。

## 二八定理：四种循环一览

| 循环类型 | 怎么启动 | 怎么停 | 什么时候用 |
|----------|----------|--------|------------|
| 轮次循环 | 你发一句提示词 | Claude 自己判断干完了 | 探索、试水、没固定流程的短任务 |
| 目标循环 | /goal 设条件 | 条件达标 或 达到轮次上限 | 有明确「怎样算完成」的中大型任务 |
| 时间循环 | /loop 或 /schedule 定时 | 你取消 或 活干完了 | 定期重复的活、需要跟外部系统交互 |
| 主动循环 | 事件/定时（无需你在线） | 每个子任务完成自己的目标 | 长期运行的流水线：Bug 分类、迁移、依赖升级 |

### 最简单的理解方式

把四种循环想象成你跟工人打交道的方式：

- 轮次循环 = 你站在工人旁边，干一步看一步，每步都说「好，下一步做XX」
- 目标循环 = 你说「把房间打扫到一尘不染」，然后走开，工人自己反复擦直到你回来检查通过
- 时间循环 = 「每天早上八点来扫一遍」，说完就不管了
- 主动循环 = 「有人在门口放了快递你就收进来、脏了你就擦、缺东西你就买」，全自动运转

### 关键原则

质量保障：
- 代码库干净 -> Claude 会遵循已有模式
- 把验收标准写进 Skill -> Claude 能自己检查自己
- 让文档随手可查 -> 减少瞎猜
- 用第二个 Agent 做审查 -> 没人给自己找茬找得准
- 单次失败别修完就算 -> 把它写成系统规则防止下次

Token 管理：
- 小任务不用大炮打蚊子（不需要多 Agent 或循环）
- 说清楚「做到什么程度算完」-> 减少无效轮次
- 大规模前先在一小块上试点
- 确定性的活写脚本跑，别让 Agent 推理
- 间隔别太密，匹配实际变化频率
- 用 /usage 看明细

> 原文：[微信公众号 - 你说的完全正确（YAR师）](https://mp.weixin.qq.com/s/fyjE5EhnV1jKzE8NnscZDQ)
> 说明：基于 Claude Code 团队对 Agent Loop 的官方分类和实战指南的微信文章。
