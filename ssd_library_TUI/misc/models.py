from typeguard import typechecked
from dataclasses import dataclass, field

from valid8 import validate

from ssd_library_TUI.misc.dataclass import validate_dataclass
from ssd_library_TUI.misc.regex import matches_pattern


@typechecked
@dataclass(frozen=True)
class ISBN:
    value: str = field(init=True)
    regex = r'^(?=(?:\D*\d){10}(?:(?:\D*\d){3})?$)[\d-]+$'

    def __post_init__(self):
        validate_dataclass(self)
        validate('ISBN pattern', value=self.value, min_len=13, max_len=13, custom=matches_pattern(self.regex))

    def __str__(self):
        return self.value
