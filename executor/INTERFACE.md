# Protocol Executor — Component Interface / 组件接口

Source / 源码：`executor/executor.py`（Protocol Executor v0.3）

## Responsibility / 职责

Loads `protocol/*.json` step definitions and executes them sequentially.
加载 Protocol 的 JSON 步骤定义并顺序执行。
模板感知：支持 `{{inputs.key}}`、`{{steps.N.key}}` 与字面量 `{date}` 占位符。
Fail-fast：某一步没有对应 handler 或抛异常时立即中止整个 Protocol（返回 False），不允许假成功。

## Public API / 公开接口

- `ProtocolExecutor()`：
  - `load(protocol_id) -> dict | None` — 加载 `protocol/<protocol_id>.json`
  - `execute(protocol_id, inputs=None) -> bool` — 顺序执行全部步骤，逐步记录到 `self.state`
- Action handlers（由步骤的 `action` 字段分派，命名约定 `_handle_<action>`，当前覆盖）：
  `search_files` `check_stale` `call_manager` `generate_report` `fetch_url`
  `generate_summary` `create_knowledge_page` `generate_sidecar` `update_index`
  `emit_event` `update_hot_md` `append_log` `write_next_plan` `check_threshold` `emit_warning`
- `llm_summarize(text) -> str | None` — 可选 LLM 摘要（OpenAI 兼容接口，仅标准库 urllib）；
  需环境变量 `AGENT_RUNTIME_LLM_BASE_URL` + `AGENT_RUNTIME_LLM_API_KEY`，模型取 `AGENT_RUNTIME_LLM_MODEL`（默认 `gpt-4o-mini`）；未配置或失败时退回提取式摘要

## Events / 事件

- 发出：`_handle_emit_event` 发任意自定义事件（默认类型 `custom`）；`_handle_emit_warning` 发 `agent.warning`（source=`executor`）
- 消费：无

## Files & Directories / 读写的文件与目录

- 读：`protocol/*.json`（协议定义）、`knowledge/*.json`（sidecar，staleness 检查）、`state/*.json`（经 StateManager）、`index.md`、`hot.md`
- 写：`state/*.json`（经 StateManager，agent_id=`'Executor'`）、`reports/`（执行报告）、`source/original/`（抓取原文）、`source/summaries/`（摘要）、`知识库/*.md`（新知识页，UTF-8 BOM）、`knowledge/*.json`（sidecar）、`index.md`、`hot.md`、`log.md`（append-only）、`下次工作计划.md`

## Dependencies / 依赖

- `state-manager/manager.py` — `StateManager`（`_handle_call_manager`、`_handle_update_hot_md` 等）
- `event-bus/event_bus.py` — `get_bus` / `Event`（`_handle_emit_event`、`_handle_emit_warning`）
- 可选：OpenAI 兼容 LLM endpoint（环境变量驱动，未配置则全离线运行）
- 被使用：Planner（`run_task()` 调用 `execute()`）
