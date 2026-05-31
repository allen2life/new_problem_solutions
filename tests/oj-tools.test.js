import test from 'node:test';
import assert from 'node:assert/strict';
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
