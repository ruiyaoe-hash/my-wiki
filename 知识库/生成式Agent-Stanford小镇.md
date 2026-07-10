---
title: 生成式Agent：Stanford 小镇
created: '2026-06-28'
updated: '2026-06-28'
type: note
domain: ai-engineering
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Agent记忆技术全景]]'
- '[[CoALA 认知架构]]'
- '[[MemGPT 虚拟上下文管理]]'
- '[[AI持续学习]]'
tags:
- Agent记忆
- 生成式Agent
- Stanford
- 记忆架构
- 涌现行为
description: arXiv 2304.03442。Stanford Joon Sung Park 等人在一个 Sims 风格的沙盒中部署 25 个生成式
  Agent，观察 → 反思 → 规划三步记忆架构，涌现出情人节派对等自主社交行为。Agent 记忆研究的奠基之作。
---
# 生成式Agent：Stanford 小镇

> 来源：[arXiv 2304.03442](https://arxiv.org/abs/2304.03442) · 2023 年 4 月 · Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein (Stanford)
> 正式名称：**Generative Agents: Interactive Simulacra of Human Behavior**
> 又名：Stanford AI Town / Smallville / 斯坦福 AI 小镇

这是 Agent 记忆方向的**奠基之作**。2023 年 4 月发布，被引用数千次，几乎每一个后来的 Agent 记忆方案（MemGPT、Mem0、HippoRAG、CoALA）都要引用它。

---

## 实验设置

- **25 个生成式 Agent** 放在一个 Sims 风格的沙盒环境中
- 每个 Agent 有名字、身份、日常作息（如「Isabella 是咖啡店老板，每天早上 8 点开店」）
- 用户可以用自然语言与任意 Agent 交互，也可以给 Agent 设定意图
- **核心挑战**：Agent 如何记住过去发生的事，并根据记忆做出合理的后续行为？

---

## 记忆架构：观察 → 反思 → 规划

```
观察 (Observation) → 反思 (Reflection) → 规划 (Planning)
     ↑                                        ↓
     └────────── 检索 (Retrieval) ←───────────┘
```

### 1. 观察 (Observation)
Agent 感知到的事件被记录为自然语言的记忆流（memory stream）——「Isabella 看到 Klaus 走进了咖啡店」「Maria 正在写论文」。

### 2. 反思 (Reflection)
不是每条观察都永远保留。系统会定期对记忆流做**层级抽象**：
- 底层：原始事件
- 中层：关于某人的印象（「Klaus 最近在研究音乐」）
- 高层：关于世界的信念（「这个小镇的人喜欢艺术」）

反思让 Agent 形成了超越原始数据的高层认知。

### 3. 规划 (Planning)
Agent 根据当前情境检索相关记忆，生成当天的行动计划。规划不是一次性写死的——Agent 会在执行过程中根据新观察动态调整。

---

## 情人节派对：自发涌现的社会行为

这是论文里最著名的案例：

> 研究者只给 **一个** Agent（Isabella）植入了初始意图：「我要办一场情人节派对」。

接下来的两天里，**没有任何额外编程**，Agent 们自主发生了以下行为链：

1. Isabella 开始装饰咖啡店、准备派对物料
2. 她主动邀请了朋友 Maria，Maria 又告诉了 Klaus
3. Klaus 邀请了 Ayesha 作为约会对象一起去派对
4. 多个 Agent 在派对当天同时出现在咖啡店
5. 派对结束后，Isabella 在记忆流中记录了「派对很成功」

**这是涌现行为（emergent behavior）**——没有一个中央控制器在协调，行为是从每个 Agent 的局部记忆和决策中涌现出来的。

---

## 学术影响

这篇论文确立了一个公式，后来被几乎所有 Agent 记忆框架继承：

> **Agent = LLM + 记忆流 + 检索 + 反思 + 规划**

| 后来者 | 继承了什么 |
|--------|-----------|
| **MemGPT** | 「记忆流 + 检索」→ 扩展为 OS 式虚拟上下文管理 |
| **Mem0** | 「记忆流 + 层级抽象」→ 工程化为 ADD-only 记忆基础设施 |
| **CoALA** | 「记忆架构」→ 形式化为认知架构理论框架 |
| **HippoRAG** | 「检索」→ 升级为海马体式联想检索 |
| **FadeMem** | 「信息过载」→ 引入主动遗忘解决存储膨胀 |

---

## 与你的知识库

你的 [[Agent记忆技术全景]] 如果追根溯源，起点就是这篇论文。它定义了问题空间，后来者都在它的框架内工作。Standord 小镇最值得记住的不是「25 个 Agent 会开派对」的 demo 效果，而是那个**三步记忆架构**——它是 Agent 记忆设计的「Hello World」。
