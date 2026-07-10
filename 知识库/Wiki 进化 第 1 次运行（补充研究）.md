---
type: analysis
title: "Wiki 进化 第 1 次运行（补充研究）"
description: "补齐第 1 次运行中因 DDG/arXiv 不可用而缺失的搜索维度，更新搜索工具策略"
created: "2026-07-08"
updated: "2026-07-08"
tags: ["wiki 进化", "搜索工具", "能力地图", "研究补充"]
status: draft
domain: meta
related: ["Wiki 进化 第 1 次运行", "知识管理闭环蓝图"]
---

# Wiki 进化 第 1 次运行（补充研究）

## 搜索工具诊断报告（2026-07-08）

对五个搜索端点进行全面连通性测试：

| 工具 | 状态 | HTTP 码 | 原因 |
|------|------|---------|------|
| DDG（三端点） | ❌ 永久失效 | 000 | GFW 网络层阻断 |
| arXiv API | ⚠️ 严重限流 | 429 | 共享 IP 被限，20 秒冷却无效 |
| Bing (cn.bing.com) | ⚠️ 不可抓取 | 200 | JS 渲染，HTML 正文为空 |
| GitHub API（无认证） | ✅ 可用 | 200 | 限流 60 次/小时 |
| GitHub API（gh CLI 认证） | ✅ 最佳 | 200 | 限流 5000 次/小时 |
| Hacker News API | ✅ 可用 | 200 | 无认证，无限流 |
| OpenAlex API | ⚠️ 低质 | 200 | CS/AI 领域论文覆盖率低 |
| Google / Baidu | ❌ 不可用 | 000 | 网络阻断 |

**结论**：在中国大陆网络环境下，可靠的搜索通道只有两个——GitHub API（认证后）+ Hacker News API。学术论文搜索暂无稳定替代方案。

**已更新**：`agents/capability-map.md`——DDG 标记为失效，新增 GitHub 认证策略和 HN API。

## 补充研究发现

### 研究-A：AI 工程（GitHub topic:agent-memory）

| 项目 | 星数 | 关键信息 |
|------|------|----------|
| supermemoryai/supermemory | **28,249** | 记忆和上下文引擎，可完全本地运行，"AI 时代的记忆 API" |
| topoteretes/cognee | **27,311** | 开源 AI Agent 记忆平台，跨会话持久长期记忆 |
| volcengine/OpenViking | **26,404** | 自演化上下文数据库，统一 Agent 记忆 + 知识 RAG + 技能 |
| 666ghj/MiroFish | 68,087 | 群体智能引擎（关联度存疑） |

### 关键发现

1. **Cognee 爆发式增长**：上次入库时（6 月底）星数 ~429，现在 GitHub topic:agent-memory 搜索显示 27,311 星。一个月内增长了 60+ 倍。（注：需直接访问仓库验证星数，topic 搜索结果可能因缓存不准）

2. **supermemory（28K 星）是 wiki 完全未收录的新项目**：定位是"AI 时代的记忆 API"，可完全本地运行。这与你的 wiki 本地优先理念高度对齐。

3. **OpenViking 被你收录了但数据需要刷新**：wiki 中的 OpenViking 页面可能基于较旧版本。

### 对原始实验报告的影响

第 1 次运行报告中的「覆盖缺口」需要补充 supermemory 条目。P0-1（更新外部记忆-行业全景）需要新增 supermemory。

## 数据可信度

- GitHub topic 搜索的星数可能与仓库实际星数有延迟（topic 标签的缓存机制）
- 建议用 `gh api repos/OWNER/REPO` 直接验证关键仓库的实时数据
- 本次补充研究的质量与原始报告一致，仍偏工程视角
