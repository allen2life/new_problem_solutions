#!/usr/bin/env python3
"""Call a local-configured image API for an OJ one-page explainer plan."""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import re
import shutil
import sys
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
DEFAULT_API_FILE = "ai_image_api.md"


class ConfigError(RuntimeError):
    pass


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for path in [current, *current.parents]:
        if (path / ".git").exists():
            return path
    return current


def extract_yaml_block(text: str) -> str:
    match = re.search(r"```ya?ml\s*\n(.*?)\n```", text, re.DOTALL | re.IGNORECASE)
    if not match:
        raise ConfigError("ai_image_api.md must contain a fenced yaml block.")
    return match.group(1)


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value[0:1] in {"'", '"'} and value[-1:] == value[0]:
        return value[1:-1]
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(yaml_text: str) -> dict[str, Any]:
    """Parse the small YAML subset expected in ai_image_api.md.

    This avoids adding a PyYAML dependency. It supports top-level key/value
    pairs and one-level nested maps such as `extra:`.
    """

    result: dict[str, Any] = {}
    current_map: dict[str, Any] | None = None
    current_indent = 0

    for raw_line in yaml_text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        if ":" not in line:
            raise ConfigError(f"Unsupported yaml line: {raw_line}")

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if indent == 0:
            current_map = None
            current_indent = 0
            if value == "":
                nested: dict[str, Any] = {}
                result[key] = nested
                current_map = nested
                current_indent = indent + 2
            else:
                result[key] = parse_scalar(value)
        elif current_map is not None and indent >= current_indent:
            current_map[key] = parse_scalar(value)
        else:
            raise ConfigError(f"Unsupported yaml indentation: {raw_line}")

    return result


def load_config(repo_root: Path, api_file: str) -> dict[str, Any]:
    path = repo_root / api_file
    if not path.exists():
        raise ConfigError(f"API config not found: {path}")

    text = path.read_text(encoding="utf-8")
    yaml_text = extract_yaml_block(text)
    config = parse_simple_yaml(yaml_text)

    missing = [name for name in ("base_url", "token", "model") if not config.get(name)]
    if missing:
        raise ConfigError(f"Missing required config field(s): {', '.join(missing)}")

    return config


