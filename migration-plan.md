# 目录迁移计划

## 当前状态（Phase 1）

新旧两套结构并存。旧结构是 Obsidian 时代的遗产，新结构是 Agent Runtime 的骨架。
两者目前共存，但职责明确区分。

## 旧 → 新 映射表

| 旧目录 | 当前用途 | 新位置 | 迁移时间 | 说明 |
|--------|---------|--------|---------|------|
| `知识库/` | 80 篇知识页，Obsidian 主工作区 | `knowledge/` | Phase 2 | 知识引擎上线后迁移。在此之前 Obsidian 仍从这里读写。 |
| `源/原文/` | 54 篇原始材料 | `source/originals/` | Phase 2 | 与 Knowledge Store 同步迁移 |
| `源/摘要/` | 51 篇 AI 摘要 | `source/summaries/` | Phase 2 | 同上 |
| `agents/` | 7 个协议文件 | `protocol/` | Phase 2 | 当 Protocol 从 Markdown 升级为 YAML/JSON 时迁移 |
| `归档/` | 历史会话和日志 | `archive/` | Phase 3 | Planner 上线后重新组织归档结构 |
| `工作台/` | 自媒体文章和模板 | 暂不迁移 | — | 这是你的个人工作空间，不是 Runtime 的一部分 |

## 迁移原则

1. **不删旧文件。** 迁移 = 复制到新位置 + 在原位置加 `_MIGRATED.md` 标记。旧文件保留至少一个 Phase 周期。
2. **不跨 Phase 迁移。** 每个 Phase 只迁它负责的那一层。Phase 2 只迁 Knowledge 和 Source。Phase 3 才迁 Protocol 和 Archive。
3. **Obsidian 兼容性优先。** 只要你还用 Obsidian 阅读知识页，`知识库/` 目录就不改名。
4. **旧结构最终进入 `legacy/`。** 全部迁移完成后，旧目录移入 `legacy/` 作为历史快照。

## 迁移检查清单

- [ ] Phase 2：知识库/ → knowledge/
- [ ] Phase 2：源/ → source/
- [ ] Phase 3：agents/ → protocol/（含格式升级）
- [ ] Phase 3：归档/ → archive/（含结构重组）
- [ ] Phase 5：工作台/ → 决定保留或移出仓库
- [ ] Phase 6：清理旧目录，移入 legacy/，打 tag 归档
