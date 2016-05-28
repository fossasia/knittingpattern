from collections import OrderedDict


class IdCollection(object):

    def __init__(self):
        self._items = OrderedDict()

    def append(self, item):
        self._items[item.id] = item

    def at(self, index):
        keys = list(self._items.keys())
        key = keys[index]
        return self[key]

    def __getitem__(self, id):
        return self._items[id]

    def __bool__(self):
        return bool(self._items)

    def __iter__(self):
        for id in self._items:
            yield self[id]

    def __len__(self):
        return len(self._items)
