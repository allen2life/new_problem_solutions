# AI 一图流批量生成方法与过程

> 现状说明（2026-06-22）：本文记录的是旧的图片模型批量生成过程，保留用于复盘历史结果。新的主流程已经改为 `dense_algorithm_board`：由 agent 生成 `problem-analysis-workspace/ai-image-layout.json`，再用 `.agents/skills/oj-ai-image-explainer/scripts/render_dense_algorithm_board.py` 在本地通过 Playwright 渲染 `1920x1088` PNG，不再依赖 `ai_image_api.md` 调用图片生成 API。

这份文档记录本仓库这一次批量生成题解 `one-page-explainer.png` 的实际做法，目的是让另一个 AI 或人工审核者可以复盘：

1. 用了哪些正式脚本。
2. 做过哪些临时补充操作。
3. 为什么标准批处理会自然跑完。
4. 为什么后续又继续尝试 `[仅评估]` 项。
5. 最终停在什么地方。
6. 结果如何校验。

本文只描述方法和过程，不包含 API 密钥。

## 1. 涉及文件

- 主技能说明：[`/.agents/skills/oj-ai-image-explainer/SKILL.md`](/home/rainboy/mycode/rbook_new_problem_solutions/.agents/skills/oj-ai-image-explainer/SKILL.md)
- 批处理脚本：[`/.agents/skills/oj-ai-image-explainer/scripts/batch_generate_oj_images.py`](/home/rainboy/mycode/rbook_new_problem_solutions/.agents/skills/oj-ai-image-explainer/scripts/batch_generate_oj_images.py)
- 单题出图脚本：[`/.agents/skills/oj-ai-image-explainer/scripts/generate_oj_image.py`](/home/rainboy/mycode/rbook_new_problem_solutions/.agents/skills/oj-ai-image-explainer/scripts/generate_oj_image.py)
- 标准批处理清单：[`/todo_work.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_work.md)
- 强制补跑清单：[`/todo_force_only_eval.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_force_only_eval.md)
- 本机私有 API 配置：`ai_image_api.md`

## 2. 这次批量的目标

目标不是“给所有题都生成图”，而是分两层推进：

1. 先跑标准批处理，只处理脚本判断为适合生成的一批题。
2. 如果标准批处理没有因为额度或接口失败而停止，再继续尝试一部分原本只做评估、不建议生成的题，验证还能不能继续扩大覆盖面。

这样做的原因是：

- 先让高价值题目拿到图片。
- 再把剩余额度消耗在边界题目上。
- 一旦出现真实接口故障或额度问题，就立即停下，不继续盲跑。

## 3. 配置切换

这次没有继续使用旧站点，而是把仓库根目录的 `ai_image_api.md` 切换为 OpenAI 兼容模式。

本次有效配置的关键点是：

```yaml
mode: "openai_compatible"
base_url: "<hidden>"
image_endpoint: "/images/generations"
token: "<hidden>"
model: "gpt-image-2"
timeout_seconds: 300
check_balance: false
size: "1920x1088"
quality: "high"
response_format: "url"
```

关键说明：

- 这次站点的可用接口不是 `/v1/images/generations`，而是 `/images/generations`。
- `check_balance: false`，表示本次没有接入统一余额探针，停止条件主要依赖真实请求报错。
- `generate_oj_image.py` 已支持 `openai_compatible` 模式。

## 4. 正式脚本能力

### 4.1 `batch_generate_oj_images.py` 的职责

这个脚本负责三件事：

1. 扫描 `problems/` 下所有题目。
2. 判断哪些题解“已完成”，哪些题适合生成 AI 一图流。
3. 为适合的题批量准备评估文件、计划文件，并真正出图。

它对“已完成题解”的判断条件包括：

- `index.md` 已存在。
- `main.cpp` 和 `brute.cpp` 已存在。
- 正文不再是脚手架占位。
- `description` 不为空。
- 至少包含 `### 题意`、`### 思路`、`### 代码`、`### 复杂度`。
- 正文长度足够，不是过短题解。

它还会跳过：

- 已经有 `one-page-explainer.png` 的题。
- 之前已有“自动检查未通过”且还没有最终采用图的题，避免重复卡死在同一题。

### 4.2 `generate_oj_image.py` 的职责

这个脚本只负责单题出图：

