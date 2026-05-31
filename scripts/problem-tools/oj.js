#!/usr/bin/env node

import { spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import readline from 'readline';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectDir = path.resolve(__dirname, '../..');
const indexJsPath = path.join(projectDir, 'old_scripts/online_judge/index.js');

function ask(question) {
  if (!process.stdin.isTTY) {
    return Promise.resolve('');
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer);
    });
  });
}

function isYes(answer) {
  return ['y', 'yes', '是', '是的', '好', '下载'].includes(answer.trim().toLowerCase());
}

if (!fs.existsSync(indexJsPath)) {
  console.error(`online judge entry not found: ${indexJsPath}`);
  process.exit(1);
}

const answer = await ask('是否下载对应的题面到 problem.md? [y/N] ');
const args = [...process.argv.slice(2)];

if (isYes(answer)) {
  args.unshift('--download-statement');
}

const result = spawnSync(process.execPath, [indexJsPath, ...args], {
  stdio: 'inherit',
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
