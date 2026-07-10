---
title: Agent记忆技术全景
created: '2026-06-27'
updated: '2026-06-27'
type: note
domain: ''
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Mem0 记忆层]]'
- '[[HippoRAG 记忆框架]]'
- '[[Letta 状态化Agent]]'
tags:
- Agent记忆
- 技术分类
- 认知架构
- 检索
- 框架
description: NirDiamant/Agent_Memory_Techniques (557 stars)。30 个可运行 Jupyter Notebook，覆盖
  Agent 记忆的六大分类：短期、长期、认知架构、检索路由、框架、评估生产。
---
# Agent 记忆技术全景

> 来源：NirDiamant/Agent_Memory_Techniques (557 stars) · 30 个可运行 Jupyter Notebook

作者 Nir Diamant 还著有《RAG Made Simple》（Amazon Bestseller in Generative AI）。此仓库是 Agent 记忆领域目前最全面的**可运行技术手册**。

---

## 六大分类（30 项技术）

| 分类 | 解决的问题 | 技术编号 |
|------|-----------|----------|
| **短期记忆** | 保留最近对话而不撑满上下文窗口 | 01 - 05 |
| **长期记忆** | 跨 Session、跨用户、跨时间的知识保存 | 06 - 11 |
| **认知架构** | 工作记忆、层级记忆、反思记忆系统 | 12 - 19 |
| **检索与路由** | 决定"回忆什么"和"何时回忆" | 20 - 23 |
| **框架** | 生产级记忆库（Mem0, Letta, Zep, Graphiti） | 24 - 27 |
| **评估与生产** | 测量、基准测试、部署记忆 | 28 - 30 |

---

## 行业关键信号

README 中明确列出了 2026 年记忆领域的六大方向：

1. **Anthropic 的 7 层记忆模型**（2026 年 3 月）：从对话上下文到跨项目知识，定义 Claude Code 的记忆层级
2. **Mem0**：托管记忆层，个性化 AI 快速采用
3. **Letta (MemGPT)**：自我编辑记忆 + inner/outer monologue 架构
4. **Zep**：面向 Agent 长期记忆的时间知识图谱
5. **Graphiti**：从情景记忆到语义记忆的知识图谱提取
6. **MemOS & Memori**：记忆即基础设施平台，面向生产级 Agent

---

## 与你 Wiki 的对照

你当前的 Wiki 涵盖的模式：

| Wiki 已有 | 对应技术分类 | 状态 |
|-----------|-------------|------|
| index.md 导航 | 检索路由 | ✅ 已实现 |
| log.md 时间线 | 长期记忆（时序） | ✅ 已实现 |
| wikilink 交叉链接 | 知识图谱（实体链接） | ✅ 人工维护 |
| frontmatter 结构化 | 语义记忆 | ✅ 已实现 |
| hot.md 热缓存 | 短期记忆 | ✅ 已实现 |
| 自动化 lint | 认知架构（反思） | ⚠️ 半自动 |
| 自动实体链接 | 长期记忆 | ❌ 未实现 |
| 多信号检索 | 检索路由 | ❌ 未实现 |
| Agent 自我编辑 | 认知架构 | ❌ 未实现 |

### 建议补齐的方向

1. **自动实体链接**——参照 Mem0/HippoRAG,让 Agent 自动识别新知识中已存在的实体并链接
2. **多信号检索**——语义搜索 + 关键词 + 实体匹配的融合检索
3. **Agent 自我编辑**——参照 Letta,Agent 能主动整理和优化已有知识结构
