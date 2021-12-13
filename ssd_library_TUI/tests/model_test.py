import pytest
from valid8 import ValidationError

from ssd_library_TUI.misc.models import ISBN


def test_isbn_wrong_values():
    wrong_values = ['aaaaaa--aa', '978-134-A3-98', '341-18-37-1-7', '800-12-521-123']

    for value in wrong_values:
        with (pytest.raises(ValidationError)):
            ISBN(value)


def test_isbn_good_values():
    good_values = ['978-134-23-98', '800-12-521-12']

    for value in good_values:
        ISBN(value)
