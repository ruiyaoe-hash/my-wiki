# Contributing / 贡献指南

欢迎贡献。本项目约束很少，但以下几条是硬性的。
Contributions welcome. Few rules, but these are hard requirements.

## 运行测试 / Run Tests

```bash
python -m unittest discover tests
```

提交前必须全绿。新增能力必须带测试。
All green before submitting. New capabilities need tests.

## 零依赖 / Zero Dependencies

运行时代码只允许 Python 标准库。新依赖需要一个非常有说服力的理由。
Runtime code is stdlib-only. New dependencies need a very good reason.

## 自定义协议 / Custom Protocols

1. 复制 `protocol/TEMPLATE.json` 为 `protocol/my-protocol.json`
2. 定义 steps（action + params），action 必须对应 `executor/executor.py` 里的 `_handle_<action>` 方法
3. 缺失 handler 会 fail-fast（协议直接失败），不会静默跳过
4. 文件一律 UTF-8 编码

## 分支纪律 / Branch Discipline

- `develop` — 施工线 / where work happens
- `main` — 成品线 / only merges that pass acceptance, tagged releases

验收通过才合 main，合并即打 tag。
Merge to main only after acceptance passes; every merge gets a tag.
