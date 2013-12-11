from nose.tools import assert_raises, eq_, ok_

from lxmlbind.api import Dict, of, tag
from lxmlbind.tests.test_address import Address
from lxmlbind.tests.test_person import Person


@tag("dict")
@of(Address, Person)
class PersonAddressDict(Dict):
    """
    Example using typed dict.
    """
    pass


def test_person_address_dict():
    """
    Verify dict operations.
    """
    person1 = Person()
    person1.first = "John"

    person2 = Person()
    person2.first = "Jane"

    address = Address()
    address.city = "Springfield"

    # empty collection
    collection = PersonAddressDict()

    eq_(len(collection), 0)
    ok_("address" not in collection)
    ok_("person" not in collection)
    with assert_raises(KeyError):
        collection["address"]
    with assert_raises(KeyError):
        collection["person"]

    # set item
    collection["person"] = person1

    eq_(len(collection), 1)
    ok_("person" in collection)
    eq_(collection["person"], person1)
    eq_(set(collection.keys()), {"person"})
    eq_(set(collection.values()), {person1})
    eq_(set(collection.items()), {("person", person1)})

    # add item
    collection.add(address)

    eq_(len(collection), 2)
    ok_("address" in collection)
    eq_(collection["address"], address)
    eq_(set(collection.keys()), {"address", "person"})
    eq_(set(collection.values()), {address, person1})
    eq_(set(collection.items()), {("address", address), ("person", person1)})

    # delete item
    del collection["address"]
    eq_(len(collection), 1)
    ok_("address" not in collection)
    with assert_raises(KeyError):
        collection["address"]
    eq_(set(collection.keys()), {"person"})
    eq_(set(collection.values()), {person1})
    eq_(set(collection.items()), {("person", person1)})

    # adding duplicate key
    collection.add(person2)

    eq_(len(collection), 1)
    eq_(collection["person"], person2)
