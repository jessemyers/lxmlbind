"""
Example objects for testing.
"""

from lxmlbind.api import Base, Property


class Trivial(Base):
    pass


class Person(Base):
    first = Property("first")
    last = Property("last")
