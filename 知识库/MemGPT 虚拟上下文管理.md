---
title: MemGPT 虚拟上下文管理
created: '2026-06-28'
updated: '2026-06-28'
type: note
domain: ai-engineering
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Agent记忆技术全景]]'
- '[[Letta 状态化Agent]]'
- '[[生成式Agent-Stanford小镇]]'
- '[[Mem0 记忆层]]'
tags:
- Agent记忆
- MemGPT
- Letta
- 上下文管理
- UC Berkeley
description: arXiv 2310.08560。UC Berkeley 提出让 LLM 像操作系统一样管理记忆——在「主存」和「外存」之间自动换页，突破固定上下文窗口。后来商业化为
  Letta。
---
# MemGPT 虚拟上下文管理

> 来源：[arXiv 2310.08560](https://arxiv.org/abs/2310.08560) · 2023 年 10 月 · Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, **Ion Stoica**, **Joseph E. Gonzalez** (UC Berkeley Sky Computing Lab)
> 论文全称：**MemGPT: Towards LLMs as Operating Systems**
> 后续：团队成立 [Letta](https://www.letta.com)，原 repo `cpacker/MemGPT` → 归档至 `letta-ai/letta-code`

MemGPT 的核心洞察来自一个类比：**LLM 的上下文窗口就像计算机的内存（RAM），有限且易失；但计算机还有硬盘（外存），可以存放远超内存的数据**。为什么 LLM 不也这样呢？

---

## 虚拟上下文管理 (Virtual Context Management)

MemGPT 在 LLM 内部实现了一个**分页系统**——不是在硬件层面，而是在提示词层面：

```
┌──────────────────────────────────┐
│         Main Context (主存)        │
│  正在使用的对话 + 最近检索的记忆    │
│  ← LLM 只能直接看到这部分          │
├──────────────────────────────────┤
│       External Context (外存)      │
│  完整对话历史 / 文档 / 长期记忆    │
│  ← 靠 LLM 自主调用函数来读写       │
└──────────────────────────────────┘
```

LLM 被赋予了自主调度的能力：当它需要的信息不在「主存」里时，它可以主动发起一次函数调用，从「外存」中取出相关内容换入上下文窗口——一个 LLM 版的缺页中断（page fault）。

---

## 关键设计

### 1. 自导向内存管理

不是外部系统替 LLM 管理记忆，而是 **LLM 自己决定什么时候存、什么时候取、取什么**。MemGPT 给 LLM 暴露了一套记忆操作函数：
- `conversation_search(query)` — 搜索历史对话
- `archival_memory_search(query)` — 搜索长期归档
- `core_memory_append(content)` — 写入核心记忆

### 2. 固定 vs 可变上下文

| 上下文类型 | 内容 | 管理方式 |
|-----------|------|----------|
| 固定上下文 | 系统指令、人格设定、核心记忆 | 始终在最前面 |
| 可变上下文 | 对话历史、检索到的记忆、函数返回 | 动态换入换出 |

### 3. 中断式函数调用

当 LLM 判断「当前信息不够」时，它可以先暂停回复、调函数、等结果回来、再继续——这个模式后来被 OpenAI/Anthropic 的工具调用/function calling 体系吸收。

---

## 从 MemGPT 到 Letta

| 阶段 | 时间 | 形态 |
|------|------|------|
| MemGPT 论文 | 2023.10 | 学术原型，UC Berkeley |
| MemGPT 开源 | 2023-2024 | GitHub `cpacker/MemGPT`，累计 ~12k stars |
| Letta 公司 | 2024-2025 | 商业化，Y Combinator |
| Letta 框架 | 2025+ | 状态化 Agent 平台，`letta-ai/letta-code` |

Letta 继承了 MemGPT 的核心理念（Agent 自己管理记忆），并扩展到：
- 自我编辑记忆（memory blocks）
- 多 Agent 身份系统
- MemFS（Git 管理的文件式上下文）
- 桌面 App + CLI + 浏览器集成

详见 [[Letta 状态化Agent]]。

---

## 与其他方案对比

| 方案 | 记忆管理方式 | 谁在决策 |
|------|-------------|----------|
| Stanford 小镇 | 记忆流 + 反思 + 规划 | 系统规则 + LLM |
| **MemGPT** | **虚拟上下文管理 + 函数调用** | **LLM 自主调度** |
| Mem0 | ADD-only 记忆层 API | 外部调用 |
| FadeMem | 自适应衰减 + 融合 | 系统规则驱动 |

MemGPT 的独特性在于：把记忆操作的决策权交给了 LLM 自己，让 Agent 成为记忆的「所有者」而非「租户」。

---

## 与你的知识库

你的 [[知识管理闭环蓝图]] 中提到的 OpenRath 四步闭环（采集 → 编译 → 检索 → 行动）和 MemGPT 的「主存 ↔ 外存换页」有结构性呼应——都是把「信息在不同层级之间流动」作为核心设计。区别在于 MemGPT 让 LLM 自己决定什么时候流动。
