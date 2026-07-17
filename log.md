## [2026-07-16] wrapup | 会话收尾
- state/session.json：状态标记为 ended
- state/current-task.json：标记为 completed
- state/task-queue.json：清空
- hot.md：追加本次会话成果 Memory（HMS 分析 + Phase 0+1 完成）

## [2026-07-16] docs | CHANGELOG.md 替代迁移标记文件
- 删除 migration-plan.md + 3 个 _MIGRATION_NOTICE.md
- 新建 CHANGELOG.md：v0.0.0-wiki → v0.0.0 → v0.1.0 → Unreleased 完整版本历史
- 原则：版本变化写在 CHANGELOG 里，旧版通过 git checkout v0.0-wiki 恢复

## [2026-07-16] plan | 目录迁移计划 + 旧目录标记
- migration-plan.md：旧→新目录映射表 + 迁移时间表 + 检查清单
- 知识库/_MIGRATION_NOTICE.md、源/_MIGRATION_NOTICE.md、agents/_MIGRATION_NOTICE.md：迁移标记
- 原则：不删旧文件、不跨 Phase 迁移、Obsidian 兼容性优先

## [2026-07-16] build | Phase 1 完成——State Runtime v0.1

### 新建
- state/ 4 个 JSON 文件（schema + session + task-queue + current-task）
- state-manager/manager.py（lock/validate/merge/history/recover）
- policy.md（Agent 权限矩阵 v0.1）

### 修改
- hot.md：TODO 迁移到 state，只保留 Memory
- AGENTS.md：新增 State 层说明

### 验证
- State Manager 全部 5 个操作测试通过

## [2026-07-16] evolve | Phase 0 完成——Ontology v0.1

### Step 0a：Perspective + Object Rule
- ontology/perspective.md：Runtime 视角声明
- ontology/object-rule.md：一条规则判定一等对象（寻址+状态查询+执行操作）

### Step 0b：Object Discovery
- 从 7 个 protocol + hot.md + AGENTS.md 中扫描
- 发现 13 个候选对象

### Step 0c：Ontology v0.1
- ontology/ontology.md：7 个确认对象（Knowledge/Source/Memory/State/Session/Protocol/Task）+ 1 个预留（Event）
- 每个对象定义：一句话 + 生命周期 + Owner + Consumer
- 不含 Schema（Phase 1 后萃取）

### 项目分支结构
- main 分支：v0.0-wiki 基线（tag 已打）
- develop 分支：Phase 0 开发在此进行
- 预留目录：state/ memory/ protocol/ capability/ planner/ workflow/

## [2026-07-16] ingest | HMS GitHub 仓库深度分析
- 源/原文/hms-readme-en.md、hms-readme-zh.md：英文/中文 README 原文
- 源/原文/hms-longmemeval-benchmark.py：LongMemEval 基准测试实现
- 知识库/HMS 全息记忆系统——深度源码分析.md：完整对象模型 + 架构分层 + 评估框架 + 与我们的对照表
- 关键发现：Go SDK 暴露了 100+ model 文件，包含 Bank/Document/Entity/Directive/MentalModel/Consolidation/Operation/AuditLog 等完整对象体系
- hms-embed CLI 已经是产品级记忆层，直接集成 Claude Code/Cursor/Windsurf

## [2026-07-16] ingest | Shadoweave HMS 全息记忆系统入库
- 源/原文/shadoweave-hms-wechat.md：新智元报道原文（6054 字）
- 源/摘要/shadoweave-hms-summary.md：AI 摘要
- 知识库/HMS 全息记忆系统.md：知识页（核心概念 + 与我们项目的对照表）
- 核心验证：留存/回忆分离 = State/Memory 分离；五动词协议 = Protocol API化；自进化 = EVR
- GitHub：Shadow-Weave/HMS

