from __future__ import annotations

import re

from .base import BaseFetcher, FetchError, ProblemData


class CodeforcesFetcher(BaseFetcher):
    name = "codeforces"
    aliases = ("cf",)
    site_prefixes = ("https://codeforces.com", "https://www.codeforces.com")

    def parse_url(self, url: str) -> tuple[str, str]:
        clean = url.split("?")[0].split("#")[0]
        patterns = [
            r"/contest/(\d+)/problem/([A-Za-z0-9]+)",
            r"/problemset/problem/(\d+)/([A-Za-z0-9]+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, clean)
            if match:
                return self.name, f"{match.group(1)}{match.group(2)}"
        raise FetchError(f"无法从 Codeforces URL 解析题号：{url}")

    def problem_link(self, problem_id: str) -> str:
        match = re.fullmatch(r"(\d+)([A-Za-z0-9]+)", problem_id)
        if not match:
            return "https://codeforces.com"
        return f"https://codeforces.com/contest/{match.group(1)}/problem/{match.group(2)}"

    def build_data_from_id(self, oj: str, problem_id: str) -> ProblemData:
        return ProblemData(
            oj=self.name,
            problem_id=problem_id,
            problem_dir_id=problem_id,
            source=self.problem_link(problem_id),
            title=problem_id,
        )
