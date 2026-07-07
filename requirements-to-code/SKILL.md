---
name: requirements-to-code
description: 将需求文档转化为结构化功能树、可交互原型、生产级前端代码及完整测试。当用户提供需求文档（.docx/.md/.pdf）、要求"根据需求做页面/系统"、需要功能拆解或原型制作、提到"需求转代码"、或要求从零搭建前端项目时，必须使用此 skill。支持截图/URL/Figma 作为 UI 参考来驱动页面布局。新建项目与迭代需求两种模式，自动适配现有项目技术栈与代码规范，覆盖从需求分析到可交付的、经过测试的代码的完整流程。
---

# 需求到代码（Requirements to Code）

你是一名产品架构师兼全栈前端工程师。你的工作是将散文式需求转化为结构化、可验证、经过测试的交付物。

---

## 快速开始

**先判定，再动手。** 看到需求文档后的第一步不是写代码，而是回答四个问题：

```
1. 这是什么类型的项目？
   ├─ 没有任何前端代码，从零开始 → 新建模式 → 必须先问技术栈（阶段 0.3）
   ├─ 有前端代码 + specs/features.json 存在 → 迭代模式（完整） → Delta 机制
   └─ 有前端代码但无 specs/ 目录 → 迭代模式（轻量） → 先逆向生成基线（阶段 0.4）

2. 做到哪一步？
   ├─ "只要功能树" → 阶段 0 → 1
   ├─ "做到原型为止" → 阶段 0 → 1 → 2 → 3 → 4
   ├─ "做到代码为止" → 阶段 0 → 1 → 2 → 3 → 4 → 5 → 6
   ├─ "完整流程（默认）" → 全部阶段
   └─ "新增 XX 功能" → 迭代模式快捷入口

3. 有没有 UI 参考？
   ├─ 有截图/URL/Figma → 阶段 3 分析参考
   └─ 无参考 → 阶段 3 使用 frontend-design skill 推导设计

4. 需求是否清晰？
   ├─ 清晰 → 直接进入预处理
   └─ 模糊 → 提出 2-3 个澄清性问题
```

**需求文档缺少 UI 层信息，因此必须主动询问。新建项目缺少技术栈，必须主动询问（或提供一键脚手架）。**

---

## 核心原则

1. **绝不从散文直接跳到代码。** 始终通过功能树——一种结构化的 JSON 表示，其中每个节点是独立的、可验证的用户故事，包含明确的状态、触发器和数据依赖。

2. **状态是头等公民。** 散文式需求往往把角色、页面、状态和边界情况混在段落里。每个功能节点必须显式覆盖 loading / empty / error / normal 及边界状态。

3. **UI 参考填补需求文档的空白。** 需求文档只记录业务流程，不记录 UI 布局。在原型生成前，必须通过截图/URL/Figma/frontend-design skill 来确定页面布局。未经声明就凭空设计 UI 是不可接受的。

4. **每个阶段有检查点，检查点不过不进入下一阶段。** 如果用户说"这个不对"，回到最早受影响的阶段重新推导——不修修补补。

5. **迭代模式下不合并，分层存储。** 每次迭代在 `specs/iterations/` 下独立存储，根目录文件从所有 delta 叠加生成。

6. **迭代模式下优先复用，杜绝重复造轮子。** 生成新代码前，必须先扫描项目中已有的组件、hooks、utils、types、依赖包。功能相近就复用，功能不够就扩展，不新建重复轮子。新代码风格严格仿照既有代码。

---

## 工作模式

### 模式 A：新建项目（Greenfield）

项目目录下不存在 `specs/features.json` 且无现有前端代码。从零开始完整执行所有阶段。

**进入阶段 0 后，必须先完成技术栈问卷（阶段 0.3），否则后续阶段无法生成可运行的代码。**

### 模式 B：迭代需求（Brownfield）

项目已存在前端代码。根据 specs/ 的有无分为两种子模式：

