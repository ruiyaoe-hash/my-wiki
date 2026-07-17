# Agent Runtime Policy / 策略 — Agent Permission Matrix / 权限矩阵

Defines which agents can access which files.
定义哪些 Agent 可以访问哪些文件。

| Agent | state/ | knowledge/ | ontology/ | protocol/ | 说明 |
|-------|--------|-----------|-----------|-----------|------|
| Wiki Agent / Wiki 维护 | Read / 读 | Read+Write / 读写 | Read / 只读 | Read / 只读 | Auto ingest and update / 自动入库更新 |
| Human / 人类 | All / 全部 | All / 全部 | All / 全部 | All / 全部 | System admin / 系统管理员 |

Default: any unlisted agent gets Read-only.
默认：未列出的 Agent 仅有只读权限。
