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

## 6. 题目解析工作流（给 AI 与手写题解使用）

本仓库提供两类本地 skill：

- `oj-problem-format-spec`：只规定题解 Markdown 的格式、目录结构、frontmatter、章节标题和代码嵌入方式。
- `oj-problem-analysis-writer`：负责写题目解析内容，完成辅助理解和对拍的 `brute.cpp`，并根据过程文档生成正式 `index.md`。

两个 skill 位于：

```text
.agents/skills/oj-problem-format-spec/SKILL.md
.agents/skills/oj-problem-analysis-writer/SKILL.md
```

### 6.1 标准题目目录

新题目只使用目录型结构：

```text
problems/<oj>/<problem_id>/
├── index.md
├── main.cpp
├── brute.cpp
├── gen.py
└── problem-analysis-workspace/
    ├── 01-problem-understanding.md
    ├── 02-observation-and-model.md
    ├── 03-solution-derivation.md
    ├── 04-correctness-and-edge-cases.md
    ├── 05-complexity-and-implementation.md
    ├── 06-final-index-draft.md
    └── duipai-report.md
```

正式电子书内容写入 `index.md`。`### 思路` 中引用 `brute.cpp` 帮助读者理解朴素做法：

```markdown
@include-code(./brute.cpp, cpp)
```

正式提交代码固定为 `main.cpp`，并在 `### 代码` 中使用：

```markdown
@include-code(./main.cpp, cpp)
```

`problem-analysis-workspace/` 是每道题的学习和推导过程目录，已通过 `.gitignore` 忽略，不作为最终电子书内容提交。

### 6.2 使用 skill 写题解

推荐流程：

1. 在 `problems/<oj>/<problem_id>/` 下准备 `main.cpp`。
2. 使用 `oj-problem-analysis-writer` 完成或修正 `brute.cpp`。
3. 让 AI 使用 `oj-problem-analysis-writer` 生成或补全 `problem-analysis-workspace/*.md`。
4. AI 根据 `06-final-index-draft.md` 和 `oj-problem-format-spec` 写入正式 `index.md`。
5. 如果要对拍，再准备或补全 `gen.py` 并运行对拍脚本。
6. 人工检查 `index.md` 的题意、思路、复杂度和代码引用。

示例提示：

```text
使用 oj-problem-analysis-writer，解析 problems/luogu/1001/
根据 main.cpp 和过程文档生成 index.md
```

如果只需要创建或修正格式骨架，使用：

```text
使用 oj-problem-format-spec，规范 problems/luogu/1001/index.md
```

### 6.3 随机数据、样例检查与对拍脚本

通用脚本放在：

```text
scripts/problem-analysis-tools/
```

随机数据生成：

```bash
python3 scripts/problem-analysis-tools/gen_random.py --pattern array -n 10 --min 1 --max 100
python3 scripts/problem-analysis-tools/gen_random.py --pattern tree -n 20
python3 scripts/problem-analysis-tools/gen_random.py --pattern graph -n 10 -m 15
python3 scripts/problem-analysis-tools/gen_random.py --pattern string -n 12 --charset abc
python3 scripts/problem-analysis-tools/gen_random.py --pattern permutation -n 10
```

对拍（给 Agent 和自动化使用，纯命令行）：

```bash
python3 scripts/problem-analysis-tools/duipai.py \
  --gen problems/luogu/1001/gen.py \
  --user problems/luogu/1001/main.cpp \
  --brute problems/luogu/1001/brute.cpp \
  -n 200
```

人工交互式对拍：

```bash
cd problems/luogu/1001
python3 ../../../scripts/problem-analysis-tools/duipai-human.py
```

样例运行器：

```bash
cd problems/luogu/1001
python3 ../../../scripts/problem-analysis-tools/check_sample.py
```

也可以从项目根目录指定题目目录：

```bash
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001 --source main.cpp --timeout 2
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001 --timeout 1 --memory-mb 256
```

`check_sample.py` 会自动查找 `main.cpp`，没有时回退到 `1.cpp`。它会识别 `in/out`、`in1/out1`、`data/*.in` 与同名 `.out/.ans`；如果只有输入没有答案，会运行并标记为 `NO_ANSWER`。`--timeout` 控制时间限制，`--memory-mb` 控制内存判定线，内部默认额外给 16MB 保护余量。

对拍失败时会保存：

```text
problems/<oj>/<problem_id>/duipai-failed/
```

对拍记录默认写入：

```text
problems/<oj>/<problem_id>/problem-analysis-workspace/duipai-report.md
```

这些过程目录和失败样例目录已加入 `.gitignore`。

## 7. 工具使用

所有用户可直接运行的工具都支持：

```bash
<tool> --help
```

内部支撑库 `scripts/problem-tools/mylib/` 不作为用户命令使用。

也可以用 navi 作为交互式 cheatsheet：

```bash
navi --path scripts/navi
```

推荐配置一个 alias，让 navi 默认使用本仓库的 cheatsheet：

```bash
alias rbook-navi='command navi --path /home/rainboy/mycode/抽离rbook中的题目/scripts/navi'
```

把它写入 `~/.zshrc`：

```bash
echo "alias rbook-navi='command navi --path /home/rainboy/mycode/抽离rbook中的题目/scripts/navi'" >> ~/.zshrc
source ~/.zshrc
```

之后直接使用：

```bash
rbook-navi
rbook-navi --query duipai
rbook-navi --query sample
```

如果希望覆盖 `navi` 命令本身，也可以写成：

```bash
alias navi='command navi --path /home/rainboy/mycode/抽离rbook中的题目/scripts/navi'
```