#### B1：完整迭代（已有 specs/）

项目已有 `specs/features.json` 等文件。使用 Delta 机制（详见 `references/iteration-delta.md`）：

1. 读取当前完整功能树 → `specs/features.json`
2. 执行项目上下文扫描（见阶段 0）
3. 分析新需求差异 → `added / modified / removed`
4. 生成变更摘要 → `specs/iterations/NNN-slug/change-summary.md`，用户确认
5. 叠加 delta → 重新生成当前完整的 `features.json`、`routes.json`、`components.json`
6. 后续阶段只处理变更部分

#### B2：轻量迭代（无 specs/，需逆向生成基线）

项目有前端代码但无 `specs/` 目录。此时无法做 diff，因为不知道"现状"是什么。

**策略：针对性逆向，不全量扫描。**

具体方法见阶段 0.4。逆向生成基线后，后续迭代自动进入 B1 模式。

---

## 工作流总览

```
需求文档（.docx / .md / .pdf）+ UI参考（截图/URL/Figma/无）+ 技术栈（新建必须）
      │  阶段 0：预处理 + 评估 + 技术栈/UI参考收集 + 项目扫描/逆向基线
      ▼
specs/requirements.md + specs/project-context.md (+ specs/features.json 基线)
      │  阶段 1：提取/合并功能树
      ▼
specs/features.json
      │  阶段 2：推导架构
      ▼
specs/routes.json + specs/components.json
      │  阶段 3：UI 参考分析（无参考时调用 frontend-design skill）
      ▼
specs/layout-reference.json
      │  阶段 4：生成原型（index.html + 各页面 + 导航）
      ▼
specs/prototypes/index.html + *.html
      │  阶段 5：API 契约 + Mock 数据层
      ▼
specs/api/openapi.yaml + src/mocks/*
      │  阶段 6：生成生产代码（迭代模式：优先复用既有组件/类型/hooks）
      ▼
src/components/*, src/pages/*, src/router/*, src/hooks/*
      │  阶段 7：生成测试
      ▼
src/__tests__/*, e2e/*
```

---

## 阶段 0：预处理与评估

**产出：** `specs/requirements.md`、`specs/project-context.md`（+ 迭代 B2 模式下还有 baseline `specs/features.json` 等），以及确定的执行模式和范围。

### 0.1 文档格式处理

| 格式 | 处理方式 |
|---|---|
| `.md` | 直接读取 |
| `.docx` | 若 Python 可用 → `python scripts/convert_docx_to_md.py <input.docx> specs/requirements.md`；否则用 pandoc：`pandoc input.docx -t markdown -o specs/requirements.md`；都没有则用 macOS `textutil -convert txt` |
| `.pdf` | `pdftotext` 或 Python `PyPDF2` |
| 纯文本/粘贴 | 直接保存为 `specs/requirements.md` |
| 在线文档（语雀/飞书/Notion） | WebFetch 获取；不可达则请用户导出 |

> **关于 scripts/ 目录下的 Python 脚本：** 它们是加速器而非依赖。如果用户环境有 Python 3，直接运行。如果没有，手动执行等效操作：docx 转换用 pandoc/textutil 命令，delta 叠加直接写 JSON 合并逻辑，项目扫描直接用 Read + 分析即可。

### 0.2 模式判定

检查：
- `src/` 或前端代码是否存在？
- `specs/features.json` 是否存在？

→ 确定：新建 / 完整迭代(B1) / 轻量迭代(B2)。向用户确认判定结果。

### 0.3 新建项目：技术栈问卷（必须）

**新建项目必须逐项确认技术栈。** 不给用户选择题就写代码等于猜谜——生成的代码大概率跑不起来。

逐项询问（可以一次性列出让用户批量回答，也可以一问一答）：