1. 读取 `ai_image_api.md`。
2. 读取 `problem-analysis-workspace/ai-image-plan.md`。
3. 调用图片接口。
4. 保存生成文件。
5. 生成阶段性报告。

这次它已经支持：

- OpenAI 兼容图片接口。
- 同步图片返回。
- 重试部分网络类错误。

## 5. 标准批处理的实际执行方法

标准入口命令是：

```bash
python3 .agents/skills/oj-ai-image-explainer/scripts/batch_generate_oj_images.py --phase generate
```

这里没有重新跑 `--phase all`，因为仓库里大量题目的评估和计划文件之前已经准备过；这次重点是继续生成。

标准流程是：

1. 扫描所有题目。
2. 跳过已经有最终图的题。
3. 对仍然处于“高优先级生成”状态的题逐个出图。
4. 每题出图后自动检查 PNG：
   - 是否存在。
   - 是否是合法 PNG。
   - 分辨率是否足够。
   - 宽高比是否正常。
   - 文件大小是否明显异常。
5. 自动检查通过后：
   - 复制为 `one-page-explainer.png`
   - 更新 `problem-analysis-workspace/ai-image-report.md`
   - 在 `index.md` 中插入：

```md
#### 一图流解析

这张图先把本题从读题、关键观察到正式算法的主路线串起来，适合先建立整体印象。

![一图流解析](./one-page-explainer.png)
```

### 5.1 这一步为什么会自然结束

这次标准批处理没有因为“额度不足”或“接口挂掉”而中断，而是把当前脚本判定为“应该生成”的题全部处理完了。

处理完之后，重新看 [`/todo_work.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_work.md) 的结果是：

- 已纳入批处理：`116` 题
- 未纳入批处理：`317` 题

这 116 题在当前清单里全部是 `[仅评估]`，说明：

- 当前剩下的 ready 题仍然是“文章完整，可评估”的题。
- 但脚本已经不再认为它们属于应该优先出图的那一批。
- 换句话说，标准意义上的“高优先级生成项”已经耗尽。

## 6. 为什么继续跑 `[仅评估]`

用户后来要求“再尝试一轮”，核心意图不是机械重复，而是：

- 如果图片站还能继续工作，就把剩余的边界题也试掉一些。
- 真正遇到接口故障，再停。

这和标准脚本的默认策略不同。标准脚本只会处理 `item.should_generate == True` 的题；而 `[仅评估]` 项在默认逻辑里不会进入生成阶段。

所以后续用了一个临时的、一次性的内联 Python runner，专门去强制跑 `[仅评估]` 项。

## 7. 临时强制补跑的做法

这一部分不是仓库正式脚本能力，而是本次批处理额外加的一层人工补流程。

### 7.1 第一轮补跑的问题

第一次强制补跑一开始就撞到了 `P1054`：

- 该题属于 `[仅评估]`
- 但本地还没有 `problem-analysis-workspace/ai-image-plan.md`

因此第一次失败信息是：

```text
[Errno 2] No such file or directory: '.../problem-analysis-workspace/ai-image-plan.md'
```

这说明一个事实：

- 标准脚本只有在“应该生成”的题上才保证计划文件齐全。
- 对 `[仅评估]` 项直接硬跑 `generate_for_problem(...)` 是不够的。

### 7.2 修正后的补跑逻辑

后续改成了下面这套流程：

1. 从 ready 题里筛出 `item.should_generate == False` 的题。
2. 跳过已经有最终图的题。
3. 跳过类似 `P8855` 这种“之前自动检查未通过，且还没有最终采用图”的题，避免反复卡住。
4. 对每个候选题先调用 `prepare_problem(item)`。
5. 如果 `prepare_problem(item)` 没有为这题写出计划文件，再显式补写 `ai-image-plan.md`。
6. 再调用 `generate_for_problem(item)`。
7. 把结果写回 [`/todo_force_only_eval.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_force_only_eval.md)。

可以把这次实际补跑逻辑概括成下面这段伪代码：

```python
for item in only_eval_items:
    if item already has final image:
        continue
    if item has unresolved review failure:
        continue

    family, short1, short2 = prepare_problem(item)
    if ai-image-plan.md does not exist:
        write ai-image-plan.md with make_plan(...)

    ok, message = generate_for_problem(item)
    update todo_force_only_eval.md
    if real provider error:
        stop batch
```

注意：这里的“伪代码”是对本次终端操作的忠实整理，不保证和当时在 shell 中输入的临时代码逐字一致。

