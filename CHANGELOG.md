# Changelog / 变更日志

All notable changes / 所有显著变更 to this project will be documented in this file.

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

---

## [Unreleased]

### Fixed
- 输出编码自配置：executor 入口对 stdout/stderr 做 `reconfigure(encoding='utf-8', errors='replace')`，中文协议日志在 Windows 控制台(GBK)与 CI 重定向(cp1252)下不再乱码或抛 UnicodeEncodeError，不再依赖 PYTHONIOENCODING 外部环境变量

### Added
- AGENTS.md 新增"Working Agreement / 合作方式"一节（沟通、执行风格、Git/分支/编码/诚实/发布六条纪律）
- 结构化命令层（v1.3.0 Step 1，agents/cli.py）：`agent-runtime` 扩展为子命令结构 check / ingest / wrapup / status / run，全部薄分发到现有 Executor/Planner；check/ingest/wrapup/status 支持 `--json` 机器可读输出（供后续网页控制台调用）；裸 `agent-runtime` 与旧式参数（--loop/--interval/--recover）自动映射 run 子命令，旧用法零影响；入口从 agents.wiki_agent:main 切换到 agents.cli:main；新增 tests/test_cli.py 共 12 用例

---

## [1.2.2] — 2026-07-18

新用户视角验证（fresh clone 走 QUICKSTART）驱动的清理与修复。

### Fixed
- 仓库清理：untrack 5 个个人痕迹文件（hot.md / log.md / index.md / milestones.md / BOOTSTRAP.md，本地保留）；untrack 误提交的 agent_runtime.egg-info（.gitignore 补 `*.egg-info/`）
- update_index：index.md 缺失时自动创建最小索引（新用户 clone 后 ingest 的索引步骤不再静默跳过）

### Added
- README 顶部"30 秒看懂"定位段：是什么 / 适合谁 / 三步上手 / 诚实边界
- QUICKSTART 补 Windows 控制台中文乱码说明（chcp 65001 / PYTHONIOENCODING）
- 回归测试 ×1（update_index 自建索引）；测试总数 31 → 32

---

## [1.2.1] — 2026-07-18

首次 dogfood（真实 URL 入库 + 巡检）驱动的修复轮。

### Fixed
- ingest 抓取：改用浏览器 UA（微信等平台对爬虫 UA 返回 18KB 反爬桩页，实测修复后获取 3.6MB 完整页）；新增桩页检测警告（suspect_stub）
- 摘要生成：HTML 输入先转纯文本（h1-h3 转 #/## 标记），修复"要点为空"
- sidecar 生成：从页面 frontmatter 解析（此前 domain/tags/source 被硬编码值覆盖）；补 related 键对齐 schema

### Added
- check 协议第 4 步 `check_links`：断链检测（规则与 scripts/build_graph.py 一致）
- 巡检报告升级：包含实际结果（stale 清单、断链清单），不再只有步骤状态
- 回归测试 ×2（HTML 摘要、sidecar frontmatter）；测试总数 29 → 31

已知限制：source 回链指向非 .md 原文（如 .html）时会被断链检测计为断链（误报），下一轮排除。

---

## [1.2.0] — 2026-07-17

市场化工程化：让"任何人 clone/安装即可用"可验证。

### Added
- LICENSE（MIT）——此前 README 宣称 MIT 但无许可证文件
- GitHub Actions CI：`.github/workflows/test.yml`（ubuntu + windows × Python 3.11/3.12 跑 unittest）；README 加 CI 与 License badge
- pip 打包：`pyproject.toml`，`pip install -e .` 后可用 `agent-runtime` 命令
- `scripts/ingest.py`：ingest 协议的命令行入口（此前只能写 Python 调用）
- `examples/QUICKSTART.md`：5 分钟上手路径（全部命令实机验证）
- `.github/ISSUE_TEMPLATE/`（bug/功能）+ `CONTRIBUTING.md`

### Changed
- 目录改名（pip 打包前置）：`event-bus/` → `event_bus/`、`state-manager/` → `state_manager/`、`agents/wiki-agent.py` → `agents/wiki_agent.py`；引用全部同步（代码、脚本、文档）
- 各包新增 `__init__.py`，可作为正常 Python 包导入
- test_schema_validation：fresh clone（无 sidecar）时优雅跳过而非失败——CI 可跑

---

## [1.1.0] — 2026-07-17

名实对齐 + 真实验收 + 文档裁决一轮。所有条目均有运行证据。

