---
title: Shadoweave HMS 全息记忆系统
source: https://mp.weixin.qq.com/s/fIW88tVvRw7GtXgmG5dExg
source_label: 新智元
date: 2026-07-16
ingested: 2026-07-16
type: summary
---

# Shadoweave HMS 全息记忆系统 - 摘要

## 一句话

一支平均 24 岁的 00 后团队（CMU、清华、哈佛等），做出了 AI 记忆层 HMS（全息记忆系统），双榜 SOTA，定位为 AI 时代的中立记忆协议。

## 核心思路

1. 留存和回忆分离：像人脑一样，海马体快系统暂存 -> 皮层慢系统巩固
2. 回忆不是查库，是先想清楚找什么、用 6 种不同的钥匙检索、然后验证
3. 自进化：6 个模块让系统越用越强
4. 五动词协议：read/write/handoff/rollback/verify 定义记忆层的标准接口

## 产品

- Memory Bank：个人记忆账户，数据所有权归用户
- HMS SDK：面向基座模型、Agent、机器人厂商

## 关键数据

- LongMemEval：92.8% 准确率（之前最强 88.8%）
- LoCoMo：93.5%
- 自进化提升：92.4% -> 92.8%（6 个精细模块）

## 与我们项目的关联

- 留存/回忆分离 = 我们的 State vs Memory 分离
- 五动词协议 = 我们的 Protocol 从 Prompt 升级为 Machine-Readable
- 记忆独立成层 = 我们的模型无关、工具无关原则
- 自进化飞轮 = 我们的 EVR 方法论
