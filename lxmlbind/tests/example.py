"""
Example objects for testing.
"""
from lxmlbind.api import Base, IntProperty, Property


class Trivial(Base):
    pass


class Person(Base):
    first = Property("first")
    last = Property("last")


class Address(Base):
    street_number = IntProperty("street/number")
    street_name = Property("street/name")
    city = Property("city")
    state = Property("state")
    zip_code = IntProperty("zipCode")


class AddressBookEntry(Base):
    person = Person.property("person")
    address = Address.property("address")
