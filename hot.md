---
type: meta
title: "热缓存"
description: "热缓存：记录最近会话上下文、用户偏好和下次会话约定。"
timestamp: "2026-07-08T23:59:00Z"
updated: 2026-07-08
---

# 近期上下文

## 知识库当前状态
- 69 篇知识库（59 概念页 + 10 MOC 页）
- 3 域 MOC：Agent 记忆与认知 / Agent 系统工程 / 知识管理
- 7 子 MOC：记忆系统 / 认知机制 / Agent 架构与协作 / 工具与模式 / PKM 方法论 / Wiki 工程 / 行业观察
- 55 个标签（29 英/26 中）
- 源/原文/ 新增 4 篇：Lilian Weng 原博客、机器之心编译、autoresearch README、claude-code 架构

## 本次会话成果（2026-07-08，傍晚）

### Harness 工程专题入库
- 翁荔《Harness Engineering for Self-Improvement》完整摄入
- 2 知识页：[[Harness 工程]]（概念）+ [[Harness 工程对我们的启示]]（80/20 实用建议）
- 1 源摘要 + 4 源原文（含 karpathy/autoresearch 和 claude-code 两个 GitHub 仓库）
- 自动抓取并归档了 GitHub 仓库 README

### 关键认知
- Harness = 模型外面的"脚手架"：工作流、上下文管理、工具调用、评估
- RSI 路径判断：近期先发生在 Harness 层而非模型权重层
- 三大设计模式：工作流自动化 / 文件系统作为持久化记忆 / 子智能体与后台任务
- 我们的 AGENTS.md + 协议文件 + Wiki 就是在做 Harness 工程
- Claude Code 内部架构发现：Dream 系统（autoDream）跟我们 wrapup 协议的"记忆整合"思路高度一致

## 下次会话约定
- P0：更新外部记忆-行业全景（补充 4 个 2026 高星项目）
- P0：创建 Claude-Obsidian 对标分析 + Agent 记忆技术栈对比
- P1：标签分层（域/方法/工具/状态四类）
- P1：给 4 篇综述页补充实质内容或明确标记 stub
- P1：考虑借鉴 Claude Code Dream 系统改进 wrapup 协议的"记忆整合"步骤
- P2：引入页面新鲜度评分
- 搜索工具：DDG 不再使用，默认走 GitHub API（gh CLI 认证）

## 用户偏好确认
- 中文优先，大白话（小学可理解）
- 来源必须附带 URL + 一句话概括
- 目录结构：知识库平铺 + 源/原文/平铺，靠 MOC/Index 导航
- 分类原则：MOC 做导航（挑选），Index 做库存（全面）
