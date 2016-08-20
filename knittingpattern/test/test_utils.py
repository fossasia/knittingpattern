from knittingpattern.utils import unique
import pytest


class TestUniquenes(object):

    """Test the function unique."""

    @pytest.mark.parametrize("input,expected_result", [
        ([], []), ([[1, 1, 1, 1, 1]], [1]),
        ([[1, 2, 3], [4, 3, 2, 1]], [1, 2, 3, 4]),
        ([[None, 4], [4, 6, None]], [None, 4, 6]),
        ([[[], [1]], [[1], [0], []]], [[], [1], [0]])])
    @pytest.mark.parametrize("use_generator", [True, False])
    def test_results(self, input, expected_result, use_generator):
        if use_generator:
            input = [(element for element in listing) for listing in input]
        result = unique(input)
        assert result == expected_result
