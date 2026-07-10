# 吃进去 (Ingest) 协议

## 七步流程


1. 存到 源/原文/ — 原始内容归档
1.5 指定知识域 — 确认 domain 值（ai-engineering / meta / 其他），写入 frontmatter
2. 提取概念和实体 — 写入 知识库/，一个文件一个概念
3. 写源摘要 — 写入 源/摘要/，带 source 类型 frontmatter
4. 更新根 index.md — 新增页面加入全局索引
5. 在 log.md 顶部追加操作记录 — 格式 ## [日期] ingest | 摘要
6. 刷新 hot.md — 更新当前状态、本次成果、下次约定

## 写入规范

- 知识页 frontmatter: type, title, description, created, updated, tags, status, related
- 源摘要 frontmatter: type, title, description, timestamp, created, tags, status, related
- 知识页用 wikilink 关联相关页面
- 一文一概念，避免大杂烩


## 铁律（2026-07-08 新增）

1. **每次编辑知识页必须同步更新 frontmatter 的 `updated` 字段为当前日期**。不允许 created == updated 在非首次创建后仍保持相同。
2. **所有入库文件必须有 `source` 字段（URL）和 `source_label` 字段（一句话说明该链接是什么内容）**。方便后期检索和溯源。
3. **知识页必须回链到源材料**——在页面底部用 `> 原文/来源：` 格式标注，引用源/原文/ 或源/摘要/ 中的对应文件。
