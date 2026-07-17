---
title: "Phase 0+1 Review — 2026-07-17"
created: "2026-07-17"
type: review
status: completed — P1 三项已修
---

# Phase 0+1 Review — v0.1 回头看

> 审查范围: ontology/ (3 文件) + state-manager/manager.py + hot.md 拆分结果
> 参考基线: 下次工作计划.md Review 清单 + 终局对抗性审查记录 + 开发路线图

---

## Q1: 7 个对象的定义有没有遗漏或模糊?

### 发现 1.1 — Memory 的 Owner 写错 (P1)

ontology.md 写 Memory 的 Owner 是 **"Memory Store (Phase 1 实现的 State Manager 的一部分)"**。但实际:

- State Manager (`manager.py`) 里零行 Memory 相关代码。它管的是 state JSON 文件的读写锁，不是 Memory。
- [[State 与 Memory 的分离]] 知识页明确说 Memory 五层是 Phase 2 的事。
- CHANGELOG 也把 Memory 五层放在 v0.2.0 计划里。

**结论:** 文字和实现不一致。Phase 1 实际上只实现了 State Store，没有 Memory Store。Owner 应改为 "Memory Store (Phase 2 实现)。Phase 1 无 Memory 实现，仅概念占位。"

### 发现 1.2 — Session 和 State 边界模糊 (P2)

ontology.md 把 Session 列为独立对象，但又写 "Phase 1 作为 State Store 的一部分实现"。在 `manager.py` 里，session.json、current-task.json、task-queue.json 三者被完全同等地对待——都是同一套 `read/write/merge` 操作。

但 Session 的生命周期比 State 长。一个 Session 包含多个 Task，每个 Task 有自己的 State。Session 结束 ≠ State 清空中间态。这个结构关系在 ontology 里没有体现，在代码里也没有区分。

**建议:** ontology 里加一句显式说明 Session 和 State 的结构关系: "一个 Session 包含 1..N 个 Task，每个 Task 有自己的瞬时 State。Session 结束时，它管理的所有 Task 的 State 必须已完成或显式中止。"

### 发现 1.3 — Protocol 的当前存储位置与 Ontology 不匹配 (P2)

ontology.md 写 Protocol 的 Owner 是 "Protocol Registry (Phase 2 实现)，当前手动维护"。但 7 个协议文件实际放在 `agents/` 目录，不是 `protocol/`。Ontology 应该如实反映当前状态，而不是只描述未来目标。

**建议:** 在 Protocol 的生命周期里加一行 "当前形态: 7 个 Markdown 文件在 agents/ 目录，由 AGENTS.md 的按需加载规则管理。Phase 2 将迁移至 protocol/ 并升级为 YAML。"

### 发现 1.4 — 缺少 Graph 对象 (P2)

Phase 2 计划构建四种 Graph (Knowledge/Capability/Workflow/Dependency)。它们在整个路线图中是核心基础设施，但 ontology 里完全没有 Graph 这个概念。

用你的对象规则来检验: Runtime 在执行 Task 时需要按 ID 找到一个具体的 Graph，查询它的节点和边（状态查询），然后进行遍历、过滤、更新（执行操作）。三项全满足 → Graph 是一等对象。

**建议:** 在 ontology 里加 "Graph（图）— Phase 2 预留"。或至少说明: "四种 Graph 是对已有对象之间关系的建模，不作为独立的一等对象，而是 Knowledge/Capability/Protocol/Task 之间的索引层"——不管你选哪种结论，必须明确宣布，不能留空。

### 发现 1.5 — Event 定位偏低 (P2)

Event 被放在 ontology 第 8 位标注 "Phase 3 预留"。但 [[终局对抗性审查记录]] 严重级 #6 的结论是: "只保留 State Store + Event Bus + Memory Store"——Event Bus 是与 State Store 平级的三核心之一。

如果 Event Bus 是核心组件，它应该在 ontology 里有更强的定位。不是说 Phase 3 实现不对，而是 ontology 不应该用 "预留" 这种弱语气来描述一个核心组件。

**建议:** Event 从 "Phase 3 预留" 改为 "Phase 1 搭框架 (stub)，Phase 3 正式启用"。同时在 manager.py 旁边建一个 `event-bus/stub.py`，哪怕只是一个空的类接口定义，也比完全没有强。

### 发现 1.6 — Capability 的排除需要再审视 (P3)

object-rule.md 把 Capability 排除在一等对象之外，理由是 "Runtime 不查询它的状态做决策"。但 Phase 2 的 Capability Graph 要求 Runtime 按 ID 查找一个能力节点，查询它的前置依赖和工具链，并根据查询结果做路由决策。如果这些操作成立了，Capability 就满足一等对象的三个条件。

**结论:** 现在不急着改，但 Phase 2 开始构建 Capability Graph 时，应该重新用对象规则检验一次。如果那时发现满足了，就在 ontology 里补上。

### 综合判定: 7 个对象的基本框架正确，但存在 2 个描述错误 + 2 个缺失 + 2 个定位问题

| 对象 | 状态 | 问题 |
|------|------|------|
| Knowledge | ✅ 清晰 | — |
| Source | ✅ 清晰 | — |
| Memory | ⚠️ Owner 写错 | P1: Phase 1 实际无实现 |
| State | ✅ 清晰 | — |
| Session | ⚠️ 边界模糊 | P2: 与 State/Manager 的关系没说清 |
| Protocol | ⚠️ 位置不准 | P2: 未反映 agents/ 的当前现实 |
| Task | ✅ 清晰 | — |
| Event | ⚠️ 定位偏低 | P2: 应该是核心组件，不是"预留" |
| (Graph) | 🔴 缺失 | P2: Phase 2 核心组件，ontology 完全没提 |
| (Capability) | 🟡 待定 | P3: Phase 2 时重新检验 |

