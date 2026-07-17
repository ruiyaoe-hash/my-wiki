# 工具能力地图

> 按"我要做什么"反向索引到最优工具链。执行任务前必查，禁止 which/--help 摸索。
> 每次踩坑后补充一行。选择标准：质量优先、效率次之，不追求最快但追求最可靠。

---

## 信息获取

### 微信公众号文章 → 分层策略（先判断文章类型）

**第一优先：标准文章（rich_media_content 直接可见）**
→ Python requests + Chrome UA + regex 提取 `rich_media_content` 内的 p/span/section 文本
- 适用：大多数普通公众号文章

**第二优先：新版模板（content_noencode 十六进制编码）**
→ Python requests + 提取 `content_noencode` 字段 + `\xNN` 解码 + HTML 标签清理
- 标志：`js_content` 标签带 `visibility: hidden` 且 `content_noencode` 字段存在

**第三优先：纯 JS 动态加载（appmsg 为空）**
→ 当前不可行。备选：手动词条到跨平台版本或搜索引擎缓存

**禁用手法：** curl.exe（遇验证墙返回空）、in-app browser 直接 goto（30s+ 超时）

### 微信公众号 OCR 图片识别（文字不足时触发）
→ 提取所有 `<img>` CDN URL → curl.exe 下载 → view_image 读图描述
→ 触发条件：纯文本提取 < 200 汉字

### GitHub 仓库 README → raw.githubusercontent.com
→ `curl.exe -sL "https://raw.githubusercontent.com/OWNER/REPO/main/README.md"`

### 仓库 README URL 失效处理
→ raw.githubusercontent.com 返回 404 时，仓库可能已改名/归档/迁移 → 先用 DuckDuckGo 搜索 "REPO_NAME github" 确认当前仓库地址
- 不盲目尝试多个 URL 变体
### GitHub 仓库搜索 → GitHub API /search
→ Python urllib.request 调 `/search/repositories?q=...`，未认证限流 60 次/小时

### arXiv 论文搜索 → arXiv API（XML，免费）
→ Python urllib.request 调 `export.arxiv.org/api/query?search_query=...`，30s timeout

### 日常网络搜索 → GitHub API（首选，已认证）+ Hacker News API（社区讨论）
→ **首选**：`gh search repos "QUERY" --limit 10`（已认证，限流 5000 次/小时）
→ **备选**：`gh api /search/repositories?q=QUERY`（更灵活的参数控制）
→ **社区趋势**：`curl -sL "https://hacker-news.firebaseio.com/v0/topstories.json"`（无认证，无限流）
→ **学术论文**：arXiv API（需间隔 >= 20 秒单请求，否则 429）或 OpenAlex API（对 CS/AI 领域覆盖率低）

### DuckDuckGo 端点 → 已失效（2026-07-08 确认）
→ `html.duckduckgo.com`、`lite.duckduckgo.com`、`duckduckgo.com` 三个端点全部返回 HTTP 000
→ 原因：中国大陆网络层面阻断（GFW）
→ **不要再用 DDG**，直接走 GitHub API

### JS 渲染的国外知识站点 → 当前不可行，降级策略
→ Python requests 返回空 body 时判定为 JS 渲染站点 → 改用 DuckDuckGo HTML 搜索 site:domain → 或 Google 缓存 → 或找替代文档源（GitHub README 等）
- 标志：主内容区 `<main>` 为空或仅含 `<script>` / skeleton loader
- 已知 JS 渲染站点：cn.bing.com, bing.com, linkingyourthinking.com, notes.andymatuschak.org
### 国外主流博客 / Substack / Medium → Python requests + Chrome UA

### 播客 RSS → curl.exe -sL RSS_URL

### X (Twitter) → Nitter 公共实例
→ `curl.exe -sL "https://nitter.net/USERNAME"`

### Reddit → Reddit JSON API（免费）
→ `curl.exe -sL "..." -H "User-Agent: Mozilla/5.0"`

### YouTube → yt-dlp 字幕提取
→ `yt-dlp --write-auto-subs --sub-lang zh-Hans,en --convert-subs srt --skip-download URL`

### 论文全文 → arXiv PDF / Semantic Scholar / Sci-Hub（按序）

