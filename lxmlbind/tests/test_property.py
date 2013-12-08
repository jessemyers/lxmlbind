"""
Property descriptor tests.
"""
from nose.tools import assert_raises, eq_

from lxmlbind.api import Property
from lxmlbind.tests.example import Person


def test_person_get_class():
    """
    Verify data descriptor __get__ against Person class.
    """

    # get works on class instance to return Property instance
    eq_(type(Person.first), Property)
    eq_(Person.first.path, "first")
    eq_(Person.first.tags, ["first"])
    eq_(Person.last.path, "last")
    eq_(Person.last.tags, ["last"])


def test_person_get():
    """
    Verify data descriptor __get__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # get works and returns None for absent property
    eq_(person.first, "John")
    eq_(person.last, None)


def test_person_set():
    """
    Verify data descriptor __set__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # set works
    eq_(person.last, None)
    person.last = "Doe"
    eq_(person.last, "Doe")
    eq_(person.to_xml(), "<person><first>John</first><last>Doe</last></person>")


def test_person_delete():
    """
    Verify data descriptor __delete__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # delete works
    del person.first
    eq_(person.first, None)
    eq_(str(person), "<person/>")

    # cannot delete absent property
    with assert_raises(AttributeError) as capture:
        del person.last
    eq_(capture.exception.message, "'<class 'lxmlbind.tests.example.Person'>' object has not attribute 'last'")