---

## Q2: State Manager 的接口够不够? 要不要加 merge_conflict_handler?

### 结论: 必须加。同时还有 3 个值得加的。

### 发现 2.1 — merge_conflict_handler 缺失 (P1)

`merge()` 的实现是 `{**current, **updates}`——浅合并，无版本号，无冲突检测。如果有两个 Agent 同时 merge 同一个文件，后写的直接覆盖，没有任何提示。

在多 Agent 场景下，这会导致静默数据丢失。虽然当前只有一个 Codex Agent，但 Phase 1 的 design goal 就是 "多 Agent 状态协调器"。

**建议的最小实现:**

```python
def merge(self, filename, updates, agent_id, base_version=None):
    current = self.read(filename)
    if base_version is not None:
        if current.get('_version', 0) != base_version:
            return {
                'success': False,
                'conflict': True,
                'current_version': current.get('_version', 0),
                'your_version': base_version,
                'current_data': current,
                'your_updates': updates
            }
    merged = {**current, **updates,
              '_version': current.get('_version', 0) + 1}
    ok = self.write(filename, merged, agent_id)
    return {'success': ok, 'conflict': False,
            'new_version': merged.get('_version')}
```

思路: 给每个 state 文件加 `_version` 字段，merge 时发出 base_version，如果版本号不匹配说明中间有人改过，返回冲突对象而不是静默覆盖。

### 发现 2.2 — validate 没有用 state-schema.json (P2)

`validate()` 是硬编码的字段检查。`state-schema.json` 已经定义了完整的 JSON Schema，但没被使用。如果要扩容 state 文件或加新字段，两处都要改，且容易不同步。

**建议:** 不要求 Phase 1 就做 schema-driven validation（太重了），但在 `validate()` 里加一个 TODO 注释，标注 "Phase 2: load state-schema.json and validate against it"。

### 发现 2.3 — 缺少多文件原子操作 (P2)

一个常见的操作: 从 task-queue.json 取一个任务 → 写入 current-task.json → 更新 task-queue.json。这三个写应该是原子或至少是连贯的。但目前 `acquire` 是单文件锁，没有办法跨文件。

**建议:** 加一个 `batch_write(files, agent_id)` 方法，接受 `{filename: data}` 的字典，先对所有文件 acquire 锁（全部获取到才继续），然后逐文件写。

### 发现 2.4 — status() 太薄 (P3)

`status()` 只列出文件名。对于一个 "状态协调器"，这等于只回答 "有哪些文件" 而没回答 "它们状态如何"。

**建议:** 加 `health_check()`，返回每个文件的: 是否可读、是否有锁、锁是否 stale、历史深度、数据基本一致性。3 行代码的成本，换一个能诊断问题的工具。

---

## Q3: hot.md 拆完之后，有没有信息丢失?

### 结论: 有。两处。

### 缺失 3.1 — 下次工作计划 游离在 state 系统之外 (P1)

State 系统的设计意图是 "进站先读 state/session.json + state/current-task.json 就知道接下来做什么"。但实际上，下次工作计划是 [[下次工作计划.md|一个独立的 Markdown 文件]]，task-queue.json 里没有任何条目。

AGENTS.md 现在写 "进度和 TODO 不再从 hot.md 读取"，但没有说从 下次工作计划.md 读。这导致新 Agent 进站后不知道该去哪找待办。

**建议:** 下次收尾时，把下次工作计划.md 里的 Review 清单和 Phase 2 步骤，以 task 条目的形式写入 task-queue.json。下次工作计划.md 可以保留作为人类可读版本，但 state/ 必须是权威源。

### 缺失 3.2 — history 只记了最终态，没记过程 (P2)

`.history/` 里 `current-task.json.history` 有 2 条记录，但都是 `status: idle`。Phase 0 → Phase 1 之间的状态切换（idle → running → completed → idle）没有被记录。history 只捕获了 `write()` 调用的瞬间快照，没有捕获状态机转换。

**建议:** 这不是 Phase 1 必须修的事，但在 manager.py 的 `write()` 方法注释里加一条: "Phase 2: 引入 transition log（状态机转换记录），而非当前快照式的 history。"

### 缺失 3.3 — old hot.md 的 intermediate TODO 确实丢了 (P3)

这是拆分设计本身就接受的代价。old hot.md 的中间 TODO 状态（例如 "Phase 0 Step b 进行中，刚读完知识页的 heading 结构"）是瞬时的，按照 State 的定义本来就该在 Task 完成后清空。它们在拆分时没被保留是正确的。

**结论:** 不是 bug，是 design。但以后 State Manager 的 `_save_history()` 如果能记状态机转换而非最终快照，就可以在需要时重建中间过程。

---

## 总结: Review 通过，但有三件事必须改

| 优先级 | 改哪里 | 改什么 |
|--------|--------|--------|
| P1 (必须) | ontology.md | 修正 Memory Owner（Phase 1 → Phase 2） |
| P1 (必须) | manager.py | 加 merge_conflict_handler（_version 乐观锁） |
| P1 (必须) | AGENTS.md | 进站协议里明确标注 下次工作计划.md 为待办源 |
| P2 (推荐) | ontology.md | 补充 Session/State 边界说明 + Protocol 当前位置 + Event 定级修改 + Graph 预留声明 |
| P2 (推荐) | manager.py | validate 加 TODO 注释，加 batch_write，加 health_check |
| P3 (可选) | manager.py | history 模式加 transition log TODO 注释 |

做完 P1 三项后，Review 正式通过，可进 Phase 2。

---

## 版本记录

- v0.1 (2026-07-17): Review 初稿，基于 下次工作计划.md Review 清单的三问展开
