# Memory Store — Component Interface / 组件接口

Source / 源码：`memory/memory_store.py`（Memory Store v0.2）

## Responsibility / 职责

Five-layer memory architecture L0–L4. Memory records are APPEND-ONLY — never modified, only archived.
五层记忆架构。记忆记录只追加——不修改、不删除，只做归档迁移。

- L0 Working Memory / 工作记忆：内存字典，Task 完成时清空（volatile）
- L1 Session Memory / 会话记忆：每会话一个 JSON 持久化文件
- L2 Project Memory / 项目记忆：项目级持久记录（records / decisions / milestones）
- L3 Semantic Memory / 语义记忆：知识页 sidecar 索引（sem_index / sem_search）
- L4 Archive / 归档：超期会话文件自动迁入 archive/

## Public API / 公开接口

`MemoryStore()`：

- L0：`wm_set(key, value)` / `wm_get(key, default=None)` / `wm_clear()`
- 五动词协议（update/delete 刻意缺席——append-only）：
  - `write(level, scope, content, record_type='note', source=None, metadata=None) -> MemoryRecord` — level 为 `'session'`（scope=session_id）或 `'project'`（scope=category）
  - `read(level, scope, limit=None) -> list`
  - `query(level, scope=None, record_type=None, source=None) -> list` — 按类型/来源过滤
- `archive_task(task_state, session_id) -> MemoryRecord` — 已完成 Task 的 State 转为不可变 Memory（type=`task_archive`）
- L3：`sem_index(force=False) -> dict` / `sem_search(query, field='title') -> list`
- L4：`archive_sessions(older_than_days=30) -> dict`
- `status() -> dict` — L0/L1/L2 概览
- `MemoryRecord(content, record_type='note', source=None, metadata=None)` — 单条不可变记忆；`to_dict()`

## Events / 事件

- Emits / 发出：无
- Consumes / 消费：无

## Files & Directories / 读写的文件与目录

- 读写：`memory/sessions/<session_id>.json`（L1）、`memory/project.json`（L2）、`memory/semantic_index.json`（L3 索引缓存）
- 写：`memory/archive/*.json`（L4，由 `archive_sessions()` 从 sessions/ 迁入）
- 读：`knowledge/*.json`（sidecar，构建 L3 索引；跳过 `metadata-schema.json`）

## Dependencies / 依赖

- 不依赖其他组件（仅标准库）
- 被使用：Planner（`archive_task`、`wm_clear`、`status`）