这种写法会让当前 shell 中的 `navi` 默认只搜索本仓库 cheatsheet；如果还想保留系统其他 navi cheatsheet，建议使用 `rbook-navi` 这个独立 alias。

说明见 [`docs/tools/navi.md`](docs/tools/navi.md)。

### 7.1 题解分析工具

| 工具 | 位置 | 文档 |
| --- | --- | --- |
| `check_sample.py` | `scripts/problem-analysis-tools/check_sample.py` | [`docs/tools/check_sample.md`](docs/tools/check_sample.md) |
| `check_problem.py` | `scripts/problem-analysis-tools/check_problem.py` | [`docs/tools/check_problem.md`](docs/tools/check_problem.md) |
| `new-problem` / `new-problem.py` | `scripts/problem-analysis-tools/new-problem.py` | [`docs/tools/new-problem.md`](docs/tools/new-problem.md) |
| `fetch_problem.py` | `scripts/problem-analysis-tools/fetch_problem.py` | [`docs/tools/fetch_problem.md`](docs/tools/fetch_problem.md) |
| `problem_status.py` | `scripts/problem-analysis-tools/problem_status.py` | [`docs/tools/problem_status.md`](docs/tools/problem_status.md) |
| `gen_random.py` | `scripts/problem-analysis-tools/gen_random.py` | [`docs/tools/gen_random.md`](docs/tools/gen_random.md) |
| `duipai.py` | `scripts/problem-analysis-tools/duipai.py` | [`docs/tools/duipai.md`](docs/tools/duipai.md) |
| `duipai-human.py` | `scripts/problem-analysis-tools/duipai-human.py` | [`docs/tools/duipai-human.md`](docs/tools/duipai-human.md) |
| `shrink_failed.py` | `scripts/problem-analysis-tools/shrink_failed.py` | [`docs/tools/shrink_failed.md`](docs/tools/shrink_failed.md) |
| `data_tool.py` | `scripts/problem-analysis-tools/data_tool.py` | [`docs/tools/data_tool.md`](docs/tools/data_tool.md) |

### 7.2 旧版写题辅助工具

总览见 [`docs/problem-tools.md`](docs/problem-tools.md)。

| 工具 | 位置 | 文档 |
| --- | --- | --- |
| `b` | `scripts/problem-tools/b` | [`docs/tools/problem-tools-b.md`](docs/tools/problem-tools-b.md) |
| `duipai.py` | `scripts/problem-tools/duipai.py` | [`docs/tools/problem-tools-duipai.md`](docs/tools/problem-tools-duipai.md) |
| `one-duipai.py` | `scripts/problem-tools/one-duipai.py` | [`docs/tools/problem-tools-one-duipai.md`](docs/tools/problem-tools-one-duipai.md) |
| `test-data.py` | `scripts/problem-tools/test-data.py` | [`docs/tools/problem-tools-test-data.md`](docs/tools/problem-tools-test-data.md) |
| `randint.py` | `scripts/problem-tools/randint.py` | [`docs/tools/problem-tools-randint.md`](docs/tools/problem-tools-randint.md) |
| `input2dot.py` | `scripts/problem-tools/input2dot.py` | [`docs/tools/problem-tools-input2dot.md`](docs/tools/problem-tools-input2dot.md) |
| `dot2png.py` | `scripts/problem-tools/dot2png.py` | [`docs/tools/problem-tools-dot2png.md`](docs/tools/problem-tools-dot2png.md) |
| `luogu.py` | `scripts/problem-tools/luogu.py` | [`docs/tools/problem-tools-luogu.md`](docs/tools/problem-tools-luogu.md) |
| `oj` | `scripts/problem-tools/oj.js` | [`docs/tools/problem-tools-oj.md`](docs/tools/problem-tools-oj.md) |
| `r-lldb` | `scripts/problem-tools/lldb.sh` | [`docs/tools/problem-tools-r-lldb.md`](docs/tools/problem-tools-r-lldb.md) |
| `nvimsizer` | `scripts/problem-tools/nvimsizer.sh` | [`docs/tools/problem-tools-nvimsizer.md`](docs/tools/problem-tools-nvimsizer.md) |
| `transfer` | `scripts/problem-tools/transfer.sh` | [`docs/tools/problem-tools-transfer.md`](docs/tools/problem-tools-transfer.md) |
| `r-list-all-scripts.py` | `scripts/problem-tools/r-list-all-scripts.py` | [`docs/tools/problem-tools-r-list-all-scripts.md`](docs/tools/problem-tools-r-list-all-scripts.md) |

## 8. 项目结构

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
├── scripts/problem-analysis-tools/ # 题解分析、随机数据与对拍脚本
├── .agents/skills/        # 本仓库使用的本地 AI skills
├── mcp/                   # MCP 网关服务
└── docs/                  # 设计与计划文档
```

## 9. 常用命令

### 根项目

```bash
npm test
npm start
```

题目解析工具：

```bash
python3 scripts/problem-analysis-tools/gen_random.py --pattern array -n 5
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001
python3 scripts/problem-analysis-tools/duipai.py --gen problems/luogu/1001/gen.py --user problems/luogu/1001/main.cpp --brute problems/luogu/1001/brute.cpp -n 200
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

## 10. 开发说明

- 题目数据来自 `problems/`，启动时会扫描并用于检索。
- 如需扩展 AI 能力，优先在 `mcp/src/tools/` 下新增工具。
- API 变更后，请同步更新：
  - `views/api.pug`
  - `mcp/README.md`
