import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import * as matter from 'gray-matter';

const __workdir = path.resolve();
const __problemdir = path.join(__workdir, 'problems');
const __problemJsonPath = path.join(__workdir, 'problems.json');

class ProblemManager {
  constructor(opts = { auto_load: true }) {
    this.name = 'problems';
    this.problem_files = [];
    this.problems = [];
    this.problemMap = new Map();
    this.config = null;

    if (opts.auto_load) {
      this.load_problems();
    }

    this.config = this.load_config();
  }

  load_config(configPath = 'config.yml') {
    try {
      let configFile = path.join(__workdir, configPath);
      if (!fs.existsSync(configFile) && configPath === 'config.yml') {
        configFile = path.join(__workdir, 'book.yaml');
      }

      if (!fs.existsSync(configFile)) {
        return {};
      }

      const content = fs.readFileSync(configFile, 'utf8');
      return yaml.load(content) || {};
    } catch (error) {
      console.warn(`加载配置文件失败: ${error.message}`);
      return {};
    }
  }

  save_problems() {
    fs.writeFileSync(__problemJsonPath, JSON.stringify(this.problems, null, 2));
  }

  load_problems() {
    if (!fs.existsSync(__problemJsonPath)) {
      this.init();
      this.save_problems();
      return;
    }

    try {
      this.problems = JSON.parse(fs.readFileSync(__problemJsonPath, 'utf8'));
      this.sortProblems();
      this.buildIndex();
    } catch (error) {
      console.warn(`加载缓存失败: ${error.message}, 重新扫描`);
      this.init();
      this.save_problems();
    }
  }

  buildIndex() {
    this.problemMap.clear();
    for (const p of this.problems) {
      this.problemMap.set(`${p.oj}/${p.problem_id}`, p);
    }
  }

  sortProblems() {
    this.problems.sort((a, b) => {
      const dateDiff = (b.dateA || 0) - (a.dateA || 0);
      if (dateDiff !== 0) {
        return dateDiff;
      }

      const aKey = `${a.oj || ''}/${a.problem_id || ''}/${a.md_path || ''}`;
      const bKey = `${b.oj || ''}/${b.problem_id || ''}/${b.md_path || ''}`;
      return aKey.localeCompare(bKey);
    });
  }

  find(oj, problem_id) {
    return this.problemMap.get(`${oj}/${problem_id}`);
  }

  problem_url(oj, id) {
    return `/problems/${oj}/${id}`;
  }

  github_url(mdPath) {
    const repository = this.config?.github_repository || this.config?.github?.repository;
    if (!repository || !mdPath) {
      return '';
    }

    const branch = this.config?.github_branch || this.config?.github?.branch || 'main';
    const normalizedRepo = repository.replace(/\/+$/, '');
    const normalizedPath = path.posix
      .normalize(`problems/${mdPath}`)
      .split('/')
      .map((segment) => encodeURIComponent(segment))
      .join('/');

    return `${normalizedRepo}/blob/${encodeURIComponent(branch)}/${normalizedPath}`;
  }

  front_matter(md_path) {
    const raw_md = fs.readFileSync(md_path, 'utf8');
    return matter.default(raw_md).data;
  }

  md_path_to_url(md_path) {
    if (!md_path || md_path.length === 0) {
      throw new Error('md_path is empty');
    }

    const prob_front = this.front_matter(md_path);
    if (!prob_front.oj || !prob_front.problem_id) {
      throw new Error(`md_path: ${md_path} front_matter.oj or front_matter.problem_id is empty`);
    }

    return this.problem_url(prob_front.oj, prob_front.problem_id);
  }

  scanProblems() {
    const files = [];
    const ignoredDirs = new Set(['problem-analysis-workspace', 'duipai-failed']);

    const walkDir = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (ignoredDirs.has(entry.name)) {
            continue;
          }
          walkDir(fullPath);
        } else if (entry.isFile() && entry.name === 'index.md') {
          files.push(path.relative(__problemdir, fullPath));
        }
      }
    };

    walkDir(__problemdir);
    return files;
  }

  init() {
    const files = this.scanProblems();
    this.problem_files = files;
    this.problems = [];

    for (const md of files) {
      const md_path = path.join(__problemdir, md);
      const prob_front = this.front_matter(md_path);

      if (!prob_front) {
        console.log(`md_path: ${md_path} front_matter is empty`);
        continue;
      }

      if (!prob_front.oj || !prob_front.problem_id) {
        console.log(`md_path: ${md_path} front_matter.oj or front_matter.problem_id is empty`);
        continue;
      }

      this.problems.push({
        ...prob_front,
        md_path: md,
        url: this.problem_url(prob_front.oj, prob_front.problem_id),
        dateA: prob_front.date ? new Date(prob_front.date).getTime() : 0,
      });
    }

    this.sortProblems();
    this.buildIndex();
  }

  getAll() {
    return this.problems;
  }

  filterByTag(tag) {
    return this.problems.filter((p) => p.tags && p.tags.includes(tag));
  }

  filterByOJ(oj) {
    return this.problems.filter((p) => p.oj === oj);
  }

  search(keyword) {
    const lowerKeyword = keyword.toLowerCase();
    return this.problems.filter((p) => {
      const title = (p.title || '').toLowerCase();
      const problem_id = (p.problem_id || '').toLowerCase();
      return title.includes(lowerKeyword) || problem_id.includes(lowerKeyword);
    });
  }

  paginate(page = 1, limit = 20) {
    const offset = (page - 1) * limit;
    const total = this.problems.length;
    const totalPages = Math.ceil(total / limit);
    const data = this.problems.slice(offset, offset + limit);

    return {
      data,
      pagination: {
        total,
        page,
        limit,
        totalPages,
      },
    };
  }

  getAllTags() {
    const tagSet = new Set();
    for (const p of this.problems) {
      if (!p.tags) {
        continue;
      }
      for (const tag of p.tags) {
        tagSet.add(tag);
      }
    }
    return Array.from(tagSet).sort();
  }

  getAllOJs() {
    const ojSet = new Set();
    for (const p of this.problems) {
      if (p.oj) {
        ojSet.add(p.oj);
      }
    }
    return Array.from(ojSet).sort();
  }
}

export default ProblemManager;
