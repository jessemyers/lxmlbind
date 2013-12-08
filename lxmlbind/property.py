"""
Declarative object properties that map to `lxml.etree` content.
"""


class Property(object):
    """
    A declarative property that also serves as a data descriptor.
    """
    def __init__(self, path, type=str):
        """
        Create a property using an XPath-like expression that designates a specific
        element in the `lxml.etree`. True XPath syntax is not supported because it
        complicates creation of parent elements in the __set__ implementation.

        :param path: a '/' deliminated path
        """
        self.path = path
        self.tags = path.split("/")
        self.type = type

    def __get__(self, instance, owner):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.
        """
        if instance is None:
            return self
        element = instance.search(self.tags)
        if element is None:
            return None
        if element.text is None:
            return None
        return self.type(element.text)

    def __set__(self, instance, value):
        """
        Provide read access to an XML element (based on the property's path) as an object attribute.

        If the element does not exist, it will be created (as will any missing parent elements).
        """
        element = instance.search(self.tags, create=True)
        if value is None:
            element.text = None
        else:
            element.text = str(value)

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
