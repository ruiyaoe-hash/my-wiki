---
title: Agent Runtime v0.1
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- Agent-Runtime
- architecture
- wiki-evolution
---

# Agent Runtime v0.1

## 一句话定义

一个 **模型无关、工具无关、知识驱动、持续演化** 的 Agent 运行时。

任何 AI 助手进入后，不需要从头理解系统，而是通过标准化的 State -> Protocol -> Knowledge -> Memory 流程直接开始工作。

## 五代 Agent Knowledge System

| 代 | 名字 | 例子 | 作用 |
|---|------|------|------|
| 1 | Documentation | GitHub Wiki | 给人看 |
| 2 | PKM | Obsidian, Logseq | 帮人思考 |
| 3 | RAG | LangChain, NotebookLM | 帮 AI 检索 |
| 4 | Knowledge Runtime | 我们 | 让 AI 按协议执行 |
| 5 | Agent OS | 未来 | AI 自己维护运行环境 |


## 为什么不是管理知识，而是管理 AI 如何利用知识

很多人觉得自己是在做 PKM，其实还是在做笔记。这个系统的设计目标已经发生了质变：

- 旧问题：怎么把知识存好？
- 新问题：怎么让 AI 在正确的时刻、用正确的方式、调用正确的知识？

这是两个完全不同的问题。一个关心存储，一个关心执行。

## 核心区分

- 旧定位是 AI Wiki —— 知识存在 Markdown 里，AI 来读
- 新定位是 Agent Runtime —— 知识 + 协议 + 状态 + 执行引擎，AI 来跑

## 设计原则

1. 模型无关：Codex、Claude、GPT、Gemini 都能用同一套协议
2. 工具无关：今天是 Obsidian + Markdown，明天可能是 SQLite + API
3. 知识驱动：Planner 先查 Knowledge 再决定做什么，不是盲搜
4. 持续演化：EVR 方法论保证系统从真实使用中自我改进

## 与现有 Wiki 的关系

Wiki 不会消失，而是降级为 Runtime 的 Knowledge Store——只是一个存储适配层。
