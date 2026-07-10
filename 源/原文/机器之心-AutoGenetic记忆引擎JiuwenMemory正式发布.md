---
source_url: https://mp.weixin.qq.com/s/loIZliLAfYr4z2eedjmX1w
source: 机器之心 微信公众号
type: raw
created: 2026-07-06
tags: [Agent记忆, AutoGenetic, JiuwenMemory, 华为, openJiuwen, 记忆引擎, raw]
---

# 华为开源 Agent 记忆引擎 JiuwenMemory：让记忆从"存下来"变成"长出来"

> 来源: https://mp.weixin.qq.com/s/loIZliLAfYr4z2eedjmX1w
> 发布: 机器之心
> 入库日期: 2026-07-06

## 核心摘要

华为 openJiuwen 社区开源了专为智能体设计的自主生长记忆引擎 AutoGenetic Memory。核心思想是：每一条记忆都像一段"基因片段"。AutoDreaming 与 GraphMemory 让基因片段更准，分层记忆体系与 MemoryTurbo 让基因构建更高效，Swarm 群体记忆让记忆基因在群体间实现组织级沉淀与共享。

LoCoMo 基准：作为插件接入 OpenClaw，准确率提升 15%，Token 消耗降低超 60%。

## 关键架构特性

**分层记忆体系 L0-L3**：L0 原始信息层 → L1 摘要记忆层 → L2 结构化记忆层（情景+语义） → L3 用户画像层

**AutoDreaming**：三阶段——浅睡增量筛选、REM LLM单遍提取归类、深睡语义去重冲突消解。全程无需人工标注，可溯源至原始会话。

**MemoryTurbo**：动能解耦（原始对话瞬间写入缓存层）+ 离心式语义聚类（小模型先按话题合并、一组一起提取）。用户感知时延降低 80%，Token 用量再降 50%+。

**Graph Memory**：Episode 保留来源溯源，Entity 和 Relation 沉淀结构化结果，图谱持续合并更新。

**动态 Adapter 层**：双维度解耦——Plugin 维度面向 Agent 平台，Provider 维度面向记忆引擎。"记忆不属于任何一个框架，它是跨平台共享的基础设施。"

**Swarm Memory**：个体记忆 → 组织级记忆池，新 Agent 继承已沉淀的领域知识，"一人经验、全员受益"。

## 相关资源

- openJiuwen 官网: https://www.openjiuwen.com/
- JiuwenMemory 代码仓: https://gitcode.com/openJiuwen/agent-memory/
