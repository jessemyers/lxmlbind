"""
Property descriptor tests.
"""
from textwrap import dedent

from nose.tools import assert_raises, eq_

from lxmlbind.api import Property
from lxmlbind.tests.example import Address, Person


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
    eq_(person.to_xml(), "<person><first>John</first><last>Doe</last></person>")


def test_person_delete():
    """
    Verify data descriptor __delete__ against Person instance.
    """
    person = Person.from_xml("<person><first>John</first></person>")

    # __delete__ works
    del person.first
    eq_(person.first, None)
    eq_(str(person), "<person/>")

    # cannot delete unassigned property
    with assert_raises(AttributeError) as capture:
        del person.last
    eq_(capture.exception.message, "'<class 'lxmlbind.tests.example.Person'>' object has no attribute 'last'")


def test_address_types():
    """
    Test type processing using Address instance.
    """
    address1 = Address()
    address1.street_number = "1600"
    address1.street_name = "Pennsylvania Ave"
    address1.city = "Washington"
    address1.state = "DC"
    address1.zip_code = 20500

    xml = dedent("""\
        <address>
          <street>
            <number>1600</number>
            <name>Pennsylvania Ave</name>
          </street>
          <city>Washington</city>
          <state>DC</state>
          <zipCode>20500</zipCode>
        </address>""")
    address2 = Address.from_xml(xml)

    # street_number and zip_code are int, no matter how assigned
    eq_(type(address1.street_number), int)
    eq_(type(address1.zip_code), int)
    eq_(type(address2.street_number), int)
    eq_(type(address2.zip_code), int)

    # and both forms are equivalent
    eq_(address1, address2)
