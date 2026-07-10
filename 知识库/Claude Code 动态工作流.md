---
type: concept
title: "Claude Code 动态工作流"
description: "动态工作流是用 JavaScript 脚本编排成百上千个子 Agent 的机制，核心价值是计划写死在代码里和对抗审查"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["Claude Code", "动态工作流", "Agent", "编排", "JavaScript"]
status: draft
domain: ai-engineering
related: ["Claude Code 并行 Agent 机制", "Claude Code Goal 目标循环"]
source: "https://code.claude.com/docs/en/workflows"
source_label: "Claude Code 官方文档：动态工作流编排子Agent指南"
---

# Claude Code 动态工作流

## 一句话概括

动态工作流就是用一段 JavaScript 脚本把成百上千个子 Agent 组织起来干活。核心区别是——普通对话里 Claude 是「边想边指挥」，工作流是「先写好剧本再执行」。剧本能反复用，还能让 Agent 互相挑刺。

## 二八定理：核心 20%

### 和子代理、技能的本质区别

| 方法 | 谁拿着计划 | 中间结果放哪 | 能管多少 Agent |
|------|------------|--------------|----------------|
| 子代理 | Claude（轮次判断） | Claude 的上下文 | 每轮几个 |
| 技能 | Claude（按提示执行） | Claude 的上下文 | 同子代理 |
| Agent 团队 | 队长 Agent | 共享任务清单 | 几个长期对等 Agent |
| 动态工作流 | 一段脚本（代码） | 脚本变量 | 几十到几百个 |

关键好处：计划变成代码后，你可以——
- 反复跑同样的流程（可复现）
- 让独立 Agent 互相对抗审查（比自己审查自己靠谱得多）
- 从多个角度分别出方案、再放在一起比较
- 上下文不炸——中间的脏活累活不占主对话 Token

### 怎么启动

方式一：说关键词 ultracode
```
ultracode: 审计 src/routes/ 下所有 API 端点有没有缺鉴权
```
Claude 会识别出来，写一段 JS 脚本编排多个子 Agent 干活。

方式二：全局开启 /effort ultracode
开了之后，每个复杂任务 Claude 都自己判断要不要用工作流。关掉用 /effort high。

方式三：跑写好的工作流
```
/deep-research Node.js v20 到 v22 权限模型改了什么？
```
/deep-research 是 Claude Code 自带的例子——会把问题拆成多个搜索方向、并行拉来源、交叉验证、输出带引用的报告。

### 工作流跑起来什么样

1. 启动前让你看一眼计划（几个阶段、多少 Agent、Token 预估），你说跑它才开始。
2. 后台跑着，不阻塞你继续聊天。
3. 用 /workflows 打开进度面板——能看到每个阶段跑了几轮、花了多少 Token、进去还能看每个 Agent 干了啥。
4. 跑完结果汇总给你。交叉验证没通过的内容已经被过滤掉了。

### 六个工作流模板（说人话版）

1. 全仓审计：「用工作流审计每个 API 路由有没有缺鉴权，让不同 Agent 互相验证」-> 一个文件一个 Agent，最后汇总交叉审查。
2. 死磕到底：「跑 npx tsc --noEmit，修报错，重复直到通过或连续两轮没进展」-> 修-查-修-查的循环。
3. 大批迁移：「把 src/components 下所有组件从 styled-components 迁到 Tailwind，每个文件单独隔离」-> 每个文件一个 Agent，互不干扰。
4. 分散审查：「审查这个 PR 里每个改的文件，然后合并成一份排序报告」-> 每个文件一个审查 Agent，最后汇总去重。
5. 竞品调研：「并行读三个对手的公开文档和 changelog，对比限流策略」-> 多路并行，最后综合比较。
6. 死磕 flaky 测试：「反复跑测试套件，找出间歇性失败，连续两轮没新发现就停」-> 耐心重复直到稳定。

### 关键能力：保存和复用

跑完一次成功的，在 /workflows 界面按 s 键保存。以后用 /你的名字 就能再跑。可以保存到项目里（团队共享）或自己目录（个人用）。

### 限制和成本

- 最多 16 个并发 Agent，总共最多 1000 个 Agent
- 比普通对话烧更多 Token——先在小子集上试点
- 中间不能插话打断（除非权限弹窗）
- 脚本里不能直接读写文件或执行命令（通过 Agent 间接做）

### 控制规模的配置

在 /config 里可以设大小偏好：small（<5 个）、medium（<15 个）、large（<50 个）、unrestricted（默认）。

> 原文：[Orchestrate subagents at scale with dynamic workflows](https://code.claude.com/docs/en/workflows)
> 说明：Claude Code 官方文档，详解动态工作流的原理、触发方式和六种典型编排模式。
