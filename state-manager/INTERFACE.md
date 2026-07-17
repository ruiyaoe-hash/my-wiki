# State Manager — Component Interface / 组件接口

Source / 源码：`state-manager/manager.py`（State Manager v0.1）

## Responsibility / 职责

Multi-agent state coordination: lock, validate, read/write, merge, history, recover.
多 Agent 状态协调：乐观锁、schema 校验、读写、合并、历史记录、崩溃恢复。
多 Agent 同时操作同一份 state 时的唯一真相源（single source of truth）。

## Public API / 公开接口

`StateManager(state_dir=None)` — 默认指向仓库 `state/` 目录：

- `acquire(filename, agent_id, timeout_s=30) -> str | None` — 获取乐观锁，返回 lock token；超时返回 None
- `release(filename, token) -> bool` — 释放锁（token 匹配才释放）
- `read(filename) -> dict | None` — 读取 state JSON 文件
- `write(filename, data, agent_id) -> bool` — 校验 + 历史快照 + 带锁写入
- `validate(filename, data) -> bool` — 硬编码校验规则（Phase 2 计划改为加载 `state/state-schema.json`）
- `merge(filename, updates, agent_id, base_version=None) -> dict` — 基于 `_version` 字段的乐观并发合并，返回 success/conflict 信息
- `batch_write(file_data_map, agent_id) -> bool` — 多文件原子写入，任一失败全部回滚锁
- `get_history(filename, limit=10) -> list` — 最近变更历史
- `recover(filename) -> bool` — 从最近一条历史快照恢复
- `status() -> dict` — state 文件列表
- `health_check() -> dict` — 逐文件健康检查（readable / locked / history_depth）

## Events / 事件

- Emits / 发出：无
- Consumes / 消费：无

## Files & Directories / 读写的文件与目录

- 读写：`state/*.json`（`current-task.json`、`task-queue.json`、`session.json` 有硬编码必填字段校验）
- 写：`state/.locks/<file>.lock`（锁文件；超过 60s 视为 stale 自动清理）
- 写：`state/.history/<file>.history`（每次写入前快照旧值，每文件最多保留 50 条）

## Dependencies / 依赖

- 不依赖其他组件（仅 Python 标准库：json / os / time / pathlib / datetime）
- 被使用：Planner（agent_id=`'Planner'`）、Executor（agent_id=`'Executor'`）