| 类别 | 问题 | 常见选项 |
|---|---|---|
| **框架** | React / Vue / Angular / Svelte / Solid？ | React 18+ / Vue 3+ |
| **构建工具** | Vite / Webpack / Next.js / Nuxt / Remix？ | Vite（推荐） |
| **TypeScript** | 用吗？（默认用） | Yes / No |
| **CSS 方案** | Tailwind / CSS Modules / Sass / styled-components / Emotion？ | Tailwind（推荐） |
| **组件库** | shadcn/ui / Ant Design / MUI / Element Plus / Naive UI / 无？ | shadcn/ui（推荐，开箱即用）|
| **状态管理** | Zustand / Redux / Pinia / Jotai / 只用 hooks？ | Zustand（轻量）/ 只用 hooks（简单场景）|
| **路由** | React Router / Vue Router / TanStack Router？ | 框架默认方案 |
| **测试框架** | Vitest / Jest + React Testing Library / Playwright？ | Vitest + RTL + Playwright |
| **包管理** | pnpm / npm / yarn / bun？ | pnpm（推荐） |
| **目录规范** | 有无特殊偏好？（默认按功能拆分：`components/`, `pages/`, `hooks/`, `api/`） | 默认即可 |
| **API 模式** | REST / GraphQL / tRPC？Auth 方案？HTTP client？ | REST + axios/fetch |

**一键脚手架方案（推荐给用户以减少决策负担）：**

> 如果你不想逐项选择，推荐这套开箱即用组合：
> **React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui + Zustand + React Router + Vitest + RTL + Playwright + pnpm**
> 这是当前业界最主流的前端技术栈，生态成熟，文档齐全。要我按这套直接开始吗？

如果用户选了一键方案，在阶段 6 生成代码前，用 `npm create vite@latest` 或等价命令初始化项目骨架。

### 0.4 迭代项目：项目扫描 + 逆向基线

#### 通用项目扫描（B1 和 B2 都要做）

若 Python 可用 → `python scripts/scan_project.py [project_dir]` 生成初始报告。无论脚本是否可用，都需补充分析：

1. **框架与构建工具** — package.json → 框架、构建工具、TypeScript、CSS 方案
2. **组件库/设计系统** — dependencies 中的组件库、Tailwind 配置中的 design tokens
3. **目录结构与命名规范** — `src/` 组织方式；**采样 5+ 个组件**提取代码风格（声明方式、类型位置、样式方案、状态管理、文件名规范、路径别名、import 顺序）
4. **已有组件清单** — 列出所有共享组件和页面组件及其用途（**关键：后续生成新代码时必须优先复用**）
5. **已有 hooks/utils/types** — 列出已有的数据获取 hooks、工具函数、公共类型（**关键：避免重复定义**）
6. **路由模式** — 现有路由配置和 Layout 组件
7. **API 调用模式** — HTTP 封装、数据获取 hooks、认证方式、请求/响应类型定义
8. **测试框架** — 测试库、测试文件位置和命名规范

产出 `specs/project-context.md`，**特别标注"可复用资产清单"**（已有组件、hooks、utils、types）。

#### B2 子模式：逆向生成基线

当项目有前端代码但无 `specs/` 时，需要从代码逆向推导出功能树基线。**不需要扫描整个项目**，策略如下：

**1. 判断项目规模，选择策略：**

| 项目规模 | 判断依据 | 策略 |
|---|---|---|
| 小型 | < 10 个页面/路由 | 全量逆向 — 扫描所有页面，生成完整 baseline |
| 中型 | 10-30 个页面 | 采样逆向 — 先逆向本次需求相关的页面，其余页面只记录路由和标题 |
| 大型 | 30+ 个页面或 monorepo | 局部逆向 — 只逆向本次需求涉及的功能区域，其余标记为 `{ "id": "...", "title": "...", "page": "...", "source": "not-reverse-engineered" }` |

**2. 逆向分析的方法：**

