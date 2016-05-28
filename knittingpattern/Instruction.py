TYPE = "type"
KNIT_TYPE = "knit"
PURL_TYPE = "purl"
DEFAULT_TYPE = KNIT_TYPE
COLOR = "color"
CONSUMED_MESHES = "number_of_consumed_meshes"
PRODUCED_MESHES = "number_of_produced_meshes"


class Instruction(object):

    def __init__(self, specification, inherited_values=[]):
        self.specification = [specification] + inherited_values

    @property
    def type(self):
        return self.get(TYPE, DEFAULT_TYPE)

    @property
    def color(self):
        return self.get(COLOR, None)

    @property
    def number_of_consumed_meshes(self):
        return self.get(CONSUMED_MESHES, 1)

    @property
    def number_of_produced_meshes(self):
        return self.get(PRODUCED_MESHES, 1)

    def has_color(self):
        return self.color is not None

    def does_knit(self):
        return self.type == KNIT_TYPE

    def does_purl(self):
        return self.type == PURL_TYPE

    def get(self, key, default):
        for d in self.specification:
            if key in d:
                return d[key]
        return default

    def __getitem__(self, key):
        default = []
        value = self.get(key, default)
        if value is default:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        default = []
        value = self.get(key, default)
        return value is not default


__all__ = ["Instruction"]
