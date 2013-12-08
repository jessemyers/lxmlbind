"""
Example objects for testing.
"""

from lxmlbind.api import Base, Property, tag


class Trivial(Base):
    pass


class Person(Base):
    first = Property("first")
    last = Property("last")


class Address(Base):
    street_number = Property("street/number", get_type=int)
    street_name = Property("street/name")
    city = Property("city")
    state = Property("state")
    zip_code = Property("zipCode", get_type=int)


class AddressBookEntry(Base):
    person = Property("person", type=Person)
    address = Property("address", type=Address)


@tag("metadata-string")
class JenkinsMetadataString(Base):
    """
    Example taken from Jenkins Metadata plugin string encoding:

        <metadata-string>
          <name>foo</name>
          <description></description>
          <parent class="metadata-tree" reference="../../.."/>
          <generated>true</generated>
          <exposedToEnvironment>false</exposedToEnvironment>
          <value>bar</value>
        </metadata-string>

    """
    def get_bool(text):
        return text != "false"

    def set_bool(value):
        return "true" if value else "false"

    name = Property("name")
    description = Property("description")
    parent = Property("parent", **{"class": "metadata-tree", "reference": "../../.."})
    generated = Property("generated", get_type=get_bool, set_type=set_bool)
    exposed = Property("exposedToEnvironment", get_type=get_bool, set_type=set_bool)
    value = Property("value")
