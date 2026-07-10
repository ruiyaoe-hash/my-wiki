import os

PAGES_DIR = r"D:\my-wiki\知识库"
os.makedirs(PAGES_DIR, exist_ok=True)

pages = {}

# --- Page 1 ---
pages["Agent Runtime v0.1.md"] = """---
title: Agent Runtime v0.1
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- Agent-Runtime
- architecture
- wiki-evolution
---

# Agent Runtime v0.1

## 一句话定义

一个 **模型无关、工具无关、知识驱动、持续演化** 的 Agent 运行时。

任何 AI 助手进入后，不需要从头理解系统，而是通过标准化的 State -> Protocol -> Knowledge -> Memory 流程直接开始工作。

## 五代 Agent Knowledge System

| 代 | 名字 | 例子 | 作用 |
|---|------|------|------|
| 1 | Documentation | GitHub Wiki | 给人看 |
| 2 | PKM | Obsidian, Logseq | 帮人思考 |
| 3 | RAG | LangChain, NotebookLM | 帮 AI 检索 |
| 4 | Knowledge Runtime | 我们 | 让 AI 按协议执行 |
| 5 | Agent OS | 未来 | AI 自己维护运行环境 |

## 核心区分

- 旧定位是 AI Wiki —— 知识存在 Markdown 里，AI 来读
- 新定位是 Agent Runtime —— 知识 + 协议 + 状态 + 执行引擎，AI 来跑

## 设计原则

1. 模型无关：Codex、Claude、GPT、Gemini 都能用同一套协议
2. 工具无关：今天是 Obsidian + Markdown，明天可能是 SQLite + API
3. 知识驱动：Planner 先查 Knowledge 再决定做什么，不是盲搜
4. 持续演化：EVR 方法论保证系统从真实使用中自我改进

## 与现有 Wiki 的关系

Wiki 不会消失，而是降级为 Runtime 的 Knowledge Store——只是一个存储适配层。
"""

# --- Page 2 ---
pages["EVR 方法论.md"] = """---
title: EVR 方法论
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- methodology
- EVR
- system-evolution
- agent-engineering
---

# EVR 方法论

## 一句话定义

Extraction -> Validation -> Refinement：从已经工作的系统中发现隐含结构，通过真实运行验证，根据反馈持续修正。

## 三步走

### Extraction

不是发明新结构，而是从已有系统里把隐性结构显式化。

你的 ingest-protocol 已经隐含了 Source -> Summary -> Knowledge 三层对象关系。你的 wrapup-protocol 已经隐含了 State -> Memory 的转换边界。不做 Extraction 就去设计 Ontology，就是在猜。

### Validation

不是单元测试，而是用真实任务跑一遍。建了 State 层，跑一个完整的 research 任务，发现 Task 缺字段、State 和 Memory 边界模糊。不跑就不会发现。

### Refinement

根据 Validation 的结果修改系统定义。增加新对象、拆分模糊对象、废弃无用对象。不是一次性设计完，是持续改。

## 与其他方法论的对比

| 方法 | 特点 | 适合 |
|------|------|------|
| Architecture First | 先设计全部架构再写代码 | 需求完全确定的项目 |
| Code First | 先写代码再整理 | 快速原型 |
| EVR | 先跑起来，再萃取结构，持续修正 | 持续演化的 Agent 系统 |

## 为什么 EVR 适合这个项目

因为这个项目本身就是一个不断演化的系统。你的知识不是凭空设计出来的，是从论文、实践、协议中提炼的。Runtime 也应该从真实运行中萃取，而不是从一开始就设计完美。
"""

# --- Page 3 ---
pages["Runtime Object 识别规则.md"] = """---
title: Runtime Object 识别规则
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- ontology
- object-rule
- runtime
---

# Runtime Object 识别规则

## Perspective 声明

本系统以 Runtime 为观察视角，而不是以知识管理、存储实现或用户界面为观察视角。

## 一条规则

如果 Runtime 需要在某个时刻，用这个实体的标识符找到它、查询它的当前状态、并对它执行一个操作——那它就是一等对象。

三个要素缺一不可：

| 要素 | 含义 | 不满足的例子 |
|------|------|------------|
| 寻址 | 能用 ID 找到它 | Domain——没法寻址 |
| 状态查询 | Runtime 需要知道它的状态才能做决策 | Index——纯指针列表 |
| 执行操作 | 不只是读，还有写/改/删 | 标签——只能间接查询 |

## 判定示例

### 通过：Task

Runtime 能通过 task-id 找到它、查询 status（created/running/done）、执行 start/pause/complete。三个要素全部满足。

### 不通过：Domain

无法寻址一个具体的 Domain。Agent Memory 不是系统里的一个实体，它只是 Knowledge 对象的一个标签属性。

### 边缘：Capability

有名字 research，但 Runtime 会不会查询 research 的状态然后做决策？不会。Runtime 直接用 Workflow。Capability 更像一个标签层。
"""

