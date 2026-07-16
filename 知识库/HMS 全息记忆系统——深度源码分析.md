---
title: HMS 全息记忆系统——深度源码分析
created: "2026-07-16"
updated: "2026-07-16"
type: note
domain: ai-engineering
status: evergreen
source: https://github.com/Shadow-Weave/HMS
source_label: Shadow-Weave/HMS (GitHub)
tags:
- memory-system
- agent-memory
- protocol
- self-evolution
- shadoweave
- source-analysis
---

# HMS 全息记忆系统——深度分析

## 项目概况

207 stars，25 forks，2026-07-12 创建（4 天）。Stars 还在快速增长。

## 架构分层

从仓库结构看，HMS 分四层：

| 层 | 目录 | 做什么 |
|---|------|--------|
| Core Daemon | core/daemon | 本地嵌入式记忆引擎（hms-embed CLI） |
| Dataplane | core/dataplane | 数据存储层（PostgreSQL + pgvector） |
| Interface | interface/sdk | 多语言 SDK（Python/Go/Rust/TypeScript） |
| Lab | lab/evaluation | 基准测试框架（LongMemEval + LoCoMo） |

## Go SDK 中的完整对象模型

从 Go SDK 的 100+ model 文件逆向出的完整对象模型——这是 HMS 真正的设计蓝图：

### 核心存储对象

| 对象 | 文件 | 含义 |
|------|------|------|
| Bank | banks | 记忆银行（顶层命名空间，类似数据库） |
| Document | documents | 记忆文档（一条记忆记录） |
| Entity | entities | 知识图谱节点（人名、事物、概念） |
| Chunk | chunks | 记忆片段（文档的子单元） |
| Tag | tags | 标签（Bank 和 Document 的双层标签系统） |
| File | files | 文件留存（支持图片等非文本记忆） |

### 智能对象

| 对象 | 文件 | 含义 |
|------|------|------|
| Directive | directives | 指令/规则（指导系统行为的声明式规则） |
| Mental Model | mental_models | 心智模型（系统自动学到的用户行为模式） |
| Consolidation | consolidation | 记忆巩固（压缩、合并、去重） |

### 运行时对象

| 对象 | 文件 | 含义 |
|------|------|------|
| Operation | operations | 异步操作（创建/查询/取消/重试） |
| Audit Log | audit_logs | 审计日志（谁在什么时候做了什么） |
| Webhook | webhooks | Webhook（事件驱动的外部集成） |
| Budget | budget | 用量配额 |

### 核心操作

| 操作 | 含义 |
|------|------|
| Retain | 写入记忆（结构化提取 + 存入） |
| Recall | 回忆记忆（多钥匙检索 + 验证 + 组织证据） |
| Reflect | 深度回答（综合多条记忆生成上下文答案） |
| Reprocess | 重处理文档（修改来源文本后重新提取） |
| Delete | 删除记忆 |
| Update | 更新记忆 |

### Entity（知识图谱节点）

HMS 不是 Key-Value 存储——每个 Entity 是一个知识图谱节点：

- entity_id / entity_type / name
- state（当前状态值，支持版本追踪）
- observations（观测记录，支持时间序列）
- 关联记忆文档的引用

这意味着 HMS 内部维护的是一张 Knowledge Graph，不是文档列表。

### Mental Model（心智模型）

这是 HMS 最与众不同的概念。系统自动从用户交互中学习规律，形成 Mental Model：

- trigger_conditions：触发条件（标签组合、字段匹配）
- output_rules：输出规则（基于触发条件自动执行的规则）
- 用户不需要手动编写规则，系统通过使用自动学会

这本质上是 EVR 的 V+R 在记忆层的实现。

### Directive（指令/规则）

用户可以显式设置的规则，例如"计划中的事件不应计为已完成"。

与 Mental Model 的区别：Directive 是用户手动设置的，Mental Model 是系统自动学习的。

## hms-embed CLI——产品化记忆层

最让人吃惊的是 hms-embed。它不是一个玩具 Demo，而是一个完整的产品：

### 架构

- 本地 daemon（后台进程，首次启动下载依赖+加载模型需 1-3 分钟）
- 自动管理生命周期（5 分钟无操作自动退出）
- PostgreSQL + pgvector 嵌入式存储
- 多 Profile 支持（每个 Profile 独立端口 8889-9888）

