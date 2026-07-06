# 大型项目并行执行策略

当需求文档超长或功能节点过多时，单个 agent 会遭遇上下文溢出、质量衰减和单线程瓶颈。本文档定义何时以及如何并行执行。

---

## 执行模式判定

根据功能树的规模自动选择：

| 功能节点数 | 页面数 | 执行模式 | 策略 |
|---|---|---|---|
| ≤ 5 | 1-2 | **串行模式** | 一个 agent 串行执行所有阶段 |
| 6-15 | 3-5 | **轻量并行** | 架构阶段串行；原型+代码+测试按页面用 Agent 并行 |
| 16-40 | 6-15 | **标准并行** | 架构阶段串行；使用 Workflow 编排并发 agent，每页面一个 |
| 40+ | 15+ | **分批并行** | 按 P0/P1/P2 优先级分批，每批一个 Workflow；P0 先交付 |

---

## 必须串行的阶段

功能树和架构推导（阶段 1-2）是全局决策——路由命名、组件拆分、数据实体定义互相耦合。**这两个阶段始终由一个 agent 串行处理。**

如果需求文档过长（>20 页），拆分策略是按文档章节拆分，而非按功能拆分：
- 将文档分成 2-3 份，每份用一个 agent 提取功能树片段
- 汇总 agent 读取所有片段 → 去重 → 检查冲突 → 生成完整功能树

---

## 可并行的阶段

架构确定后，阶段 3-7（原型、API、代码、测试）按页面/路由并行，因为各页面正交：

```
specs/features.json + specs/routes.json + specs/layout-reference.json
      │
      ├── Agent A: /orders 页面（原型 + 组件代码 + 测试）
      │
      ├── Agent B: /orders/:id 页面（原型 + 组件代码 + 测试）
      │
      ├── Agent C: /users 页面（原型 + 组件代码 + 测试）
      │
      ├── Agent D: /dashboard 页面（原型 + 组件代码 + 测试）
      │
      └── Agent E: 共享组件 + API 层 + Mock 数据 + 路由配置（全局基础设施）
```

---

## 每个 Agent 的输入包

每个并行 agent 收到的上下文只包含它处理的页面和共享基础设施：

```json
{
  "pageContext": {
    "page": "/orders",
    "features": ["仅本页面的功能节点"],
    "routes": ["仅本页面的路由定义"],
    "components": {
      "shared": ["本页面用到的共享组件"],
      "pageComponents": ["本页面的专属组件"]
    },
    "layoutReference": { "本页面的布局参考" },
    "dataDependencies": ["本页面用到的 API 依赖"]
  },
  "globalContext": {
    "designTokens": { "全局设计 tokens" },
    "techStack": { "技术栈信息" },
    "apiBasePath": "/api",
    "pathAlias": "@/",
    "componentLibrary": "shadcn/ui"
  }
}
```

**关键原则：每个 agent 只拿到它要处理的页面和共享基础设施的上下文，不包含其他页面信息。**

---

## 并行后的汇总与一致性检查

所有并行 agent 完成后，汇总 agent 检查：

1. **路由冲突** — 所有 agent 生成的路由配置是否一致
2. **组件重复** — 两个 agent 是否各写了一个功能相同的组件（应合并到 shared）
3. **API 类型冲突** — 两个 agent 对同一接口定义了不同类型（应统一到 `src/api/types.ts`）
4. **样式一致性** — 设计 tokens 使用是否正确
5. **跨页面导航** — 页面间的链接是否正确指向

---

## 迭代模式下的并行

迭代模式天然支持小范围并行：
- 一次迭代只改一个页面 → 串行即可
- 一次迭代同时加 3 个新页面 → 3 个 agent 并行
- 一次迭代修改共享组件（被 5 个页面使用）→ 先更新共享组件，再检查受影响页面

---

## 用户可见性要求

不能让并行 agent 在后台静默运行。每次并行时必须：

### 1. 发起并行前播报计划

```
现在开始并行生成 4 个页面的原型：
  - Agent A: /orders（订单列表页）
  - Agent B: /orders/:id（订单详情页）
  - Agent C: /users（用户管理页）
  - Agent D: /dashboard（数据仪表盘）

每个 Agent 完成后会推送通知。你随时可以输入 /workflows 查看实时进度。
```

### 2. 使用 Workflow 工具时
- 用 `phase()` 为每个阶段创建命名分组
- 用 `label` 给每个 agent 取描述性名称（如 `'/orders 订单列表'` 而非 `'agent-1'`）
- 在关键里程碑用 `log()` 输出进度
- 在 meta.phases 中声明阶段

### 3. 使用 Agent 工具时（无 Workflow 场景）
- 给每个 agent 取描述性名称
- 完成后主动报告各 agent 的产出摘要

### 4. 并行完成后的汇总报告

```
所有 4 个页面原型已生成完毕：
  ✓ /orders — orders.html（5 状态，3 交互流程）
  ✓ /orders/:id — orders-detail.html（4 状态）
  ✓ /users — users.html（5 状态，含批量操作）
  ✓ /dashboard — dashboard.html（3 统计卡片 + 2 图表）
汇总检查：路由一致 ✓ | 无组件重复 ✓ | 导航链接正确 ✓
```

### 可用机制

| 机制 | 作用 | 使用方式 |
|---|---|---|
| **进度树** | Workflow 终端实时进度树，每行一个 phase/agent | `phase()` + `label` |
| **`/workflows` 命令** | 用户查看所有活跃 workflow 进度 | 告知用户可用 |
| **Agent 完成通知** | 背景 agent 完成时自动推送 | 默认行为 |
| **`log()` 函数** | 进度消息显示在进度树上方 | `log('3/4 pages done...')` |
| **主 agent 播报** | 分派前告知并行内容和规模 | 发起前文字说明 |
