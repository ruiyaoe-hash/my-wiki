# 上下文用量自动预警

> 对标 Claude Code 的百分比进度条。Codex 没有内置的百分比显示，但 Goal + token_budget 机制可以实现同等效果。
> 当前模型：DeepSeek V4 Pro，上下文窗口 1M token（输入），128K token（输出上限）。
> 阈值基于绝对 token 数（Lost in the Middle 研究），非窗口百分比。

## 触发条件
- 每次对话开始时，如果当前没有活跃的 Goal，自动 create_goal，设置 token_budget=100000
- 每次收到用户消息后，先用 get_goal 获取 tokensUsed 和 tokenBudget
- 计算 percentUsed = tokensUsed / tokenBudget * 100

## 预警阈值（基于质量拐点，非容量上限）

> 依据：Lost in the Middle (Stanford/UC Berkeley, 2023) — LLM 对上下文中段信息利用率显著下降，拐点约 50K token。

| 用量 | Token 数 | 动作 |
|------|----------|------|
| < 50K | 0-50K | 不提示，正常对话 |
| 50K-100K | 接近 Lost in the Middle 拐点 | 回复末尾轻提示 |
| 100K-200K | 超过社区实践共识的退化拐点 | 主动建议收尾 |
| > 200K | 越过两倍质量拐点 | 强制提示：强烈建议立即收尾 |

## 收尾流程

触发信号：用户说出"收尾"、"结束"、"wrapup"、"今天到这"或类似闭口信号时，立即执行。

1. 创建会话归档页 → 写入 归档/会话/
2. 更新 hot.md
3. 更新 log.md
4. 更新根 index.md
5. 更新子目录 index.md

纪律约束：收尾信号一旦发出，五步不可跳过。

## 注意事项
- token_budget 统计从 create_goal 开始算，不包含创建前的历史
- token_budget=100000 是质量保护预算，不是容量上限
- 一个中文字 ≈ 1.5-2 token
