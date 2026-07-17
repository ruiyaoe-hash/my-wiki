# Agent Runtime — AI Assistant Guide / AI 助手工作说明

This file tells any AI agent how to navigate and operate this system.
本文件告诉任何 AI 助手如何导航和操作系统。

## Key Directories / 关键目录

- knowledge/ — JSON metadata for every knowledge page / 知识页 JSON 元数据
- protocol/ — Protocol definitions (what the system can do) / 协议定义
- state/ — Runtime state (current task, session) / 运行时状态
- memory/ — Memory Store L0-L4 / 记忆存储
- planner/ — Task orchestration engine / 任务编排引擎
- event-bus/ — Component communication / 组件通信

## Entry Protocol / 进站协议

When entering, read in this order / 进站时按此顺序读取：
1. state/session.json — session status / 会话状态
2. state/current-task.json — current task context / 当前任务上下文

## Available Protocols / 可用协议

| Protocol | Trigger / 触发 | Description / 说明 |
|----------|----------------|-------------------|
| check | lint, check, 检查 | Full wiki health check / 全库健康检查 |
| ingest | ingest, 入库 | Import external content / 外部内容入库 |
| wrapup | wrapup, 收尾 | End session, archive state / 结束会话 |
| context-budget | auto | Token usage monitoring / Token 监控 |

## Self-Check / 自检清单

- Python: write .py files first, never use -c with multi-line / 先写 .py 文件
- Encoding: always UTF-8 for non-ASCII text / 非 ASCII 文本一律 UTF-8
- Chinese paths: use cmd /c or apply_patch, never PowerShell here-string
- Git: git rm --cached before branch switch is dangerous / git rm --cached 后切换分支危险
