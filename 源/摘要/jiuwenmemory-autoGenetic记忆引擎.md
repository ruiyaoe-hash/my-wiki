
---
type: source
title: "华为开源 Agent 记忆引擎 JiuwenMemory：让记忆从存下来变成长出来"
description: "机器之心发布的华为 openJiuwen 社区开源 AutoGenetic Memory（JiuwenMemory）详细介绍。涵盖 L0-L3 分层记忆、AutoDreaming、MemoryTurbo、GraphMemory、Adapter 层和 Swarm Memory 六大核心技术。"
timestamp: "2026-06-30"
created: 2026-07-02
tags: [agent-memory, huawei, openjiuwen, open-source, machine-heart]
domain: ai-engineering
status: complete
source: "https://mp.weixin.qq.com/s/loIZliLAfYr4z2eedjmX1w"
raw: "_raw/articles/jiuwenmemory.txt"
---

# 华为开源 Agent 记忆引擎 JiuwenMemory

> 来源：机器之心（公众号） · 2026-06-30
> 原文链接：https://mp.weixin.qq.com/s/loIZliLAfYr4z2eedjmX1w
> raw 归档：`_raw/articles/jiuwenmemory.html`（HTML） + `jiuwenmemory.txt`（纯文本）

## 核心判断

当模型能力逐步趋同，Agent 的天花板从"能不能答对"转向"能不能持续记住同一个人"。JiuwenMemory 的答案是：记忆应该从被动存储变为主动生长。

## 关键技术要点

| 组件 | 一句话概括 | 关键数据 |
|------|-----------|---------|
| 分层记忆 (L0-L3) | 原始对话→摘要→结构化→画像，各归其位 | Token 成本大幅降低 |
| AutoDreaming | 模拟人类睡眠，后台异步加工记忆 | 在线零开销，Token 线性可控 |
| MemoryTurbo | 前台产气后台增压，越用越快 | 时延降低 80%，Token 再降 50%+ |
| GraphMemory | 孤立事实→关系网络，理解长期关联 | 多跳检索，解决语义遗漏 |
| Adapter 层 | Plugin/Provider 双维度解耦，平台无关 | 已支持 OpenClaw + Mem0 |
| Swarm Memory | 个体→组织级记忆池，一人经验全员受益 | 新 Agent 从零起步问题 |

## 评测数据

在 LoCoMo 基准上接入 OpenClaw，相较原生记忆：
- 准确率：提升 **15%**
- Token 消耗：降低 **60%+**

## 与现有对比

JiuwenMemory 与 [[Mem0 记忆层]] 开源了（Mem0 原生开源已有一段时间），但定位不同：
- Mem0 侧重新应用户级记忆 SDK，API 化
- JiuwenMemory 更强调记忆的自主生长与组织级群体共享
- 两者在 Adapter 层可以共存（Provider 维度已内置 Mem0）

## 相关概念页

- [[AutoGenetic记忆引擎]] — 知识库中的完整概念页面
- [[Mem0 记忆层]]
- [[外部记忆-行业全景]]
- [[Agent记忆技术全景]]
- [[OpenViking 上下文数据库]]