### 小红书 / 抖音 → 当前不可行
 
 ### 飞书公开 Wiki / 知识库 → lark-cli docs +fetch
 → 识别 URL 中的 wiki token（`https://*.feishu.cn/wiki/<TOKEN>`），直接：
   `lark-cli docs +fetch --doc <TOKEN> --api-version v2 --format pretty`
 → 不需要关心是哪个空间（space 无关），token 全局有效
 → 公开知识库（如通往AGI之路）走 bot identity 即可；私有文档需切换 user identity
 → 配图需额外调用图片接口，正文纯文本可一步拿到
 → 错误路径：HTTP 请求（一律重定向到飞书登录页）、搜索引擎（不索引飞书 wiki 正文）

---

## 代码执行

### 复杂 Python 脚本 → 写 .py 文件再运行
→ 禁止嵌套超过 2 层的引号转义
→ 模式：`@'...'@ | Set-Content file.py -Encoding UTF8; python file.py`

### PowerShell -Encoding UTF8
→ 读非 ASCII 文本文件时必须指定

### pip 安装 → `python -m pip` 代替 `pip`
→ PowerShell 中 pip 路径有问题

---

## 文件操作

### 编辑文件 → apply_patch
→ 不用 cat 或 shell write 技巧创建/编辑文件

### 搜索文本 → rg（首选）
→ `rg "pattern"` 或 `rg --files`

### 搜索文件 → Get-ChildItem -Recurse -Filter

---

## Wiki 内部操作

### 提问 → 先 hot.md → 再 index.md → 再深入知识页
### 吃进去 → 六步流程：存 raw → 提取概念 → 写源摘要 → 更新 index → 更新 log → 刷新 hot
### 收尾 → 五步流程：归档页 → 刷新 hot → 更新 log → 更新 index → 更新子目录 index
### 检查 → 找断链、孤儿页、过时内容、矛盾

### 工具降级路径（通用）
当首选工具不可用时，按优先级降级：
状态工具（浏览器/Playwright） → 无状态工具（Python requests） → 搜索引擎缓存（DuckDuckGo HTML）
每次降级在注释中标注原因

---

## GitHub 操作（gh CLI + GitHub App，已认证）

### 通用原则
- `gh` CLI 已认证（账号：ruiyaoe-hash），优先用 `gh` 代替 curl/requests
- GitHub MCP 工具也可用（`mcp__codex_apps__github___*`），但 `gh` CLI 更灵活稳定
- 认证权限：repo（私有仓库读写）、read:org（组织读取）、workflow（CI/部署）

### 读取仓库内容 → gh API 调用
→ `gh api repos/OWNER/REPO/contents/PATH --jq '表达式'`
→ 大文件用 `gh api ... --jq '.content' | base64 -d`
→ 对比：`gh api repos/OWNER/REPO/compare/BASE...HEAD --jq '.files[] | "\(.filename) \(.status)"'`

### 查看仓库元数据 → gh repo view
→ `gh repo view OWNER/REPO --json name,description,url,stargazerCount,forkCount`
→ 分支机构：`gh api repos/OWNER/REPO/branches`
→ 最后更新：`gh api repos/OWNER/REPO --jq .pushed_at`

### 搜索仓库/代码/issue → gh search
→ `gh search repos "QUERY" --limit 10`
→ `gh search code "QUERY" --repo OWNER/REPO`
→ `gh search issues "QUERY" --repo OWNER/REPO --state open`

### 查看/管理 PR → gh pr
→ `gh pr list -R OWNER/REPO --state open`
→ `gh pr view PR_NUMBER -R OWNER/REPO --json title,body,additions,deletions,files`
→ `gh pr checkout PR_NUMBER`（需要 git clone 场景）
→ `gh pr review PR_NUMBER -R OWNER/REPO --approve`（代码审查）

### 查看/管理 Issues → gh issue
→ `gh issue list -R OWNER/REPO --state open --json title,labels,assignees`
→ `gh issue view ISSUE_NUMBER -R OWNER/REPO`
→ `gh issue create -R OWNER/REPO --title "..." --body "..."`

### 检查 CI/Actions → gh run
→ `gh run list -R OWNER/REPO --branch main --limit 5`
→ `gh run view RUN_ID -R OWNER/REPO --log`（查看失败日志）

