"""This module contains the :class:`~knittingpattern.Prototype.Prototype`
that can be used to create inheritance on object level instead of class level.
"""


class Prototype(object):
    """This class provides inheritance of its specifications on object level.

    .. _prototype-key:

    Throughout this class `specification key` refers to a
    :func:`hashable <hash>` object
    to look up a value in the specification.
    """

    def __init__(self, specification, inherited_values=()):
        """create a new prototype

        :param specification: the specification of the prototype.
          This specification can be inherited by other prototypes.
          It can be a :class:`dict` or an other
          :class:`knittingpattern.Prototype.Prototype` or anything else that
          supports :meth:`__contains__` and :meth:`__getitem__`

        To look up a key in the specification it will be walked through

        1. :paramref:`specification`
        2. :paramref:`inherited_values` in order

        However, new lookups can be inserted at before
        :paramref:`inherited_values`, by calling :meth:`inherit_from`.

        """
        self.__specification = [specification] + list(inherited_values)

    def get(self, key, default=None):
        """
        :return: the value behind :paramref:`key` in the specification.
          If no value was found, :paramref:`default` is returned.
        :param key: a :ref:`specification key <prototype-key>`
        """
        for base in self.__specification:
            if key in base:
                return base[key]
        return default

    def __getitem__(self, key):
        """``prototype[key]``

        :param key: a :ref:`specification key <prototype-key>`
        :return: the value behind :paramref:`key` in the specification
        :raises KeyError: if no value was found

        """
        default = []
        value = self.get(key, default)
        if value is default:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        """``key in prototype``

        :param key: a :ref:`specification key <prototype-key>`
        :return: whether the key was found in the specification
        :rtype: bool

        """
        default = []
        value = self.get(key, default)
        return value is not default

    def inherit_from(self, new_specification):
        """Inherit from a :paramref:`new_specification`

        :param new_specification: a specification as passed to :meth:`__init__`

        The :paramref:`new_specification` is inserted before the first
        :paramref:`inherited value <__init__.inherited_values>`.

        If the order is

        1. :paramref:`~__init__.specification`
        2. :paramref:`~__init__.inherited_values`

        after calling ``prototype.inherit_from(new_specification)`` the lookup
        order is

        1. :paramref:`~__init__.specification`
        2. :paramref:`new_specification`
        3. :paramref:`~__init__.inherited_values`

        """
        self.__specification.insert(1, new_specification)


__all__ = ["Prototype"]
