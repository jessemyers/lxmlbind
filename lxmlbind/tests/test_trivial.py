from lxml import etree
from nose.tools import assert_raises, eq_, ok_
from six import b

from lxmlbind.api import Base
from lxmlbind.base import eq_xml


class Trivial(Base):
    """
    Example using trivial construction.
    """
    pass


def test_trivial():
    """
    Verify Base functions in Trivial class.
    """
    trivial = Trivial()
    ok_(trivial._element is not None)
    ok_(trivial._parent is None)
    eq_(trivial._element.tag, trivial._tag())
    eq_(trivial.to_xml(), b("<trivial/>"))


def test_tag_mismatch():
    """
    Exception raised in `from_xml` for mismatched element.
    """
    with assert_raises(Exception) as capture:
        Trivial.from_xml("<mismatched/>")
    eq_(str(capture.exception),
        "'<class 'lxmlbind.tests.test_trivial.Trivial'>' object requires tag 'trivial', not 'mismatched'")


def assert_generates_equivalent_xml(cls, raw_xml):
    """
    Verify that the XML we get out of `to_xml` matches the input.
    """
    bound_object = cls.from_xml(raw_xml)
    encoded_xml = bound_object.to_xml()
    ok_(eq_xml(etree.XML(encoded_xml), etree.XML(raw_xml)))


def test_trivial_from_xml():
    """
    Verify XML decoding with Trivial class.
    """
    for raw_xml in ["<trivial/>",
                    "<trivial></trivial>",
                    "<trivial><ignore>this</ignore></trivial>"]:
        yield assert_generates_equivalent_xml, Trivial, raw_xml
