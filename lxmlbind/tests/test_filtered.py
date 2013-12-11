from textwrap import dedent

from nose.tools import eq_

from lxmlbind.api import List, Property


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


def test_filtered():
    """
    Test filtering.
    """
    filtered1 = Filtered()
    eq_(filtered1.foo, None)
    eq_(filtered1.bar, None)
    filtered1.foo = "foo"
    filtered1.bar = "bar"
    eq_(filtered1.foo, "foo")
    eq_(filtered1.bar, "bar")

    xml = dedent("""\
        <filtered>
          <value type="foo">foo</value>
          <value type="bar">bar</value>
        </filtered>""")
    filtered2 = Filtered.from_xml(xml)
    eq_(filtered2.foo, "foo")
    eq_(filtered2.bar, "bar")
    eq_(filtered1, filtered2)
