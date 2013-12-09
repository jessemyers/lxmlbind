"""
Example objects for testing.
"""
from lxmlbind.api import Base, IntProperty, List, of, Property, tag


class Trivial(Base):
    pass


class Person(Base):
    first = Property()
    last = Property()


class Address(Base):
    street_number = IntProperty("street/number")
    street_name = Property("street/name")
    city = Property()
    state = Property()
    zip_code = IntProperty("zipCode")


class AddressBookEntry(Base):
    person = Person.property()
    address = Address.property()


@tag("person-list")
@of(Person)
class PersonList(List):
    pass
