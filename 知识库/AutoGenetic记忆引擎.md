---
title: AutoGenetic 记忆引擎（JiuwenMemory）
created: '2026-07-02'
updated: '2026-07-06'
type: note
domain: ai-engineering
status: growing
related:
- '[[外部记忆-行业全景]]'
- '[[Mem0 记忆层]]'
- '[[HippoRAG 记忆框架]]'
- '[[Agent记忆技术全景]]'
- '[[LLM Wiki模式]]'
- '[[OpenViking 上下文数据库]]'
- 'Context 即 Agent（概念）'
tags:
- agent-memory
- memory-engine
- huawei
- openjiuwen
- auto-genetic
- graph-memory
- swarm
description: 华为 openJiuwen 社区开源的自生长 Agent 记忆引擎。设计理念是让记忆像基因片段一样自主生长、跨平台共享、可自我演化。核心特征：L0-L3
  分层记忆、AutoDreaming 后台加工、MemoryTurbo 低延迟、GraphMemory 关系网络、Adapter 解耦、Swarm 群体记忆。
---
# AutoGenetic 记忆引擎（JiuwenMemory）

华为 openJiuwen 社区于 2026年6月底 开源的 Agent 记忆引擎，核心理念是把记忆从"存下来"变成"长出来"——每条记忆像基因片段一样可复制、可共享、可演化。

在 LoCoMo 基准上，作为插件接入 OpenClaw 后准确率提升 15%，Token 消耗降低超 60%。

---

## 分层记忆体系（L0–L3）

解决扁平时间轴记录导致的信息混杂问题：

| 层级 | 名称 | 内容 |
|------|------|------|
| L0 | 原始信息层 | 完整对话历史 + 时间戳元数据，支持回溯与全量分析 |
| L1 | 摘要记忆层 | LLM 压缩单次会话关键结论，降低 Token 消耗 |
| L2 | 结构化记忆层 | 情景记忆（事件/决策时间轴） + 语义记忆（背景知识/技术细节） |
| L3 | 用户画像层 | 偏好、习惯、角色定位、结构化变量（姓名/时区/语言） |

三价值：信息密度逐级放大、偏好与技术细节不互相覆盖、各层独立存储跨会话持久保留。

---

## AutoDreaming（自动做梦）

受人类睡眠记忆固化启发，将记忆提取等高成本计算从在线对话路径剥离，转入后台定时离线异步完成。

- **浅睡**：增量筛选
- **REM**：LLM 单遍完成提取与归类
- **深睡**：语义去重、冲突消解后写入长期记忆
- 控制手段：忙碌退避、断点续扫、压缩截断、批次封顶，Token 开销线性可控

类比：基因的"复制校对与自然选择"——淘汰无效/矛盾片段，留下已验证的优质基因。

---

## MemoryTurbo（记忆涡轮增压）

前台对话产生"排气"（新增信息），后台飞轮旋转转化为"增压"（结构化记忆），越用越高效。

- 动能解耦：原始对话瞬间写入缓存向量库，记忆提取异步调度
- 离心式语义聚类：小模型先按话题合并对话，一组一起提取，摊销 LLM 调用
- 效果：用户感知时延降低 80%，Token 用量再降 50%+

---

## GraphMemory（关系化记忆）

将孤立事实升级为动态关系网络，让 Agent 理解"人、事、物"的长期关联。

- 实体与关系链路召回上下文，解决纯语义相似度检索的遗漏问题
- Episode 保留来源溯源，图谱持续合并更新
- 跨会话、跨文档信息组织成关系网络，支撑组织级知识复用

---

## 动态 Adapter 层（不绑定设计）

双维度解耦架构：

- **Plugin 维度**：面向 Agent 平台（已支持 OpenClaw 等）
- **Provider 维度**：面向记忆引擎存储（已内置 JiuwenMemory 和 Mem0）

核心哲学：记忆不属于任何框架，是跨平台共享的基础设施。平台变了记忆不丢。

---

## Swarm Memory（群体记忆）

从个体记忆到组织级记忆池的范式升级：

- 每个 Agent 独立积累个体记忆，同时将可共享经验沉淀至组织级记忆池
- 新 Agent 加入时继承组织已沉淀的领域知识、客户画像与问题解决路径
- "一人经验、全员受益"，记忆从个体资产升级为组织级数据资产

---

## 与现有记忆生态的关系

JiuwenMemory 是继 [[Mem0 记忆层]]（YC S24）之后又一个开源记忆引擎，但设计方向不同：

- **Mem0** 侧重通用记忆 SDK 和 API 化，面向开发者快速集成
- **HippoRAG** 侧重海马体启发的持续学习与保留
- **JiuwenMemory** 则更强调**记忆的自主生长能力**——不仅存得住，还要自己"做梦"、自己"进化"，同时引入 Swarm 群体记忆的跨 Agent 沉淀
- 它与 [[OpenViking 上下文数据库]]（字节开源，L0/L1/L2 分层加载）有相似的分层设计哲学

---

## 相关资源

- openJiuwen 官网：https://www.openjiuwen.com/
- JiuwenMemory 代码仓：https://gitcode.com/openJiuwen/agent-memory/
- 原文：[[jiuwenmemory-autoGenetic记忆引擎|JiuwenMemory 源摘要]]
- 源文章：机器之心报道（原文已归档至源/原文/）

> 本页由 2026-07-02 机器之心文章《华为开源 Agent 记忆引擎 JiuwenMemory》入库生成。

## 2026-07 机器之心《JiuwenMemory：让记忆从"存下来"变成"长出来"》（补充来源）

2026-07-06 入库的第二篇原文（源/原文/机器之心-AutoGenetic记忆引擎JiuwenMemory正式发布.md），对 6 月报道做了更深入的系统阐述。新增的架构细节：

**MemoryTurbo 离心式语义聚类细节**：小模型先按话题合并对话、一组一起提取，既保证连贯避免语义漂移、又大幅摊销大模型调用次数。效果——用户感知时延降低 80%，Token 用量降低 50%+。

**Adapter 层"双维度解耦"设计哲学**：Plugin 维度面向 Agent 平台（已支持 OpenClaw）、Provider 维度面向记忆引擎（已内置 JiuwenMemory 和 Mem0）。核心主张——"记忆不属于任何一个框架，它是跨平台共享的基础设施"。

**产业趋势判断**：Agent 记忆的竞赛正在从"能不能记住"转向"记下来的东西能不能自主生长"。三条独立路线（AutoGenetic Memory / Memory as Metabolism 五步代谢 / SCM 睡眠巩固）在此方向上收敛。这个判断与 [[Memory as Metabolism 记忆代谢]] 的核心论证高度同构。
