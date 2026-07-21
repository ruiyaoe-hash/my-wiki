# Web Console — Component Interface / 组件接口

Source / 源码：`console/server.py`（Web Console v1.3，stdlib http.server）

## Responsibility / 职责

本地网页操作界面：按钮执行协议 + 健康总览。零业务逻辑的薄壳，
所有能力来自 Step 1 命令层（`agents/cli.py`）。只监听 127.0.0.1，本机单人使用。

Local web UI: buttons run protocols, dashboard shows health. Thin shell over
the structured CLI; binds 127.0.0.1 only, single-user by design.

## Public API / 公开接口

- `serve(port=8765, open_browser=True) -> int` — 启动服务（端口被占顺延，最多试 10 个）；入口为 `agent-runtime console`
- `make_server(port) -> ThreadingHTTPServer` — 构造服务实例（测试用，port=0 取空闲端口）
- `list_protocols() -> list[dict]` — 从 `protocol/*.json` 声明式生成按钮清单（`runnable`/`form` 字段）
- `run_protocol(protocol_id, params) -> dict` — 持全局锁走命令层，返回 `{rc, result}`
- `read_log(n=20)` / `recent_events(n=8)` — 操作日志与事件流尾部

## HTTP Routes / 路由

- `GET /` — 单页控制台（内联 HTML/JS，无前端依赖）
- `GET /api/status` — 健康总览（cli._collect_status + recent_events）
- `GET /api/protocols` — 按钮清单
- `GET /api/log` — 最近 20 条操作日志
- `POST /api/run` — 执行协议，body `{"protocol": id, "params": {...}}`；rc≠0 返回 400

## Write Protection / 写操作保护（三层）

1. 前端 confirm 二次确认
2. 操作日志追加落盘 `state/console-log.jsonl`（ts/protocol/params/argv/rc）
3. 全局执行锁（同时只跑一个协议）+ 底层 StateManager 既有锁

可运行协议白名单在 `COMMAND_MAP`（check/ingest/wrapup）；无映射的协议
（如 context-budget）页面展示为"仅自动触发"。POST 体上限 64KB。

## Events / 事件

- 发出：无（协议执行产生的事件由 Executor/Planner 发出）
- 消费：读 `event_bus/history/events.jsonl` 尾部用于展示

## Files & Directories / 读写的文件与目录

- 读：`protocol/*.json`（按钮清单）、`state/*.json`（经 cli/status）、`event_bus/history/events.jsonl`、`reports/check-*.md`
- 写：`state/console-log.jsonl`（操作日志，append-only）；协议执行产生的写入与对应协议一致（经命令层）

## Dependencies / 依赖

- `agents/cli.py` — Step 1 命令层（全部执行能力）
- 被使用：用户浏览器；测试 `tests/test_console.py`
