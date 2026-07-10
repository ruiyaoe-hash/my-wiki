---
title: Runtime Object 识别规则
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- ontology
- object-rule
- runtime
---

# Runtime Object 识别规则

## Perspective 声明

本系统以 Runtime 为观察视角，而不是以知识管理、存储实现或用户界面为观察视角。

## 一条规则

如果 Runtime 需要在某个时刻，用这个实体的标识符找到它、查询它的当前状态、并对它执行一个操作——那它就是一等对象。

三个要素缺一不可：

| 要素 | 含义 | 不满足的例子 |
|------|------|------------|
| 寻址 | 能用 ID 找到它 | Domain——没法寻址 |
| 状态查询 | Runtime 需要知道它的状态才能做决策 | Index——纯指针列表 |
| 执行操作 | 不只是读，还有写/改/删 | 标签——只能间接查询 |

## 判定示例

### 通过：Task

Runtime 能通过 task-id 找到它、查询 status（created/running/done）、执行 start/pause/complete。三个要素全部满足。

### 不通过：Domain

无法寻址一个具体的 Domain。Agent Memory 不是系统里的一个实体，它只是 Knowledge 对象的一个标签属性。

### 边缘：Capability

有名字 research，但 Runtime 会不会查询 research 的状态然后做决策？不会。Runtime 直接用 Workflow。Capability 更像一个标签层。


## 不需要 Non-Object.md

如果 Object Rule 足够清晰，不需要一个单独的文件列出什么不是 Object。三个判定示例就足够。
