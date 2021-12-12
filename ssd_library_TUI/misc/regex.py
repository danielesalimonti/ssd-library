from typing import Callable
import typeguard
import re


@typeguard.typechecked
def matches_pattern(regex: str) -> Callable [[str], bool]:
    r = re.compile(regex)

    def result(str_to_match: str):
        return bool(r.fullmatch(str_to_match))

    return result