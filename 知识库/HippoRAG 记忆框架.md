---
title: HippoRAG 记忆框架
created: '2026-06-27'
updated: '2026-06-27'
type: note
domain: ''
status: developing
related:
- '[[外部记忆-行业全景]]'
- '[[Mem0 记忆层]]'
- '[[AI持续学习]]'
tags:
- Agent记忆
- HippoRAG
- 持续学习
- 知识图谱
- 联想检索
description: OSU NLP 团队，3.8k stars。NeurIPS'24 → ICML'25。受海马体启发的 LLM 长期记忆框架，实现非参数持续学习。比
  GraphRAG/RAPTOR/LightRAG 更高效。
---
# HippoRAG 记忆框架

> 来源：OSU-NLP-Group/HippoRAG (3,789 stars) · NeurIPS '24 → ICML '25

HippoRAG 2 是一个强大的 LLM 记忆框架,受人类海马体长期记忆机制启发,增强 LLM 在新知识中识别和利用关联的能力——镜像了人类长期记忆的关键功能。

---

## 核心理念：从 RAG 到 Memory

传统 RAG 是"每次考试现翻课本"。HippoRAG 要做的不是翻得更快,而是让 LLM **真正记住并建立关联**——就像人脑的海马体把新经验和已有知识编织在一起。

### 三个关键维度

HippoRAG 2 在三个维度上评估持续学习能力：

1. **事实记忆（Factual Memory）**：能准确记住具体的知识点（NaturalQuestions, PopQA）
2. **意义建构（Sense-making）**：能整合大规模、复杂上下文（NarrativeQA）
3. **联想检索（Associativity）**：能跨多跳推理,找到间接关联（MuSiQue, 2Wiki, HotpotQA, LV-Eval）

HippoRAG 2 在所有三个类别上超越了其他方法。

### 高效索引

相比 GraphRAG、RAPTOR、LightRAG 等图方案,HippoRAG 2 的离线索引资源消耗显著更低,同时保持在线检索的成本和延迟优势。

---

## 与你 Wiki 的关联

- **意义建构**：你的 Wiki 通过交叉链接和结构化管理,本质上在做 HippoRAG 想自动化的事——帮 LLM 理解"这几条信息之间有什么关系"。
- **联想检索**：Wiki 的 wikilink 网络就是人工版的联想检索图。HippoRAG 把这个过程自动化了。
- **持续学习**：HippoRAG 的"非参数持续学习"概念,与你 Wiki 的"新资料摄入 → 更新相关页面 → 保持一致性"是同一类操作。
