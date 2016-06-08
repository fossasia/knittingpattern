
class Prototype(object):

    def __init__(self, specification, inherited_values=[]):
        self.__specification = [specification] + inherited_values

    def get(self, key, default=None):
        for d in self.__specification:
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

    def inherit_from(self, specification):
        self.__specification.insert(1, specification)


__all__ = ["Prototype"]
