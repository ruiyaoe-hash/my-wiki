---
title: LangGraph Memory 工作流记忆
created: '2026-07-06'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: developing
source: ChatGPT对话推荐（2026-07-06 会话），LangChain 生态的 Agent 工作流框架
related:
- '[[Letta 状态化Agent]]'
- '[[Mem0 记忆层]]'
- '[[Session管理]]'
- '[[多智能体系统]]'
tags:
- Agent记忆
- 工作流
- LangGraph
- LangChain
- Session管理
description: ChatGPT对话推荐的开源项目第四名。LangChain生态的Agent工作流框架，以状态图方式管理Agent记忆和任务流转。
---

# LangGraph Memory 工作流记忆

> 来源：ChatGPT 对话推荐（2026-07-06 会话）
> 定位：工作流 Agent 代表
> 生态：LangChain 生态的核心框架

## 核心定位

LangGraph 以有向状态图（StateGraph）的方式建模 Agent 的工作流和记忆管理。与 Letta 的"记忆 OS"定位不同，LangGraph 更侧重于任务状态的可视化和流程控制。

## 与 Letta 的关键差异

- **Letta**：以 Agent 自主管理记忆为核心，强调自我编辑、身份连续性、MemFS
- **LangGraph**：以工作流状态管理为核心，强调任务拆解、状态流转、检查点

两者不互斥，而是解决不同层面的问题：Letta 解决"Agent 记得什么"，LangGraph 解决"Agent 做到哪一步了"。

## 状态

> README 已入库：源/原文/LangGraph README.md。GitHub: https://github.com/langchain-ai/langgraph

## 相关页面

- [[Session管理]] — Agent 运行时状态管理
- [[Letta 状态化Agent]] — 状态化 Agent 的对比参照
- [[多智能体系统]] — 多 Agent 工作流编排
