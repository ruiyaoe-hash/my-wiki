# Agent Runtime — AI Assistant Guide / AI 助手工作说明

This file tells any AI agent how to navigate and operate this system.
本文件告诉任何 AI 助手如何导航和操作系统。

## Key Directories / 关键目录

- knowledge/ — JSON metadata for every knowledge page / 知识页 JSON 元数据
- protocol/ — Protocol definitions (what the system can do) / 协议定义
- state/ — Runtime state (current task, session) / 运行时状态
- memory/ — Memory Store L0-L4 / 记忆存储
- planner/ — Task orchestration engine / 任务编排引擎
- event_bus/ — Component communication / 组件通信
- tests/ — Component test suite / 组件测试套件
- scripts/ — Maintenance scripts (sidecar rebuild/validate, dependency graph) / 维护脚本（sidecar 重建与校验、依赖图生成）
- console/ — Web console (local web UI over the CLI) / 网页控制台（命令层之上的本地网页界面）

## Component Interfaces / 组件接口

Each runtime component documents its public API, events, and file I/O in its own INTERFACE.md:
每个运行时组件在自己的 INTERFACE.md 中记录公开接口、事件与文件读写：

- state_manager/INTERFACE.md — State coordination (lock/validate/merge/history/recover) / 状态协调
- event_bus/INTERFACE.md — Pub/sub event bus / 发布订阅事件总线
- memory/INTERFACE.md — Memory Store L0-L4 / 五层记忆存储
- executor/INTERFACE.md — Protocol Executor / 协议执行器
- planner/INTERFACE.md — Task orchestration engine / 任务编排引擎
- console/INTERFACE.md — Web console (local web UI) / 网页控制台

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

## Working Agreement / 合作方式

与库主协作的约定（2026-07-18 沉淀，双方确认）：

- 沟通：中文；解释用大白话（库主非技术背景），代码/命令/标识符保持原样
- 执行风格：小步可见，每步一句话进展；大任务拆小——不派"黑盒"长任务子代理（中途不可见，曾被误认为卡死）
- Git 纪律：commit/merge/tag/push/rm 等变更类操作先说明再执行，一次确认只管当次；**merge 后立刻跑测试**
- 分支纪律：develop 施工，验收通过当天合 main 打 tag，不倒挂过夜
- 编码纪律：一律 UTF-8；不用 PowerShell here-string 写文件；Python 先写 .py 再跑；rm --cached 后立即提交且不切分支
- 诚实纪律：宣称必须有运行证据（测试/文件/输出）；没验证过的部分明说没验证
- 发布纪律：对外动作（push、Release、改 GitHub 设置）单独确认
