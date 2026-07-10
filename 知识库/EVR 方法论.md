---
title: EVR 方法论
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- methodology
- EVR
- system-evolution
- agent-engineering
---

# EVR 方法论

## 一句话定义

Extraction -> Validation -> Refinement：从已经工作的系统中发现隐含结构，通过真实运行验证，根据反馈持续修正。

## 三步走

### Extraction

不是发明新结构，而是从已有系统里把隐性结构显式化。

你的 ingest-protocol 已经隐含了 Source -> Summary -> Knowledge 三层对象关系。你的 wrapup-protocol 已经隐含了 State -> Memory 的转换边界。不做 Extraction 就去设计 Ontology，就是在猜。

### Validation

不是单元测试，而是用真实任务跑一遍。建了 State 层，跑一个完整的 research 任务，发现 Task 缺字段、State 和 Memory 边界模糊。不跑就不会发现。

### Refinement

根据 Validation 的结果修改系统定义。增加新对象、拆分模糊对象、废弃无用对象。不是一次性设计完，是持续改。

## 与其他方法论的对比

| 方法 | 特点 | 适合 |
|------|------|------|
| Architecture First | 先设计全部架构再写代码 | 需求完全确定的项目 |
| Code First | 先写代码再整理 | 快速原型 |
| EVR | 先跑起来，再萃取结构，持续修正 | 持续演化的 Agent 系统 |

## 为什么 EVR 适合这个项目

因为这个项目本身就是一个不断演化的系统。你的知识不是凭空设计出来的，是从论文、实践、协议中提炼的。Runtime 也应该从真实运行中萃取，而不是从一开始就设计完美。
