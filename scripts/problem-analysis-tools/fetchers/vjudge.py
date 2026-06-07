from __future__ import annotations

import re

from .base import BaseFetcher, FetchError, FetchResult, ProblemData, normalize_space


class VJudgeFetcher(BaseFetcher):
    name = "vjudge"
    aliases = ("poj", "hdu", "atcoder", "openj_bailian")
    site_prefixes = ("https://vjudge.net", "https://www.vjudge.net", "https://vjudge.net.cn")

    def match_name(self, oj: str) -> bool:
        return oj.lower() in (self.name, *self.aliases, "codeforces")

    def parse_url(self, url: str) -> tuple[str, str]:
        clean = url.split("?")[0].split("#")[0]
        match = re.search(r"/problem/([A-Za-z0-9_]+)-([^/]+)$", clean)
        if not match:
            raise FetchError(f"无法从 VJudge URL 解析 OJ 和题号：{url}")
        return match.group(1).lower(), match.group(2)

    def problem_link(self, oj: str, problem_id: str) -> str:
        return f"https://vjudge.net/problem/{oj}-{problem_id}"

    def build_data_from_id(self, oj: str, problem_id: str) -> ProblemData:
        save_oj = oj.lower()
        return ProblemData(
            oj=save_oj,
            problem_id=problem_id,
            problem_dir_id=problem_id,
            source=self.problem_link(save_oj, problem_id),
            title=problem_id,
        )

    def fetch(self, oj: str, problem_id: str) -> FetchResult:
        data = self.build_data_from_id(oj, problem_id)
        warnings: list[str] = []
        try:
            html = self.http_get(data.source)
            title = self.parse_title(html)
            if title:
                data.title = title
        except FetchError as exc:
            warnings.append(str(exc))
        warnings.append("VJudge 第一版只抓标题，不实现完整题面/样例抓取。")
        data.warnings.extend(warnings)
        return FetchResult(data=data, fetched=bool(data.title and data.title != problem_id), warnings=warnings)

    def parse_title(self, html: str) -> str:
        match = re.search(r'id=["\']prob-title["\'][\s\S]*?<h2[^>]*>([\s\S]*?)</h2>', html)
        if not match:
            return ""
        text = re.sub(r"<[^>]+>", "", match.group(1))
        return normalize_space(text)
