import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync, spawnSync } from 'node:child_process';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import LUOGU from '../old_scripts/online_judge/luogu.js';

test('Luogu downloader renders problem.md content', () => {
  const luogu = new LUOGU();
  const markdown = luogu.problem_statement_markdown(
    {
      title: 'Test Problem',
      description: 'problem description',
      input: 'input format',
      output: 'output format',
      samples: [{ input: '1 2', output: '3' }],
      hint: 'hint text',
    },
    'P9999',
  );

  assert.match(markdown, /^# P9999 Test Problem/);
  assert.match(markdown, /## 题目描述\n\nproblem description/);
  assert.match(markdown, /## 输入格式\n\ninput format/);
  assert.match(markdown, /## 输出格式\n\noutput format/);
  assert.match(markdown, /## 输入输出样例 #1/);
  assert.match(markdown, /```\n1 2\n```/);
  assert.match(markdown, /```\n3\n```/);
  assert.match(markdown, /## 说明\/提示\n\nhint text/);
});

function runTreeDraw(args, input = '') {
  return execFileSync(
    'python3',
    ['scripts/problem-analysis-tools/tree_draw.py', ...args],
    {
      cwd: process.cwd(),
      input,
      encoding: 'utf8',
    },
  );
}

test('tree_draw renders normal tree SVG from edge list', () => {
  const dir = mkdtempSync(join(tmpdir(), 'tree-draw-'));
  const output = join(dir, 'normal.svg');
  const stdout = runTreeDraw(['--type', 'normal', '-o', output, '--markdown'], [
    '5',
    '1 2',
    '1 3',
    '2 4',
    '2 5',
    '',
  ].join('\n'));
  const svg = readFileSync(output, 'utf8');

  assert.match(stdout, /!\[树形结构示意图\]\(\.\/normal\.svg\)/);
  assert.match(svg, /<svg /);
  assert.match(svg, /data-id="1"/);
  assert.match(svg, /data-id="5"/);
  assert.match(svg, /<line x1=/);
});

test('tree_draw renders binary tree child table with edge labels', () => {
  const dir = mkdtempSync(join(tmpdir(), 'tree-draw-'));
  const input = join(dir, 'binary.txt');
  const output = join(dir, 'binary.svg');
  writeFileSync(input, [
    '5',
    '1 2 3',
    '2 4 5',
    '3 0 0',
    '4 0 0',
    '5 0 0',
    '',
  ].join('\n'));

  runTreeDraw(['--type', 'binary', '--input', input, '--output', output]);
  const svg = readFileSync(output, 'utf8');

  assert.match(svg, />L<\/text>/);
  assert.match(svg, />R<\/text>/);
  assert.match(svg, /data-id="4"/);
});

test('tree_draw renders JSON tree with node style overrides', () => {
  const dir = mkdtempSync(join(tmpdir(), 'tree-draw-'));
  const output = join(dir, 'json.svg');
  const data = JSON.stringify({
    type: 'binary',
    root: 'a',
    nodes: [
      { id: 'a', label: '8', left: 'b', right: 'c', style: { fill: '#fee2e2' } },
      { id: 'b', label: '3' },
      { id: 'c', label: '10' },
    ],
  });

  runTreeDraw(['--type', 'json', '--output', output], data);
  const svg = readFileSync(output, 'utf8');

  assert.match(svg, /data-id="a"/);
  assert.match(svg, />8<\/text>/);
  assert.match(svg, /fill="#fee2e2"/);
});

test('tree_draw renders segment tree preset', () => {
  const dir = mkdtempSync(join(tmpdir(), 'tree-draw-'));
  const output = join(dir, 'segment.svg');

  runTreeDraw(['--type', 'segment', '--size', '4', '--output', output]);
  const svg = readFileSync(output, 'utf8');

  assert.match(svg, />\[1,4\]<\/text>/);
  assert.match(svg, />\[1,2\]<\/text>/);
  assert.match(svg, /<rect /);
});

test('ptool can locate tree_draw help', () => {
  const stdout = execFileSync(
    'scripts/navi/ptool',
    ['tree_draw', '--help'],
    { cwd: process.cwd(), encoding: 'utf8' },
  );

  assert.match(stdout, /使用 Walker 风格布局绘制树结构 SVG/);
});

function writeProblemFixture(dir, frontmatterLines) {
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'main.cpp'), 'int main() { return 0; }\n');
  writeFileSync(join(dir, 'index.md'), [
    '---',
    ...frontmatterLines,
    '---',
    '',
    '[[TOC]]',
    '',
    '### 题意',
    '',
    '### 思路',
    '',
    '### 代码',
    '',
    '@include-code(./main.cpp, cpp)',
    '',
    '### 复杂度',
    '',
    '### 总结',
    '',
  ].join('\n'));
}

test('check_problem requires description and warns when it is empty', () => {
  const fixtureRoot = join(process.cwd(), 'problems', '__tmp_check_description__');
  const problemDir = join(fixtureRoot, 'P1');
  const baseFrontmatter = [
    'oj: "luogu"',
    'problem_id: "P1"',
    'title: "Test"',
    'date: 2026-06-13 10:00',
    'toc: true',
    'tags: []',
    'categories: []',
    'source:',
  ];

  try {
    rmSync(fixtureRoot, { recursive: true, force: true });
    writeProblemFixture(problemDir, baseFrontmatter);
    const missing = spawnSync(
      'python3',
      ['scripts/problem-analysis-tools/check_problem.py', problemDir],
      { cwd: process.cwd(), encoding: 'utf8' },
    );
    assert.equal(missing.status, 1);
    assert.match(missing.stdout, /frontmatter 缺少字段：description/);

    writeProblemFixture(problemDir, [
      ...baseFrontmatter.slice(0, 3),
      'description: ""',
      ...baseFrontmatter.slice(3),
    ]);
    const empty = spawnSync(
      'python3',
      ['scripts/problem-analysis-tools/check_problem.py', problemDir],
      { cwd: process.cwd(), encoding: 'utf8' },
    );
    assert.equal(empty.status, 0);
    assert.match(empty.stdout, /frontmatter description 为空/);
  } finally {
    rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('new-problem scaffold includes description and recommend frontmatter fields', () => {
  const fixtureRoot = join(process.cwd(), 'problems', '__tmp_new_problem_description__');
  const problemDir = join(fixtureRoot, 'P1');

  try {
    rmSync(fixtureRoot, { recursive: true, force: true });
    const result = spawnSync(
      'python3',
      [
        'scripts/problem-analysis-tools/new-problem.py',
        '__tmp_new_problem_description__',
        'P1',
        '--title',
        'Test',
      ],
      { cwd: process.cwd(), encoding: 'utf8' },
    );

    assert.equal(result.status, 0);
    const indexMd = readFileSync(join(problemDir, 'index.md'), 'utf8');
    assert.match(indexMd, /title: "Test"\ndescription: ""\ndate:/);
    assert.match(indexMd, /categories: \[\]\npre: \[\]\ncommon: \[\]\nrecommend: \[\]\nsource:/);
  } finally {
    rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('fetch_problem self-test creates index description field', () => {
  const result = spawnSync(
    'python3',
    ['scripts/problem-analysis-tools/fetch_problem.py', '--self-test'],
    { cwd: process.cwd(), encoding: 'utf8' },
  );

  assert.equal(result.status, 0);
  assert.match(result.stdout, /self-test passed/);
});

test('check_relations validates external recommend items', () => {
  const fixtureRoot = join(process.cwd(), 'problems', '__tmp_check_recommend__');
  const problemDir = join(fixtureRoot, 'P1');

  try {
    rmSync(fixtureRoot, { recursive: true, force: true });
    writeProblemFixture(problemDir, [
      'oj: "__tmp_check_recommend__"',
      'problem_id: "P1"',
      'title: "Test"',
      'description: "测试推荐练习字段。"',
      'date: 2026-06-13 10:00',
      'toc: true',
      'tags: []',
      'categories: []',
      'pre: []',
      'common: []',
      'recommend:',
      '  - oj: "leetcode"',
      '    problem_id: "62"',
      '    title: "Unique Paths"',
      '    url: "https://leetcode.com/problems/unique-paths/"',
      '    reason: "同样是基础网格路径计数 DP。"',
      '    relation: "similar"',
      'source:',
    ]);

    const ok = spawnSync(
      'python3',
      ['scripts/problem-analysis-tools/check_relations.py', problemDir],
      { cwd: process.cwd(), encoding: 'utf8' },
    );
    assert.equal(ok.status, 0);
    assert.match(ok.stdout, /通过：关系字段符合当前规范。/);

    writeProblemFixture(problemDir, [
      'oj: "__tmp_check_recommend__"',
      'problem_id: "P1"',
      'title: "Test"',
      'description: "测试推荐练习字段。"',
      'date: 2026-06-13 10:00',
      'toc: true',
      'tags: []',
      'categories: []',
      'pre: []',
      'common: []',
      'recommend:',
      '  - oj: "leetcode"',
      '    problem_id: "62"',
      '    reason: "同样是基础网格路径计数 DP。"',
      '    relation: "unknown"',
      'source:',
    ]);

    const bad = spawnSync(
      'python3',
      ['scripts/problem-analysis-tools/check_relations.py', problemDir],
      { cwd: process.cwd(), encoding: 'utf8' },
    );
    assert.equal(bad.status, 1);
    assert.match(bad.stdout, /relation=`unknown` 不合法/);
    assert.match(bad.stdout, /缺少 `url`/);
  } finally {
    rmSync(fixtureRoot, { recursive: true, force: true });
  }
});

test('navi fetch-url prompts for URL instead of using a fixed default', () => {
  const cheat = readFileSync('scripts/navi/problem-tools.cheat', 'utf8');
  const lines = cheat.split('\n');
  const start = lines.findIndex((line) => line === '% fetch-url');
  const end = lines.findIndex((line, index) => index > start && line.startsWith('% '));
  const block = lines.slice(start, end === -1 ? undefined : end).join('\n');

  assert.notEqual(start, -1);
  assert.match(block, /fetch_problem <problem_url>/);
  assert.doesNotMatch(block, /^\$ problem_url:/m);
});
