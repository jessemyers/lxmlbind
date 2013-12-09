"""
Declarative object properties that map to `lxml.etree` content.
"""


def get_text(element, parent):
    return element.text


def get_int(element, parent):
    if element.text is None:
        return None
    return int(element.text)


def get_long(element, parent):
    if element.text is None:
        return None
    return long(element.text)


def set_text(element, value, parent):
    if value is None:
        element.text = None
    else:
        element.text = str(value)


def set_child(element, value, parent):
    if value is not None:
        # replace existing element with assigned one
        element_parent = element.getparent()
        element_parent.remove(element)
        element_parent.append(value.element)
        value._parent = parent


class Property(object):
    """
    A declarative property that also serves as a data descriptor.
    """
    def __init__(self,
                 path=None,
                 get_func=get_text,
                 set_func=set_text,
                 attributes_func=None,
                 auto=False,
                 default=None,
                 **kwargs):
        """
        Create a property using an XPath-like expression that designates a specific
        element in the `lxml.etree`. True XPath syntax is not supported because it
        complicates creation of parent elements in the __set__ implementation.

        :param path: a '/' deliminated path; if omitted, defaults to the assigned name
        :param get_func: a function use to transform __get__ output
        :param set_func: a function use to transform __set__ input
        :param auto: whether this property will be automatically created
        :param default: default value to use
        :param kwargs: optional attributes applied to newly created leaf element on __set__
        """
        self.path = path
        self.get_func = get_func
        self.set_func = set_func
        self.auto = auto
        self.default = default
        self.attributes_func = attributes_func
        self.attributes = kwargs

    @property
    def tags(self):
        return self.path.split("/")

    def __get__(self, instance, owner):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.
        """
        if instance is None:
            return self
        element = instance.search(self.tags, create=self.auto, set_attributes=self._set_attributes)
        if element is None:
            return None
        return self.get_func(element, parent=instance)

    def __set__(self, instance, value):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.

        If the element does not exist, it will be created (as will any missing parent elements).
        """
        element = instance.search(self.tags, create=True, set_attributes=self._set_attributes)
        self.set_func(element, value, parent=instance)

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

    def _set_attributes(self, element, instance):
        """
        Set attributes on newly created `lxml.etree` elements for this property.
        """
        if self.attributes_func is None:
            element.attrib.update(self.attributes)
        else:
            self.attributes_func(element, instance)


class IntProperty(Property):
    def __init__(self,
                 path=None,
                 get_func=get_int,
                 set_func=set_text,
                 *args,
                 **kwargs):
        super(IntProperty, self).__init__(path=path,
                                          get_func=get_func,
                                          set_func=set_func,
                                          *args,
                                          **kwargs)


class LongProperty(Property):
    def __init__(self,
                 path=None,
                 get_func=get_long,
                 set_func=set_text,
                 *args,
                 **kwargs):
        super(LongProperty, self).__init__(path=path,
                                           get_func=get_func,
                                           set_func=set_func,
                                           *args,
                                           **kwargs)
