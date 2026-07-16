# Runtime Object 识别规则

## 一条规则

> 如果 Runtime 需要在某个时刻，用这个实体的标识符找到它、查询它的当前状态、并对它执行一个操作——那它就是一等对象。

三个要素缺一不可：

| 要素 | 含义 | 不满足的例子 |
|------|------|------------|
| 寻址 | 能用 ID 找到它 | "Domain"——没法寻址一个具体的域 |
| 状态查询 | Runtime 需要知道它的状态才能做决策 | "Index"——纯指针列表 |
| 执行操作 | 不只是读，还有写/改/删 | "标签"——只能间接查询 |

## 判定示例

### 通过：Task

Runtime 能通过 task-id 找到它、查询 status、执行 start/pause/complete。三个要素全部满足。

### 不通过：Domain

"Agent 记忆与认知"这个域是 Knowledge 对象的一个标签属性，不是独立实体。

### 边缘：Capability

"Research"有名字，但 Runtime 不查询它的状态做决策。它挂在 Protocol 和 Workflow 上作为索引，不是独立对象。
