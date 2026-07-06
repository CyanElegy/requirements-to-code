#!/usr/bin/env python3
"""
Scan a frontend project directory and produce a project-context.md summary.

Usage:
    python scan_project.py [project_dir]

If project_dir is omitted, defaults to the current working directory.
Output is written to stdout.
"""

import sys
import json
import os
from pathlib import Path


def find_file(root: Path, *names: str) -> Path | None:
    """Find the first existing file from a list of candidates."""
    for name in names:
        p = root / name
        if p.exists():
            return p
    return None


def read_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def extract_tech_stack(pkg_json: dict) -> dict:
    """Extract framework, build tool, CSS solution, test framework from package.json."""
    deps = {**pkg_json.get("dependencies", {}), **pkg_json.get("devDependencies", {})}
    dep_lower = {k.lower(): k for k in deps}

    info: dict[str, str | None] = {
        "framework": None,
        "buildTool": None,
        "cssSolution": None,
        "testFramework": None,
        "testLibraries": [],
        "componentLibrary": None,
        "stateManagement": None,
        "typeScript": "typescript" in deps or "typescript" in pkg_json.get("devDependencies", {}),
    }

    # Framework
    for fw in ["react", "vue", "svelte", "angular", "solid-js"]:
        if fw in dep_lower or f"@angular/core" in dep_lower:
            info["framework"] = fw
            break

    # Build tool
    for bt in ["vite", "webpack", "parcel", "rollup", "turbo"]:
        if bt in dep_lower:
            info["buildTool"] = bt
            break
    if info["buildTool"] is None and "react-scripts" in dep_lower:
        info["buildTool"] = "create-react-app"
    if info["buildTool"] is None and "next" in dep_lower:
        info["buildTool"] = "next.js"

    # CSS
    for css in ["tailwindcss", "sass", "less", "stylus"]:
        if css in dep_lower:
            info["cssSolution"] = css
            break
    if info["cssSolution"] is None:
        if "styled-components" in dep_lower:
            info["cssSolution"] = "styled-components"
        elif "@emotion/react" in dep_lower:
            info["cssSolution"] = "emotion"
        elif "css-in-js" in dep_lower or "styled-jsx" in dep_lower:
            info["cssSolution"] = "css-in-js"

    # Test
    test_map = {
        "vitest": "vitest", "jest": "jest", "mocha": "mocha",
        "playwright": "playwright", "cypress": "cypress",
        "@testing-library/react": "react-testing-library",
    }
    for pkg, name in test_map.items():
        if pkg in dep_lower:
            if info["testFramework"] is None and name in ("vitest", "jest", "mocha"):
                info["testFramework"] = name
            else:
                info["testLibraries"].append(name)

    # Component library
    for lib in ["shadcn-ui", "@shadcn/ui", "antd", "@mui/material", "@chakra-ui/react",
                "@mantine/core", "radix-ui", "arco-design", "tdesign-react",
                "element-plus", "naive-ui", "@nextui-org/react"]:
        if lib in dep_lower or lib.replace("-", "/") in dep_lower:
            info["componentLibrary"] = lib
            break

    # State management
    for sm in ["zustand", "jotai", "recoil", "valtio", "pinia", "vuex", "redux", "@reduxjs/toolkit"]:
        if sm in dep_lower:
            info["stateManagement"] = sm
            break
    if info["stateManagement"] is None and info["framework"] == "react":
        info["stateManagement"] = "useState/useContext (no external library detected)"

    return info


def scan_directory_structure(root: Path) -> list[str]:
    """Get top-level and key second-level directories under src/."""
    src = root / "src"
    if not src.exists():
        return ["(no src/ directory found)"]

    lines = []
    for item in sorted(src.iterdir()):
        if item.is_dir():
            subdirs = [s.name for s in sorted(item.iterdir()) if s.is_dir()]
            if subdirs:
                lines.append(f"  src/{item.name}/ (contains: {', '.join(subdirs[:8])})")
            else:
                lines.append(f"  src/{item.name}/")
        else:
            lines.append(f"  src/{item.name}")
    return lines