## [2026-07-10] evolve | Wiki 进化大讨论——AI Wiki → Agent Runtime v0.1
- 系统定位升级：从 AI 可读的知识库 到 Agent 可运行的执行环境
- 核心方法论：EVR（Extraction → Validation → Refinement）
- 架构设计：七层架构（Vision → Ontology → Runtime → Knowledge+Capability → Planner → Application → Interface）
- 本体论：Runtime Object 识别规则（寻址 + 状态查询 + 执行操作）
- 关键分离：State（瞬时）vs Memory（不可变），Knowledge（对象）vs Capability（动作）
- 新建 6 篇知识页：Agent Runtime v0.1、EVR 方法论、Runtime Object 识别规则、七层架构、State 与 Memory 的分离、Schema Extraction 方法
- 开发路线：Phase 0（Schema Extraction）→ Phase 1（State Runtime）→ Phase 2（Knowledge+Capability）→ Phase 3（Planner+Application）
- GitHub 备份：[ruiyaoe-hash/my-wiki](https://github.com/ruiyaoe-hash/my-wiki)，227 文件，public
- hot.md / index.md / README.md 同步更新

﻿
## [2026-07-10] backup | GitHub 完整备份
- 仓库：[ruiyaoe-hash/my-wiki](https://github.com/ruiyaoe-hash/my-wiki)
- 内容：227 文件，545 KB，213 文件 + 1 bootstrap + Obsidian 配置
- 状态：public，main 分支，已验证远程树完整性
- 注意：源/原文/ 中 14.2MB PDF 已通过 .gitignore 排除
## [2026-07-08] upgrade | Harness 工程吸收——协议升级
- wrapup-protocol.md：六步→七步，新增第7步"剪枝 (Prune)"，借鉴 Claude Code Dream 系统
- 新建 agents/踩坑集.md：失败模式记录模板，目标积累20条后做模式分析
- AGENTS.md：新增"场景→技能链"映射表（6个高频场景 + 对应协议链）
- AGENTS.md：自检清单新增 protocol-gap 标记规则
- 理论来源：翁荔《Harness Engineering for Self-Improvement》80/20吸收

## [2026-07-08] ingest | 翁荔《Harness Engineering for Self-Improvement》入库
- 源/原文/：lilian-weng 原博客 + 机器之心中文编译 + karpathy/autoresearch README + claude-code 架构分析
- 源/摘要/：harness-engineering-self-improvement-summary.md
- 知识库/：[[Harness 工程]] + [[Harness 工程对我们的启示]]
- GitHub 仓库：karpathy/autoresearch (90K+ stars), yasasbanukaofficial/claude-code (3.6K stars)
- 核心发现：RSI 近期更可能先发生在 Harness 层而非模型权重层；文件系统作为持久化记忆是关键模式

﻿
## [2026-07-08] archive | 收尾——市场信号追踪系统上线
- 📋 市场信号.md：17 个对象追踪基线建立
- 引擎协议：第 0 阶段（市场信号读取）+ 🔄 刷新类建议
- 68 页知识库（58 知识 + 10 MOC），3 域 7 子 MOC

## [2026-07-08] archive | 全天会话归档——Wiki 架构重构 + 知识生命周期引擎首航
- 知识库：67 页（57 知识 + 10 MOC），3 域 7 子 MOC 结构
- MOC：🏠 Agent 记忆与认知 / 🏠 Agent 系统工程 / 🏠 知识管理
- 收尾协议升级为六步（+MOC 链路验证步骤）
- 会话归档页：归档/会话/2026-07-08 会话归档.md

## [2026-07-08] fix | 断链修复 + 协议补丁 + 标签审计
- AutoGenetic记忆引擎.md：修复 3 处断链（[[Context 即 Agent]] 改为纯文本、旧路径 [[原始资料/...]] 和 [[_raw/...]] 修正）
- ingest-protocol.md：新增三条铁律——每次编辑更新 updated 字段、所有入库文件必须有 source + source_label、知识页必须回链源材料
- check-protocol.md：新增 Frontmatter 一致性检查项（created vs updated、source/source_label 缺失检测）
- 标签审计：实际 55 个标签（非 128），29 英/26 中/0 混合，中英疑似重复仅 4 对且均弱相关，暂不合并
- AI驱动知识管理.md 和 AI持续学习.md 中的跨目录 wikilink（指向 源/原文/ 文件）在 Obsidian 中可正常解析，不做修改

## [2026-07-08] cleanup | 源/原文/ 回归平铺
- 撤销上一步创建的 5 个子目录
- articles/ 和 claude-code/ 内容搬回 root
- openrath-examples/（代码）、web-captures/（爬虫数据）直接删除——不属于原文库
- staging-archive/ 移至 归档/暂存归档/
- 原则：源/原文/ = 只有 .md 原文，平铺。跟知识库/ 保持一致。

## [2026-07-08] cleanup | 源/原文/ 目录整理
- OpenRath 代码（7 py + 1 toml + 1 html + 2 md）→ 源/原文/openrath-examples/
- 网页抓取（3 html + 3 txt + 2 html + 1 txt）→ 源/原文/web-captures/
- 14.5 MB PDF 加入 .gitignore
- 暂存区硅基流动报告（1 md + 1 pdf）→ 源/原文/staging-archive/
- 根目录从 65 项 → 46 项（45 md + 1 pdf）

## [2026-07-08] restructure | 五层 index 角色重新定义
- 根 index.md：从 MOC 菜单 → 封面页（what/why/recent）
- 知识库/index.md：对齐新 MOC 结构，成为完整目录（57 页按域分层）
- 源/摘要/index.md：从断链列表 → 按域分区的摘要库存
- 源/原文/index.md：断链 wikilink 全部移除，非 md 文件改为纯文本标注
- 归档/会话/index.md：补全会话摘要，增加 7 月新条目
- 原则：MOC 做导航（挑选），Index 做库存（全面），互不重复

## [2026-07-08] restructure | MOC 架构重构：3 域 × 统一维度 + 7 子 MOC
- 旧：🏠 AI工程(40链接超载) + 🏠 元知识 + 🏠 AI人才(空壳) —— 三个 MOC 命名维度不统一
- 新：🏠 Agent 记忆与认知 + 🏠 Agent 系统工程 + 🏠 知识管理 —— 全部按「关注点」统一命名
- 新增 7 个子 MOC：记忆系统 / 认知机制 / Agent 架构与协作 / 工具与模式 / PKM 方法论 / Wiki 工程 / 行业观察
- 每个域 MOC 控制在 7 个直接链接以内（1 入门 + 2 子 MOC + 4 综述/产出）
- AI人才 降级为 📋 行业观察（stub 状态，保留结构等未来内容充实）
- 根 index.md 已更新指向新 MOC
- 删除旧 MOC 文件：🏠 AI工程.md / 🏠 元知识.md / 🏠 AI人才.md
## [2026-07-08] toolchain | 搜索工具链诊断 + 能力地图更新 + 研究补充
- DDG 三端点全挂（HTTP 000，GFW 阻断），从能力地图移除
- arXiv 429 限流顽固（20s 冷却无效），降级为"谨慎使用"
- Bing HTML JS 渲染，不可抓取
- GitHub API 确认稳定（无认证 60/h，gh CLI 认证 5000/h）
- HN API 确认可用（无认证无限流）
- 补充研究：发现 supermemory (28K⭐) 未收录
- capability-map.md 更新：搜索策略 DDG → GitHub API + HN API

## [2026-07-08] wiki 进化 | 第 1 次实验运行
- 启动知识生命周期引擎：4 研究 Agent + 2 挑刺 Agent + 1 合成 Agent
- GitHub API 搜索发现 17 条（5+3+6+3），DDG 不可用，arXiv 限流
- 对抗审查发现 6 条有效质疑（3 数据源偏差 + 3 证据缺口）
- 产出 P0×3、P1×4、P2×3 改进建议
- 实验报告：知识库/Wiki 进化 第 1 次运行.md
- 待办写入：知识管理闭环蓝图.md 待办段落
- 降级记录：DDG 000（端点不可达）→ GitHub API | arXiv 429 → 跳过

﻿
## [2026-07-08] lint | P0 清理 + 知识库平铺统一
- P0 清理：删除 3 个临时文件（_ingest_tmp.py, _knowledge.js, _check.py）
- P0 清理：删除空 MOC/ 目录（含 0 字节 🏠 AI工程.md 僵尸文件）
- P0 清理：删除 3 个僵尸文件（weixin-article4.txt-0字节, okf-knowledge-readme.md-20字节, 🏠 首页.md-错误内容）
- P0 清理：删除 2 个空目录（工作台/复盘/, 工作台/项目/）
- P1 统一：5 篇 Claude Code 页面从 知识库/概念/ 搬回 知识库/ 根目录，删除空 概念/ 目录
- P1 统一：知识库确认平铺策略（58 篇全在知识库/根目录，0 个子目录）
- P2 修复：根 index.md 中 5 个 MOC/ 和 方法/ 前缀断链全部修正
- 根目录文件清单：AGENTS.md, hot.md, index.md, log.md, milestones.md, 使用者画像.md

## [2026-07-08] ingest | Claude Code 四种 Loop + 四篇官方文档 80/20 入库
- 微信文章入库：源/原文/articles/2026-07-08-claude-code-loops-wechat.md
- 四篇官方文档入库：源/原文/claude-code/（agents.md, goal.md, routines.md, workflows.md）
- 5 篇知识页入库：Claude Code Agent 循环机制、并行 Agent 机制、Goal 目标循环、Routines 云端例程、动态工作流
- 5 篇源摘要入库：源/摘要/claude-code-*-summary.md
- 所有来源均标注 URL + 一句话说明（source_label）
- 内容用大白话重写，以生活化比喻（工人/剧本/裁判）解释抽象概念
## [2026-07-06] archive | 收尾完成（六轮会话，累计入库 15 篇概念 + 11 篇原文 + 10 篇源摘要）
- 归档页：2026-07-06 会话归档.md（六轮完整会话归档）
- hot.md + log.md 刷新
## [2026-07-06] archive | 原文入库完成（11篇原文 + 10篇源摘要 + 14篇概念页回链）
- 6篇论文原文入库（源/原文/）：Memory in the Age of AI Agents、From Human Memory to AI Memory、AI Meets Brain、Memory for Autonomous LLM Agents、Memory as Metabolism、SCM
- 1篇对话原文入库：ChatGPT对话-AI记忆与智能进化（17K chars）
- 4个项目README入库：Zep、LangGraph、Cognee、ChatGPT对话
- 10篇源摘要入库（源/摘要/）：6篇论文 + 3个项目 + 1篇对话
- 14篇概念页状态更新：全部从"概念占位页"回链到已入库原文
- 源/摘要/index.md 刷新（33→43篇）
## [2026-07-06] ingest | ChatGPT 对话对标入库 + 差距分析（15 篇新建 + 4 个基础设施文件更新）
- ChatGPT 共享对话完整解析：五篇必读论文 + 五个开源项目 + 八个研究热点对标
- 新建 11 个概念占位页：4 篇综述论文 + 3 个开源项目 + 4 个热点（详见 知识库/index.md）
- 新建 3 个分析页：Memory as Metabolism 记忆代谢、SCM 睡眠巩固记忆、主动遗忘 Learned Forgetting
- 新建 1 个分析报告：[[Wiki知识缺口分析报告-ChatGPT对话对照]]（覆盖矩阵 + 结构性缺口 + P0-P3 优先级）
- 🏠 AI工程 MOC 新增综述论文/工具与项目/前沿研究热点三个章节
- 知识库/index.md 全面刷新（61 篇）
- 标签索引新增 12 个标签（112→128）
- hot.md + log.md 同步刷新
## [2026-07-02] archive | 会话归档
- 归档页：2026-07-02 会话归档.md（全量 v2 架构落地 + 两篇文章入库）
## [2026-07-02] restructure | v2.1 全平铺架构落定
- 知识库/ 所有子目录拆平（概念/方法/分析/MOC 全部回归平铺，37 文件同一平面）
- 源/原文/ 子目录拆平（articles/okf/openrath 全部平铺，54 文件）
- Frontmatter 全面重写：36页 type: note + 3页 type: moc，删除主观类型标签
- 新 frontmatter 四层：Identity（title/created/updated/type）+ Source（source_url/author）+ Structure（domain/status/related）+ Content（tags/description）
- 全局标签索引：知识库/标签索引.md 已创建，112 个唯一标签，按受控词汇组织
- 所有 MOC wikilink 路径修复（概念/X→X，方法/X→X，分析/X→X，MOC/X→X）
- 硅基流动报告在 源/暂存/ 等待处理
## [2026-07-02] restructure | 全量 v2 架构落地
- 源/ 目录：原文（_raw迁入）+ 摘要（原始资料迁入）+ 暂存（硅基流动报告放入）
- 知识库/ 目录：概念/ 方法/ 分析/ MOC 四层 + index
- 工作台/ 目录：产出/ 模板/ 项目/ 复盘（自媒体文章迁入产出）
- 归档/ 目录：会话/ 日志/（会话归档迁入）
- 使用者画像.md 升至根目录（基础设施层）
- 硅基流动_横纵分析报告.md + .pdf → 源/暂存/
- 所有 MOC、协议文件、AGENTS.md、index.md 路径已更新
## [2026-07-02] infra | 会话归档移出知识库 + log 按月归档
- 8 个会话归档文件从 知识库/ → 会话归档/（平铺归档不再干扰概念页）
- 创建 会话归档/index.md（归档浏览入口）
- 创建 会话归档/2026-06-log.md（回填6月操作时间线）
- 更新引用：根 index.md、知识库/index.md、🏠 AI工程.md（替换为迁移提示语）
- 更新协议：wrapup-protocol + context-budget 写入路径改为 会话归档/
- AGENTS.md log 说明新增：每月末归档旧条目到 会话归档/YYYY-MM-log.md
- 知识库规模回归纯净：仅概念页 + MOC（44篇概念页 + 3篇域 MOC），无归档杂音
## [2026-07-02] infra | 情景记忆 + 衰老淘汰机制
- 创建 [[使用者画像]]（L3 用户画像层，domain: meta）
- 创建 [[模板-项目复盘]]（情景记忆模板，每项目一篇复盘）
- 创建 agents/check-protocol.md（详细 lint 协议，含衰老检测）
- 更新 AGENTS.md：lint 流程引用 check-protocol + 按需加载表新增
- 更新 🏠 元知识 MOC：新增"Context 层"章节
- 知识库规模：45篇（42概念页 + 3域 MOC）+ 34原始资料
- 概念来源：JiuwenMemory（AutoGenetic 记忆引擎）的情景记忆理念
## [2026-07-02] ingest | JiuwenMemory（华为开源 AutoGenetic 记忆引擎）
- 来源：机器之心《华为开源 Agent 记忆引擎 JiuwenMemory：让记忆从存下来变成长出来》
- 概念页：[[AutoGenetic记忆引擎]] 已创建
- 源摘要：原始资料/jiuwenmemory-autoGenetic记忆引擎.md 已创建
- raw 归档：_raw/articles/jiuwenmemory.html + jiuwenmemory.txt
- 关键发现：L0-L3分层记忆、AutoDreaming、MemoryTurbo、GraphMemory、Adapter解耦、Swarm群体记忆
## [2026-06-30] session | GitHub 认证 + Get笔记集成
- GitHub 认证完成（ruiyaoe-hash，scopes: repo, read:org, workflow）
- getnote skill 补齐：SKILL.md + api-reference.md + credentials.ps1
- 能力地图新增两大章节：GitHub 操作 / 得到大脑（Get笔记）操作
- API 测试通过（读写 + 中文 UTF-8 编码修复）
- @getnote/mcp v1.5.2 已全局安装










## 2026-07-17 | Phase 3 完成 + v1.0.1 发布

### 本次成果
- Phase 3: Event Bus（15 种事件类型）+ Memory Store L0-L4 五层 + Planner + Dependency Graph（81 节点 380 边）+ WikiAgent 全部落地
- v1.0: ingest 协议全链路实现（5 步）+ Memory L3-L4 + Executor v0.2（10 个 handler）+ Protocol 模板 + README 重写
- Review: ontology v0.2 / manager.py merge_conflict_handler / AGENTS.md 修正
- 仓库清理: 325 → 38 文件，纯运行时
- 文档: README + CHANGELOG + source/README
- 恢复: checkout main + merge 事故导致本地文件丢失，已通过 git worktree 恢复
- 定位: Agent Runtime（主）/ Agent OS（愿景）

### 当前状态
- main: v1.0.1 已发布，38 文件纯运行时
- develop: 继续开发
- v1.0.1 tag: 已推送
- [2026-07-17T14:16:44.089485+00:00] wrapup: 会话 2026-07-17-003（ended），任务 (无)（completed）
