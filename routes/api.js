import express from 'express';
import MarkdownRenderer from '../lib/markdown.js';
import path from 'path';
import fs from 'fs';
import problemManager from '../lib/instance.js';

const router = express.Router();
const problemdir = path.resolve('problems');

router.get('/', (req, res) => {
  const endpoints = [
    {
      method: 'GET',
      path: '/api/problems',
      desc: '题目列表，支持分页和筛选',
      query: 'page, limit, oj, tag, search',
      example: '/api/problems?page=1&limit=20&oj=poj',
    },
    {
      method: 'GET',
      path: '/api/problems/:oj/:id',
      desc: '单个题目详情（包含渲染后的 HTML）',
      query: '-',
      example: '/api/problems/poj/3061',
    },
    {
      method: 'GET',
      path: '/api/tags',
      desc: '标签列表',
      query: '-',
      example: '/api/tags',
    },
    {
      method: 'GET',
      path: '/api/oj',
      desc: 'OJ 平台列表',
      query: '-',
      example: '/api/oj',
    },
  ];

  res.render('api', {
    title: 'API 文档',
    endpoints,
    baseUrl: `${req.protocol}://${req.get('host')}`,
  });
});

// GET /api/problems - Get problem list with pagination and filters
router.get('/problems', (req, res, next) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const oj = req.query.oj;
    const tag = req.query.tag;
    const search = req.query.search;

    let problems = problemManager.getAll();

    // Apply filters
    if (oj) {
      problems = problemManager.filterByOJ(oj);
    }

    if (tag) {
      problems = problemManager.filterByTag(tag);
    }

    if (search) {
      problems = problemManager.search(search);
    }

    // Apply pagination
    const offset = (page - 1) * limit;
    const total = problems.length;
    const totalPages = Math.ceil(total / limit);
    const data = problems.slice(offset, offset + limit);

    res.json({
      data,
      pagination: {
        total,
        page,
        limit,
        totalPages
      }
    });
  } catch (error) {
    next(error);
  }
});

// GET /api/problems/:oj/:id - Get single problem detail
router.get('/problems/:oj/:id', (req, res, next) => {
  try {
    const { oj, id } = req.params;
    const problem = problemManager.find(oj, id);

    if (!problem) {
      return res.status(404).json({
        error: 'Problem not found',
        oj,
        problem_id: id
      });
    }

    const mdPath = path.join(problemdir, problem.md_path);

    if (!fs.existsSync(mdPath)) {
      return res.status(404).json({
        error: 'Problem markdown file not found',
        md_path: problem.md_path
      });
    }

    const renderer = new MarkdownRenderer(mdPath, problemManager);
    const content = renderer.toJSON();

    res.json({
      oj: problem.oj,
      problem_id: problem.problem_id,
      title: problem.title,
      tags: problem.tags || [],
      md_path: problem.md_path,
      url: problem.url,
      html_content: content.html_content,
      md_content: content.md_content
    });
  } catch (error) {
    next(error);
  }
});

// GET /api/tags - Get all tags
router.get('/tags', (req, res, next) => {
  try {
    const tags = problemManager.getAllTags();
    res.json(tags);
  } catch (error) {
    next(error);
  }
});

// GET /api/oj - Get all OJ platforms
router.get('/oj', (req, res, next) => {
  try {
    const ojs = problemManager.getAllOJs();
    res.json(ojs);
  } catch (error) {
    next(error);
  }
});

export default router;
