---
type: concept
title: "Claude Code Routines 云端例程"
description: "例程是保存在云端的 Claude Code 配置，可以定时、API 触发或 GitHub 事件触发自动运行"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["Claude Code", "Routines", "云端", "自动化", "调度"]
status: draft
domain: ai-engineering
related: ["Claude Code Goal 目标循环", "Claude Code 动态工作流"]
source: "https://code.claude.com/docs/en/routines"
source_label: "Claude Code 官方文档：云端例程自动化调度指南"
---

# Claude Code Routines 云端例程

## 一句话概括

例程就是把「让 Claude 干的活」打包存到 Anthropic 的云上，它可以定时自动跑、别人调用 API 触发它跑、或者 GitHub 有动静时自动跑——你的电脑关了一样干。

## 二八定理：核心 20%

### 例程是什么

一个例程 = prompt（你要它干啥）+ 代码仓库 + 连接器（Slack/Linear/Jira等）+ 触发器（何时启动）。

它在 Anthropic 的云服务器上跑，不是在你电脑上。跑的时候是全自动的——没有人机对话、没有审批弹窗、一路自己干到底。

### 三种触发方式

| 触发方式 | 什么时候跑 | 典型场景 |
|----------|------------|----------|
| 定时 | 每小时/每天/每周，或指定时间 | 每天早上整理 Issue 队列、每周扫描文档过时 |
| API | 你发一个 HTTP POST 给它 | 部署后自动做冒烟测试、监控告警时自动排查 |
| GitHub | PR 开了/合了、release 发了 | 自动审查代码风格和安全问题、自动把改动同步到另一个仓库 |

一个例程可以同时挂多种触发器。比如：每天定时跑 + 每个新 PR 也跑 + 部署脚本也可以手动调用。

### 六个真实使用场景

1. 积压整理：每天晚上定时，自动给新 Issue 打标签、分配给对应负责人、发 Slack 汇总。
2. 告警响应：监控工具调 API 触发例程，自动分析错误栈、关联最近提交、直接开 draft PR 修。
3. 定制代码审查：每个新 PR 触发，按团队自己的检查清单审查，人只需要看架构设计。
4. 部署验证：CD 流水线部署后调 API，自动跑冒烟测试、检查错误日志、发 go/no-go。
5. 文档对齐：每周扫描已合并 PR，发现文档引用了被改掉的 API 就自动开 PR 更新。
6. 跨库同步：SDK-A 的 PR 合了，自动把相同改动搬到 SDK-B，保持两边同步。

### 创建和管理的要点

- 在 claude.ai/code/routines 网页上创建，或在 Desktop App 里创建。
- prompt 是最关键的部分——因为没人盯着，prompt 必须自给自足，说清楚做什么、成功标准是什么。
- 代码仓库：每次运行从默认分支 clone，Claude 在 claude/ 前缀的分支上干活。
- 环境（Environment）：控制例程能上网到什么程度、有什么密钥、需要装什么工具。
- 例程属于你的个人账号，不跟团队共享。它做的事都以你的 GitHub 身份出现。

### 和本地调度的区别

|  | 云端例程 | 本地定时任务 |
|--|----------|--------------|
| 跑在哪 | Anthropic 云 | 你的电脑 |
| 电脑关了还能跑 | 能 | 不能 |
| 创建方式 | claude.ai/code/routines 或 App | Desktop App 选 Local |
| 适合 | 需要可靠运行的生产任务 | 个人开发辅助 |

> 原文：[Automate work with routines](https://code.claude.com/docs/en/routines)
> 说明：Claude Code 官方文档，详解云端例程的创建、触发方式和六种典型使用场景。
