import test from 'node:test';
import assert from 'node:assert/strict';
import MarkdownRenderer from '../lib/markdown.js';
import ProblemManager from '../lib/problem.js';

test('ProblemManager find returns problem by oj/id', () => {
  const pm = new ProblemManager();
  const p = pm.find('poj', '3061');
  assert.ok(p);
  assert.equal(p.oj, 'poj');
  assert.equal(p.problem_id, '3061');
});

test('MarkdownRenderer resolves [[oj/id]] to problem link', () => {
  const pm = new ProblemManager();
  const md = new MarkdownRenderer('', pm);
  md.md_content = 'See [[poj/3061]] now.';
  const html = md.toHTML();
  assert.match(html, /href="\/problems\/poj\/3061"/);
  assert.match(html, /class="problem-link"/);
});

test('MarkdownRenderer renders TOC and KaTeX math', () => {
  const pm = new ProblemManager();
  const md = new MarkdownRenderer('', pm);
  md.md_content = `[[TOC]]

## Section Title

Inline math $a_i + b_i$.

$$
dp[i][j] = a_i + b_j
$$`;

  const html = md.toHTML();
  assert.match(html, /table-of-contents|toc-body/);
  assert.match(html, /Section Title/);
  assert.match(html, /class="katex"/);
  assert.match(html, /class="katex-display"/);
});

test('MarkdownRenderer includes code relative to markdown file', () => {
  const md = new MarkdownRenderer('problems/luogu/9094/index.md');
  const html = md.toHTML();

  assert.doesNotMatch(html, /@include-code/);
  assert.match(html, /line-numbers-mode|language-cpp|language-clike/);
  assert.match(html, /int main/);
  assert.match(html, /std/);
  assert.match(html, /cin/);
  assert.match(html, /<span class="token operator">><\/span><span class="token operator">><\/span>/);
});

test('MarkdownRenderer supports migrated rbook markdown extensions', () => {
  const md = new MarkdownRenderer('problems/OpenJ_Bailian/1651/index.md');
  md.md_content = `[[TOC]]

## Section

!!! warning 注意
body
!!!

::: fold
hidden
:::

::: center
centered
:::

- [x] done

:smile:

![alt](a.png =100x200)

[relative](./other.md)

++ins++ ~~del~~ ==mark== H~2~O x^2^
`;

  const html = md.toHTML();
  assert.match(html, /toc-body/);
  assert.match(html, /class="admonition warning"/);
  assert.match(html, /<details><summary>/);
  assert.match(html, /<div class="center">/);
  assert.match(html, /class="task-list"/);
  assert.match(html, /class="emoji"/);
  assert.match(html, /width="100" height="200"/);
  assert.match(html, /href="\/problems\/OpenJ_Bailian\/1651\/other.html"/);
  assert.match(html, /<ins>ins<\/ins>/);
  assert.match(html, /<s>del<\/s>/);
  assert.match(html, /<mark>mark<\/mark>/);
  assert.match(html, /H<sub>2<\/sub>O/);
  assert.match(html, /x<sup>2<\/sup>/);
});
