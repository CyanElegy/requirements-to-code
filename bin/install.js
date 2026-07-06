#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

const SKILL_NAME = 'requirements-to-code';
const TARGET_DIR = path.join(os.homedir(), '.claude', 'skills', SKILL_NAME);

const ASSETS = ['SKILL.md', 'README.md', 'README_CN.md', 'references', 'scripts'];

const args = process.argv.slice(2);
const isForce = args.includes('--force') || args.includes('-f');
const isNonInteractive = !process.stdin.isTTY || args.includes('--yes') || args.includes('-y');

function log(msg) { console.log(`\x1b[36m➜\x1b[0m ${msg}`); }
function success(msg) { console.log(`\x1b[32m✔\x1b[0m ${msg}`); }
function warn(msg) { console.log(`\x1b[33m⚠\x1b[0m ${msg}`); }

function getSourceDir() {
  return path.resolve(__dirname, '..');
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function prompt(question) {
  return new Promise((resolve) => {
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

async function install() {
  const sourceDir = getSourceDir();

  // Guard: don't install from self to self
  if (path.resolve(sourceDir) === path.resolve(TARGET_DIR)) {
    warn(`源目录与目标目录相同 (${TARGET_DIR})，无需安装`);
    log('npx requirement-to-code 已在此目录下运行，skill 已就绪');
    return;
  }

  log(`安装 ${SKILL_NAME} skill 到 ${TARGET_DIR}`);

  // Verify source files exist BEFORE any removal
  for (const asset of ASSETS) {
    const srcPath = path.join(sourceDir, asset);
    if (!fs.existsSync(srcPath)) {
      warn(`找不到源文件: ${srcPath}`);
      process.exit(1);
    }
  }

  // Handle existing installation
  if (fs.existsSync(TARGET_DIR)) {
    if (isForce) {
      log('检测到已有安装，--force 模式：覆盖中...');
    } else if (isNonInteractive) {
      log('检测到已有安装，非交互模式：跳过（使用 --force 强制覆盖）');
      return;
    } else {
      warn('检测到已有安装。');
      const answer = await prompt('  覆盖现有安装? [y/N] ');
      if (answer !== 'y' && answer !== 'yes') {
        log('已取消安装');
        return;
      }
      log('覆盖中...');
    }
    fs.rmSync(TARGET_DIR, { recursive: true, force: true });
  }

  // Create target and copy
  fs.mkdirSync(TARGET_DIR, { recursive: true });
  for (const asset of ASSETS) {
    const srcPath = path.join(sourceDir, asset);
    const destPath = path.join(TARGET_DIR, asset);
    if (fs.statSync(srcPath).isDirectory()) {
      copyDir(srcPath, destPath);
      log(`已复制目录: ${asset}/`);
    } else {
      fs.copyFileSync(srcPath, destPath);
      log(`已复制文件: ${asset}`);
    }
  }

  success(`✅ ${SKILL_NAME} 安装完成！`);
  console.log('');
  console.log('  现在在 Claude Code 中说类似这样的话即可触发：');
  console.log('  "根据这份需求文档，帮我做一个订单管理系统"');
  console.log('');
  console.log('  如需更新：npx requirement-to-code --force');
}

install();
