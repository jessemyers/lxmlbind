"""
Examples taken from Jenkins XML configurations.

Several examples come from the Jenkins Metadata plugin.
"""
from textwrap import dedent

from nose.tools import eq_

from lxmlbind.api import Base, Property, tag


def get_bool(text):
    return text != "false"


def set_bool(value):
    return "true" if value else "false"


class MetadataBase(Base):
    """
    All of the main Metadata types share a common set of attributes:

        <name>foo</name>
        <description></description>
        <parent class="metadata-tree" reference="../../.."/>
        <generated>true</generated>
        <exposedToEnvironment>false</exposedToEnvironment>
        <value>bar</value>
    """
    name = Property("name")
    description = Property("description", auto=True)
    parent = Property("parent", auto=True, **{"class": "metadata-tree", "reference": "../../.."})
    generated = Property("generated", auto=True, default=False, get_type=get_bool, set_type=set_bool)
    exposed = Property("exposedToEnvironment", auto=True, default=False, get_type=get_bool, set_type=set_bool)


@tag("metadata-string")
class MetadataString(MetadataBase):
    value = Property("value")


@tag("metadata-number")
class MetadataNumber(MetadataBase):
    value = Property("value", get_type=long)


@tag("metadata-date")
class MetadataDate(MetadataBase):
    time = Property("value/time", get_type=long)
    timezone = Property("value/timezone")
    checked = Property("checked", get_type=get_bool, set_type=set_bool)


def test_metadatastring():
    string1 = MetadataString()
    string1.name = "foo"
    string1.value = "bar"

    xml = dedent("""\
        <metadata-string>
          <name>foo</name>
          <description></description>
          <parent class="metadata-tree" reference="../../.."/>
          <generated>false</generated>
          <exposedToEnvironment>false</exposedToEnvironment>
          <value>bar</value>
        </metadata-string>""")
    string2 = MetadataString.from_xml(xml)
    eq_(string2.name, "foo")
    eq_(string2.description, None)
    eq_(string2.parent, None)
    eq_(string2.generated, False)
    eq_(string2.exposed, False)
    eq_(string2.value, "bar")

    eq_(string1, string2)


def test_metadatanumber():
    number1 = MetadataNumber()
    number1.name = "foo"
    number1.value = 3

    xml = dedent("""\
        <metadata-number>
          <name>foo</name>
          <description></description>
          <parent class="metadata-tree" reference="../../.."/>
          <generated>false</generated>
          <exposedToEnvironment>false</exposedToEnvironment>
          <value>3</value>
        </metadata-number>""")
    number2 = MetadataNumber.from_xml(xml)
    eq_(number2.name, "foo")
    eq_(number2.description, None)
    eq_(number2.parent, None)
    eq_(number2.generated, False)
    eq_(number2.exposed, False)
    eq_(number2.value, 3)

    eq_(number1, number2)


def test_jenkinsmetadatadate():
    date1 = MetadataDate()
    date1.name = "time"
    date1.generated = True
    date1.exposed = False
    date1.checked = False
    date1.time = 1385409911044
    date1.timezone = "America/Los_Angeles"

    xml = dedent("""\
        <metadata-date>
          <name>time</name>
          <description></description>
          <parent class="metadata-tree" reference="../../.."/>
          <generated>true</generated>
          <exposedToEnvironment>false</exposedToEnvironment>
          <value>
            <time>1385409911044</time>
            <timezone>America/Los_Angeles</timezone>
          </value>
          <checked>false</checked>
        </metadata-date>""")
    date2 = MetadataDate.from_xml(xml)
    eq_(date2.name, "time")
    eq_(date2.description, None)
    eq_(date2.parent, None)
    eq_(date2.generated, True)
    eq_(date2.exposed, False)
    eq_(date2.time, 1385409911044)
    eq_(date2.timezone, "America/Los_Angeles")
    eq_(date2.checked, False)

    eq_(date1, date2)
