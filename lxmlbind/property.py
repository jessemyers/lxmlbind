"""
Declarative object properties that map to `lxml.etree` content.
"""


def get_text(element):
    return element.text


def get_int(element):
    if element.text is None:
        return None
    return int(element.text)


def get_long(element):
    if element.text is None:
        return None
    return long(element.text)


def set_text(element, value):
    if value is None:
        element.text = None
    else:
        element.text = str(value)


def set_child(element, value):
    if value is not None:
        # replace existing element with assigned one
        parent = element.getparent()
        element.getparent().remove(element)
        parent.append(value.element)


class Property(object):
    """
    A declarative property that also serves as a data descriptor.
    """
    def __init__(self,
                 path,
                 get_func=get_text,
                 set_func=set_text,
                 auto=False,
                 default=None,
                 **kwargs):
        """
        Create a property using an XPath-like expression that designates a specific
        element in the `lxml.etree`. True XPath syntax is not supported because it
        complicates creation of parent elements in the __set__ implementation.

        :param path: a '/' deliminated path
        :param get_func: a function use to transform __get__ output
        :param set_func: a function use to transform __set__ input
        :param auto: whether this property will be automatically created
        :param default: default value to use
        :param kwargs: optional attributes applied to newly created leaf element on __set__
        """
        self.path = path
        self.tags = path.split("/")
        self.get_func = get_func
        self.set_func = set_func
        self.auto = auto
        self.default = default
        self.attributes = kwargs

    def __get__(self, instance, owner):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.
        """
        if instance is None:
            return self
        element = instance.search(self.tags, create=self.auto, attributes=self.attributes)
        if element is None:
            return None
        return self.get_func(element)

    def __set__(self, instance, value):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.

        If the element does not exist, it will be created (as will any missing parent elements).
        """
        element = instance.search(self.tags, create=True, attributes=self.attributes)
        self.set_func(element, value)

    def __delete__(self, instance):
        """
        Provide delete access to an XML element (based on the property's path) as an object attribute.
        """
        element = instance.search(self.tags)
        if element is None:
            raise AttributeError("'{}' object has no attribute '{}'".format(instance.__class__, self.path))
        if element.getparent() is not None:
            element.getparent().remove(element)
        else:
            raise Exception("Cannot detach root element")


class IntProperty(Property):
    def __init__(self,
                 path,
                 get_func=get_int,
                 set_func=set_text,
                 auto=False,
                 default=None,
                 **kwargs):
        super(IntProperty, self).__init__(path, get_func, set_func, auto, default, **kwargs)


class LongProperty(Property):
    def __init__(self,
                 path,
                 get_func=get_long,
                 set_func=set_text,
                 auto=False,
                 default=None,
                 **kwargs):
        super(LongProperty, self).__init__(path, get_func, set_func, auto, default, **kwargs)
