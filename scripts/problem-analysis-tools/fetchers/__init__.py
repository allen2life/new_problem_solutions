"""Fetcher providers used by fetch_problem.py."""

from .base import FetchError, FetchResult, ProblemData, Sample
from .codeforces import CodeforcesFetcher
from .luogu import LuoguFetcher
from .vjudge import VJudgeFetcher


FETCHERS = [
    LuoguFetcher(),
    CodeforcesFetcher(),
    VJudgeFetcher(),
]


__all__ = [
    "CodeforcesFetcher",
    "FETCHERS",
    "FetchError",
    "FetchResult",
    "LuoguFetcher",
    "ProblemData",
    "Sample",
    "VJudgeFetcher",
]
