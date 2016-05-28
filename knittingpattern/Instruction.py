TYPE = "type"
KNIT_TYPE = "knit"
PURL_TYPE = "purl"
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"
CONSUMED_MESHES = "number_of_consumed_meshes"
PRODUCED_MESHES = "number_of_produced_meshes"


class Instruction(object):

    def __init__(self, specification):
        self.specification = specification

    @property
    def type(self):
        return self.specification.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        return self.specification.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        return self.specification.get(CONSUMED_MESHES, 1)

    @property
    def number_of_produced_meshes(self):
        return self.specification.get(PRODUCED_MESHES, 1)

    def has_color(self):
        return self.color is not None

    def does_knit(self):
        return self.type == KNIT_TYPE

    def does_purl(self):
        return self.type == PURL_TYPE
        
    def __getitem__(self, key):
        return self.specification[key]
        
    def __iter__(self):
        for key in self.specification:
            yield key


__all__ = ["Instruction"]
