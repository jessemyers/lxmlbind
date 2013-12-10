"""
Baseline object tests.
"""
from nose.tools import assert_raises, eq_, ok_

from lxml import etree

from lxmlbind.base import eq_xml
from lxmlbind.tests.example import Person, PersonList, Trivial


def test_trivial():
    """
    Verify Base functions in Trivial class.
    """
    trivial = Trivial()
    ok_(trivial._element is not None)
    ok_(trivial._parent is None)
    eq_(trivial._element.tag, trivial.tag())
    eq_(trivial.to_xml(), "<trivial/>")
    eq_(trivial.to_xml(), str(trivial))


def test_person():
    """
    Verify Base functions in Person class.
    """
    person = Person()
    ok_(person._element is not None)
    ok_(person._parent is None)
    eq_(person._element.tag, person.tag())
    eq_(person.first, None)
    eq_(person.last, None)
    eq_(person.to_xml(), """<person type="object"/>""")
    eq_(person.to_xml(), str(person))


def test_person_list():
    """
    Verify list operations.
    """
    person1 = Person()
    person1.first = "John"

    person2 = Person()
    person2.first = "Jane"

    # test append and __len__
    person_list = PersonList()
    eq_(len(person_list), 0)
    person_list.append(person1)
    eq_(len(person_list), 1)
    eq_(person1._parent, person_list)

    person_list.append(person2)
    eq_(len(person_list), 2)
    eq_(person2._parent, person_list)

    eq_(person_list.to_xml(),
        """<person-list><person type="object"><first>John</first></person><person type="object"><first>Jane</first></person></person-list>""")  # noqa

    # test __getitem__
    eq_(person_list[0].first, "John")
    eq_(person_list[0]._parent, person_list)
    eq_(person_list[1].first, "Jane")
    eq_(person_list[0]._parent, person_list)

    # test __iter__
    eq_([person.first for person in person_list], ["John", "Jane"])
    ok_(all([person._parent == person_list for person in person_list]))

    # test __delitem__
    with assert_raises(IndexError):
        del person_list[2]
    del person_list[1]
    eq_(len(person_list), 1)
    eq_(person_list.to_xml(),
        """<person-list><person type="object"><first>John</first></person></person-list>""")

    # test __setitem__
    person_list[0] = person2
    eq_(person_list.to_xml(),
        """<person-list><person type="object"><first>Jane</first></person></person-list>""")


def test_tag_mismatch():
    """
    Exception raised in `from_xml` for mismatched element.
    """
    with assert_raises(Exception) as capture:
        Trivial.from_xml("<mismatched/>")
    eq_(capture.exception.message,
        "'<class 'lxmlbind.tests.example.Trivial'>' object requires tag 'trivial', not 'mismatched'")


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
