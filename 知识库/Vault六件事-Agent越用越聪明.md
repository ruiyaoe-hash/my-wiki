---
title: Vault六件事-Agent越用越聪明
created: '2026-06-28'
updated: '2026-06-28'
type: note
source_url: https://mp.weixin.qq.com/s/oFcr-wj6TUAV-s9Rsi1zYg
source: 微信公众号 万涂幻象 MAGAZINE vol.241 · 2026.05.26
domain: meta
status: developing
related:
- '[[祥瑞知识管理三部曲]]'
- '[[AI记忆的遗忘曲线]]'
- '[[KEA架构与知识流转]]'
- '[[Agent记忆技术全景]]'
tags:
- 知识管理
- Agent记忆
- Vault
- 三层记忆
- PROGRESS
- Skill
description: 祥瑞 vol.241。六件让 Claude Code 每天比昨天更聪明的事：三层记忆、对话交班、PROGRESS.md、能力地图、Skill系统、自检体检。
---
# Vault 六件事：Agent 越用越聪明

## 核心论断

> "聪明的不是 AI，是你的 Vault。"

Agent 越用越聪明这件事，跟 Agent 本身关系不大。你换 Claude、换 GPT、换 Gemini，差别没有想象中那么大。真正决定它聪不聪明的，是它住的那个文件夹长什么样。

## 六件事总览

### 1. 三层记忆分离

| 层级 | 内容 | 存储方式 | 加载策略 |
|------|------|----------|----------|
| L1 持久画像 | 用户是谁、性格、使命 | user.md，半年改一次 | 需要理解背景时才读 |
| L2 程序性记忆 | 标准做法、踩过的坑 | 按主题切碎成小文件 + MEMORY.md 索引（几 KB） | 启动只读索引，命中再读详情 |
| L3 历史检索 | 每天的事件流水 | 按天分日志 + OpenViking 语义索引 | 平时不读，需要时语义搜 |

**关键设计：语义去重。** memory_update.py 在写入前做语义比对，已有同义条目则跳过，补充细节则 merge，真正新的才追加。杜绝"同一件事换说法重复记"。

**效果**：启动 token 从三万砍到三千。

### 2. 对话交班（五步协议）

每次对话结束自动执行：
- A. 经验教训 → L2 程序性记忆
- B. 事实流水 → L3 日志
- C. 知识编译 → 独立笔记
- D. 文件统计 → Vault 总览
- E. 自检：下一个 session 能不能独立拿到所有需要的信息？

### 3. PROGRESS.md

每个项目一个 PROGRESS.md，记录当前状态、待办、决策记录。Agent 跨对话续上故事。里面包含任务拆解、进度、决策记录、踩坑笔记、相关记忆索引。

### 4. 能力地图（反向索引）

不按"工具名"组织，按"我要做什么"组织。格式：
```
消息推送 → lark-cli im +messages-send
知识检索 → brain_search / ov find / obsidian-cli
```
Agent 执行任务前必查地图，禁止 which/--help 摸索。从最初二十几行长到两百多行。

### 5. Skill 系统

每个 skill = SKILL.md + references/ + scripts/。平时不加载，触发词激活时才读。

**内化 vs 安装**：不直接装别人的 skill，而是让 AI 读完后提炼设计思想，结合自己的语料重新长出来。"骨架是别人的，血肉是自己的。"

### 6. 自检 + Hooks + 定期体检

三层质量保证：
- **动作级**：每次完成动作照着自检清单过一遍（CLAUDE.md 第 0 节）
- **工具级**：PostToolUse hooks 强制语法校验、路径合规、frontmatter 合规
- **系统级**：vault-gardener（周检） + cc-health（月检）

## 对 Wiki 的启示

| 祥瑞的做法 | Wiki 可借鉴 |
|-----------|------------|
| L1/L2/L3 记忆分离 | hot.md(L1) + memory.md(L2) + log.md(L3) 角色更清晰 |
| 对话交班五步 | ingest 流程自动化 |
| PROGRESS.md | 项目级进度追踪 |
| 能力地图 | Agent 能力手册页 |
| Skill 内化 | 引入外部 skill 的标准流程 |
| 语义去重 | 知识页面自动去重 |
| PostToolUse hooks | lint 自动化 + frontmatter 守门 |
