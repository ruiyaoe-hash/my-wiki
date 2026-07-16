---
title: HMS 全息记忆系统
created: "2026-07-16"
updated: "2026-07-16"
type: note
domain: ai-engineering
status: evergreen
source: https://mp.weixin.qq.com/s/fIW88tVvRw7GtXgmG5dExg
source_label: 新智元
tags:
- memory-system
- agent-memory
- protocol
- self-evolution
- shadoweave
---

# HMS 全息记忆系统

## 一句话

Shadoweave（织影）团队做的 AI 记忆层——不是又一个存储方案，而是 AI 时代的中立记忆协议。

## 核心架构

### 留存与回忆分离

HMS 的第一个关键判断：把记忆拆成两件独立的事。

- 留存（Retention）：经历被结构化沉淀进稳定记忆库，一旦沉淀不再被随手改写
- 回忆（Recall）：面对具体问题，现场重建回答所需的证据

这和人脑的互补学习系统一致：海马体暂存 -> 睡眠中回放给皮层 -> 皮层缓慢巩固。

### 三步回忆法

不是查库，是规划-检索-验证：

1. 先想清楚要找什么，再动手。先把问题拆开（时间段、人物、事物），把相对时间换算成确切日期
2. 六把不同的钥匙：按时间追、按人串、按上下文补、按最新值查、按矛盾抓、按关系跳
3. 找完回头验一遍：每格证据都填上了吗？不够就补。去重、按时序排好、标注来源

### 五动词协议

HMS 的核心接口：read / write / handoff / rollback / verify。

任何模型、Agent、机器人只要实现这五个动词就能接入。这是 Protocol 从 Prompt 升级为 Machine-Readable 的完美范例。

### 自进化飞轮

HMS-self-evolve 的 6 个模块：计数去重、相对日期锚定、精确日期回填、数值差异校准、当前与历史状态仲裁、双层来源锚定。

本质上是 EVR 方法论在记忆层的一个具体实现：从真实使用中发现错误模式 -> 自动修正。

## 与我们项目的关系

| HMS 概念 | 我们的对应 |
|----------|-----------|
| 留存与回忆分离 | State（瞬时）vs Memory（不可变）分离 |
| 五动词协议 | Protocol 从 Prompt 升级为 Machine-Readable API |
| 记忆独立成层 | 模型无关、工具无关原则 |
| 自进化飞轮 | EVR 方法论（Extraction -> Validation -> Refinement） |
| Memory Controller | Agent Runtime 的 Knowledge Engine 层 |
| Memory Bank | Agent Workspace 的 Knowledge 面板 |

## 关键数据

- LongMemEval：92.8%（此前最强 HMS-base 92.4%，Hindsight 88.8%）
- LoCoMo：93.5%
- GitHub：https://github.com/Shadow-Weave/HMS
