import test from 'node:test';
import assert from 'node:assert/strict';
import { buildApp } from '../app.js';
import ProblemManager from '../lib/problem.js';
import problemManagerInstance from '../lib/instance.js';

test('Fastify app renders the index page', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /text\/html/);
  assert.match(response.body, /题目列表/);
  assert.match(response.body, /<table/);
  assert.match(response.body, /原题/);
  assert.match(response.body, /最后更新/);
  assert.match(response.body, /难度/);
  assert.doesNotMatch(response.body, /problem-floating-toolbar/);

  await app.close();
});

test('Fastify app returns paginated problem JSON', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/api/problems?limit=2',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /application\/json/);

  const body = response.json();
  const expectedProblems = new ProblemManager().getAll().slice(0, 2);

  assert.equal(body.data.length, 2);
  assert.equal(body.pagination.limit, 2);
  assert.deepEqual(
    body.data.map((p) => `${p.oj}/${p.problem_id}`),
    expectedProblems.map((p) => `${p.oj}/${p.problem_id}`),
  );

  await app.close();
});

test('Fastify app returns a problem detail page', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/problems/OpenJ_Bailian/1651',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /text\/html/);
  assert.match(response.body, /1651/);
  assert.match(response.body, /href="https:\/\/github\.com\/RainboyOJ\/new_problem_solutions\/blob\/master\/problems\/OpenJ_Bailian\/1651\/index\.md"/);
  assert.match(response.body, />GitHub</);
  assert.match(response.body, /prism-tomorrow\.min\.css/);
  assert.match(response.body, /src="\/javascripts\/code-copy\.js"/);
  assert.match(response.body, /class="problem-floating-toolbar"/);
  assert.match(response.body, /data-problem-font="increase"/);
  assert.match(response.body, /data-scroll-top/);
  assert.match(response.body, /mermaid@11\/dist\/mermaid\.min\.js/);
  assert.match(response.body, /src="\/javascripts\/problem-toolbar\.js"/);
  assert.match(response.body, /src="\/javascripts\/problem-mermaid\.js"/);
  assert.match(response.body, /href="\/relations\?oj=OpenJ_Bailian&amp;pid=1651"/);
  assert.match(response.body, /难度:/);
  assert.match(response.body, /problem-difficulty-badge/);
  assert.match(response.body, />无题目</);
  assert.match(response.body, /disabled/);
  assert.doesNotMatch(response.body, /problemStatementModal/);

  await app.close();
});

test('Fastify app renders problem statement modal when problem.md exists', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/problems/luogu/P1968',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /text\/html/);
  assert.match(response.body, />显示题目</);
  assert.match(response.body, /data-bs-target="#problemStatementModal"/);
  assert.match(response.body, /id="problemStatementModal"/);
  assert.match(response.body, /modal-xl/);
  assert.match(response.body, /modal-dialog-scrollable/);
  assert.match(response.body, /luogu P1968 - 题目/);
  assert.match(response.body, /题目描述/);
  assert.match(response.body, /输入输出样例/);
  assert.match(response.body, /class="katex"/);
  assert.doesNotMatch(response.body, />无题目</);

  await app.close();
});

test('Fastify app renders the relation graph page', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/relations',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /text\/html/);
  assert.match(response.body, /题目关系图/);
  assert.match(response.body, /id="relations-graph-root"/);
  assert.match(response.body, /href="\/relations-graph\/assets\/index\.css"/);
  assert.match(response.body, /src="\/relations-graph\/assets\/index\.js"/);
  assert.doesNotMatch(response.body, /cytoscape@3/);
  assert.doesNotMatch(response.body, /problem-relations-graph\.js/);

  await app.close();
});

test('Fastify app returns relation graph JSON', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/api/relations',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.headers['content-type'], /application\/json/);

  const body = response.json();
  assert.ok(Array.isArray(body.nodes));
  assert.ok(Array.isArray(body.edges));
  assert.ok(body.summary.nodes > 0);
  assert.ok(body.nodes.every((node) => typeof node.difficulty === 'string'));
  assert.ok(body.edges.some((edge) => edge.type === 'pre' || edge.type === 'common'));

  await app.close();
});

test('Fastify app returns problem description in detail API', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/api/problems/OpenJ_Bailian/1651',
  });

  assert.equal(response.statusCode, 200);
  assert.equal(typeof response.json().description, 'string');

  await app.close();
});

test('Fastify app renders TOC and KaTeX on markdown problem pages', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/problems/OpenJ_Bailian/1651',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.body, /table-of-contents|toc-body/);
  assert.match(response.body, /class="katex"/);
  assert.match(response.body, /class="katex-display"/);

  await app.close();
});

test('Fastify app renders problem relation lists on detail pages', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/problems/luogu/P3387',
  });

  assert.equal(response.statusCode, 200);
  assert.match(response.body, /前置题目/);
  assert.match(response.body, /后置题目/);
  assert.match(response.body, /HDU 1269/);
  assert.match(response.body, /P2746/);
  assert.match(response.body, /P2272/);

  await app.close();
});

test('Fastify app renders external problem recommendations on detail pages', async () => {
  const problem = problemManagerInstance.find('OpenJ_Bailian', '1651');
  const originalRecommend = problem.recommend;
  problem.recommend = [
    {
      oj: 'leetcode',
      problem_id: '62',
      title: 'Unique Paths',
      url: 'https://leetcode.com/problems/unique-paths/',
      reason: '同样是基础网格路径计数 DP。',
      relation: 'similar',
    },
  ];

  const app = await buildApp({ logger: false });

  try {
    const response = await app.inject({
      method: 'GET',
      url: '/problems/OpenJ_Bailian/1651',
    });

    assert.equal(response.statusCode, 200);
    assert.match(response.body, /推荐练习/);
    assert.match(response.body, /leetcode 62/);
    assert.match(response.body, /Unique Paths/);
    assert.match(response.body, /target="_blank"/);
    assert.match(response.body, /similar/);
    assert.match(response.body, /is-recommend-similar/);
  } finally {
    problem.recommend = originalRecommend;
    await app.close();
  }
});

test('Fastify app returns JSON 404s under /api', async () => {
  const app = await buildApp({ logger: false });

  const response = await app.inject({
    method: 'GET',
    url: '/api/not-found',
  });

  assert.equal(response.statusCode, 404);
  assert.match(response.headers['content-type'], /application\/json/);
  assert.equal(response.json().error, 'Not found');

  await app.close();
});
