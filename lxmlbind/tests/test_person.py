from lxml import etree
from nose.tools import assert_raises, eq_, ok_
from six import b

from lxmlbind.api import attributes, Base, Property, tag
from lxmlbind.base import eq_xml


@tag("person")
@attributes(type="object")
class Person(Base):
    """
    Example using basic properties.
    """
    first = Property()
    last = Property()


def test_person():
    """
    Verify Base functions in Person class.
    """
    person = Person()
    ok_(person._element is not None)
    ok_(person._parent is None)
    eq_(person._element.tag, person._tag())
    eq_(person.first, None)
    eq_(person.last, None)
    eq_(person.to_xml(), b("""<person type="object"/>"""))


def assert_generates_equivalent_xml(cls, raw_xml):
    """
    Verify that the XML we get out of `to_xml` matches the input.
    """
    bound_object = cls.from_xml(raw_xml)
    encoded_xml = bound_object.to_xml()
    ok_(eq_xml(etree.XML(encoded_xml), etree.XML(raw_xml)))


def test_person_from_xml():
    """
    Verify XML decoding with Person class.
    """
    for raw_xml in ["<person><first>John</first><last>Smith</last></person>",
                    "<person/>",
                    "<person><ignore>this</ignore></person>"]:
        yield assert_generates_equivalent_xml, Person, raw_xml


def test_person_get_class():
    """
    Verify data descriptor __get__ against Person class.
    """
    # __get__ works on class instance to return Property instance
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

    # __get__ works and returns None for absent property
    eq_(person.first, "John")
    eq_(person.last, None)


def test_person_set():
    """
    Verify data descriptor __set__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # __set__ works
    eq_(person.last, None)
    person.last = "Doe"
    eq_(person.last, "Doe")
    eq_(person.to_xml(), b("<person><first>John</first><last>Doe</last></person>"))


def test_person_delete():
    """
    Verify data descriptor __delete__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # __delete__ works
    del person.first
    eq_(person.first, None)
    eq_(person.to_xml(), b("<person/>"))

    # cannot delete unassigned property
    with assert_raises(AttributeError) as capture:
        del person.last
    eq_(str(capture.exception), "'<class 'lxmlbind.tests.test_person.Person'>' object has no attribute 'last'")
