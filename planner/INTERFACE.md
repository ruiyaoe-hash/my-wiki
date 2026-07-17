# Planner — Component Interface / 组件接口

Source / 源码：`planner/planner.py`（Planner v0.1）

## Responsibility / 职责

Layer 2 Runtime Core 的执行引擎（见 `知识库/Agent Runtime 七层架构.md`，2026-07-17 裁决）。
Dynamic orchestration / 动态编排：
读 Task 队列 → 匹配 Protocol → 调 ProtocolExecutor 执行 → 发 Event → 归档到 Memory Store。

## Public API / 公开接口

- `TASK_TYPE_TO_PROTOCOL` — task_type → protocol_id 映射表；未知类型回退到 `check`
- `Planner()`：
  - `start_session(session_id=None) -> str` — 置 `session.json` 为 active，发 `session.started`
  - `end_session() -> str` — 置 session 为 ended，归档当前 Task 到 Memory，清空 L0 工作记忆，发 `session.ended`
  - `execute_next_task() -> dict | None` — 从 `task-queue.json` 弹出队首任务并写入 `current-task.json`，发 `task.started`
  - `run_task(task) -> bool` — 匹配并执行单个任务的 Protocol，按结果更新 current-task 并发完成/失败事件
  - `run_loop(max_tasks=5) -> int` — 主循环：开会话 → 连续执行队列任务 → 闭会话 → 事件历史落盘，返回完成数
  - `status() -> dict` — 队列长度 + 当前任务 + 事件历史数 + Memory 概览

## Events / 事件

- 发出（source=`'Planner'`）：`session.started` `session.ended` `task.started` `task.completed` `task.failed` `protocol.started` `protocol.completed` `agent.error`
- 消费：暂无（当前代码无 `subscribe` 调用，Phase 3 计划启用事件驱动）

## Files & Directories / 读写的文件与目录

- 读写（均经 StateManager，agent_id=`'Planner'`）：`state/session.json`、`state/task-queue.json`、`state/current-task.json`
- 写（经所依赖组件）：`memory/sessions/<session_id>.json`（MemoryStore.archive_task）、`event_bus/history/events.jsonl`（EventBus.persist）
- 不直接打开 `protocol/*.json`——Protocol 文件由 Executor 加载

## Dependencies / 依赖

- `state_manager/manager.py` — `StateManager`
- `executor/executor.py` — `ProtocolExecutor`
- `event_bus/event_bus.py` — `get_bus` / `Event` / `EventTypes`
- `memory/memory_store.py` — `MemoryStore`
