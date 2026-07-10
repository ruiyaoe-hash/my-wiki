---
type: concept
title: "Claude Code Goal 目标循环"
description: "/goal 命令的核心机制：设定完成条件，Claude 自动多轮迭代直到达标"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["Claude Code", "/goal", "目标循环", "自动化", "Agent Loop"]
status: draft
domain: ai-engineering
related: ["Claude Code 并行 Agent 机制", "Claude Code 云端例程"]
source: "https://code.claude.com/docs/en/goal"
source_label: "Claude Code 官方文档：/goal 目标循环机制详解"
---

# Claude Code Goal 目标循环

## 一句话概括

跟 Claude 说「把这个活干完再停」，而不是每步都你来催。Claude 自己一轮一轮干活，每轮干完让另一个「小裁判」看一眼是否达标，不行就接着干。

## 二八定理：核心 20%

### 怎么用

```
/goal 所有测试用例通过，且 lint 检查干净
/goal 主页 Lighthouse 分数提到 90 分以上，最多试 5 次
/goal CHANGELOG.md 包含本周所有已合并 PR 的条目
```

### 它的工作方式（幼儿园版）

1. 你说出「做到什么程度算完成」
2. Claude 开始干活（一轮）
3. 干完一轮，一个小裁判（Haiku 模型）看一眼
4. 裁判说「还没达标」-> Claude 接着干下一轮
5. 裁判说「达标了」-> 停下，交给你

关键细节：裁判不自己跑命令、不读文件。它只能看 Claude 在对话里说了什么。所以你的条件必须是「Claude 能在对话里证明给你看」的东西。

### 怎么写出好条件

一个顶用的条件分三块：
- 可测量的终点：测试通过、构建成功、文件数量达标、队列清空
- 怎么证明：npm test 退出码为 0、git status 是干净的
- 不能碰的底线：「不能修改任何别的测试文件」

再加个保险：「或者最多 20 轮后停下」——防止死循环烧 Token。

### 和别的东西怎么配合

| 功能 | 干什么的 |
|------|----------|
| /goal | 轮次之间不停，直到条件满足 |
| /loop | 隔一段时间就重跑，不看条件 |
| auto mode | 单轮里不问你就能调工具 |
| Stop hook | 每轮结束跑个脚本/让模型判定要不要停 |

黄金搭档：auto mode + /goal。auto mode 让 Claude 单轮不打断，/goal 让 Claude 多轮不停。两个一起开，你人就可以去喝咖啡了。

### 重要细节

- 一个会话只能有一个活跃的 goal。设新的会覆盖旧的。
- /goal（不带参数）看当前状态：跑了几轮、花了多少 Token、裁判上回说了啥。
- /goal clear 提前终止。
- 会话断了用 --resume 续上，goal 条件保留，但轮次计数和时间归零。
- 可以在非交互模式跑：claude -p "/goal ..."
- 裁判的 Token 费用很少，走小模型（默认 Haiku）。

> 原文：[Keep Claude working toward a goal](https://code.claude.com/docs/en/goal)
> 说明：Claude Code 官方文档，详解 /goal 的设定、裁判机制和条件编写指南。
