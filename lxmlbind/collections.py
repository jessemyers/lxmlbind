"""
Declarative object collection classes.
"""
from functools import partial
from itertools import imap


from lxmlbind.api import Base


class List(Base):
    """
    Extension that supports treating elements as list of other types.

    Attempts to maintainer _parent references.
    """
    @classmethod
    def of(cls):
        """
        Defines what this class is a list of.

        :returns: a function that operates on `lxml.etree` elements, returning instances of `Base`.
        """
        return Base

    def _of(self):
        return partial(self.of(), parent=self)

    def append(self, value):
        self._element.append(value._element)
        value._parent = self

    def __getitem__(self, key):
        item = self._of()(self._element.__getitem__(key))
        return item

    def __setitem__(self, key, value):
        self._element.__setitem__(key, value._element)
        value._parent = self

    def __delitem__(self, key):
        # Without keeping a parallel list of Base instances, it's not
        # possible to detach the _parent pointer of values added via
        # append() or __setitem__. So far, not keeping a parallel list
        # is worth it.
        self._element.__delitem__(key)

    def __iter__(self):
        return imap(self._of(), self._element.__iter__())

    def __len__(self):
        return len(self._element)
