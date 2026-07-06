# Requirements to Code（需求到代码）

> 将需求文档转化为结构化功能树、可交互原型、生产级前端代码及完整测试。

[![English](https://img.shields.io/badge/README-English-blue)](README.md)

一个 Claude Code skill，将散文式需求文档转化为结构化功能树、可交互原型、生产级前端代码及全面测试。

## 功能特性

- **📄 多格式输入** — 支持 `.docx`、`.md`、`.pdf` 或纯文本需求
- **🌳 功能树** — 需求与代码之间的结构化中间层，每个节点都是可验证的用户故事
- **🎨 UI 参考分析** — 通过截图（PNG/JPG）、URL、Figma、口头描述确定布局，无参考时调用 `frontend-design` skill 自动推导
- **🖼️ 可交互原型** — 自包含 HTML + 浮动状态切换器（loading/empty/error/normal），index.html 导航枢纽一键浏览
- **🔌 API 契约 + Mock** — 自动推导 OpenAPI 3.0 + MSW mock 数据（5 种场景切换）
- **🧩 生产级代码** — 自动适配项目技术栈与代码规范
- **✅ 完整测试** — 验收标准逐条映射为单元/集成/E2E 测试
- **🔄 迭代模式** — Delta 增量变更追踪，每次迭代独立存储、完全可溯源
- **⚡ 并行执行** — 多页面项目自动按页面拆分并行 agent

## 快速开始

### 安装

通过 Claude Code skill 系统安装（推荐）：

```bash
npx skills add CyanElegy/requirements-to-code --skill requirements-to-code
```

或通过 Claude Code 插件系统安装：

```
/plugin install github.com/CyanElegy/requirements-to-code
```

或直接克隆到 skills 目录：

```bash
git clone https://github.com/CyanElegy/requirements-to-code.git ~/.claude/skills/requirements-to-code
```

### 使用

直接用自然语言对话即可触发：

```
"根据这份需求文档，帮我做一个订单管理系统"
"把这份 PRD 转成可交互原型"
"给现有的订单页面新增批量导出功能"（迭代模式）
"做到原型为止就好"
"只要功能树"
```

Skill 会自动判断：
- **新建项目** vs **迭代项目**（是否有现有代码）
- **执行范围** — 完整流程 / 到原型 / 到代码 / 只要功能树
- **UI 参考** — 主动询问是否有截图、URL 或 Figma

### 产出物

```
项目/
  specs/
    features.json              # 完整功能树
    routes.json                # 路由定义
    components.json            # 组件清单
    layout-reference.json      # UI 布局参考
    prototypes/
      index.html               # 导航枢纽页
      orders.html              # 各页面原型（自包含）
      ...
    iterations/                # 迭代历史（完全可溯源）
    api/
      openapi.yaml             # API 契约
      adapter-guide.md         # 前后端对接指南
  src/
    api/ components/ pages/ router/ hooks/ types/ layouts/ mocks/ __tests__/
  e2e/
```

## 环境要求

- **Claude Code**（CLI / 桌面应用 / IDE 扩展）
- Python 3（可选 — 辅助脚本有手动降级方案）
- `pandoc`（可选 — 获得最佳 `.docx` 转换质量）

## 新建项目默认技术栈

从零搭建时的推荐一键方案：

**React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui + Zustand + React Router + Vitest + RTL + Playwright + pnpm**

每个选项都可以在交互式设置中自定义。

## 工作流

```
需求文档（.docx/.md/.pdf）+ UI 参考（截图/URL/Figma）
      │  阶段 0：预处理 + 评估 + 技术栈/UI参考收集 + 项目扫描
      ▼
specs/requirements.md + specs/project-context.md
      │  阶段 1：提取功能树（迭代模式则应用 delta）
      ▼
specs/features.json
      │  阶段 2：推导架构（路由 + 组件）
      ▼
specs/routes.json + specs/components.json
      │  阶段 3：UI 参考分析（无参考时调用 frontend-design skill）
      ▼
specs/layout-reference.json
      │  阶段 4：生成可导航原型（index.html 枢纽）
      ▼
specs/prototypes/index.html + *.html
      │  阶段 5：API 契约 + Mock 数据层
      ▼
specs/api/openapi.yaml + src/mocks/*
      │  阶段 6：生成生产代码（迭代模式优先复用既有资产）
      ▼
src/components/*, src/pages/*, src/router/*, src/hooks/*
      │  阶段 7：生成测试（单元 + 集成 + E2E）
      ▼
src/__tests__/*, e2e/*
```

## 目录结构

```
requirements-to-code/
├── SKILL.md                          # 主 skill 指令
├── references/                       # 渐进式加载参考文件
│   ├── schemas.md                    # JSON Schema 定义
│   ├── templates.md                  # 代码模板（原型/Hook/测试）
│   ├── parallel-execution.md         # 大型项目并行策略
│   ├── ui-reference-analysis.md      # 截图/URL/Figma/design-skill 分析
│   ├── iteration-delta.md            # 迭代模式 Delta 机制
│   └── pitfalls.md                   # 常见陷阱与恢复策略
└── scripts/                          # 辅助脚本（Python）
    ├── convert_docx_to_md.py         # .docx → .md 转换
    ├── apply_delta.py                # 迭代模式 Delta 合并
    └── scan_project.py              # 项目上下文扫描
```

## License

MIT
