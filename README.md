# rbook 题目库项目

这是一个基于 Fastify 的题目库网站，题目来源于 `problems/` 目录中的 Markdown 文件。项目同时提供：

- 网页浏览与检索（Pug + Bootstrap）
- RESTful API（供程序和 AI 调用）
- MCP 网关（`./mcp`，用于 AI 工具化调用）

## 1. 功能概览

- Markdown 题目渲染（Front Matter + 正文）
- 题目列表分页、OJ/标签筛选、搜索
- 题目详情页渲染
- API 接口：
  - `GET /api/problems`
  - `GET /api/problems/:oj/:id`
  - `GET /api/tags`
  - `GET /api/oj`
  - `GET /api`（API 文档页）
- 双链解析：`[[oj/problem_id]]`

## 2. 环境要求

- Node.js 18+
- npm
- Docker 24+（可选，用 Docker 部署时需要）
- Docker Compose 插件（可选，用 `docker compose` 部署时需要）

## 3. 启动网站服务

在项目根目录执行：

```bash
npm install
npm start
```

默认访问地址：

- 网站首页：`http://127.0.0.1:3000/`
- API 文档：`http://127.0.0.1:3000/api`

## 4. 使用 Docker 安装与启动

项目已经提供 `Dockerfile` 和 `docker-compose.yml`。Docker 镜像启动时会执行 `npm start`，并自动扫描 `problems/` 生成 `problems.json`。

Docker 镜像会由 GitHub Actions 推送到 GHCR：

```text
ghcr.io/rainboyoj/new_problem_solutions:master
```

国内 VPS 如果拉取 `ghcr.io` 较慢，可以优先使用下面两个加速地址：

```text
ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master
gh-proxy.org/docker/ghcr.io/rainboyoj/new_problem_solutions:master
```

### 4.1 从 GHCR 拉取镜像

推荐顺序是先拉国内加速镜像，失败后再试原始 GHCR：

```bash
docker pull ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master
docker tag ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master problems-solution:deploy
```

如果 `ghcr.nju.edu.cn` 不可用，再试：

```bash
docker pull gh-proxy.org/docker/ghcr.io/rainboyoj/new_problem_solutions:master
docker tag gh-proxy.org/docker/ghcr.io/rainboyoj/new_problem_solutions:master problems-solution:deploy
```

最后 fallback 到原始 GHCR：

```bash
docker pull ghcr.io/rainboyoj/new_problem_solutions:master
docker tag ghcr.io/rainboyoj/new_problem_solutions:master problems-solution:deploy
```

如果 GHCR package 不是 Public，需要先登录：

```bash
docker login ghcr.io -u YOUR_GITHUB_USERNAME
```

密码使用 GitHub Personal Access Token，至少需要 `read:packages` 权限。

### 4.2 本地构建镜像

在项目根目录执行：

```bash
docker build -t problems-solution:deploy .
```

### 4.3 使用 Docker Compose 启动

```bash
docker compose up -d
```

默认配置会把本机 `./problems` 只读挂载到容器的 `/app/problems`，并把容器 `3000` 端口映射到本机 `127.0.0.1:3300`。

访问地址：

- 网站首页：`http://127.0.0.1:3300/`
- API 文档：`http://127.0.0.1:3300/api`

查看运行状态和日志：

```bash
docker compose ps
docker compose logs -f problems-solution
```

停止服务：

```bash
docker compose down
```

也可以不重新 tag，直接指定镜像地址启动：

```bash
IMAGE_REF=ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master docker compose up -d
```

### 4.4 不使用 Compose 直接运行

```bash
docker run --rm \
  -p 3000:3000 \
  -v "$PWD/problems:/app/problems:ro" \
  problems-solution:deploy
```

直接运行时访问：`http://127.0.0.1:3000/`

### 4.5 更新部署

使用 GHCR 镜像部署时，拉取新镜像后重启：

```bash
docker pull ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master
docker tag ghcr.nju.edu.cn/rainboyoj/new_problem_solutions:master problems-solution:deploy
docker compose up -d
```

本地构建部署时，代码或题目数据更新后重新构建并启动：

```bash
git pull
docker build -t problems-solution:deploy .
docker compose up -d
```

## 5. 使用 MCP（给 AI 调用）

MCP 服务位于 `./mcp`，它会调用上面的主站 API。

### 5.1 安装与启动

```bash
cd mcp
npm install
TARGET_API_BASE_URL=http://127.0.0.1:3000 npm start
```

默认监听：`http://127.0.0.1:3333`

### 5.2 MCP 提供的核心工具

- `search_problems`
- `get_problem_detail`

详细说明见：`mcp/README.md`

## 6. 项目结构

```text
.
├── app.js                 # Fastify 应用构建入口
├── bin/www                # 网站启动脚本
├── lib/                   # 核心模块（题目管理、markdown 渲染等）
├── routes/                # 页面路由与 API 路由
├── views/                 # Pug 模板
├── public/                # 静态资源
├── problems/              # 题目 Markdown 数据（本地数据源）
├── scripts/problem-tools/ # 写题辅助脚本
├── mcp/                   # MCP 网关服务
└── docs/                  # 设计与计划文档
```

## 7. 常用命令

### 根项目

```bash
npm test
npm start
```

源码阅读路径见：`docs/source-guide.md`

VPS + GitHub 自动部署教程见：`docs/deployment/vps-github-auto-deploy.md`

写题辅助脚本安装与使用见：`docs/problem-tools.md`

### MCP 子项目

```bash
cd mcp
npm test
npm start
npm run start:stdio
```

## 8. 开发说明

- 题目数据来自 `problems/`，启动时会扫描并用于检索。
- 如需扩展 AI 能力，优先在 `mcp/src/tools/` 下新增工具。
- API 变更后，请同步更新：
  - `views/api.pug`
  - `mcp/README.md`