- **路由** → 从 router 配置文件提取所有路由 → `specs/routes.json`
- **组件** → 从 `src/components/` 列举已有组件、props 签名、用途 → `specs/components.json`
- **功能节点** → 从页面组件 + 路由推导功能树：
  - 每个路由 → 一个功能节点（至少）
  - 分析页面组件的 JSX 结构 → 识别子功能（筛选、分页、CRUD 操作等）
  - API 调用（fetch/axios/useQuery 等）→ 提取 dataDependencies
  - 条件渲染 → 识别不同状态
  - `"inferred": true` 标注所有推断字段（因为不是从需求文档提取的）
- **对于无法自动分析的复杂逻辑**（如接口动态生成按钮、权限控制渲染等）→ 标记为 `"note": "需人工确认"`，列出不确定性供用户修正

**3. 向用户确认：**

逆向完成后，展示基线摘要并询问：
> 我从现有代码逆向生成了功能树基线，包含 X 个功能节点、Y 个路由、Z 个组件。以下是摘要，请确认或修正。确认后我会用它作为基线，后续迭代就可以做 diff 了。

用户确认后的基线即为"当前完整态"，本次迭代的 delta 基于此计算。

### 0.5 UI 参考收集（必须询问）

需求文档通常缺少 UI 层信息，必须主动询问。话术参见 `references/ui-reference-analysis.md`。

如果用户提供了截图，用 Read 读取并初步分析。详细分析在阶段 3。

### 0.6 需求澄清

如果需求不清晰，提出 2-3 个澄清性问题。不清晰时不要硬猜。

---

## 阶段 1：功能树

**输入：** `specs/requirements.md`（+ 迭代模式下的旧/逆向 baseline `specs/features.json`）
**输出：** `specs/features.json`（+ 迭代模式下的 `specs/iterations/NNN-slug/`）

### 节点结构

完整 schema 见 `references/schemas.md`。核心字段：

| 字段 | 规则 |
|---|---|
| `id` | 唯一 kebab-case |
| `priority` | P0=核心流程 / P1=重要 / P2=增强 / P3=锦上添花 |
| `acceptanceCriteria` | "假设/当/则"格式，每节点 ≤5 条 |
| `states` | 列表页≥4 种(loading/empty/error/normal)；表单页≥5 种(+idle/validating/submitting/success/error) |
| `dataDependencies[].inferred` | 推断字段标注 `true` |
| `version` | 每次修改递增 |

### 通用规则

1. 每个用户可见的交互都是一个功能节点
2. 数据依赖必须命名具体字段和类型
3. subFeatures 引用其他功能 ID
4. 每个节点覆盖所有相关状态

### 迭代模式

使用 delta 格式（完整 schema 见 `references/schemas.md`）。若 Python 可用 → `python scripts/apply_delta.py <features.json> <delta.json> --in-place`；否则手动合并 JSON（按 added/modified/removed 逐条处理）。

### 验证检查点

- [ ] 每个页面至少一个功能节点
- [ ] 每个功能覆盖所有状态
- [ ] 导航交互都有目标路由
- [ ] 无功能超过 5 条验收标准
- [ ] 所有 ID 唯一 kebab-case
- [ ] 推断字段已标注 `inferred: true`
- [ ] 迭代模式：change-summary.md 经用户确认

---

## 阶段 2：架构推导

**输入：** `specs/features.json`
**输出：** `specs/routes.json`、`specs/components.json`

完整 schema 见 `references/schemas.md`。

### 推导规则

1. **路由将相关功能分组** — 多个功能节点共享同一页面时合并到一个路由
2. **布局是抽象的** — 识别布局模式（authenticated/public），明确每种包含的外壳组件
3. **2+ 页面使用的组件 → 共享组件**；只用一次的 → 页面专属
4. **每个组件列出 props 和 states** — 在写代码前先确定 API 接口
5. **迭代模式：优先扩展现有组件 props**，而非新建重复组件。查看 project-context.md 中的"可复用资产清单"，确认是否已有功能相近的组件。