### Fixed
- 编码事故修复：protocol/*.json、graphs/graph-index.json、migration/migrate.py、CHANGELOG、log.md 的中文乱码全部修复；check 协议步骤 2 目录恢复为 知识库/
- MemoryStore：record_type 丢失 bug（所有记录退化为 note）+ metadata 嵌套修正
- Executor：缺失 handler 由静默 SKIP 改为 fail-fast（杜绝协议假成功）
- wrapup 协议第 4 步：write 全量覆写改为 update 合并（不再被 validate 静默拒绝）
- metadata-schema.json 与 dependency-graph-schema.json 的 `$schema` 键修复

### Added
- Executor 5 个新 handler：update_hot_md / append_log / write_next_plan / check_threshold / emit_warning；`{date}` 模板变量；可插拔 LLM 摘要接口（AGENT_RUNTIME_LLM_*，默认提取式摘要）
- tests/：unittest 套件 29 用例全绿（state/event-bus/memory/executor/planner/schema）
- scripts/：rebuild_sidecars.py、validate_sidecars.py、build_graph.py、demo_recovery.py、run_real_ingest.py
- Observability：event-bus persist 改追加模式 + load_history；state/execution-status.json（Planner 实时更新）
- wiki-agent：`--loop N --interval S --recover` 多轮运行与崩溃恢复（10 轮无人工干预 + 恢复演示 PASS）
- ontology/catalog.json：动态对象目录；Graph 对象 reserved → active
- 5 个组件 INTERFACE.md（state-manager/event-bus/memory/executor/planner）

### Changed
- sidecar 全部重建（84 个）：md frontmatter 为唯一事实源；metadata-schema 枚举对齐真实词汇
- graphs/dependency.json 真实落盘：113 节点 286 边（取代此前未持久化的 81/380 说法）
- ingest 协议：知识页落入 知识库/，自动携带 source 回链（符合入库铁律）
- 七层架构：Planner 归 Layer 2 执行引擎（六层）；Protocol 格式定稿 JSON（弃 YAML，零依赖原则）
- policy.md 权限矩阵覆盖全部组件目录；真实 ingest 端到端入库（Engram 企业级记忆层）

---

## [1.0.2] — 2026-07-17（含 v1.0.1 开源发布与编码修复线）

（原 [Unreleased] 段落实为 v1.0/v1.0.1/v1.0.2 的发布内容）

### Added (v0.2.0 计划)

- Knowledge Engine（knowledge/ + source/）
- 四种 Graph（Knowledge/Capability/Workflow/Dependency）
- Protocol 从 Markdown 升级为 JSON（原拟 YAML，v1.1.0 定稿 JSON）
- Memory 五层架构（Working/Session/Project/Semantic/Archive）

### Added — 2026-07-17 Phase 2
- knowledge/：81 篇知识页的 metadata JSON sidecar（schema: metadata-schema.json）
- source/：源材料归档目录（original/ + summaries/ + codebases/）
- graphs/：四种 Graph 的 schema 定义（dependency-graph-schema.json + graph-index.json）
- protocol/：4 个核心协议从 Markdown 升级为 JSON（check/ingest/wrapup/context-budget）+ 1 个 stub（capability-map）
- executor/executor.py：Protocol Executor v0.1（4 个 handler，smoke test 通过）

### Changed — 2026-07-17 Review 修正
- ontology.md v0.2：Memory Owner 更正、Session/State 边界明确、Protocol 当前位置如实反映、Event 定位升级为核心组件、Graph 新增为第 9 号预留对象
- manager.py：merge() 加 _version 乐观锁冲突检测、新增 batch_write() 和 health_check()
- AGENTS.md：State 层进站协议增加 下次工作计划.md 回退规则

### Added — 2026-07-17 Phase 3
- event-bus/event_bus.py：15 种事件类型的 pub/sub 总线 + history + persist
- memory/memory_store.py：五层记忆 L0-L4（Working/Session/Project/Semantic/Archive）
- planner/planner.py：动态编排引擎（dequeue → match → execute → archive）
- graphs/dependency.json：81 节点 380 边的依赖图（未持久化；v1.1.0 重新落盘为 113 节点 286 边）
- agents/wiki-agent.py：首个通用 Wiki 维护 Agent（check + ingest）

### Added — 2026-07-17 v1.0 收尾
- executor v0.2：模板变量解析 + 10 个 handler（fetch_url/generate_summary/create_knowledge_page/generate_sidecar/update_index/emit_event 等）
- ingest 协议完整实现（5 步全链路：抓取→存档→摘要→知识页→索引）
- protocol/TEMPLATE.json：新用户自定义协议模板
- migration/migrate.py：旧目录→新结构迁移脚本
- README.md：重写为通用工具上手文档
- 全链路集成测试：6 项全部通过

---

## [0.1.0] — 2026-07-16

### Added

- `ontology/` 目录：Perspective + Object Rule + Ontology v0.1（7 个一等对象定义）
- `state/` 目录：4 个 JSON 文件（schema + session + task-queue + current-task）
- `state-manager/manager.py`：多 Agent 状态协调器（lock/validate/merge/history/recover）
- `policy.md`：Agent 权限矩阵 v0.1
- `CHANGELOG.md`：本文件

### Changed

- hot.md：TODO/进度迁移到 state/，hot.md 只保留不可变 Memory
- AGENTS.md：新增 State 层读取说明（进站先读 state 文件）

### 目录结构变化

```
新增：
  ontology/    ← Phase 0 产物
  state/       ← Phase 1 产物
  state-manager/ ← Phase 1 产物
  policy.md    ← Phase 1 产物

保留（Phase 2 迁移）：
  知识库/       → 将迁至 knowledge/
  源/           → 将迁至 source/
  agents/       → 将迁至 protocol/

旧版可用 git checkout v0.0-wiki 恢复。
```

---

## [0.0.0] — 2026-07-10

### Added

- 初始 Wiki 快照：80 篇知识页，3 域 7 子 MOC
- 54 篇源原文 + 51 篇源摘要
- 7 个 Agent 协议文件（agents/）
- 基础设施：AGENTS.md、hot.md、index.md、log.md
- README.md：AI 助手快速说明书
- GitHub 仓库创建：[ruiyaoe-hash/my-wiki](https://github.com/ruiyaoe-hash/my-wiki)

### Changed

- 系统定位从"AI Wiki"升级为"Agent Runtime v0.1"

---

## [0.0.0-wiki] — 2026-06-24 ~ 2026-07-08

原始 Wiki 阶段。标签：`v0.0-wiki`

- 69 篇知识页，3 域 MOC 架构
- 完整会话归档（2026-06-24 ~ 2026-07-08）
- MOC 架构重构、五层 index 角色定义、Harness 工程入库
- 知识生命周期引擎首次实验运行
