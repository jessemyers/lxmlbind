from nose.tools import assert_raises, eq_

from lxmlbind.api import Base, Dict, of, tag, key
from lxmlbind.tests.test_person import Person


class Ignore(Base):
    pass


@tag("dict")
@of(Person, Ignore)
@key(lambda item: getattr(item, "first", None))
class KeyDict(Dict):
    """
    Example using `key()`.
    """
    pass


def test_key():
    """
    Ensure that dict functions work for custom keys.
    """
    key_dict = KeyDict()
    eq_(len(key_dict), 0)

    person1 = Person(first="John", last="Smith")
    person2 = Person(first="Jane", last="Doe")

    key_dict.add(person1)
    key_dict.add(person2)

    eq_(len(key_dict), 2)
    eq_(key_dict["John"], person1)
    eq_(key_dict["Jane"], person2)

    del key_dict["Jane"]

    eq_(len(key_dict), 1)
    eq_(key_dict["John"], person1)
    with assert_raises(KeyError):
        key_dict["Jane"]


def test_empty_key():
    """
    Ensure that empty keys are added as a list.
    """
    key_dict = KeyDict()
    eq_(len(key_dict), 0)

    key_dict.add(Ignore())
    key_dict.add(Ignore())

    eq_(key_dict.keys(), [])
    eq_(key_dict.values(), [])
    eq_(key_dict.items(), [])

    eq_(len(key_dict), 2)
    with assert_raises(KeyError):
        key_dict[None]