---

## 阶段 3：UI 参考分析

**输入：** 用户提供的截图/URL/Figma/口头描述（或无） + `specs/features.json` + `specs/routes.json`
**输出：** `specs/layout-reference.json`

详细分析方法见 `references/ui-reference-analysis.md`。完整 schema 见 `references/schemas.md`。

### 三条路径

| 情况 | 处理方式 |
|---|---|
| **有截图** | 用 Read 读取图片 → 分析布局骨架、UI 组件、交互模式、信息层级 → 输出 layout-reference.json |
| **有 URL** | WebFetch 获取页面 → 分析 DOM 结构 → 输出 layout-reference.json |
| **有 Figma** | 通过 Figma MCP 读取设计稿 → 输出 layout-reference.json |
| **有口头描述** | 解析自然语言 → 映射到布局模式 → 输出 layout-reference.json |
| **无任何参考** | **调用 `frontend-design` skill** 为每个页面推导有意的、独特的视觉设计 → 输出 layout-reference.json |

### 无参考时：使用 frontend-design skill

**当用户没有提供截图/URL/Figma/口头描述时，不要用"后台管理模板"式的平庸布局。** 必须调用 `frontend-design` skill，让它根据页面的功能特征来推导设计：

具体方法见 `references/ui-reference-analysis.md` 中的"使用 frontend-design skill 推导设计"章节。

### 关键产出：`specs/layout-reference.json`

包含每个页面的 zones（区块划分）、interactionPatterns（交互模式）、density（信息密度）、responsiveStrategy（响应式策略）和全局 designTokens。

---

## 阶段 4：原型生成

**输入：** `specs/features.json` + `specs/routes.json` + `specs/components.json` + `specs/layout-reference.json`
**输出：** `specs/prototypes/index.html` + 各页面 HTML 文件

### 导航枢纽模式

**不生成孤立的一堆 .html 文件。** 生成一个 `specs/prototypes/index.html` 作为导航枢纽：

```
specs/prototypes/
  index.html          ← 导航枢纽页（侧边栏列出所有页面 + 点击切换 iframe 或直接导航）
  orders.html         ← 各页面原型（自包含，也可独立打开）
  orders-detail.html
  users.html
  ...
```

`index.html` 结构：
- 左侧/顶部导航栏，列出所有页面名称（来自 routes.json）
- 点击导航项 → 在右侧内容区用 `<iframe>` 加载对应页面，或直接 `window.location` 跳转
- 显示当前所在页面、页面总数
- 可选：在 index.html 内联展示所有页面的缩略图/卡片

**好处：** 用户打开 `index.html` 就能浏览整个系统，不需要手动逐个打开 HTML 文件。

### 原型要求

1. **自包含** — 每个页面的 CSS/JS 全内联，既可嵌入 index.html 的 iframe，也可独立打开
2. **状态全覆盖** — 浮动状态切换器切换 loading/empty/error/normal + 边界状态
3. **真实感数据** — "Acme 集团"、"¥1,234.56"、"订单 #3847 — 已发货"
4. **交互可感知** — 按钮有反馈、表单有验证、弹窗可开关、导航可跳转
5. **设计系统化** — 一致调色板、字体层级、间距尺度
6. **响应式** — 375px / 768px / 1280px+
7. **先结构后视觉** — 第一遍：布局骨架 + 状态 + 交互；第二遍：叠加设计系统

HTML 模板（含 index.html 导航枢纽模板）见 `references/templates.md`。

### 并行策略

页面数 > 2 时，按页面并行生成，最后汇总生成 index.html。详细策略见 `references/parallel-execution.md`。

---

## 阶段 5：API 契约 + Mock 数据层

**输入：** `specs/features.json` 中所有 `dataDependencies`
**输出：** `specs/api/openapi.yaml`、`src/mocks/handlers.ts`、`src/mocks/data.ts`、`specs/api/adapter-guide.md`

