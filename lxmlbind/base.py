"""
Declarative object base class.
"""
from abc import ABCMeta
from inspect import getmro
from logging import getLogger

from lxml import etree

from lxmlbind.property import Property, set_child


class Base(object):
    """
    Base class for objects using LXML object binding.
    """
    __metaclass__ = ABCMeta

    def __init__(self, element=None, *args, **kwargs):
        """
        :param element: an optional root `lxml.etree` element
        """
        if element is None:
            self._element = self._new_default_element(*args, **kwargs)
        elif element.tag != self._tag:
            raise Exception("'{}' object requires tag '{}', not '{}'".format(self.__class__,
                                                                             self._tag,
                                                                             element.tag))
        else:
            self._element = element
        self._set_default_properties()

    def _new_default_element(self, *args, **kwargs):
        """
        Generate a new default element for this object.

        Subclasses may override this function to provide more complex default behavior.
        """
        return etree.Element(self._tag, attrib=self._attributes)

    def _set_default_properties(self):
        """
        Iterate over properties and populate default values.
        """
        for class_ in getmro(self.__class__):
            for member in class_.__dict__.values():
                if not isinstance(member, Property) or not member.auto:
                    continue
                if member.__get__(self, self.__class__) is None:
                    member.__set__(self, member.default)

    @property
    def _tag(self):
        """
        Define the tag name of root element of the object.

        By default, use the class name with a leading lower case. For PEP8 compatible
        class names, this gives a lowerCamelCase name, which is a reasonable choice.

        This property may be overridden in subclasses or via the tag() decorator.
        """
        return self.__class__.__name__[0].lower() + self.__class__.__name__[1:]

    @property
    def _attributes(self):
        """
        Define attributes for the root element of the object.

        By default, empty.
        """
        return {}

    def to_xml(self, pretty_print=False):
        """
        Encode as XML string.
        """
        return etree.tostring(self._element, pretty_print=pretty_print)

    @classmethod
    def from_xml(cls, xml):
        """
        Decode from an XML string.
        """
        return cls(etree.XML(bytes(xml)))

    def search(self,
               tags,
               element=None,
               create=False,
               attributes=None,
               logger=getLogger("lxmlbind.base")):
        """
        Search `lxml.etree` rooted at `element` for the first child
        matching a sequence of element tags.

        :param tags: the list of tags to traverse
        :param element: the root element of the tree or None to use this object's element
        :param create: optionally, create the element path while traversing
        :param attributes: optional attributes dictionary to set in the leaf element, when created
        """
        head, tail = tags[0], tags[1:]
        parent = self._element if element is None else element
        child = parent.find(head)
        if child is None:
            if create:
                logger.debug("Creating element '{}' for '{}'".format(head, parent.tag))
                child = etree.SubElement(parent, head)
                if attributes is not None and not tail:
                    child.attrib.update(attributes)
            else:
                return None
        return self.search(tail, child, create) if tail else child

    def __str__(self):
        """
        Return XML string.
        """
        return self.to_xml()

    def __hash__(self):
        """
        Hash using XML element.
        """
        return self._element.__hash__()

    def __eq__(self, other):
        """
        Compare using XML element equality, ignoring whitespace differences.
        """
        return eq_xml(self._element, other._element)

    def __ne__(self, other):
        """
        Compare using XML element equality, ignoring whitespace differences.
        """
        return not self.__eq__(other)

    @classmethod
    def property(cls, path, default=None, **kwargs):
        return Property(path, get_func=cls, set_func=set_child, auto=True, default=default, **kwargs)


def tag(name):
    """
    Class decorator that overrides the default behavior of the `Base._tag` property.
    """
    def wrapper(cls):
        if not issubclass(cls, Base):
            raise Exception("lxmlbind.base.tag decorator should only be used with subclasses of lxmlbind.base.Base")
        cls._tag = name
        return cls
    return wrapper


def eq_xml(this,
           that,
           ignore_attributes=None,
           ignore_whitespace=True,
           logger=getLogger("lxmlbind.base")):
    """
    XML comparison on `lxml.etree` elements.

    :param this: an `lxml.etree` element
    :param that: an `lxml.etree` element
    :param ignore_attributes: an optional list of attributes to ignore
    :param ignore_whitespace: whether whitespace should matter
    """
    ignore_attributes = ignore_attributes or []

    # compare tags
    if this.tag != that.tag:
        if logger is not None:
            logger.debug("Element tags do not match: {} != {}".format(this.tag, that.tag))
        return False

    # compare attributes
    def _get_attributes(attributes):
        return {key: value for key, value in attributes.iteritems() if key not in ignore_attributes}

    these_attributes = _get_attributes(this.attrib)
    those_attributes = _get_attributes(that.attrib)
    if these_attributes != those_attributes:
        if logger is not None:
            logger.debug("Element attributes do not match: {} != {}".format(these_attributes,
                                                                            those_attributes))
        return False

    # compare text
    def _strip(tail):
        if tail is None:
            return None
        return tail.strip() or None

    this_text = _strip(this.text) if ignore_whitespace else this.text
    that_text = _strip(that.text) if ignore_whitespace else that.text

    if this_text != that_text:
        if logger is not None:
            logger.debug("Element text does not match: {} != {}".format(this_text,
                                                                        that_text))
        return False

    this_tail = _strip(this.tail) if ignore_whitespace else this.tail
    that_tail = _strip(that.tail) if ignore_whitespace else that.tail

    if this_tail != that_tail:
        if logger is not None:
            logger.debug("Element tails do not match: {} != {}".format(this_tail,
                                                                       that_tail))
        return False

    # evaluate children
    these_children = sorted(this.getchildren(), key=lambda element: element.tag)
    those_children = sorted(that.getchildren(), key=lambda element: element.tag)
    if len(these_children) != len(those_children):
        if logger is not None:
            logger.debug("Element children length does not match: {} != {}".format(len(these_children),
                                                                                   len(those_children)))
        return False

    # recurse
    for this_child, that_child in zip(these_children, those_children):
        if not eq_xml(this_child, that_child, ignore_attributes, ignore_whitespace):
            return False
    else:
        return True
