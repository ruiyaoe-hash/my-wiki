import os
PAGES = r'D:\my-wiki\知识库'

# Enrich Runtime Object
p = os.path.join(PAGES, 'Runtime Object 识别规则.md')
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
old = '\u8fb9\u7f18\u5bf9\u8c61\uff08\u9700\u8fdb\u4e00\u6b65\u9a8c\u8bc1\uff09'
new = '''满足规则的对象（已确认：9个）

| 对象 | 寻址 | 状态查询 | 操作 |
|------|------|---------|------|
| Knowledge | slug/path | evergreen/stale/stub | publish/link/update |
| Source | hash | ingested/referenced | ingest/reference |
| Memory | timestamp | recorded/archived | append/archive |
| State | task-id | running/paused/done | lock/update/clear |
| Protocol | name | active/deprecated | execute/deprecate |
| Task | task-id | created->running->done | start/pause/complete |
| Workflow | name | active/deprecated | execute/refine |
| Session | session-id | active/ended | start/end/recover |
| Event | event-id | emitted->consumed | emit/consume/archive |

边缘对象（需进一步验证）'''
c = c.replace(old, new)
c += '\n\n## 不需要 Non-Object.md\n\n如果 Object Rule 足够清晰，不需要一个单独的文件列出什么不是 Object。三个判定示例就足够。\n'
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK: Runtime Object enriched')

# Enrich State与Memory
p = os.path.join(PAGES, 'State 与 Memory 的分离.md')
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
ml = '''
## Memory 五层架构

| 层 | 名称 | 内容 | 生命周期 |
|---|------|------|---------|
| L0 | Working Memory | 本次 Task 瞬时上下文 | Task 结束清空 |
| L1 | Session Memory | 本次会话所有操作 | 会话结束归档 |
| L2 | Project Memory | 跨会话项目待办和进展 | 项目周期内 |
| L3 | Semantic Memory | 永久知识（现有 75 页） | 长期维护 |
| L4 | Archive | 历史归档 | 永久保存 |

hot.md 目前承担了 L0+L1+L2 三层，必须拆分。'''
insert_at = c.find('拆分方案')
c = c[:insert_at] + ml + '\n' + c[insert_at:]
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK: State与Memory enriched')

# Enrich 七层架构
p = os.path.join(PAGES, 'Agent Runtime 七层架构.md')
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
add = '''
## 四个 Primitive

| Primitive | 做什么 | 例子 |
|-----------|--------|------|
| File | 持久化、版本控制、跨工具共享 | Markdown 知识页 |
| State | 瞬时状态、任务队列、执行进度 | current-task.json |
| Graph | 实体间关系、推理路径、冲突检测 | typed relations |
| Execution | 调度、中断、恢复、执行 | Planner 循环 |

Runtime = Execution，不是 File + State + Graph。前三者是数据，Execution 才是 Runtime 本身。

## Graph 不是一种而是四种

| Graph 类型 | 节点是 | 边是 | 谁用 |
|-----------|--------|------|------|
| Knowledge Graph | 概念页 | supports/conflicts/extends | Agent 读知识时 |
| Capability Graph | 系统能力 | composed_of/prerequisite | Planner 选能力时 |
| Workflow Graph | 步骤 | next_success/next_failure | Planner 执行时 |
| Dependency Graph | 产出物 | derived_from/depends_on | 追溯来源 |

## State Manager + Multi-Agent 协调

State Manager 负责：Lock（乐观锁）、Validate（schema 校验）、Merge（冲突解决）、History（变更记录）、Recover（崩溃恢复）。

多 Agent 同时操作同一份 state 时，State Manager 是唯一真相源（single source of truth）。

## Event Bus

不轮询 State，消费 Event：KnowledgeIngested / PlannerCompleted / TaskFailed / NewSourceDetected / ConflictFound。

## Protocol 格式决策

- State：JSON（高频程序读写，需要 schema 校验）
- Protocol：YAML（人+AI 可读，低频修改）
- Config：TOML（可选，生态依赖）'''
insert_at = c.find('关键设计决策')
c = c[:insert_at] + add + '\n' + c[insert_at:]
with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('OK: 七层架构 enriched')
