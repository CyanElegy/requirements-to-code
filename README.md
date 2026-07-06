# Requirements to Code

> 将需求文档转化为结构化功能树、可交互原型、生产级前端代码及完整测试。

[![Chinese](https://img.shields.io/badge/README-中文-red)](README_CN.md)

A Claude Code skill that transforms prose requirements documents into structured feature trees, interactive prototypes, production-grade frontend code, and comprehensive tests.

## Features

- **📄 Multi-format input** — `.docx`, `.md`, `.pdf`, or plain text requirements
- **🌳 Feature tree** — Structured intermediate layer between requirements and code; every node is a verifiable user story
- **🎨 UI reference analysis** — Drive layout from screenshots (PNG/JPG), URLs, Figma designs, verbal descriptions, or auto-generate with the `frontend-design` skill
- **🖼️ Interactive prototypes** — Self-contained HTML with state switchers (loading/empty/error/normal), navigable via index.html hub
- **🔌 API contract + Mock layer** — Auto-derived OpenAPI 3.0 specs + MSW mock data with 5 scenarios
- **🧩 Production code** — Framework-aware code generation that follows your project's conventions
- **✅ Full test suite** — Unit, integration, and E2E tests mapped from acceptance criteria
- **🔄 Iteration mode** — Delta-based change tracking; only regenerate what changed
- **⚡ Parallel execution** — Multi-page projects fan out to parallel agents for speed

## Quick Start

### Installation

Install via the Claude Code skill system (recommended):

```bash
npx skills add https://github.com/CyanElegy/requirements-to-code --skill requirements-to-code
```

Or install via the Claude Code plugin system:

```
/plugin install github.com/CyanElegy/requirements-to-code
```

Or clone directly to the skills directory:

```bash
git clone https://github.com/CyanElegy/requirements-to-code.git ~/.claude/skills/requirements-to-code
```

### Usage

Just talk to Claude naturally:

```
"根据这份需求文档，帮我做一个订单管理系统"
"Turn this PRD into a working prototype"
"给现有的订单页面新增批量导出功能"（迭代模式）
```

The skill automatically detects:
- **New project** vs **iteration** (existing codebase)
- **Scope** — full pipeline / prototype only / feature tree only
- **UI references** — asks you for screenshots, URLs, or Figma links if available

### What You Get

```
project/
  specs/
    features.json              # Complete feature tree
    routes.json                # Route definitions
    components.json            # Component inventory
    layout-reference.json      # UI layout analysis
    prototypes/
      index.html               # Navigation hub
      orders.html              # Self-contained page prototypes
      ...
    iterations/                # Iteration history (full traceability)
    api/
      openapi.yaml             # API contract
      adapter-guide.md         # Backend integration guide
  src/
    api/ components/ pages/ router/ hooks/ types/ layouts/ mocks/ __tests__/
  e2e/
```

## Requirements

- **Claude Code** (CLI, desktop, or IDE extension)
- Python 3 (optional — for bundled helper scripts; all operations have manual fallbacks)
- `pandoc` (optional — for best `.docx` conversion quality)

## Tech Stack (Greenfield Default)

When creating a new project from scratch, the recommended one-click scaffold is:

**React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui + Zustand + React Router + Vitest + RTL + Playwright + pnpm**

You can customize every choice during the interactive setup.

## How It Works

```
Requirements (.docx/.md/.pdf) + UI References (screenshots/URLs/Figma)
      │  Stage 0: Preprocessing + assessment + tech stack questionnaire
      ▼
specs/requirements.md + specs/project-context.md
      │  Stage 1: Extract feature tree (or apply delta for iterations)
      ▼
specs/features.json
      │  Stage 2: Derive architecture (routes + components)
      ▼
specs/routes.json + specs/components.json
      │  Stage 3: UI reference analysis (or invoke frontend-design skill)
      ▼
specs/layout-reference.json
      │  Stage 4: Generate navigable prototypes (index.html hub)
      ▼
specs/prototypes/index.html + *.html
      │  Stage 5: API contract + Mock data layer
      ▼
specs/api/openapi.yaml + src/mocks/*
      │  Stage 6: Generate production code (reuse-first for iterations)
      ▼
src/components/*, src/pages/*, src/router/*, src/hooks/*
      │  Stage 7: Generate tests (unit + integration + E2E)
      ▼
src/__tests__/*, e2e/*
```

## Directory Structure

```
requirements-to-code/
├── SKILL.md                          # Main skill instructions
├── references/                       # Progressive disclosure reference files
│   ├── schemas.md                    # All JSON schema definitions
│   ├── templates.md                  # Code templates (prototype, hook, test)
│   ├── parallel-execution.md         # Large project parallel execution strategy
│   ├── ui-reference-analysis.md      # Screenshot/URL/Figma/design-skill analysis
│   ├── iteration-delta.md            # Iteration mode delta mechanism
│   └── pitfalls.md                   # Common pitfalls with recovery strategies
└── scripts/                          # Bundled helper scripts (Python)
    ├── convert_docx_to_md.py         # .docx → .md converter
    ├── apply_delta.py                # Delta merger for iteration mode
    └── scan_project.py              # Project context scanner
```

## License

MIT
