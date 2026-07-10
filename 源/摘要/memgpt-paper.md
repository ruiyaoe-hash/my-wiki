---
type: source
title: "MemGPT：LLM 作为操作系统"
description: "arXiv 2310.08560 论文摘要。UC Berkeley 提出虚拟上下文管理，让 LLM 像 OS 一样在主存和外存之间自动换页。"
timestamp: "2026-06-28T12:00:00Z"
created: 2026-06-28
tags: [MemGPT, 上下文管理, UC Berkeley, 论文, Letta]
status: seed
related:
  - "[[MemGPT 虚拟上下文管理]]"
  - "[[Letta 状态化Agent]]"
  - "[[Agent记忆技术全景]]"
domain: ai-engineering
---

# MemGPT: Towards LLMs as Operating Systems

**arXiv:** [2310.08560v2](https://arxiv.org/abs/2310.08560) | **发布:** 2023-10-12
**作者:** Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez (UC Berkeley)
**分类:** cs.AI, cs.CL

## 核心主张

大语言模型受限于固定上下文窗口，阻碍了在扩展对话和文档分析等任务中的效用。MemGPT 提出虚拟上下文管理——借鉴操作系统中的分层内存和分页技术——让 LLM 在主存（上下文窗口）和外存（长期存储）之间自主调度信息。

## 方法

- LLM 被赋予自主记忆操作函数：搜索对话历史、搜索长期归档、写入核心记忆
- 固定上下文（系统指令 + 人格 + 核心记忆）+ 可变上下文（动态换入换出的对话和检索结果）
- LLM 在需要时自主发起函数调用，从外存换入信息——类 OS 缺页中断

## 后续

- 开源仓库 `cpacker/MemGPT` 累计 ~12k stars
- 团队成立 Letta 公司，代码归档至 `letta-ai/letta-code`
- Letta 继承并扩展了自导向记忆管理理念
