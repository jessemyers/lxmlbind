from textwrap import dedent

from nose.tools import eq_

from lxmlbind.api import Base, IntProperty, Property


class Address(Base):
    """
    Example using typed properties and non-trivial property path.
    """
    street_number = IntProperty("street/number")
    street_name = Property("street/name")
    city = Property()
    state = Property()
    zip_code = IntProperty("zipCode")


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
