# Event Bus — Component Interface / 组件接口

Source / 源码：`event_bus/event_bus.py`（Event Bus v0.1）

## Responsibility / 职责

Central pub/sub for the Agent Runtime. Events are typed, immutable, fire-and-forget;
subscribers register by event_type.
中央发布/订阅总线。事件有类型、不可变、即发即忘；订阅者按事件类型注册处理器。
与 State Store、Memory Store 并列为 Runtime 三核心基础设施。

## Public API / 公开接口

- `Event(event_type, payload, source='unknown')` — 不可变事件（自动生成 8 位 id 与 UTC 时间戳）；`to_dict()`
- `EventBus()`：
  - `subscribe(event_type, handler) -> EventBus` — 注册处理器（可链式调用）
  - `unsubscribe(event_type, handler)` — 移除指定处理器
  - `emit(event) -> list` — 分发该事件给所有订阅者，返回各处理器结果（异常捕获为 `{'error': ...}`）
  - `get_history(event_type=None, limit=50) -> list[dict]` — 内存中的事件历史，可按类型过滤
  - `persist(filepath=None) -> str` — 事件历史落盘为 JSONL，返回路径
  - `clear()` — 清空订阅者与历史
- `get_bus() -> EventBus` — 全 Runtime 单例
- `EventTypes` — 标准事件类型常量类

## Events / 事件

标准事件类型（`EventTypes`）：

- Task：`task.created` `task.started` `task.step_completed` `task.completed` `task.failed`
- State/Session：`state.updated` `session.started` `session.ended`
- Knowledge：`knowledge.created` `knowledge.updated` `knowledge.stale`
- Protocol：`protocol.started` `protocol.step_done` `protocol.completed`
- 其他：`agent.error` `evr.extraction`

另：Executor 会发 `agent.warning` 及任意自定义类型（`_handle_emit_event`）。
本组件是通道，自身不主动发事件；消费全部已订阅类型。

## Files & Directories / 读写的文件与目录

- 写：`event_bus/history/events.jsonl`（`persist()` 追加模式，只写入新事件；`load_history()` 可从文件读回）

## Dependencies / 依赖

- 不依赖其他组件（仅标准库：json / os / uuid / datetime / pathlib）
- 被使用：Planner（发 session/task/protocol/agent.error 事件，`run_loop()` 末尾调用 `persist()`）、Executor（`get_bus` 发自定义事件与 `agent.warning`）