### API 契约（OpenAPI 3.0）

从 `dataDependencies` 自动推导：
- 每个 `source` → 一个 API 路径
- 每个 endpoint 覆盖 200 / 400 / 401 / 500 四种响应
- 推断字段在 description 标注 `[推断字段，待确认]`

### Mock 数据工厂（`src/mocks/data.ts`）

确定性工厂函数 + 真实感数据。通过 URL 参数切换五种场景：

| 场景 | 触发方式 | 用途 |
|---|---|---|
| 正常数据 | 默认 | 常规开发、演示 |
| 空数据 | `?mock=empty` | 空状态测试 |
| 错误 | `?mock=error` | 错误状态测试 |
| 边界 | `?mock=edge` | 长文本/大量数据/特殊字符 |
| 权限异常 | `?mock=unauthorized` | 401/403 测试 |

### 请求处理器（`src/mocks/handlers.ts`）

默认使用 MSW。提供 `delay()` 模拟网络延迟，让 loading 状态可见可测。

### 对接指南（`specs/api/adapter-guide.md`）

包含：Mock ↔ 真实后端切换方式、对接检查清单、已知差异表、adapter 层说明。

---

## 阶段 6：生产代码

**输入：** 原型 + components.json + routes.json + openapi.yaml + layout-reference.json + project-context.md
**输出：** `src/` 目录下的框架代码

### 迭代模式：优先复用检查（写任何新代码前必做）

**这是迭代模式最重要的规则。** 在创建每个新文件之前，执行以下检查：

```
我要新建 [组件/hook/type/util] 来满足 [功能需求]
      │
      ├─ 步骤 1：搜索 project-context.md 中的"可复用资产清单"
      │    ├─ 找到功能相近的 → 直接复用（import 使用）
      │    ├─ 找到功能部分相近的 → 扩展该组件/hook（加 props/参数），不新建
      │    └─ 没有找到 → 步骤 2
      │
      ├─ 步骤 2：搜索项目中是否有同类的依赖包
      │    ├─ 例如：已有 dayjs 就不要引入 moment；已有 lodash 就不要手写工具函数
      │    └─ 优先使用项目已有的依赖
      │
      ├─ 步骤 3：检查是否有相同签名的 type/interface
      │    ├─ 已知项目中有 `User` 类型 → 不重新定义
      │    └─ 需要扩展 → `interface UserExt extends User { ... }`
      │
      └─ 步骤 4：确认没有可复用的 → 新建
           └─ 代码风格严格参照 project-context.md 中的采样（声明方式、命名、import 顺序、样式方案）
```

**新代码风格仿照规则：**
- 采样 5+ 个现有组件，提取风格特征
- import 顺序保持一致（如 React → 第三方 → 项目模块 → 样式）
- 导出方式保持一致（named export vs default export）
- 类型定义位置保持一致（同文件 vs 独立 types 文件）
- 样式方案保持一致（Tailwind class 顺序、CSS Module 命名）
- 状态管理模式保持一致（hooks 写法、store 结构）

### 目录结构（React + TypeScript）

```
src/
  api/                     # API 调用层（client.ts + 接口文件 + types.ts）
  components/
    shared/                # 跨页面共享组件
    [page-name]/           # 页面专属组件
  pages/                   # 页面组件
  router/index.tsx         # 路由定义
  hooks/                   # 数据获取 hooks（每个数据源一个 hook）
  types/                   # 共享类型
  layouts/                 # 布局组件
  mocks/                   # Mock 数据（阶段 5 产出）
```

### 代码生成规则

1. 组件 props 与 components.json 一致
2. 状态处理是头等大事 — 每个数据组件必须处理 loading/empty/error/normal
3. API 调用统一走 `src/api/` 层 — mock ↔ 真实切换只改 client.ts
4. 路由与 routes.json 匹配
5. 代码风格遵循 project-context.md 的规范
6. 有组件库就用组件库 — 不重复实现已有原语
7. 每个数据获取需求封装为一个 hook

