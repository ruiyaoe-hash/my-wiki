# Agent Runtime Policy / 策略 — Agent Permission Matrix / 权限矩阵

Defines which agents can access which files.
定义哪些 Agent 可以访问哪些文件。

v1.1.0（2026-07-17）：矩阵扩展至全部关键目录；新增 Planner、Executor 两个运行时角色，权限依据真实代码行为。

| Agent | state/ | knowledge/ | ontology/ | protocol/ | memory/ | event-bus/ | planner/ | executor/ | graphs/ | tests/ | scripts/ | 说明 |
|-------|--------|-----------|-----------|-----------|---------|------------|----------|-----------|---------|--------|----------|------|
| Wiki Agent / Wiki 维护 | Read / 读 | Read+Write / 读写 | Read / 只读 | Read / 只读 | Read+Write / 读写 | Read / 只读 | Read / 只读 | Read / 只读 | Read / 只读 | Read / 只读 | Read / 只读 | Auto ingest and update / 自动入库更新 |
| Planner / 编排引擎 | Read+Write / 读写 | — | — | — | Read+Write / 读写 | Read+Write / 读写 | Read / 只读 | Read / 只读 | — | — | — | Runs tasks via Executor / 经 Executor 跑任务；protocol/ 由 Executor 加载，Planner 不直读 |
| Executor / 协议执行器 | Read+Write / 读写 | Read+Write / 读写 | — | Read / 只读 | — | Read / 只读 | — | Read / 只读 | — | — | — | Also writes reports/, source/, 知识库/ / 另写 reports/、source/、知识库/ 等产出目录 |
| Human / 人类 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | System admin / 系统管理员 |

Default: any unlisted agent gets Read-only.
默认：未列出的 Agent 仅有只读权限。

Notes / 备注：

- "—" = no file access in current code / 当前代码不访问该目录。
- Planner 与 Executor 对 state/ 的写入均经 StateManager（带乐观锁与校验），不直接写文件 / state writes go through StateManager with locking and validation.
- event-bus/ 的写权限指 `history/events.jsonl` 落盘；planner/、executor/、tests/、scripts/ 为代码目录，仅 Human 可改 / code directories are Human-writable only.
