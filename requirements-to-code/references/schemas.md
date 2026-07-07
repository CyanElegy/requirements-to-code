# Schema 定义

本文档包含 requirements-to-code 工作流中所有数据结构的 JSON Schema 定义。SKILL.md 各阶段会引用此文件的具体 schema。

---

## 目录

1. [功能树节点 (Feature Node)](#功能树节点-feature-node)
2. [迭代 Delta 格式](#迭代-delta-格式)
3. [路由定义 (Routes)](#路由定义-routes)
4. [组件定义 (Components)](#组件定义-components)
5. [布局参考 (Layout Reference)](#布局参考-layout-reference)

---

## 功能树节点 (Feature Node)

`specs/features.json` 的顶层结构为 `{ "features": [FeatureNode, ...] }`。每个节点定义如下：

```json
{
  "id": "kebab-case-unique-id",
  "title": "人类可读的功能名称",
  "actor": "谁执行此操作",
  "page": "/路由模式",
  "priority": "P0 | P1 | P2 | P3",
  "description": "一句话描述用户能完成什么",
  "acceptanceCriteria": [
    "假设 [前置条件]，当 [操作]，则 [预期结果]"
  ],
  "states": ["loading", "empty", "error", "normal", "边界情况"],
  "dataDependencies": [
    {
      "entity": "Order",
      "fields": ["id: string", "status: OrderStatus", "total: number", "createdAt: string"],
      "source": "GET /api/orders",
      "params": { "status": "string?", "page": "number?", "pageSize": "number?" },
      "inferred": false
    }
  ],
  "interactions": [
    {
      "trigger": "点击订单行的'查看详情'",
      "effect": "导航到 /orders/:id",
      "validation": []
    }
  ],
  "subFeatures": ["order-detail-view", "order-filter", "order-pagination"],
  "version": 1
}
```

### 字段规则

| 字段 | 规则 |
|---|---|
| `id` | 唯一 kebab-case，全局不重复 |
| `priority` | P0=核心流程 / P1=重要不阻塞 / P2=增强体验 / P3=锦上添花 |
| `acceptanceCriteria` | 每条"假设/当/则"格式，每个功能不超过 5 条 |
| `states` | 列表页至少含 loading/empty/error/normal；表单页至少含 idle/validating/submitting/success/error |
| `dataDependencies[].inferred` | 非需求文档明确声明的字段设为 `true` |
| `subFeatures` | 引用其他功能节点的 `id` |
| `version` | 每次修改递增 |

---

## 迭代 Delta 格式

迭代模式下，变更以 delta 文件存储在 `specs/iterations/NNN-slug/features-delta.json`：

```json
{
  "iteration": "003-add-batch-operations",
  "basedOn": "features.json at iteration 002-add-user-profile",
  "date": "2026-07-15",
  "changes": {
    "added": [
      { /* 完整的新功能节点 */ }
    ],
    "modified": [
      {
        "id": "order-list-view",
        "changes": {
          "states": ["原 states + 新增: batch-selecting"],
          "interactions": ["原交互 + 新增交互"],
          "version": 2
        }
      }
    ],
    "removed": [
      { "id": "legacy-export", "reason": "功能已整合到 order-export-v2" }
    ]
  },
  "unaffected": ["order-detail-view", "order-pagination", "..."]
}
```

### Delta 字段说明

| 字段 | 说明 |
|---|---|
| `basedOn` | 此 delta 基于哪个版本生成，用于溯源 |
| `changes.added` | 完整的新功能节点（含所有必填字段） |
| `changes.modified[].changes` | 只包含变更字段，未提及字段保持不变 |
| `changes.removed[].reason` | 必须说明移除原因 |
| `unaffected` | 明确标记未受影响的功能节点 ID，用于合并校验 |

---

## 路由定义 (Routes)

`specs/routes.json`：

```json
{
  "routes": [
    {
      "path": "/orders",
      "title": "订单列表",
      "authRequired": true,
      "roles": ["admin", "operator"],
      "layout": "authenticated",
      "features": ["order-list-view", "order-filter", "order-pagination"],
      "params": {},
      "queryParams": ["status", "page", "sort"],
      "meta": { "breadcrumb": "订单管理", "icon": "shopping-cart" }
    },
    {
      "path": "/orders/:id",
      "title": "订单详情",
      "authRequired": true,
      "layout": "authenticated",
      "features": ["order-detail-view", "order-status-update"],
      "params": { "id": "string" },
      "queryParams": [],
      "meta": { "breadcrumb": "订单 #:id", "parent": "/orders" }
    }
  ],
  "layouts": {
    "authenticated": { "header": true, "sidebar": true, "footer": false },
    "public": { "header": true, "sidebar": false, "footer": true }
  }
}
```

### 路由字段规则

- 多个功能节点共享同一页面时合并到一个路由（通过 `features` 数组关联）
- 动态参数在 `params` 中声明类型
- `layout` 引用 `layouts` 中的 key
- `meta.parent` 用于面包屑导航

---

## 组件定义 (Components)

`specs/components.json`：

```json
{
  "shared": [
    {
      "name": "OrderTable",
      "category": "data-display",
      "props": [
        "orders: Order[]",
        "onRowClick: (id: string) => void",
        "onSort: (field: string, order: 'asc' | 'desc') => void",
        "loading: boolean",
        "emptyText: string"
      ],
      "states": ["loading", "empty", "normal"],
      "usedBy": ["order-list-view"],
      "sharedAcross": ["/orders"]
    }
  ],
  "pageComponents": [
    {
      "name": "OrderFilterPanel",
      "page": "/orders",
      "props": [
        "filters: FilterState",
        "onChange: (filters: FilterState) => void",
        "onReset: () => void"
      ],
      "states": ["collapsed", "expanded"]
    }
  ]
}
```

### 组件分类规则

| 分类 | 判定条件 |
|---|---|
| `shared` | 被 2+ 页面使用的组件 |
| `pageComponents` | 仅在一个页面使用的组件 |

每个组件必须列出：
- 完整的 props 签名
- 所有可能的状态
- 使用方（`usedBy` 或 `page`）

---

## 布局参考 (Layout Reference)

`specs/layout-reference.json`：

```json
{
  "sources": [
    { "page": "/orders", "sourceType": "screenshot", "path": "~/Desktop/legacy-orders.png" },
    { "page": "/orders/:id", "sourceType": "screenshot", "path": "~/Desktop/legacy-order-detail.png" },
    { "page": "/dashboard", "sourceType": "auto-derived", "rationale": "数据概览页，采用顶部统计卡片+双列图表网格" }
  ],
  "layouts": {
    "/orders": {
      "layout": "header + content-only",
      "zones": [
        { "name": "page-header", "position": "top", "contents": ["title", "primary-actions"] },
        { "name": "filter-bar", "position": "below-header", "layout": "horizontal-collapsible",
          "alwaysVisible": ["search-input", "status-select"],
          "collapsedByDefault": ["date-range", "advanced-filters"] },
        { "name": "batch-toolbar", "position": "above-table", "trigger": "checkbox-selection" },
        { "name": "data-table", "position": "main-content",
          "features": ["sortable-columns", "fixed-left-checkbox", "row-hover-highlight"] },
        { "name": "pagination", "position": "below-table-right", "features": ["total-count", "page-size-changer"] }
      ],
      "interactionPatterns": [
        { "trigger": "click-row", "action": "navigate", "target": "/orders/:id" },
        { "trigger": "hover-row", "action": "highlight-row" },
        { "trigger": "checkbox-select", "action": "show-batch-toolbar" }
      ],
      "density": "comfortable",
      "responsiveStrategy": {
        "mobile": "hide-batch-toolbar, collapse-filter-to-drawer, table-to-card-list",
        "tablet": "keep-table, collapse-side-filters"
      }
    }
  },
  "designTokens": {
    "overallStyle": "企业后台管理系统",
    "tableDensity": "compact",
    "formLayout": "right-aligned-labels, single-column",
    "modalUsage": "简单操作（确认删除），复杂页面使用全屏抽屉"
  }
}
```

### 布局字段说明

| 字段 | 用途 |
|---|---|
| `sources` | 记录每个页面的布局参考来源，可溯源 |
| `layouts.<page>.zones` | 页面的区块划分，每个 zone 对应原型中的一个 DOM 区块 |
| `layouts.<page>.interactionPatterns` | 交互触发→行为的映射，决定原型和代码的事件处理 |
| `layouts.<page>.density` | `compact` / `comfortable` / `spacious` |
| `layouts.<page>.responsiveStrategy` | 各断点的适配策略 |
| `designTokens` | 全局设计决策，非具体像素值而是风格倾向 |

### 下游使用

- **原型生成**：zone → DOM 区块；interactionPatterns → 事件逻辑
- **代码生成**：zone → 组件树；responsiveStrategy → 响应式实现
- **迭代模式**：layout 级别保持不变（除非用户明确要求改布局），delta 只记录 layout 以上的变更
