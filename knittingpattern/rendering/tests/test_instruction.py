from knittingpattern.rendering.Instruction import Instruction
from pytest import fixture
from knittingpattern.Instruction import InstructionInRow
from unittest.mock import MagicMock

def row1():
    return MagicMock()


SPEC1 = {
        "svg-content"
    }


@fixture
def instruction1():
    return Instruction(SPEC1)


