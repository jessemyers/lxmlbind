"""
Declarative object decorators.
"""
from lxmlbind.api import Base


def tag(name):
    """
    Class decorator that replaces `Base.tag()` with a function that returns `name`.
    """
    def wrapper(cls):
        if not issubclass(cls, Base):
            raise Exception("lxmlbind.base.tag decorator should only be used with subclasses of lxmlbind.base.Base")

        @classmethod
        def tag(cls):
            return name

        cls.tag = tag
        return cls
    return wrapper


def attributes(**kwargs):
    """
    Class decorator that replaces `Base.attributes()` with a function that returns `kwargs`.
    """
    def wrapper(cls):
        if not issubclass(cls, Base):
            raise Exception("lxmlbind.base.attributes decorator should only be used with subclasses of lxmlbind.base.Base")  # noqa

        @classmethod
        def attributes(cls):
            return kwargs

        cls.attributes = attributes
        return cls
    return wrapper


def of(*classes):
    """
    Class decorator that replaces `List.of()` with a function that matches classes.
    """
    def wrapper(cls):
        if not issubclass(cls, Base):
            raise Exception("lxmlbind.base.of decorator should only be used with subclasses of lxmlbind.base.Base")

        tag_to_class = {
            class_.tag(): class_ for class_ in classes
        }

        @classmethod
        def of(cls):
            def _of(element, parent=None):
                return tag_to_class[element.tag](element, parent)
            return _of

        cls.of = of
        return cls
    return wrapper
