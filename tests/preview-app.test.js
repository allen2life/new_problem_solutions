import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs';
import os from 'os';
import path from 'path';

import {
  buildPreviewApp,
  resolvePreviewProblem,
  resolvePreviewProblemOrThrow,
} from '../lib/preview-app.js';

function makeTempRepo() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'rbook-preview-'));
}

function writeProblem(root, dirName = 'P1010') {
  const problemDir = path.join(root, 'problems', 'luogu', dirName);
  fs.mkdirSync(problemDir, { recursive: true });
  fs.writeFileSync(path.join(problemDir, 'main.cpp'), 'int main() { return 0; }\n');
  fs.writeFileSync(path.join(problemDir, 'diagram.png'), 'fake image data\n');
  fs.writeFileSync(path.join(problemDir, 'problem.md'), '# 原题面\n\n这是题面。\n');
  fs.writeFileSync(path.join(problemDir, 'index.md'), [
    '---',
    'title: 测试题',
    'oj: luogu',
    'problem_id: P1010',
    'tags:',
    '  - 测试',
    '---',
    '',
    '# 题解',
    '',
    '![图](./diagram.png)',
    '',
    '```mermaid',
    'flowchart LR',
    '  A --> B',
    '```',
    '',
    '@include-code(./main.cpp, cpp)',
    '',
  ].join('\n'));

  return problemDir;
}

test('resolvePreviewProblem supports luogu numeric id fallback to P-prefixed directory', () => {
  const root = makeTempRepo();
  writeProblem(root, 'P1010');

  const preview = resolvePreviewProblem('luogu', '1010', { projectRoot: root });

  assert.ok(preview);
  assert.equal(preview.problem.problem_id, 'P1010');
  assert.equal(preview.problem.oj, 'luogu');
  assert.ok(preview.aliases.includes('1010'));
  assert.ok(preview.aliases.includes('P1010'));
  assert.equal(preview.problem.md_path, 'luogu/P1010/index.md');
});

test('resolvePreviewProblem prefers the exact luogu directory when it exists', () => {
  const root = makeTempRepo();
  writeProblem(root, '1010');
  writeProblem(root, 'P1010');

  const preview = resolvePreviewProblem('luogu', '1010', { projectRoot: root });

  assert.ok(preview);
  assert.equal(preview.problemDir, path.join(root, 'problems', 'luogu', '1010'));
});

test('preview app renders the problem page, API, and relative assets', async () => {
  const root = makeTempRepo();
  writeProblem(root, 'P1010');
  const preview = resolvePreviewProblem('luogu', '1010', { projectRoot: root });
  const app = await buildPreviewApp(preview, { logger: false });

  const redirect = await app.inject({
    method: 'GET',
    url: '/problems/luogu/1010',
  });
  assert.equal(redirect.statusCode, 302);
  assert.equal(redirect.headers.location, '/problems/luogu/P1010/');

  const page = await app.inject({
    method: 'GET',
    url: '/problems/luogu/P1010/',
  });
  assert.equal(page.statusCode, 200);
  assert.match(page.headers['content-type'], /text\/html/);
  assert.match(page.body, /测试题/);
  assert.match(page.body, /src="\.\/diagram\.png"/);
  assert.match(page.body, /class="mermaid"/);
  assert.match(page.body, /language-cpp/);
  assert.match(page.body, /token function">main/);
  assert.match(page.body, /显示题目/);

  const asset = await app.inject({
    method: 'GET',
    url: '/problems/luogu/P1010/diagram.png',
  });
  assert.equal(asset.statusCode, 200);
  assert.equal(asset.body, 'fake image data\n');

  const api = await app.inject({
    method: 'GET',
    url: '/api/problems/luogu/P1010',
  });
  assert.equal(api.statusCode, 200);
  assert.equal(api.json().problem_id, 'P1010');
  assert.match(api.json().html_content, /language-cpp/);
  assert.match(api.json().html_content, /token function">main/);

  await app.close();
});

test('resolvePreviewProblemOrThrow reports candidate paths for missing problem', () => {
  const root = makeTempRepo();

  assert.throws(
    () => resolvePreviewProblemOrThrow('luogu', '1010', { projectRoot: root }),
    (error) => {
      assert.equal(error.code, 'PREVIEW_PROBLEM_NOT_FOUND');
      assert.deepEqual(error.tried, [
        'problems/luogu/1010/index.md',
        'problems/luogu/P1010/index.md',
      ]);
      return true;
    },
  );
});