### 命令集

```
configure    - 交互式设置（OpenAI/Groq/Google/Ollama）
memory retain  - 写入记忆
memory recall  - 搜索记忆
memory reflect - 综合多条记忆的上下文回答
bank list    - 列出记忆银行
profile      - 管理多套配置
daemon       - 管理后台进程
```

### 针对 AI 编程助手的适配

```bash
curl -fsSL https://docs.hms.local/get-skill | bash
```

一行命令安装到 Claude Code、Cursor、Windsurf 中。hms-embed 被设计成 AI 助手可以调用的 CLI 工具。

## 评估框架

### 流水线

两个模式共用一个标准化流程：

```
Retain -> Recall -> Answer -> Judge
```

所有系统使用同一个模型（GPT-5-mini）做统一的记忆抽取、答案生成和判题，不存在模型差异注水。

### Ledger Pipeline（账本流水线）

核心创新：不给模型直接喂检索结果，先构建一个结构化的 Evidence Ledger（证据账本）：

- 事件时间
- 提及时间
- 来源会话/文档
- 事实类型
- 证据文本
- 数值/日期/更新信号
- 原始片段

账本做好之后，才交给模型。这解决了"检索结果一堆，模型在里面拼命找"的问题。

### Self-Evolution Pipeline（自进化流水线）

在 Ledger 基础上增加轻量级 Answer-Time Controller，驱动 6 个自进化模块：

1. 计数去重
2. 相对日期锚定
3. 精确日期回填
4. 数量差异校准
5. 当前与历史状态仲裁
6. 双层来源锚定

## 与我们 Agent Runtime 的深度对照

从源码分析看，HMS 的每一个设计层在我们架构中都有对应：

| HMS 概念 | 我们的对应 | 差异 |
|----------|-----------|------|
| Bank | Knowledge Engine 的 Bank 概念 | 我们的 Bank 尚未实现 |
| Document | Knowledge 对象 | HMS 的 Document 粒度更细（有 Chunk 子层） |
| Entity | Knowledge Graph 节点 | 我们还在规划四种 Graph |
| Mental Model | EVR 的 V+R 结果（自动规则） | 我们还没到这个粒度 |
| Directive | Policy 层的规则 | 我们的 Policy 层还在设计 |
| Operation | Task 对象（带异步状态追踪） | 我们的 Task 还没异步化 |
| Audit Log | Memory Store 的审计维度 | 我们还没考虑审计 |
| Consolidation | EVR 的 Refinement（记忆压缩） | 我们有方法论但没工程实现 |
| Webhook | Event Bus 的外部版 | 我们的 Event Bus 还是内部概念 |
| hms-embed CLI | 我们的 State Manager 的外部接口 | 我们还没到 CLI 产品化这一步 |
| Profile | Session 的多配置版本 | 我们的 Session 概念更简单 |

## 关键启示

### 1. 对象模型的粒度

HMS 的对象模型比我们目前设计的精细得多。Document 下面还有 Chunk，Entity 有 Observation 时间序列，Operation 有完整的异步生命周期。我们目前的 9 个 Runtime Object 只是第一层。

### 2. 产品化速度

hms-embed 的 CLI 体验（configure → retain → recall → reflect）已经是一个可用的产品。不需要读文档，一条命令上手。我们目前连 state/ 目录都还没建。

### 3. AI 编码助手的生态卡位

HMS 专门做了一条"给 AI 编码助手装 skill"的路径——这不是巧合。他们的判断跟我们一致：记忆层的第一个客户不是人类，是 AI Agent 自己。人类通过 AI Agent 间接使用记忆层。

### 4. 学习型系统 vs 规则型系统

HMS 的 Mental Model（自动学习）vs Directive（手动规则）的区分，跟我们讨论的 EVR（自动演化）vs Policy（手动权限）的区分高度一致。两边从不同起点走到了同一对概念。

### 5. 开源战略

HMS 的代码仓库非常工程化：多语言 SDK、Docker Compose、CI/CD、`.env.example`、完整的文档树。这和"发个论文附代码"完全不是同一量级——这是产品级的开源。