def extract_plan_section(plan_text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(plan_text)
    return match.group(1).strip() if match else ""


def load_prompt(plan_path: Path) -> str:
    text = plan_path.read_text(encoding="utf-8")
    prompt = extract_plan_section(text, "prompt_zh")
    if prompt:
        return prompt

    # Fallback: use the whole plan if the agent used a slightly different
    # heading. The plan should not contain secrets.
    stripped = text.strip()
    if not stripped:
        raise ConfigError(f"Plan is empty: {plan_path}")
    return stripped


def build_request(config: dict[str, Any], prompt: str, n: int) -> dict[str, Any]:
    body: dict[str, Any] = {
        "model": config["model"],
        "prompt": prompt,
        "n": n,
    }

    if config.get("size"):
        body["size"] = config["size"]
    if config.get("response_format"):
        body["response_format"] = config["response_format"]
    if config.get("output_format"):
        body["output_format"] = config["output_format"]

    extra = config.get("extra")
    if isinstance(extra, dict):
        body.update(extra)

    return body


def join_api_url(base_url: str, path: str) -> str:
    return base_url.rstrip("/") + "/" + path.lstrip("/")


def openai_image_endpoint(config: dict[str, Any]) -> str:
    endpoint = str(config.get("image_endpoint") or "/v1/images/generations").strip()
    if endpoint.startswith("http://") or endpoint.startswith("https://"):
        return endpoint
    return join_api_url(str(config["base_url"]), endpoint)


def config_mode(config: dict[str, Any]) -> str:
    return str(config.get("mode") or config.get("provider") or "openai_compatible")


def sanitized_secrets(config: dict[str, Any]) -> list[str]:
    return [str(config.get("base_url", "")), str(config.get("token", ""))]


def sanitize_message(message: str, secrets: list[str]) -> str:
    cleaned = message
    for secret in secrets:
        if secret:
            cleaned = cleaned.replace(secret, "<hidden>")
    return cleaned


def post_json(url: str, token: str, body: dict[str, Any], timeout: float) -> dict[str, Any]:
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        details = sanitize_message(details, [url, token])
        raise RuntimeError(f"Image API HTTP {exc.code}: {details[:500]}") from exc
    except urllib.error.URLError as exc:
        details = sanitize_message(str(exc), [url, token])
        raise RuntimeError(f"Image API request failed: {details}") from exc
    except http.client.RemoteDisconnected as exc:
        raise RuntimeError("Image API request failed: remote end closed connection without response") from exc


def post_json_with_retry(
    url: str,
    token: str,
    body: dict[str, Any],
    timeout: float,
    *,
    retries: int = 5,
    sleep_seconds: float = 3.0,
) -> dict[str, Any]:
    last_error: RuntimeError | None = None
    for attempt in range(retries):
        try:
            return post_json(url, token, body, timeout)
        except RuntimeError as exc:
            last_error = exc
            message = str(exc).lower()
            retryable = (
                "remote end closed connection without response" in message
                or "timed out" in message
                or "timeout" in message
                or "temporarily unavailable" in message
            )
            if not retryable or attempt == retries - 1:
                raise
            time.sleep(sleep_seconds)
    assert last_error is not None
    raise last_error


def get_json(url: str, token: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        details = sanitize_message(details, [url, token])
        raise RuntimeError(f"Image API HTTP {exc.code}: {details[:500]}") from exc
    except urllib.error.URLError as exc:
        details = sanitize_message(str(exc), [url, token])
        raise RuntimeError(f"Image API request failed: {details}") from exc
    except http.client.RemoteDisconnected as exc:
        raise RuntimeError("Image API request failed: remote end closed connection without response") from exc


def get_json_with_retry(url: str, token: str, timeout: float, *, retries: int = 5, sleep_seconds: float = 3.0) -> dict[str, Any]:
    last_error: RuntimeError | None = None
    for attempt in range(retries):
        try:
            return get_json(url, token, timeout)
        except RuntimeError as exc:
            last_error = exc
            message = str(exc).lower()
            retryable = (
                "remote end closed connection without response" in message
                or "timed out" in message
                or "timeout" in message
                or "temporarily unavailable" in message
            )
            if not retryable or attempt == retries - 1:
                raise
            time.sleep(sleep_seconds)
    assert last_error is not None
    raise last_error


def write_image_from_item(item: dict[str, Any], output: Path, timeout: float) -> None:
    if item.get("b64_json"):
        output.write_bytes(base64.b64decode(item["b64_json"]))
        return

    if item.get("url"):
        with urllib.request.urlopen(item["url"], timeout=timeout) as response:
            output.write_bytes(response.read())
        return

    raise RuntimeError("Image API response item has neither b64_json nor url.")


def download_url(url: str, output: Path, timeout: float) -> None:
    with urllib.request.urlopen(url, timeout=timeout) as response:
        output.write_bytes(response.read())


def download_url_with_retry(url: str, output: Path, timeout: float, *, retries: int = 5, sleep_seconds: float = 3.0) -> None:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            download_url(url, output, timeout)
            return
        except Exception as exc:
            last_error = exc
            if attempt == retries - 1:
                raise
            time.sleep(sleep_seconds)
    if last_error is not None:
        raise last_error


def numbered_output_path(output: Path, index: int, total: int) -> Path:
    if total == 1:
        return output
    return output.with_name(f"{output.stem}-{index + 1}{output.suffix}")


def unwrap_data(payload: dict[str, Any]) -> Any:
    if isinstance(payload, dict) and "data" in payload:
        return payload["data"]
    return payload


def extract_task_ids(payload: dict[str, Any]) -> list[str]:
    data = unwrap_data(payload)
    candidates: list[Any] = []
    if isinstance(data, dict):
        for key in ("task_id", "task_ids", "任务ids", "任务id"):
            value = data.get(key)
            if isinstance(value, list):
                candidates.extend(value)
            elif value is not None:
                candidates.append(value)
    elif isinstance(data, list):
        candidates.extend(data)

    task_ids: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        task_id = str(item).strip()
        if not task_id or task_id in seen:
            continue
        seen.add(task_id)
        task_ids.append(task_id)
    if not task_ids:
        raise RuntimeError("Media generation response did not contain a task id.")
    return task_ids


def ensure_balance(config: dict[str, Any], timeout: float) -> None:
    if str(config.get("check_balance", "true")).lower() in {"false", "0", "no"}:
        return

    base_url = str(config["base_url"])
    token = str(config["token"])
    payload = get_json(join_api_url(base_url, "/v1/skills/balance"), token, timeout)
    if not isinstance(payload, dict):
        raise RuntimeError("Balance check returned invalid payload.")

    balance = payload.get("balance")
    quota = payload.get("api_key_quota")
    remaining = quota.get("remaining") if isinstance(quota, dict) else None

    try:
        if balance is not None and float(balance) <= 0:
            raise RuntimeError("Balance check failed: account balance is not positive.")
        if remaining is not None and float(remaining) <= 0:
            raise RuntimeError("Balance check failed: API key quota remaining is not positive.")
    except (TypeError, ValueError) as exc:
        raise RuntimeError("Balance check returned non-numeric balance/quota.") from exc


def is_success_status(status: dict[str, Any]) -> bool:
    fields = [
        str(status.get("status_group", "")),
        str(status.get("state", "")),
        str(status.get("status", "")),
    ]
    return any(value in {"已完成", "success", "succeeded", "completed", "生成完成"} for value in fields)


def is_failed_status(status: dict[str, Any]) -> bool:
    fields = [
        str(status.get("status_group", "")),
        str(status.get("state", "")),
        str(status.get("status", "")),
    ]
    return any(value in {"失败", "failed", "error", "生成失败"} for value in fields)


def generate_juxin_media_async(config: dict[str, Any], prompt: str, n: int, output: Path) -> list[Path]:
    base_url = str(config["base_url"])
    token = str(config["token"])
    timeout = float(config.get("timeout_seconds") or 120)
    poll_interval = float(config.get("poll_interval_seconds") or 5)
    max_wait = float(config.get("max_wait_seconds") or 7200)
    initial_poll_delay = float(config.get("initial_poll_delay_seconds") or 8)

    ensure_balance(config, timeout)

    params = config.get("params")
    if not isinstance(params, dict):
        params = {}

    submit_body = {
        "model": config["model"],
        "prompt": prompt,
        "params": params,
    }

    submit_url = join_api_url(base_url, "/v1/media/generate")
    task_ids: list[str] = []
    for _ in range(n):
        payload = post_json_with_retry(submit_url, token, submit_body, timeout)
        task_ids.extend(extract_task_ids(payload))

    output_paths: list[Path] = []
    status_base = join_api_url(base_url, "/v1/skills/task-status")
    deadline = time.time() + max_wait

    for index, task_id in enumerate(task_ids[:n]):
        result_url = ""
        last_status: dict[str, Any] = {}
        first_poll = True
        while time.time() < deadline:
            if first_poll and initial_poll_delay > 0:
                time.sleep(initial_poll_delay)
                first_poll = False
            query = urllib.parse.urlencode({"task_id": task_id})
            payload = get_json_with_retry(f"{status_base}?{query}", token, timeout)
            data = unwrap_data(payload)
            if not isinstance(data, dict):
                raise RuntimeError(f"Task {task_id} returned invalid status payload.")
            last_status = data

            if data.get("result_url"):
                result_url = str(data["result_url"])

            if data.get("is_final") is True or is_success_status(data) or is_failed_status(data):
                break
            time.sleep(poll_interval)

        if not last_status:
            raise RuntimeError(f"Task {task_id} did not return a status before timeout.")
        if is_failed_status(last_status):
            reason = last_status.get("error") or last_status.get("status") or "unknown task failure"
            raise RuntimeError(f"Task {task_id} failed: {reason}")
        if not result_url:
            raise RuntimeError(f"Task {task_id} finished without result_url.")

        path = numbered_output_path(output, index, n)
        download_url_with_retry(result_url, path, timeout)
        output_paths.append(path)

    return output_paths


def generate_openai_compatible(config: dict[str, Any], prompt: str, n: int, output: Path) -> list[Path]:
    timeout = float(config.get("timeout_seconds") or 120)
    body = build_request(config, prompt, n)
    endpoint = openai_image_endpoint(config)
    response = post_json_with_retry(endpoint, config["token"], body, timeout)
    data = response.get("data")
    if not isinstance(data, list) or not data:
        raise RuntimeError("Image API response missing non-empty data array.")

    output_paths: list[Path] = []
    for index, item in enumerate(data[:n]):
        if not isinstance(item, dict):
            raise RuntimeError("Image API response data item is not an object.")
        path = numbered_output_path(output, index, n)
        write_image_from_item(item, path, timeout)
        output_paths.append(path)

    return output_paths


def append_report(
    report_path: Path,
    output_paths: list[Path],
    model: str,
    size: str,
    elapsed_seconds: float,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    relative_outputs = [f"`{path.name}`" for path in output_paths]
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    section = [
        "",
        f"## 生成记录 {timestamp}",
        "",
        f"- 输出文件：{', '.join(relative_outputs)}",
        f"- 使用模型：`{model}`",
        f"- 尺寸：`{size or '未指定'}`",
        f"- 耗时：{elapsed_seconds:.1f}s",
        "- 检查结论：待检查",
        "- 是否建议插入 `index.md`：待检查",
        "",
    ]

    if report_path.exists():
        current = report_path.read_text(encoding="utf-8")
    else:
        current = "# AI 图片生成报告\n"
    report_path.write_text(current.rstrip() + "\n" + "\n".join(section), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate OJ one-page explainer image from an existing ai-image plan."
    )
    parser.add_argument("--problem-dir", required=True, help="Problem directory, e.g. problems/luogu/P1001.")
    parser.add_argument(
        "--plan",
        default="problem-analysis-workspace/ai-image-plan.md",
        help="Plan path, relative to problem-dir unless absolute.",
    )
    parser.add_argument(
        "--output",
        default="one-page-explainer-v1.png",
        help="Output image path, relative to problem-dir unless absolute.",
    )
    parser.add_argument("--n", type=int, default=1, help="Number of images to request. Default: 1.")
    parser.add_argument(
        "--api-file",
        default=DEFAULT_API_FILE,
        help="API config markdown path, relative to repo root unless absolute.",
    )
    parser.add_argument(
        "--adopt",
        action="store_true",
        help="Also copy the first generated image to one-page-explainer.png.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print a sanitized request summary without calling the API.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.n <= 0:
        raise SystemExit("--n must be positive.")

    initial_root = find_repo_root(Path.cwd())
    problem_dir = Path(args.problem_dir)
    if not problem_dir.is_absolute():
        problem_dir = (initial_root / problem_dir).resolve()
    problem_root = find_repo_root(problem_dir)
    repo_root = problem_root if (problem_root / ".git").exists() else initial_root

    plan_path = Path(args.plan)
    if not plan_path.is_absolute():
        plan_path = (problem_dir / plan_path).resolve()

    output = Path(args.output)
    if not output.is_absolute():
        output = (problem_dir / output).resolve()

    api_file = Path(args.api_file)
    api_file_arg = str(api_file if api_file.is_absolute() else args.api_file)

    try:
        config = load_config(repo_root, api_file_arg)
        prompt = load_prompt(plan_path)
    except ConfigError as exc:
        print(f"config error: {exc}", file=sys.stderr)
        return 2

    mode = config_mode(config)

    if args.dry_run:
        print("Dry run request summary:")
        print(f"- mode: {mode}")
        if mode in {"juxin", "juxin_media_async"}:
            print("- endpoint: <hidden>")
        else:
            print(f"- endpoint: {openai_image_endpoint(config)}")
        print(f"- model: {config['model']}")
        print(f"- size: {config.get('size', '')}")
        if isinstance(config.get("params"), dict):
            print(f"- params keys: {', '.join(sorted(config['params'].keys()))}")
        print(f"- n: {args.n}")
        print(f"- prompt chars: {len(prompt)}")
        print("- token: <hidden>")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    started = time.time()
    try:
        if mode in {"juxin", "juxin_media_async"}:
            output_paths = generate_juxin_media_async(config, prompt, args.n, output)
        else:
            output_paths = generate_openai_compatible(config, prompt, args.n, output)

        if args.adopt and output_paths:
            adopted = problem_dir / "one-page-explainer.png"
            shutil.copyfile(output_paths[0], adopted)

        elapsed = time.time() - started
        report_path = problem_dir / "problem-analysis-workspace" / "ai-image-report.md"
        append_report(
            report_path,
            output_paths,
            str(config.get("model", "")),
            str(config.get("size", "")),
            elapsed,
        )

        print("Generated image file(s):")
        for path in output_paths:
            print(path)
        print(f"Report updated: {report_path}")
        return 0
    except Exception as exc:
        message = sanitize_message(str(exc), sanitized_secrets(config))
        print(f"generation failed: {message}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
