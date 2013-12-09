"""
Example objects for testing.
"""
from lxmlbind.api import Base, IntProperty, List, of, Property, tag


class Trivial(Base):
    """
    Example using trivial construction.
    """
    pass


class Person(Base):
    """
    Example using basic properties.
    """
    first = Property()
    last = Property()


class Address(Base):
    """
    Example using typed properties and non-trivial property path.
    """
    street_number = IntProperty("street/number")
    street_name = Property("street/name")
    city = Property()
    state = Property()
    zip_code = IntProperty("zipCode")


class AddressBookEntry(Base):
    """
    Example using nested types.
    """
    person = Person.property()
    address = Address.property()


@tag("person-list")
@of(Person)
class PersonList(List):
    """
    Example using typed list.
    """
    pass


class Filtered(List):
    """
    Example using property filtering and attribute specification to control search behavior.
    """
    def _has_type(type_):
        def has_type(element):
            return element.attrib.get("type") == type_
        return has_type

    foo = Property("value", filter_func=_has_type("foo"), **{"type": "foo"})
    bar = Property("value", filter_func=_has_type("bar"), **{"type": "bar"})