## 8. 强制补跑的实际结果

最终的 [`/todo_force_only_eval.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_force_only_eval.md) 反映出这次补跑过程：

- `P1054`：第一次补跑时因为缺少 `ai-image-plan.md` 失败。
- `P1103`：生成成功，自动检查通过，尺寸 `1920x1088`。
- `P1140`：生成成功，自动检查通过，尺寸 `1280x720`。
- `P1233`：生成失败，报真实接口错误：

```text
Image API HTTP 502: {"error":{"message":"Upstream request failed","type":"upstream_error"}}
```

这里要区分两类失败：

1. `P1054` 是本地流程问题，不是图片服务真实故障。
2. `P1233` 才是这轮批量真正的停止点，因为它代表“接口上游失败”，继续跑的收益已经很差。

所以本次人工决策是：在 `P1233` 这里停止，不再继续扩大补跑范围。

## 9. 为什么要特别跳过 `P8855`

`P8855` 的情况不是“没跑过”，而是：

- 之前已经生成过版本。
- 自动检查或人工复核没有通过。
- 题目目录里还没有最终采用的 `one-page-explainer.png`。

如果批处理不跳过这种题，它会一直反复撞到同一个坏样本上，导致整批工作卡死在旧失败项。

所以本次脚本里加了保护：

- 如果发现该题有未解决的 review failure，就先跳过。

这是为了让批处理往前推进，而不是无限回头撞墙。

## 10. 最终校验方法

本次批量结束后，做了两类校验。

### 10.1 统计最终生成数量

使用 `problems/` 下所有 `one-page-explainer.png` 的数量作为最终落地图数量。

本次校验结果：

- 已生成最终图：`258`

### 10.2 校验每张最终图是否真的插入了 `index.md`

检查方式是：

1. 遍历所有 `one-page-explainer.png`
2. 打开同目录 `index.md`
3. 检查是否包含：

```md
![一图流解析](./one-page-explainer.png)
```

本次校验结果：

- 缺少引用的题目数：`0`

也就是说，当前仓库中所有最终采用图都已经实际接入题解正文。

## 11. 这次过程中的边界与遗留项

### 11.1 `todo_work.md` 的含义

当前 [`/todo_work.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_work.md) 里看到的 `116` 个 ready 项，不代表“还有 116 个高优先级图没生成”，而是：

- 这 116 题文章已经完整。
- 但当前评分规则只把它们归入 `[仅评估]`，不是默认自动生成队列。

### 11.2 `todo_force_only_eval.md` 的含义

这个文件不是标准脚本生成产物的一部分，而是为了记录这次“继续压榨仅评估题”的人工补跑过程。

审核时应把它理解为：

- 一份额外实验清单。
- 不是主批处理的常规出口。

### 11.3 `P1054` 记录需要人工辨别

`P1054` 现在在 [`/todo_force_only_eval.md`](/home/rainboy/mycode/rbook_new_problem_solutions/todo_force_only_eval.md) 里仍然显示失败，但它失败的原因是第一次补跑脚本没先写计划文件，不是图片站返回了坏结果。

因此审核时不要把它和 `P1233` 的 502 归为同一类故障。

## 12. 审核者建议检查的点

如果另一个 AI 要审核本次方法是否合理，建议重点看下面几点：

1. [`batch_generate_oj_images.py`](/home/rainboy/mycode/rbook_new_problem_solutions/.agents/skills/oj-ai-image-explainer/scripts/batch_generate_oj_images.py) 是否把“文章完成度判断”和“是否值得生成图片”分开了。
2. 对 review failure 的跳过策略是否合理。
3. `generate_for_problem(...)` 在自动检查失败时是否会清理错误采用图。
4. `[仅评估]` 的强制补跑是否应该沉淀成正式脚本参数，而不是继续依赖临时 runner。
5. `todo_work.md` 和 `todo_force_only_eval.md` 是否需要更明确地区分“正式队列”和“实验队列”。

## 13. 一句话结论

这次批量生成分成两段：

- 正式脚本先把默认应生成的题全部处理完。
- 然后用一次性临时 runner 继续试跑 `[仅评估]` 项，直到在 `P1233` 上遇到真实的上游 `HTTP 502` 故障后停止。

最终确认：

- `one-page-explainer.png` 总数：`258`
- 缺少 `index.md` 引用的数量：`0`
