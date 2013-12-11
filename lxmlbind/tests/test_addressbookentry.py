from textwrap import dedent

from nose.tools import eq_

from lxmlbind.api import Base
from lxmlbind.tests.test_address import Address
from lxmlbind.tests.test_person import Person


class AddressBookEntry(Base):
    """
    Example using nested types.
    """
    person = Person.property()
    address = Address.property()


def test_nested_types():
    """
    Test nested types.
    """
    entry1 = AddressBookEntry()
    entry1.person.first = "John"
    entry1.person.last = "Doe"
    entry1.address.street_number = "1600"
    entry1.address.street_name = "Pennsylvania Ave"
    entry1.address.city = "Washington"
    entry1.address.state = "DC"
    entry1.address.zip_code = 20500
    eq_(entry1.person._parent, entry1)
    eq_(entry1.address._parent, entry1)

    xml = dedent("""\
        <addressBookEntry>
          <person type="object">
            <first>John</first>
            <last>Doe</last>
          </person>
          <address>
            <street>
              <number>1600</number>
              <name>Pennsylvania Ave</name>
            </street>
            <city>Washington</city>
            <state>DC</state>
            <zipCode>20500</zipCode>
          </address>
        </addressBookEntry>""")
    entry2 = AddressBookEntry.from_xml(xml)
    eq_(entry2.person.first, "John")
    eq_(entry2.person.last, "Doe")
    eq_(entry2.address.street_number, 1600)
    eq_(entry2.address.street_name, "Pennsylvania Ave")
    eq_(entry2.address.city, "Washington")
    eq_(entry2.address.state, "DC")
    eq_(entry2.address.zip_code, 20500)
    eq_(entry1, entry2)
