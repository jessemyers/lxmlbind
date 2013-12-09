"""
Examples taken from Jenkins XML configurations.

Several examples come from the Jenkins Metadata plugin.
"""
from textwrap import dedent

from nose.tools import eq_

from lxmlbind.api import Base, List, LongProperty, Property, tag


def get_bool(element, parent):
    if element.text is None:
        return None
    return element.text != "false"


def set_bool(element, value, parent):
    if value is None:
        element.text = None
    else:
        element.text = "true" if value else "false"


class BoolProperty(Property):
    def __init__(self,
                 path=None,
                 get_func=get_bool,
                 set_func=set_bool,
                 default=False,
                 *args,
                 **kwargs):
        super(BoolProperty, self).__init__(path=path,
                                           get_func=get_func,
                                           set_func=set_func,
                                           default=default,
                                           *args,
                                           **kwargs)


def set_parent_attributes(element, instance):
    element.attrib.update({
        "class": "metadata-tree" if instance._parent is None else instance._parent.tag(),
        "reference": "../../..",
    })


class MetadataBase(Base):
    """
    All of the main Metadata types share a common set of attributes: `description`,
    `parent`, `generated`, and `exposedToEnvironent`. This base class defines those
    attributes with default behaviors.
    """
    description = Property(auto=True)
    parent = Property(auto=True, attributes_func=set_parent_attributes)
    generated = BoolProperty(auto=True)
    exposed = BoolProperty("exposedToEnvironment", auto=True)


@tag("metadata-string")
class MetadataString(MetadataBase):
    name = Property()
    value = Property()


@tag("metadata-number")
class MetadataNumber(MetadataBase):
    name = Property()
    value = LongProperty()


@tag("metadata-date")
class MetadataDate(MetadataBase):
    name = Property()
    time = LongProperty("value/time")
    timezone = Property("value/timezone")
    checked = BoolProperty()


class Children(List):
    @classmethod
    def of(cls):
        def make_metadata(element, parent=None):
            tag_to_class = {
                "metadata-date": MetadataDate,
                "metadata-number": MetadataNumber,
                "metadata-string": MetadataString,
                "metadata-tree": MetadataTree,
            }
            return tag_to_class[element.tag](element, parent)
        return make_metadata


@tag("metadata-tree")
class MetadataTree(MetadataBase):
    children = Children.property(**{"class": "linked-list"})


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


def test_jenkinsmetadatatree():
    string1 = MetadataString()
    string1.name = "foo"
    string1.value = "bar"

    tree1 = MetadataTree()
    tree1.children.append(string1)

    xml = dedent("""\
        <metadata-tree>
          <description></description>
          <parent class="metadata-tree" reference="../../.."/>
          <generated>false</generated>
          <exposedToEnvironment>false</exposedToEnvironment>
          <children class="linked-list">
            <metadata-string>
              <name>foo</name>
              <description></description>
              <parent class="metadata-tree" reference="../../.."/>
              <generated>false</generated>
              <exposedToEnvironment>false</exposedToEnvironment>
              <value>bar</value>
            </metadata-string>
          </children>
        </metadata-tree>""")
    tree2 = MetadataTree.from_xml(xml)
    eq_(tree2.description, None)
    eq_(tree2.parent, None)
    eq_(tree2.generated, False)
    eq_(tree2.exposed, False)
    eq_(len(tree2.children), 1)
    eq_(tree2.children[0].__class__, MetadataString)
    eq_(tree2.children[0].name, "foo")

    eq_(tree1, tree2)