def sample_component_style(root: Path) -> str:
    """Sample a few component files to extract code style patterns."""
    comp_dir = root / "src" / "components"
    if not comp_dir.exists():
        return "(No src/components/ directory to sample)"

    tsx_files = list(comp_dir.rglob("*.tsx")) + list(comp_dir.rglob("*.jsx"))
    if not tsx_files:
        return "(No .tsx/.jsx files found in src/components/)"

    # Sample up to 3 files, preferring smaller ones
    tsx_files.sort(key=lambda p: p.stat().st_size)
    samples = tsx_files[:3]

    observations = []
    for f in samples:
        content = f.read_text(encoding="utf-8", errors="replace")
        lines = content.split("\n")[:25]  # First 25 lines

        obs = {"file": str(f.relative_to(root))}

        # Detect declaration style
        if "export default" in content and "const " in content:
            obs["export"] = "named-const-then-default-export"
        elif "export default function" in content:
            obs["export"] = "default-export-function"
        elif "export function" in content:
            obs["export"] = "named-export-function"
        elif "export const" in content:
            obs["export"] = "named-export-const"

        # Detect type location
        if "interface " in "\n".join(lines) or "type " in "\n".join(lines):
            obs["types"] = "inline-in-component-file"

        # Detect style pattern
        if "import styles from" in content or "import * as styles" in content:
            obs["styles"] = "css-modules"
        elif "className=" in content and "tailwind" not in str(root):
            obs["styles"] = "global-css-or-styled"
        elif "styled." in content or "styled(" in content:
            obs["styles"] = "css-in-js"

        observations.append(obs)

    # Summarize
    patterns = []
    for obs in observations:
        patterns.append(f"  {obs['file']}: export={obs.get('export','?')}, types={obs.get('types','separate-file')}, styles={obs.get('styles','tailwind-or-unknown')}")

    return "\n".join(patterns)


def detect_path_alias(root: Path) -> str | None:
    """Try to detect path alias from tsconfig.json."""
    tsconfig = find_file(root, "tsconfig.json", "jsconfig.json")
    if tsconfig:
        data = read_json(tsconfig)
        paths = data.get("compilerOptions", {}).get("paths", {})
        if paths:
            for alias, targets in paths.items():
                alias_clean = alias.replace("/*", "")
                if alias_clean != "*":
                    return alias_clean
    return None


def detect_router(root: Path) -> str | None:
    """Check if a router library is in use."""
    pkg = find_file(root, "package.json")
    if not pkg:
        return None
    deps = {**read_json(pkg).get("dependencies", {}), **read_json(pkg).get("devDependencies", {})}
    for router in ["react-router-dom", "vue-router", "@angular/router", "@tanstack/react-router"]:
        if router in deps:
            return router
    return None


def generate_context_md(root: Path, tech: dict, structure: list[str],
                        style_sample: str, alias: str | None,
                        router_lib: str | None) -> str:
    """Assemble the project-context.md content."""
    lines = [
        "# 项目上下文扫描",
        "",
        f"扫描时间: {__import__('datetime').datetime.now().isoformat()}",
        f"项目根目录: {root.resolve()}",
        "",
        "## 技术栈",
        "",
        "| 类别 | 检测结果 |",
        "|---|---|",
    ]

    for label, key in [
        ("框架", "framework"),
        ("构建工具", "buildTool"),
        ("TypeScript", "typeScript"),
        ("CSS 方案", "cssSolution"),
        ("组件库", "componentLibrary"),
        ("状态管理", "stateManagement"),
        ("测试框架", "testFramework"),
        ("测试库", "testLibraries"),
    ]:
        val = tech.get(key)
        if isinstance(val, list):
            val = ", ".join(val) if val else "未检测到"
        elif isinstance(val, bool):
            val = "是" if val else "否"
        elif val is None:
            val = "未检测到"
        lines.append(f"| {label} | {val} |")

    if router_lib:
        lines.append(f"| 路由方案 | {router_lib} |")
    if alias:
        lines.append(f"| 路径别名 | {alias} |")

    lines += [
        "",
        "## 目录结构",
        "",
        "```",
        *structure,
        "```",
        "",
        "## 代码风格采样",
        "",
        style_sample,
        "",
        "## 注意事项",
        "",
        "- 以上信息由自动扫描生成。后续所有阶段的代码生成将遵循检测到的技术栈和代码规范。",
        "- 迭代模式下的新代码必须与现有风格保持一致。",
    ]
    return "\n".join(lines)


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    if not root.exists():
        print(f"Error: directory not found: {root}", file=sys.stderr)
        sys.exit(1)

    pkg = find_file(root, "package.json")
    if not pkg:
        print("Error: no package.json found — not a frontend project?", file=sys.stderr)
        sys.exit(1)

    pkg_data = read_json(pkg)
    tech = extract_tech_stack(pkg_data)
    structure = scan_directory_structure(root)
    style_sample = sample_component_style(root)
    alias = detect_path_alias(root)
    router_lib = detect_router(root)

    md = generate_context_md(root, tech, structure, style_sample, alias, router_lib)
    print(md)


if __name__ == "__main__":
    main()
