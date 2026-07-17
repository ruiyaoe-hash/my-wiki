# Ontology v0.1 — Agent Runtime 一等对象定义

> 本文件为 Phase 0 产物。只定义对象边界（是什么、谁管、谁用、活多久），
> 不定义 Schema（内部属性）。Schema 在 Phase 1 落地后从实践中萃取。

---

## 1. Knowledge（知识）

**一句话：** 系统对某个主题的结构化理解。目前以 Markdown 文件形式存在，对应你 `知识库/` 里的 80 篇知识页。

**生命周期：** 被创建（入库或手动写）→ 被引用（Planner 读、Agent 查）→ 可能被更新（修正错误、补充新发现）→ 可能标记为过期（stale）或废弃。不会删除，只会归档。

**Owner（谁管它）：** Knowledge Engine（Phase 2 实现）。当前是你手动管。

**Consumer（谁用它）：** Planner（Phase 4）、Application Agent（Phase 5）、你自己（Human）。

---

## 2. Source（源材料）

**一句话：** 不可变的原始证据。你从外部获取的任何材料（论文、博客、GitHub README）在入库时先存成 Source，然后再基于它写 Summary 和 Knowledge。

**生命周期：** 被摄入（ingest）→ 被一个或多个 Knowledge 引用 → 长存。Source 不修改、不删除——它是"证据"，证据不能改。

**Owner：** Knowledge Engine（Phase 2）。当前是你的手动操作。

**Consumer：** Knowledge（通过"来源引用"关联）、Agent（需要验证某条知识的原始依据时）。

---

## 3. Memory（记忆）

**一句话：** 已经发生且不可修改的事件记录。"2026-07-16 入库了 HMS，发现对象模型有 5 层"——这就是一条 Memory。

**生命周期：** 被记录（append）→ 被查询（Agent 想了解"之前做过什么"）→ 可能被归档（超过一定时间或数量后从 hot 迁到 archive）。Memory 不修改、不删除——发生过的事不能改写。

**Owner：** Memory Store（Phase 2 实现）。Phase 1 无 Memory 实现，仅概念占位。

**Consumer：** Agent（恢复上下文）、你自己（回顾历史）、EVR 的 Extraction 步骤（从 Memory 中发现模式）。

---

## 4. State（状态）

**一句话：** 系统此刻的瞬时快照。"Task #003 正跑到第三步，进度 62%，被 Codex 持有"——这就是 State。执行结束，State 清空。

**生命周期：** 被创建（Task 开始时）→ 被更新（Task 执行中每一步都在更新）→ 被清空（Task 完成或取消）。State 不持久化——它是瞬时的，断电就丢。关键 State 在清空前会被 Memory Store 转为 Memory。

**Owner：** State Store（Phase 1 实现）。

**Consumer：** Planner（靠 State 判断"下一步是什么"）、Agent（恢复执行时先读 State）。

---

## 5. Session（会话）

**一句话：** 一次完整的交互周期。从你打开 Codex 开始对话，到执行收尾协议结束——整个过程就是一个 Session。

**生命周期：** 被创建（Agent 进站或你发起新会话）→ 进行中（期间 Task 被创建和执行、State 被更新）→ 结束（收尾协议执行完毕）→ State 清空，关键操作记录转为 Memory。

**Owner：** Session Manager（Phase 1 作为 State Store 的一部分实现）。

**结构关系：** 一个 Session 包含 1..N 个 Task，每个 Task 有自己的瞬时 State。Session 结束时，它管理的所有 Task 的 State 必须已完成或显式中止。Session 是 State 的容器，自己也是 State Store 管理的一个对象。

**Consumer：** Agent（知道自己在一个 Session 中）、EVR（从 Session 历史中萃取模式）、你自己（回顾"上次聊了什么"）。

---

## 6. Protocol（协议）

**一句话：** "怎么做"的标准化步骤。你的 7 个 `agents/` 文件——ingest-protocol、wrapup-protocol、check-protocol 等——都是 Protocol。

**生命周期：** 被定义（编写或从经验中萃取）→ 被使用（Agent 在执行 Task 时调用）→ 可能被弃用（发现更好的做法后标记为 deprecated）→ 被替换。Protocol 不会直接删除，只会标记弃用并保留历史版本。

**Owner：** Protocol Registry（Phase 2 实现）。当前是你手动维护。

**当前形态：** 7 个 Markdown 文件存放在 agents/ 目录，由 AGENTS.md 的按需加载规则管理。Phase 2 将迁移至 protocol/ 并升级为 YAML。

**Consumer：** Planner（选择"用哪个 Protocol 来执行这个步骤"）、Agent（执行 Protocol 的具体步骤）。

---

## 7. Task（任务）

**一句话：** 被发起的执行单元。"帮我研究一下 HMS"——这句话被 Planner 解析后创建的就是一个 Task。

**生命周期：** 被创建（用户提出需求或 Planner 自我生成）→ 排队或立即执行→ 执行中（State 被不断更新）→ 完成（结果写入 Knowledge 或 Memory）或失败（记录失败原因）→ State 清空。

**Owner：** Task Engine（Phase 1 作为 State Store 的一部分实现）。

**Consumer：** Planner（编排 Task 的执行步骤）、Agent（执行 Task 中的具体操作）、你自己（知道"现在在做什么"）。

---

## 8. Event（事件）

> **核心组件。** Phase 1 搭框架（event-bus/stub.py），Phase 2 设计事件契约，Phase 3 正式启用。
> Event Bus 与 State Store、Memory Store 并列为 Agent Runtime 的三核心基础设施。

**一句话：** 系统内部发生某件事时发出的通知。"Task 完成了""知识页被更新了""Agent 崩溃了"——这些都是 Event。

**生命周期：** 被发出（emit）→ 被消费（一个或多个订阅者收到）→ 可能被记录（转为 Memory 的一部分）。

**Owner：** Event Bus（Phase 1 搭建框架，Phase 3 正式启用）。

**Consumer：** Planner（监听到 Task 完成后自动开始下一步）、EVR（监听到异常模式后触发 Extraction）。


## 9. Graph（图）— Phase 2 预留

**一句话:** 对已有对象之间关系的结构化建模。四种 Graph（Knowledge/Capability/Workflow/Dependency）构成 Runtime 的导航层。

**判定依据:** Runtime 在执行 Task 时需要按 Graph ID 找到它、查询节点和边（状态查询）、进行遍历和过滤（执行操作）。三项全满足 → 一等对象。

**生命周期:** 被构建（从 Knowledge/Protocol/Task 中萃取关系）→ 被查询（Agent 做路由决策时查 Graph）→ 可能被更新（新知识入库后重新构建）。

**Owner:** Knowledge Engine（Phase 2 实现）。

**Consumer:** Planner（路由决策）、Agent（技能链选择）、EVR（从 Graph 结构中发现模式）。

---

## 版本记录

- v0.2（2026-07-17）：Review 修正——Memory Owner 更正、Session/State 边界明确、Protocol 当前位置如实反映、Event 定位升级为核心组件、Graph 新增为第 9 号预留对象。
- v0.1（2026-07-16）：Phase 0 初始版本。7 个确认对象 + 1 个预留对象。不含 Schema。
