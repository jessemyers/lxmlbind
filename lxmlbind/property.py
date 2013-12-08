"""
Declarative object properties that map to `lxml.etree` content.
"""


class Property(object):
    """
    A declarative property that also serves as a data descriptor.
    """
    def __init__(self,
                 path,
                 get_type=str,
                 set_type=str,
                 type=None,
                 **kwargs):
        """
        Create a property using an XPath-like expression that designates a specific
        element in the `lxml.etree`. True XPath syntax is not supported because it
        complicates creation of parent elements in the __set__ implementation.

        :param path: a '/' deliminated path
        :param get_type: a function use to transform __get__ output
        :param set_type: a function use to transform __set__ input
        :param kwargs: optional attributes applied to newly created leaf element on __set__
        """
        self.path = path
        self.tags = path.split("/")
        self.get_type = get_type
        self.set_type = set_type
        self.type = type
        self.attributes = kwargs

    def __get__(self, instance, owner):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.
        """
        if instance is None:
            return self
        element = instance.search(self.tags)
        if element is None:
            return None
        if self.type is not None:
            return self.type(element)
        if element.text is None:
            return None
        return self.get_type(element.text)

    def __set__(self, instance, value):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.

        If the element does not exist, it will be created (as will any missing parent elements).
        """
        element = instance.search(self.tags, create=True, attributes=self.attributes)
        if self.type is not None:
            # XXX what about right hand value?
            return
        if value is None:
            element.text = None
        else:
            element.text = self.set_type(value)

    def __delete__(self, instance):
        """
        Provide delete access to an XML element (based on the property's path) as an object attribute.
        """
        element = instance.search(self.tags)
        if element is None:
            raise AttributeError("'{}' object has no attribute '{}'".format(type(instance), self.path))
        if element.getparent() is not None:
            element.getparent().remove(element)
        else:
            raise Exception("Cannot detach root element")
