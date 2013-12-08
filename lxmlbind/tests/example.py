"""
Example objects for testing.
"""

from lxmlbind.api import Base, Property


class Trivial(Base):
    pass


class Person(Base):
    first = Property("first")
    last = Property("last")


class Address(Base):
    street_number = Property("street/number", type=int)
    street_name = Property("street/name")
    city = Property("city")
    state = Property("state")
    zip_code = Property("zipCode", type=int)
