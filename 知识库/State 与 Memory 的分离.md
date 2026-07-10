---
title: State 与 Memory 的分离
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- state
- memory
- architecture
---

# State 与 Memory 的分离

## 核心区分

| 维度 | State | Memory |
|------|-------|--------|
| 性质 | 瞬时状态 | 不可变记录 |
| 生命周期 | Task 开始 -> Task 结束 -> 删除 | 记录后永久留存 |
| 谁写 | Planner 在执行中不断更新 | Memory Store 在收尾时追加 |
| 格式 | JSON，机器高频读写 | Markdown，人+AI 均可读 |
| 例子 | 第三步进行中，进度 62% | 2026-07-10 入库了 Harness 工程 |

## 为什么必须分开

现在的 hot.md 承担了三个职责：

- Working Memory：当前做到哪了
- Session Memory：这次会话干了什么
- Project Memory：下次要做什么

混在一起的结果：hot.md 越来越长，AI 恢复上下文越来越慢，两个不同 Agent 同时修改会冲突。

## 
## Memory 五层架构

| 层 | 名称 | 内容 | 生命周期 |
|---|------|------|---------|
| L0 | Working Memory | 本次 Task 瞬时上下文 | Task 结束清空 |
| L1 | Session Memory | 本次会话所有操作 | 会话结束归档 |
| L2 | Project Memory | 跨会话项目待办和进展 | 项目周期内 |
| L3 | Semantic Memory | 永久知识（现有 75 页） | 长期维护 |
| L4 | Archive | 历史归档 | 永久保存 |

hot.md 目前承担了 L0+L1+L2 三层，必须拆分。
拆分方案

### hot.md 保留

只存已发生的、不可变的事件记录。不要放 TODO、进度、当前任务。

### state/ 新建

- current-task.json：正在执行什么 Task，第几步，进度
- task-queue.json：排队中的 Task 列表
- execution-status.json：Runtime 当前状态

## 一句原则

凡是明天可能改变的，都不要放 hot.md。
