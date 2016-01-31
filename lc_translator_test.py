import pytest

from lc_translator import build_lc_translator


def test_translator():
    string = '123\n12345\n12'
    translator = build_lc_translator(string)
    assert translator(1, 0) == 0
    assert translator(2, 0) == 4
    assert translator(2, 1) == 5
    assert translator(3, 0) == 10
    assert translator(3, 1) == 11
