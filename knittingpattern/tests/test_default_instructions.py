from knittingpattern.InstructionLibrary import DefaultInstructions
from pytest import fixture


@fixture
def default():
    return DefaultInstructions()
