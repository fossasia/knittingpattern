from knittingpattern import new_knitting_pattern
import knittingpattern.KnittingPattern as KnittingPatternModule
from knittingpattern.KnittingPattern import KnittingPattern
from unittest.mock import Mock
from test_row_instructions import a1
import knittingpattern
from pytest import fixture


class TestInstructionColors(object):

    """Test KnittingPattern.instruction_colors."""

    @fixture
    def unique(self, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(KnittingPatternModule, "unique", mock)
        return mock

    @fixture
    def rows_in_knit_order(self, rows, monkeypatch):
        mock = Mock()
        monkeypatch.setattr(KnittingPattern, "rows_in_knit_order", mock)
        mock.return_value = rows
        return mock

    @fixture
    def rows(self):
        return [Mock(), Mock(), Mock()]

    @fixture
    def knittingpattern(self, rows):
        return KnittingPattern(Mock(), Mock(), Mock(), Mock())

    def test_result(self, knittingpattern, unique, rows_in_knit_order):
        assert knittingpattern.instruction_colors == unique.return_value

    def test_call_arguments(self, knittingpattern, unique, rows,
                            rows_in_knit_order):
        knittingpattern.instruction_colors
        instruction_colors = [row.instruction_colors for row in rows]
        unique.assert_called_once_with(instruction_colors)

    def test_chalotte(self, a1):
        assert a1.instruction_colors == [None]

    def test_cafe(self):
        pattern = knittingpattern.load_from().example("Cafe.json").first
        colors = ["mocha latte", "dark brown", "brown", "white", ]
        assert pattern.instruction_colors == colors