### 发布代码 → yeet skill
→ 三步流程：确认 scope → 提交 commit → 推分支 + 开 draft PR
→ 仅当用户明确要求推送时使用

### Github MCP 技能入口
→ 地址 review 反馈：`gh-address-comments` 技能
→ 修复 CI：`gh-fix-ci` 技能
→ 通用导航：`github` 技能

---

## 得到大脑（Get笔记）操作（Open API，需加载凭证）

### 通用原则
- Base URL：`https://openapi.biji.com/open/api/v1`
- 认证：`Authorization: Bearer <API Key>` + `X-Client-ID: <Client ID>`
- 凭证文件：`~/.codex/skills/getnote/references/credentials.ps1`
- 调用前必须先 `.`（dot-source）凭证文件
- PowerShell UTF-8 坑：必须用 `[System.Text.Encoding]::UTF8.GetBytes()` + `charset=utf-8`
- note_id 是 Snowflake ID，必须当字符串处理
- 配额：读取 20000/天，写入 2000/天，笔记写入 100/天
- 完整 API 参考见 `~/.codex/skills/getnote/references/api-reference.md`

### 保存笔记 → POST /resource/note/save
→ 用户说"帮我记一下"、"保存到笔记"、"记录下来"
→ 支持三种类型：plain_text（默认）、link（需 link_url）、img_text（需 image_urls）
→ 分享链接（biji.com/note/share_note/*、d.biji.com/*）同步返回 id
→ 普通链接异步，保存后返回 tasks[]，需 POST /resource/note/task/progress 轮询
→ 笔记正文支持 Markdown 格式和内链（https://biji.com/note/{note_id}）

### 查看笔记 → GET /resource/note/list 或 /detail
→ 列表：GET /resource/note/list（游标翻页，cursor 字段传入下一次请求）
→ 详情：GET /resource/note/detail?id={note_id}（含标签、附件、音频转写、网页原文）
→ 不同类型笔记的原文位置不同：
  - plain_text：`note.content`
  - link：原文 = `note.web_page.content`，AI 总结 = `note.content`
  - audio：转写原文 = `note.audio.original`，AI 总结 = `note.content`

### 更新笔记 → POST /resource/note/update
→ 仅支持 plain_text 类型
→ 需要 note_id（必填）、title/content/tags（至少一个）
→ tags 是替换操作，会覆盖原有标签

### 删除笔记 → POST /resource/note/delete
→ 移入回收站，非永久删除

### 语义搜索 → POST /resource/recall
→ 用户说"搜一下XX"、"找找提到XX的笔记"
→ 参数：query（搜索词）、top_k（默认 3，最大 10）
→ 也支持知识库内搜索：POST /resource/recall/knowledge（需 topic_id）

### 标签管理 → POST /resource/note/tags/add 或 /tags/delete
→ 添加：{ note_id, tags[] }
→ 删除：{ note_id, tag_id }
→ 每个标签最多 10 字，最多 5 个标签，系统标签不可删除

### 知识库管理 → /resource/knowledge/*
→ 列表：GET /knowledge/list
→ 创建：POST /knowledge/create（每天最多 50 个）
→ 笔记列表：GET /knowledge/notes
→ 批量添加/移除：POST /knowledge/note/batch-add 或 /remove
→ 订阅：子模块 /subscribe/list（他人公开的）

### 图片上传 → 三步流程
→ 1. GET /resource/image/upload_token → 获取 OSS 凭证
→ 2. multipart/form-data POST 到 OSS（凭证中的 host）
→ 3. 用返回的 access_url 调用 save_note（note_type=img_text）
→ 简化：也可以直接用 upload_image 工具（需 @getnote/mcp 运行中）

### 博主/直播 → 读取已订阅内容
→ 列表：GET /knowledge/bloggers（需 topic_id）
→ 博主内容摘要：GET /knowledge/blogger/contents
→ 博主内容详情：GET /knowledge/blogger/content/detail（含原文）
→ 直播列表：GET /knowledge/lives
→ 直播详情：GET /knowledge/live/detail（含 AI 摘要 + 转写原文）

### 分享/配额
→ 分享笔记：POST /resource/note/sharing（幂等，返回 share_url）
→ 查配额：GET /resource/rate-limit/quota（三类：read/write/write_note）

