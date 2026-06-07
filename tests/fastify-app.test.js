import test from 'node:test';
import assert from 'node:assert/strict';
import { buildApp } from '../app.js';
import ProblemManager from '../lib/problem.js';

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
  assert.match(response.body, /href="https:\/\/github\.com\/rainboyOJ\/rbook_nunjucks\/blob\/main\/problems\/OpenJ_Bailian\/1651\/index\.md"/);
  assert.match(response.body, />GitHub</);
  assert.match(response.body, /prism-tomorrow\.min\.css/);
  assert.match(response.body, /src="\/javascripts\/code-copy\.js"/);
  assert.match(response.body, /class="problem-floating-toolbar"/);
  assert.match(response.body, /data-problem-font="increase"/);
  assert.match(response.body, /data-scroll-top/);
  assert.match(response.body, /src="\/javascripts\/problem-toolbar\.js"/);

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
