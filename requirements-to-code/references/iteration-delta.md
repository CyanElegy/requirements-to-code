# 迭代模式与 Delta 机制

迭代模式（Brownfield）用于在已有项目中增量添加功能。核心理念是**不合并，分层存储**——每次迭代独立存储输入和变更增量，根目录文件从所有 delta 叠加生成。

---

## 目录结构

```
specs/
  features.json                 ← 当前完整功能树（从所有 delta 叠加生成）
  routes.json                   ← 当前完整路由表
  components.json               ← 当前完整组件清单

  iterations/                   ← 迭代历史（每次独立，完全可溯源）
    001-initial-release/
      date: 2026-07-03
      requirements.md           ← 该次迭代的原始需求
      features-delta.json       ← { added: [...], modified: [...], removed: [...] }
      change-summary.md         ← 人类可读变更摘要
      prototypes/               ← 该次迭代新增/变更的原型文件
    002-add-user-profile/
      date: 2026-07-10
      requirements.md
      features-delta.json
      change-summary.md
      prototypes/
```

---

## 设计优势

- 每次迭代增量很小（只记录变化），文件不膨胀
- 每次迭代的原始需求和变更完全可溯源
- 根目录的功能树始终是干净的"当前完整态"
- Git diff 天然可见每次迭代的改动范围

---

## 进入迭代模式的前置步骤

1. **读取当前完整功能树** — `specs/features.json`
2. **扫描现有代码** — 执行项目上下文扫描（见阶段 0）
3. **分析新需求差异** — 与新需求做 diff → `added / modified / removed`
4. **生成变更摘要** — `specs/iterations/NNN-slug/change-summary.md`，用户确认后继续
5. **叠加 delta** → 重新生成当前完整 `features.json` 等文件（可使用 `scripts/apply_delta.py`）
6. **后续阶段只处理变更部分** — 原型、Mock、代码、测试都只生成/更新受影响的文件

---

## Delta 格式

完整 schema 见 `references/schemas.md`。核心结构：

```json
{
  "iteration": "003-add-batch-operations",
  "basedOn": "features.json at iteration 002-add-user-profile",
  "date": "2026-07-15",
  "changes": {
    "added": [{ /* 完整的新功能节点 */ }],
    "modified": [{
      "id": "order-list-view",
      "changes": { /* 只含变更字段 */ }
    }],
    "removed": [{ "id": "legacy-export", "reason": "..." }]
  },
  "unaffected": ["order-detail-view", "..."]
}
```

---

## 迭代模式代码修改策略

| 变更类型 | 操作方式 |
|---|---|
| 新增功能/页面/组件 | 新建文件 |
| 修改现有功能 | Read + Edit 修改现有文件 |
| 废弃功能 | 加 `@deprecated` 注释，不直接删除 |
| 不影响的功能 | 不触碰 |

---

## 版本追踪

每个功能节点有 `version` 字段，每次修改递增。Delta 的 `basedOn` 字段记录基于哪个版本生成，保证完整的变更溯源链。
