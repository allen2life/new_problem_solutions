import test from 'node:test';
import assert from 'node:assert/strict';
import MarkdownRenderer from '../lib/markdown.js';
import ProblemManager from '../lib/problem.js';

test('ProblemManager find returns problem by oj/id', () => {
  const pm = new ProblemManager();
  const p = pm.find('OpenJ_Bailian', '1651');
  assert.ok(p);
  assert.equal(p.oj, 'OpenJ_Bailian');
  assert.equal(p.problem_id, '1651');
  assert.equal(p.md_path, 'OpenJ_Bailian/1651/index.md');
});

test('ProblemManager lists newest problems first', () => {
  const pm = new ProblemManager();
  const problems = pm.getAll();

  for (let i = 1; i < problems.length; i += 1) {
    assert.ok((problems[i - 1].dateA || 0) >= (problems[i].dateA || 0));
  }
});

test('ProblemManager builds GitHub URLs from config.yml', () => {
  const pm = new ProblemManager({ auto_load: false });

  assert.equal(pm.config.github_repository, 'https://github.com/rainboyOJ/rbook_nunjucks');
  assert.equal(
    pm.github_url('luogu/5657/index.md'),
    'https://github.com/rainboyOJ/rbook_nunjucks/blob/main/problems/luogu/5657/index.md',
  );
});

test('MarkdownRenderer resolves [[oj/id]] to problem link', () => {
  const pm = new ProblemManager();
  const md = new MarkdownRenderer('', pm);
  md.md_content = 'See [[OpenJ_Bailian/1651]] now.';
  const html = md.toHTML();
  assert.match(html, /href="\/problems\/OpenJ_Bailian\/1651"/);
  assert.match(html, /class="problem-link"/);
});

test('ProblemManager scans only formal index.md problem pages', () => {
  const pm = new ProblemManager({ auto_load: false });
  const files = pm.scanProblems();

  assert.ok(files.length > 0);
  assert.ok(files.every((file) => file.endsWith('/index.md')));
  assert.ok(files.every((file) => !file.includes('problem-analysis-workspace/')));
  assert.ok(files.every((file) => !file.includes('duipai-failed/')));
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
