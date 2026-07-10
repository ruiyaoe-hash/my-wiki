---
title: Schema Extraction 方法
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- ontology
- schema
- extraction
- methodology
---

# Schema Extraction 方法

## 一句话定义

从已经工作的系统里，把隐性的对象结构显式化。不是 Design，不是 Invent，而是 Discover。

## 与 Ontology Design 的区别

| | Ontology Design | Schema Extraction |
|---|---|---|
| 前提 | 我还没写代码，但我能设计出对象 | 我已经跑了两个月的系统 |
| 方法 | 演绎（从理论推导） | 归纳（从实践中发现） |
| 风险 | 设计出来的对象后来发现不需要 | 提取时可能漏掉边缘对象 |
| 适合 | 新项目 | 本项目 |

## 具体步骤

1. 扫协议文件：ingest-protocol 隐含了 Source -> Summary -> Knowledge；wrapup-protocol 隐含了 State -> Memory
2. 扫 hot.md：标题结构隐含了 Working / Session / Project 三层 memory
3. 扫知识页：69 页的命名和 frontmatter 隐含了 Knowledge 的属性结构
4. 过 Object Rule：把候选对象逐一过 Runtime Object 识别规则

## 为什么不用 Ontology Design

因为这个项目不是白纸。已经有 69 页知识、7 个协议、完整的操作日志和会话归档。强行从零设计一套 Ontology 等于扔掉过去两个月的运行经验。Schema Extraction 让这些经验变成资产，而不是推倒重来。
