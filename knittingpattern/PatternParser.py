from .IdCollection import IdCollection
from .KnittingPattern import KnittingPattern
from .Row import Row

class PatternParser(object):

    def __init__(self, knitting_patter_set, pattern_base):
        self.knitting_patter_set = knitting_patter_set
        self.pattern_base = pattern_base

    def parse(self):
        self.create_pattern_set()
        self.fill_pattern_set()
        return self.result

    def create_pattern_set(self):
        self.result = self.new_id_collection()

    def fill_pattern_set(self):
        pattern = self.pattern_base.get("pattern", [])
        for pattern_to_parse in pattern:
            parsed_pattern = self.new_pattern(pattern_to_parse)
            self.result.append(parsed_pattern)

    def new_id_collection(self):
        return IdCollection()

    def new_row(self, values):
        return Row(values)

    def new_pattern(self, base):
        rows = self.new_id_collection()
        for row in base.get("rows", []):
            rows.append(self.new_row(row))
        return KnittingPattern(base, rows)

__all__ = ["PatternParser"]