# --- Page 4 ---
pages["Agent Runtime 七层架构.md"] = """---
title: Agent Runtime 七层架构
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- architecture
- layered-architecture
- runtime-design
---

# Agent Runtime 七层架构

## 总览

Meta: EVR 演化机制（横向贯穿所有层）
Layer 0: Vision（稳定十年，一句定义）
Layer 1: Ontology Core（Perspective + Object Rule，一页锁死）
Layer 2: Runtime Core（State Store + Event Bus + Memory Store + Policy）
Layer 3: Knowledge + Capability（共同演化，不分先后）
Layer 4: Planner（动态编排工作流）
Layer 5: Application（Wiki Agent / 文旅 Agent / 研究 Agent）
Layer 6: Interface（Agent Workspace UI）

## 每层职责与 Exit Criteria

### Layer 0: Vision

永久不变的一句话：模型无关、工具无关、知识驱动、持续演化的 Agent Runtime。

### Layer 1: Ontology Core

产出：perspective.md + object-rule.md（仅一页，Phase 0 锁定）。不定义具体对象，只定义判定标准。

### Layer 2: Runtime Core

模块：State Store（含 lock/recover）+ Event Bus + Memory Store + 最简 Policy。
Exit：一个脚本能创建 Task、更新 State、写入 Memory、发 Event——不需要 AI 参与。

### Layer 3: Knowledge + Capability

模块：Knowledge Store + Source Store + 四种 Graph + Capability Registry + Protocol Executor。
Exit：Agent 自主完成一次 收 URL -> 入库 -> 生成知识页。

### Layer 4: Planner

职责：读 Task -> 查 Capability+Knowledge -> 编排 Workflow -> 调 Protocol -> 更新 State。
Exit：两个不同 Task 由 Planner 自动编排执行。

### Layer 5: Application

模块：Wiki 维护 Agent / 文旅策划 Agent / 研究 Agent。
Exit：至少一个 Agent 在生产环境持续运行 7 天。

### Layer 6: Interface

模块：Agent Workspace UI。
Exit：人类可以通过 UI 而非文件系统操作系统。

## 关键设计决策

- Planner 不是 Runtime 的居民，而是 Layer 2 的执行引擎
- EVR 不是第七层，而是横向元过程，贯穿所有层
- Knowledge 和 Capability 共同演化，不分先后
- Ontology 拆成 Stable Core（锁死）+ Dynamic Catalog（持续迭代）
"""

# --- Page 5 ---
pages["State 与 Memory 的分离.md"] = """---
title: State 与 Memory 的分离
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- state
- memory
- architecture
---

# State 与 Memory 的分离

## 核心区分

| 维度 | State | Memory |
|------|-------|--------|
| 性质 | 瞬时状态 | 不可变记录 |
| 生命周期 | Task 开始 -> Task 结束 -> 删除 | 记录后永久留存 |
| 谁写 | Planner 在执行中不断更新 | Memory Store 在收尾时追加 |
| 格式 | JSON，机器高频读写 | Markdown，人+AI 均可读 |
| 例子 | 第三步进行中，进度 62% | 2026-07-10 入库了 Harness 工程 |

## 为什么必须分开

现在的 hot.md 承担了三个职责：

- Working Memory：当前做到哪了
- Session Memory：这次会话干了什么
- Project Memory：下次要做什么

混在一起的结果：hot.md 越来越长，AI 恢复上下文越来越慢，两个不同 Agent 同时修改会冲突。

## 拆分方案

### hot.md 保留

只存已发生的、不可变的事件记录。不要放 TODO、进度、当前任务。

### state/ 新建

- current-task.json：正在执行什么 Task，第几步，进度
- task-queue.json：排队中的 Task 列表
- execution-status.json：Runtime 当前状态

## 一句原则

凡是明天可能改变的，都不要放 hot.md。
"""

# --- Page 6 ---
pages["Schema Extraction 方法.md"] = """---
title: Schema Extraction 方法
created: "2026-07-10"
updated: "2026-07-10"
type: note
domain: ai-engineering
status: evergreen
tags:
- ontology
- schema
- extraction
- methodology
---

# Schema Extraction 方法

## 一句话定义

从已经工作的系统里，把隐性的对象结构显式化。不是 Design，不是 Invent，而是 Discover。

## 与 Ontology Design 的区别

| | Ontology Design | Schema Extraction |
|---|---|---|
| 前提 | 我还没写代码，但我能设计出对象 | 我已经跑了两个月的系统 |
| 方法 | 演绎（从理论推导） | 归纳（从实践中发现） |
| 风险 | 设计出来的对象后来发现不需要 | 提取时可能漏掉边缘对象 |
| 适合 | 新项目 | 本项目 |

## 具体步骤

1. 扫协议文件：ingest-protocol 隐含了 Source -> Summary -> Knowledge；wrapup-protocol 隐含了 State -> Memory
2. 扫 hot.md：标题结构隐含了 Working / Session / Project 三层 memory
3. 扫知识页：69 页的命名和 frontmatter 隐含了 Knowledge 的属性结构
4. 过 Object Rule：把候选对象逐一过 Runtime Object 识别规则

## 为什么不用 Ontology Design

因为这个项目不是白纸。已经有 69 页知识、7 个协议、完整的操作日志和会话归档。强行从零设计一套 Ontology 等于扔掉过去两个月的运行经验。Schema Extraction 让这些经验变成资产，而不是推倒重来。
"""

# === Write all ===
for filename, content in pages.items():
    path = os.path.join(PAGES_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK: {filename}")

print(f"\nDone. {len(pages)} pages created.")