Hook 模板见 `references/templates.md`。

### 并行策略

页面数 > 2 时：
1. 先派一个 Agent 生成全局基础设施（api/、mocks/、types/、layouts/、router/、共享组件）
2. 再为每个页面派 Agent 生成页面代码
3. 汇总 agent 检查一致性

详细策略见 `references/parallel-execution.md`。

### 迭代模式

只生成/修改变更部分的代码。新增→新建文件；修改→Read+Edit；废弃→`@deprecated` 注释。

---

## 阶段 7：测试生成

**输入：** `specs/features.json` + 阶段 6 的代码 + `specs/project-context.md`
**输出：** 组件单测 + Hooks 测试 + 集成测试 + E2E 测试

### 功能树到测试的映射

每个功能节点的 `acceptanceCriteria` 直接映射为测试用例。覆盖范围：

```
e2e/                              # E2E：P0 关键用户流程
  orders-flow.spec.ts

src/__tests__/
  integration/                    # 集成测试：页面级渲染与交互
  components/                     # 组件单测：render、props、交互、状态、无障碍
  hooks/                          # Hooks 单测：loading → data → error → refetch
  api/                            # API 层测试：请求拦截、错误处理
```

### 测试生成规则

1. 一个组件 → 一个测试文件，位置与源文件对应
2. 每个验收标准至少一个测试用例
3. 四种状态全部覆盖（loading/empty/error/normal 各至少一个）
4. 每个用户交互至少一个测试
5. 共享组件有完整单测；页面组件依赖集成测试
6. E2E 只覆盖 P0 用户流程
7. 测试数据从阶段 5 的 Mock 工厂获取
8. 迭代模式只生成变更相关的测试

测试模板见 `references/templates.md`。

### 并行策略

单元测试和 Hook 测试耦合到各自组件，由生成该组件的 Agent 同步产出。集成测试和 E2E 在代码汇总后由 1-2 个 Agent 集中生成。详见 `references/parallel-execution.md`。

### 验证检查点

- [ ] `npm run test` 无错误全部通过
- [ ] `npm run test:e2e` P0 流程通过
- [ ] P0/P1 功能的验收标准有对应测试覆盖
- [ ] 每个组件至少四种状态的测试
- [ ] 每个数据 hook 有 loading → data → error 三态测试
- [ ] 测试使用 MSW Mock，不走真实网络

---

## 并行执行总则

大型项目（功能节点 ≥16 或页面 ≥6）自动启用并行模式。核心原则：

- **架构阶段（阶段 1-2）必须串行** — 路由和组件划分是全局决策
- **产出阶段（阶段 3-7）按页面并行** — 每个页面的原型、代码、测试正交
- **并行前播报计划** — 告知用户哪些 agent 在做什么
- **并行后汇总检查** — 路由冲突、组件重复、API 类型冲突、导航一致性

完整策略、判定矩阵、输入包格式和用户可见性要求见 `references/parallel-execution.md`。

---

## 最终产物目录

```
项目根目录/
  specs/
    requirements.md                # 原始需求副本
    project-context.md             # 项目上下文扫描（含可复用资产清单）
    features.json                  # 当前完整功能树
    routes.json                    # 当前完整路由表
    components.json                # 当前完整组件清单
    layout-reference.json          # UI 布局参考
    api/
      openapi.yaml                 # API 契约
      adapter-guide.md             # 前后端对接指南
    prototypes/                    # 当前完整原型
      index.html                   # 导航枢纽页
      orders.html                  # 各页面原型
      ...
    iterations/                    # 迭代历史
      NNN-slug/
        requirements.md            # 该次迭代的原始需求
        features-delta.json        # 变更增量
        change-summary.md          # 人类可读摘要
        prototypes/
  src/
    api/ components/ pages/ router/ hooks/ types/ layouts/ mocks/ __tests__/
  e2e/
```

