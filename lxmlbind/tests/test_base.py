"""
Baseline object tests.
"""
from nose.tools import eq_, ok_

from lxml import etree

from lxmlbind import eq_xml
from lxmlbind.tests.example import Trivial, Person


def test_trivial():
    """
    Verify Base functions in Trivial class.
    """
    trivial = Trivial()
    ok_(trivial._element is not None)
    eq_(trivial._element.tag, trivial._tag)
    eq_(trivial._element.attrib, trivial._attributes)
    eq_(trivial.to_xml(), "<trivial/>")
    eq_(trivial.to_xml(), str(trivial))


def test_person():
    """
    Verify Base functions in Person class.
    """
    person = Person()
    ok_(person._element is not None)
    eq_(person._element.tag, person._tag)
    eq_(person._element.attrib, person._attributes)
    eq_(person.first, None)
    eq_(person.last, None)
    eq_(person.to_xml(), "<person/>")
    eq_(person.to_xml(), str(person))


def assert_generates_equivalent_xml(cls, raw_xml):
    """
    Verify that the XML we get out of `to_xml` matches the input.
    """
    bound_object = cls.from_xml(raw_xml)
    encoded_xml = bound_object.to_xml()
    ok_(eq_xml(etree.XML(bytes(encoded_xml)), etree.XML(bytes(raw_xml))))


def test_trivial_from_xml():
    """
    Verify XML decoding with Trivial class.
    """
    for raw_xml in ["<trivial/>",
                    "<trivial></trivial>",
                    "<trivial><ignore>this</ignore></trivial>"]:
        yield assert_generates_equivalent_xml, Trivial, raw_xml


def test_person_from_xml():
    """
    Verify XML decoding with Person class.
    """
    for raw_xml in ["<person><first>John</first><last>Smith</last></person>",
                    "<person/>",
                    "<person><ignore>this</ignore></person>"]:
        yield assert_generates_equivalent_xml, Person, raw_xml
