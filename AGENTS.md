# 我的 AI 知识库 — AI 助手工作说明

## 文件夹说明
- 源/原文/ - 原始源码归档（okf/、openrath/、articles/ 三个子目录）
- 知识库/（含概念/方法/分析/MOC 子目录） - AI 写的知识页面（你读）。域 MOC 页面（🏠 前缀）为入口，其余为概念页
- 源/摘要/ - 源材料摘要（你读）
- 🏠 首页.md - 知识库导航主页
- agents/ - 按需加载的协议文件（触发词激活）


## State 层（Phase 1 新增）

- state/current-task.json — 当前正在执行的任务（状态、进度、持有者）
- state/task-queue.json — 排队中的任务列表
- state/session.json — 当前会话元数据
- state-manager/manager.py — 多 Agent 状态协调器（锁/校验/合并/历史/恢复）

进站时先读 state/session.json 判断会话状态，再读 state/current-task.json 恢复执行上下文。
进度和 TODO 不再从 hot.md 读取——hot.md 从现在起只保留不可变的 Memory。
如果 state/current-task.json 为空（	ask_id: null）且 task-queue.json 为空，则退回到 **下次工作计划.md** 寻找待办任务。

## 三个基础设施文件
（AI 专用）
- index.md - 全局目录。接问题先翻这里，找到相关页面再深入读
- log.md - 操作日志。每次摄入/检查/编辑/会话结束后在此追加记录。新条目放顶部。每月末将旧条目归档到 归档/会话/YYYY-MM-log.md，只保留当月记录
- hot.md - 热缓存。每次会话结束时更新，存最近上下文

## 操作协议

### 提问 (Query) — 始终加载
1. 先读 hot.md（可能已经有答案）
2. 再读 index.md 找相关页面
3. 深入读 知识库/（含概念/方法/分析/MOC 子目录） 中的页面
4. 用 wikilink 标注来源回答


### 搜索 (Search) — 始终加载
1. 先读 agents/capability-map.md，确认目标场景的最优工具链
2. 按地图指定的路径执行，禁止 which/--help 摸索
3. 状态工具不可用时（如浏览器未安装），降级到地图标注的无状态备选
4. 遇 JS 渲染站点返回空时，改用搜索引擎缓存或替代源
### 检查 (Lint) — 始终加载
1. 找断链、孤儿页、衰老内容（距上次更新超过 90 天）、矛盾
2. 报告问题，询问是否修复
3. 详细步骤见 agents/check-protocol.md
4. 在 log.md 顶部追加检查记录

---

## 按需加载规则

以下文件不在启动时全量加载。Agent 根据触发条件按需读取：

| 文件 | 触发条件 |
|------|----------|
| agents/ingest-protocol.md | 用户说"吃进去"、"入库"、"ingest" |
| agents/check-protocol.md | 用户说"检查"、"lint" |
| agents/wrapup-protocol.md | 用户说"收尾"、"结束"、"wrapup" |
| agents/capability-map.md | 执行任何外部工具调用前（搜索、抓取、API 调用） |
| agents/context-budget.md | 每次收到用户消息后轮询 get_goal，用量超 50K 时读全文 |
| agents/踩坑集.md | 遇到重复失败、工具多次重试不成功、用户指出错误模式时 |

原则：启动只读本文件 + hot.md + index.md。命中了触发条件才打开对应协议文件。

---

## 场景 → 技能链

高频场景不用每次手动判断该加载哪些协议。直接按下面的链走：

| 场景 | 触发例 | 技能链（按顺序加载执行） |
|------|--------|------------------------|
| 🔗 外部链接入库 | "看看这篇"、发 URL + "吸收/入库" | capability-map（确定抓取策略）→ ingest-protocol（七步入库）→ 自动更新 hot.md |
| 🔍 全库检查 | "检查"、"lint" | check-protocol（断链/孤儿页/stale/矛盾）→ 报告问题 → 询问是否修复 |
| 🚪 会话收尾 | "收尾"、"结束"、"wrapup" | wrapup-protocol（七步收尾，含 Prune） |
| 🔎 外部搜索 | "搜一下XX"、查资料 | capability-map（选工具链）→ 执行搜索 → 结果返回后，如果需要长期保存则走 ingest-protocol |
| 🐛 踩坑记录 | 工具多次重试失败、用户说"又出这个问题" | 读 agents/踩坑集.md（查是否已有同类记录）→ 追加新条目或更新已有条目 → 必要时在 log.md 标记 `[protocol-gap]` |
| 🔧 协议迭代 | 发现工作流卡壳、用户说"这个流程不对" | log.md 标记 `[protocol-gap]` → 记录具体问题和改进方向 → 下次会话的 hot.md P0 优先列出 |

---

## 自检清单（每次动作后）

-  PowerShell 中 Python 脚本优先写 .py 文件再运行，避免 -c 多行转义
-  文件写入后验证实际状态，不信任 stdout 的"成功"
-  非 ASCII 文本读写一律指定 -Encoding UTF8
-  不执行 git reset --hard / git checkout -- 等破坏性命令，除非用户明确要求
-  编辑文件用 apply_patch，不用 cat/shell write 技巧
-  搜索文本优先用 rg，不用 grep
-  本次卡壳是执行问题还是协议问题？如果是协议问题，在 log.md 标记 `[protocol-gap]`，下次会话优先改协议
