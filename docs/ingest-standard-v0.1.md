# 入库标准 v0.1 — 知识可信度分级与标注制度

> 状态：已确认方向（2026-07-19，库主拍板），随 digest 双周验证 dogfood
> 依据：四轮外部调研（见文末"参考依据"）
> 解决的问题：研究深入后，人类（非专家）失去内容判断力，库内信息鱼龙混杂，
> 需要一套不依赖专业知识的入库标准与好坏对错标注筛选机制。

## 核心原则

1. **判断外包给流程，不外包给人脑**：入库内容的可信度不由人裁决，
   由来源属性、交叉印证、学术基础设施三个可机器执行的信号决定。
2. **默认未核实，标注是挣来的**：每页入库即 `verification: unverified`，
   升级需要证据。允许"我不知道"存在，禁止"假装已核实"。
3. **错得明明白白**：系统不保证永不出错，保证每页的对错状态明示、
   可质疑、可追溯、可复查。被证伪的页面不删除，标记保留。
4. **人是流程审计员，不是内容裁判**：库主看控制台里的核实状态比例
   （已核实/未核实/有争议/三级来源占比），不看单篇内容对错。

## 零件一：来源分级（source_tier，入库时自动打标）

| 等级 | 含义 | 判定规则（域名启发式 v0.1） |
|------|------|------------------------------|
| T1 | 一手学术/官方来源 | arxiv.org、doi.org、*.edu、nature.com、science.org、pubmed/ncbi、acm.org、ieee.org、springer.com、官方文档站 |
| T2 | 权威机构/一手工程来源 | github.com、大厂工程博客、政府/标准组织站点、公司官方发布 |
| T3 | 自媒体/二手转述 | mp.weixin.qq.com、zhihu.com、medium.com、csdn.net、juejin.cn、头条/搜狐等 |
| T4 | 来源不明或本地材料 | 本地文件、无 URL、无法归类 |

规则是启发式，可随验证积累修正（改 `executor/executor.py` 的
`_classify_source_tier`）。判级只看来源属性，不需要懂内容。

## 零件二：认知状态元数据（每页 frontmatter 声明）

```yaml
source_tier: T3            # 来源等级（入库自动打）
verification: unverified   # unverified / verified / contested / falsified
verified_at: null          # 最近一次核实日期（unverified 时为空）
confidence: low            # high / medium / low，AI 或人评估后填，默认 low
```

sidecar（knowledge/*.json）同步携带这四个字段；md frontmatter 仍是唯一事实源。

## 零件三：核实升级路径（verification ladder）

- unverified → verified：满足任一条件
  1. 两个以上相互独立的来源交叉印证同一断言（SIFT 横向阅读思想）
  2. 来源为 T1 且未在撤稿/证伪数据库中（论文类可查 Crossref / Retraction Watch）
  升级必须同时写 `verified_at`（知识会过期，带时间戳才可复查）
- verified → contested：出现权威反对证据（如后续文献 contrast，scite 式信号）
- any → falsified：被撤稿、被学界证伪、被业界实践证伪。
  **不删除**，保留页面并标记，证伪记录本身也是知识
- 机器分类（LLM 判断、scite 分类）只能作为线索，不能单独作为升级依据
  （scite 准确性研究证明机器分类不可单独依赖）

## 零件四：定期复查（证据保鲜，check 协议扩展方向，v0.2 落地）

- `verified` 但 `verified_at` 超过 180 天 → 降级 unverified 并提示复查
- `source_tier: T3` 且 90 天未被任何后续研究引用/印证 → 标记复查
- 领域内出现新综述推翻旧结论 → 人工或 AI 标注 contested/falsified
- 控制台健康总览展示：各 verification 状态页数、各 source_tier 占比

## 与 digest 双周验证的关系

双周验证期间（2026-07-19 起两周），每篇 ingest 的文章自动带来源分级与
核实状态入库。两周后看三样东西：各等级占比、升级流程是否跑得动、
标注是否对研究有用。数据说话后再决定 v0.2（证据保鲜）与 v1.0（冻结进
领域研究规范）的走向。

## 参考依据

- CRAAP 检测法（大学图书馆标配）与 SIFT 横向阅读法（实证优于逐页清单）
- Epistemic status 标注约定（LessWrong / EA Forum 社区十余年实践）
- scite Smart Citations（支持/反对/提及的引用意图分类）及其准确性研究
- Retraction Watch 数据库（6.5 万+撤稿，已接入 Crossref/WoS/Zotero）
- A-MAC 记忆准入政策（效用×置信度×新颖度×时效，2026）
- ARA: Agent-Native Research Artifact（研究工作件文件系统协议，2026）