---

## 常见陷阱与恢复

| # | 陷阱 | 恢复方法 |
|---|---|---|
| 1 | 跳过状态 — 只做了 normal | 回顾 features.json 的 states 字段，逐项补全 |
| 2 | 孤立交互 — 按钮没有实现 | 对照 routes.json 和 interactions 逐项检查 |
| 3 | 数据模糊 — 推断字段未标注 | 排查 dataDependencies，inferred 字段标 true |
| 4 | 忽略已有规范 — 新代码风格不一致 | 回到 project-context.md，补充采样后重新生成 |
| 5 | Mock 数据太简单 | 使用工厂函数生成 10-20 条真实感数据，覆盖五种场景 |
| 6 | 测试滞后或缺失 | 回到阶段 7 补充，验收标准→测试用例逐条映射 |
| 7 | API 层与 UI 层耦合 | 统一走 src/api/ 层，组件不直接调 fetch() |
| 8 | **重复造轮子** — 新建了项目已有的组件/类型/hooks | 写新代码前先搜 project-context.md 的复用清单；搜 `src/` 下同类文件 |
| 9 | **逆向基线过重** — 花大量时间逆向无关页面 | 按阶段 0.4 的策略判断规模：大型项目只逆向需求相关的区域 |

详细恢复策略和预防措施见 `references/pitfalls.md`。

如果用户反馈"这个不对"，回到最早受影响的阶段重新推导——不修修补补，重新生成。

---

## 参考文件索引

当遇到特定主题时，读取对应的参考文件：

| 主题 | 参考文件 | 何时读取 |
|---|---|---|
| 功能树/路由/组件/layout JSON 结构 | `references/schemas.md` | 阶段 1-3 生成 JSON 时 |
| HTML 原型/Hook/测试代码模板 | `references/templates.md` | 阶段 4/6/7 生成代码时 |
| 大型项目并行执行策略 | `references/parallel-execution.md` | 功能节点 ≥16 或用户要求并行 |
| UI 参考分析方法（截图/URL/Figma/frontend-design） | `references/ui-reference-analysis.md` | 阶段 0 收集参考 + 阶段 3 分析 |
| 迭代模式 Delta 机制 | `references/iteration-delta.md` | 进入迭代模式时 |
| 常见陷阱诊断与恢复 | `references/pitfalls.md` | 遇到质量问题或用户反馈"不对" |
| Docx→Markdown 转换脚本 | `scripts/convert_docx_to_md.py` | 输入为 .docx 且 Python 可用时 |
| Delta 叠加脚本 | `scripts/apply_delta.py` | 迭代模式合并功能树且 Python 可用时 |
| 项目上下文扫描脚本 | `scripts/scan_project.py` | 阶段 0 项目扫描且 Python 可用时 |

---

## 交互流程

1. **判定模式** — 新建？完整迭代(B1)？轻量迭代(B2)？
2. **新建模式** → 必须先完成技术栈问卷（阶段 0.3），或用户选择一键脚手架
3. **迭代模式** → 立即执行项目扫描（含可复用资产清单）
4. **迭代 B2 模式** → 逆向生成 baseline（阶段 0.4），用户确认后进入 B1 流程
5. **确定范围** — 完整流程 / 到原型 / 到代码 / 只要功能树？
6. **收集 UI 参考** — 必须主动询问（使用 `ui-reference-analysis.md` 中的话术）
7. **预处理** — 文档转换、上下文扫描
8. **逐阶段推进** — 每个检查点等待用户确认后进入下一阶段
9. **需要时读参考文件** — 根据"参考文件索引"按需加载

绝不跳过检查点。绝不跳过状态覆盖。绝不交付未测试的代码。绝不凭空设计 UI 而不知会用户。迭代模式绝不重复造轮子。
