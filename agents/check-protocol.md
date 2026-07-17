
# 检查 (Lint) 协议

> 用户说"检查" / "lint" 时加载。先读 AGENTS.md 中的三段式流程，再按本协议的详细步骤执行。

## 检查项（按优先级）

### 1. 断链检查
- 扫描所有 wiki 页面中的 `[[wikilink]]`，确认目标文件存在
- 报告断链及其所在文件/行

### 2. 孤儿页检查
- 扫描 `知识库/*.md`，找出未被任何 MOC 页链接的孤立文件（排除模板页）
- 报告孤儿页清单

### 3. 衰老内容检查（New）
- 扫描 `知识库/*.md` 的 frontmatter `updated` 字段
- 条件：距上次更新超过 **90 天** 且 `status` 不是 `archived`
- 条件：距上次更新超过 **60 天** 且 `status: developing`
- 报告潜在衰老页，询问是否标记为 `status: stale`

### 4. 矛盾检测
- 跨页面扫描同 tag/concept 是否存在明显冲突描述
- 当前需手动判断，无自动检测手段

## 修复流程

1. 报告所有问题后，逐项询问"是否修复"
2. 获确认后修复断链、标记 stale、链接孤儿页到对应 MOC
3. 在 log.md 顶部追加检查记录

## 状态生命周期

```
draft → developing → growing → (90天无更新) → stale → archived
                                           ↓
                                    review → growing
```

- `draft` — 新创建未完成
- `developing` — 活跃编辑中
- `growing` — 已稳定但可更新
- `stale` — 可能过时，需审核
- `archived` — 确认过时，保留为历史参考

## 修复日志格式

```
## [日期] lint | [修复项]
- 修复断链：... → ...
- 标记 stale：...（上次更新：...）
- 链接孤儿页：... → [[MOC 页面]]
```

> 本协议由 2026-07-02 根据 JiuwenMemory 冲突消解与衰老淘汰理念创建。


### 5. Frontmatter 一致性检查（New，2026-07-08）
- 扫描 `知识库/*.md` 的 frontmatter `created` 和 `updated` 字段
- 条件：`created` == `updated` 且文件内容在创建后有实质编辑
- 报告 frontmatter 未更新的页面清单
- 条件：缺少 `source` 或 `source_label` 字段的页面
- 报告缺少来源标注的页面清单
