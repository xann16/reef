from typing import Any, Type

import pytest

from reef.common.settings_base import SettingsBase

### =========== TEST TYPES THAT DERIVE FROM SettingsBase =========== ###


class Empty(SettingsBase):
    pass


class SimpleReadOnly(SettingsBase):
    def __init__(self) -> None:
        self._p: int = 42

    @property
    def p(self) -> int:
        return self._p


class ConstantField(SettingsBase):
    @property
    def p(self) -> int:
        return 42


class InvalidField(SettingsBase):
    def __init__(self) -> None:
        self._x: int = 42

    @property
    def p(self) -> int | None:
        return self._x

    @p.setter
    def p(self, value: int) -> None:
        self._x = value


class Simple(SettingsBase):
    def __init__(self) -> None:
        self._p: Any = None

    @property
    def p(self) -> Any:
        return self._p

    @p.setter
    def p(self, value: Any) -> None:
        self._p = value


class Multi(SettingsBase):
    def __init__(self) -> None:
        self._any: Any = None
        self._num: int | None = None
        self._name: str | None = "Default"
        self._obj: Type[SettingsBase] | None = None

    @property
    def any(self) -> Any:
        return self._any

    @any.setter
    def any(self, value: Any) -> None:
        self._any = value

    @property
    def num(self) -> int:
        return self._num if self._num is not None else 42

    @num.setter
    def num(self, value: int) -> None:
        self._num = value

    @property
    def name(self) -> str | None:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def obj(self) -> Type[SettingsBase] | None:
        return self._obj

    @obj.setter
    def obj(self, value: Type[SettingsBase]) -> None:
        self._obj = value


### =========== TESTS =========== ###

# ----- TESTS FOR Empty TYPE ----- #


def test_empty_settings_get_should_raise_error():
    s = Empty()

    with pytest.raises(KeyError) as ex:
        s.get("p")

    assert "'p'" in str(ex.value)
    assert "Empty" in str(ex.value)


def test_empty_settings_set_should_raise_error():
    s = Empty()

    with pytest.raises(KeyError) as ex:
        s.set("p", "p")

    assert "'p'" in str(ex.value)
    assert "Empty" in str(ex.value)


def test_empty_settings_is_set_should_raise_error():
    s = Empty()

    with pytest.raises(KeyError) as ex:
        s.is_set("p")

    assert "'p'" in str(ex.value)
    assert "Empty" in str(ex.value)


def test_empty_settings_unset_should_raise_error():
    s = Empty()

    with pytest.raises(KeyError) as ex:
        s.unset("p")

    assert "'p'" in str(ex.value)
    assert "Empty" in str(ex.value)


def test_empty_settings_string_should_be_empty():
    s = Empty()

    s_str = str(s)

    assert s_str == ""


def test_empty_settings_repr_should_contain_type_info():
    s = Empty()

    s_repr = repr(s)

    assert "Empty" in s_repr


# ----- TESTS FOR SimpleReadOnly TYPE ----- #


def test_readonly_settings_get_should_get_initial_value():
    s = SimpleReadOnly()

    value = s.get("p")

    assert value == 42
    assert value == s.p


def test_readonly_settings_set_should_raise_error():
    s = SimpleReadOnly()

    with pytest.raises(RuntimeError) as ex:
        s.set("p", "p")

    assert "'p'" in str(ex.value)
    assert "SimpleReadOnly" in str(ex.value)
    assert "read-only" in str(ex.value)


def test_readonly_settings_is_set_should_be_true():
    s = SimpleReadOnly()

    is_value_set = s.is_set("p")

    assert is_value_set


def test_readonly_settings_unset_should_raise_error():
    s = SimpleReadOnly()

    with pytest.raises(RuntimeError) as ex:
        s.unset("p")

    assert "'p'" in str(ex.value)
    assert "SimpleReadOnly" in str(ex.value)
    assert "read-only" in str(ex.value)


def test_readonly_settings_string_should_contain_property_value():
    s = SimpleReadOnly()

    s_str = str(s)

    assert "p" in s_str
    assert "42" in s_str


def test_readonly_settings_repr_should_contain_type_and_property_info():
    s = SimpleReadOnly()

    s_repr = repr(s)

    assert "SimpleReadOnly" in s_repr
    assert "p" in s_repr
    assert "42" in s_repr


# ----- TESTS FOR ConstantField TYPE ----- #


def test_constant_settings_get_should_get_constant_value():
    s = ConstantField()

    value = s.get("p")

    assert value == 42
    assert value == s.p


def test_constant_settings_set_should_raise_error():
    s = ConstantField()

    with pytest.raises(RuntimeError) as ex:
        s.set("p", "p")

    assert "'p'" in str(ex.value)
    assert "ConstantField" in str(ex.value)
    assert "read-only" in str(ex.value)


def test_constant_settings_is_set_should_be_false():
    s = ConstantField()

    is_value_set = s.is_set("p")

    assert not is_value_set


def test_constant_settings_unset_should_raise_error():
    s = ConstantField()

    with pytest.raises(RuntimeError) as ex:
        s.unset("p")

    assert "'p'" in str(ex.value)
    assert "ConstantField" in str(ex.value)
    assert "read-only" in str(ex.value)


def test_constant_settings_string_should_contain_property_value():
    s = ConstantField()

    s_str = str(s)

    assert "p" in s_str
    assert "42" in s_str


def test_constant_settings_repr_should_contain_type_and_property_info():
    s = ConstantField()

    s_repr = repr(s)

    assert "ConstantField" in s_repr
    assert "p" in s_repr
    assert "42" in s_repr


# ----- TESTS FOR InvalidField TYPE ----- #


def test_invalid_settings_get_should_get_initial_value():
    s = InvalidField()

    value = s.get("p")

    assert value == 42
    assert value == s.p


def test_invalid_settings_set_should_change_property_value():
    s = InvalidField()

    s.set("p", 7)

    assert s.get("p") == 7
    assert s.p == 7
    assert not s.is_set("p")  # misleading value due to malformed backing field


def test_invalid_settings_is_set_should_be_false():
    s = InvalidField()

    is_value_set = s.is_set("p")

    assert not is_value_set


def test_invalid_settings_unset_should_raise_error():
    s = InvalidField()

    with pytest.raises(RuntimeError) as ex:
        s.unset("p")

    assert "'p'" in str(ex.value)
    assert "InvalidField" in str(ex.value)
    assert "not backed" in str(ex.value)


def test_invalid_settings_string_should_contain_property_value():
    s = InvalidField()

    s_str = str(s)

    assert "p" in s_str
    assert "42" in s_str


def test_invalid_settings_repr_should_contain_type_and_property_info():
    s = InvalidField()

    s_repr = repr(s)

    assert "InvalidField" in s_repr
    assert "p" in s_repr
    assert "42" in s_repr


# ----- TESTS FOR Simple TYPE ----- #


def test_simple_settings_get_should_get_initial_value():
    s = Simple()

    value = s.get("p")

    assert value is None
    assert value == s.p


def test_simple_settings_set_should_change_property_value():
    s = Simple()

    s.set("p", 42)

    assert s.get("p") == 42
    assert s.p == 42
    assert s.is_set("p")


def test_simple_settings_property_setter_should_change_property_value():
    s = Simple()

    s.p = 42

    assert s.get("p") == 42
    assert s.p == 42
    assert s.is_set("p")


def test_simple_settings_is_set_should_be_false():
    s = Simple()

    is_value_set = s.is_set("p")

    assert not is_value_set


def test_simple_settings_unset_should_change_value_to_none():
    s = Simple()

    s.set("p", 42)
    s.unset("p")

    assert not s.is_set("p")
    assert s.p is None


def test_simple_settings_string_should_contain_property_value():
    s = Simple()

    s_str = str(s)

    assert "p" in s_str
    assert "None" in s_str


def test_simple_settings_repr_should_contain_type_and_property_info():
    s = Simple()

    s_repr = repr(s)

    assert "Simple" in s_repr
    assert "p" in s_repr
    assert "None" in s_repr


# ----- TESTS FOR Multi TYPE - String Representations ----- #


def test_settings_to_string_should_list_all_properties_recursively():
    s = Multi()
    s.any = "xxx"
    s.obj = Multi()
    s.obj.name = "SET"
    s.obj.obj = Multi()
    s.obj.obj.num = 12345

    s_str = str(s)

    assert s_str.count("name") == 3
    assert s_str.count("obj") == 3
    assert s_str.count("any") == 3
    assert s_str.count("num") == 3
    assert s_str.count("Default") == 2
    assert s_str.count("SET") == 1
    assert s_str.count("42") == 2
    assert s_str.count("12345") == 1
    assert s_str.count("xxx") == 1

    s_str = s.to_string()


def test_settings_to_string_optionally_should_list_all_properties_without_recursion():
    s = Multi()
    s.any = "xxx"
    s.obj = Multi()
    s.obj.name = "SET"
    s.obj.obj = Multi()
    s.obj.obj.num = 12345

    s_str = s.to_string(recurse=False)

    assert s_str.count("name") == 1
    assert s_str.count("obj") == 2
    assert s_str.count("object") == 1
    assert s_str.count("any") == 1
    assert s_str.count("num") == 1
    assert s_str.count("Default") == 1
    assert s_str.count("SET") == 0
    assert s_str.count("42") == 1
    assert s_str.count("12345") == 0
    assert s_str.count("xxx") == 1

    assert "Multi" in s_str


def test_settings_to_string_optionally_should_list_only_set_properties():
    s = Multi()
    s.any = "xxx"
    s.obj = Multi()
    s.obj.name = "SET"
    s.obj.obj = Multi()
    s.obj.obj.num = 12345

    s_str = s.to_string(skip_unset=True)

    assert s_str.count("name") == 3
    assert s_str.count("obj") == 2
    assert s_str.count("any") == 1
    assert s_str.count("num") == 1
    assert s_str.count("Default") == 2
    assert s_str.count("SET") == 1
    assert s_str.count("42") == 0
    assert s_str.count("12345") == 1
    assert s_str.count("xxx") == 1

    assert "None" not in s_str


# ----- TESTS FOR Multi TYPE - Nasted Objects and Paths - Get ----- #


def test_nested_settings_get_should_get_initial_values():
    s = Multi()
    s.name = "L1"
    s.obj = Multi()
    s.obj.name = "L2"
    s.obj.obj = Multi()
    s.obj.obj.name = "L3"

    assert s.get("name") == "L1"
    assert s.get("name") == s.name

    assert s.get("obj.name") == "L2"
    assert s.get("obj.name") == s.obj.name

    assert s.get("obj.obj.name") == "L3"
    assert s.get("obj.obj.name") == s.obj.obj.name

    assert s.get("obj.obj.any") is None
    assert s.get("obj.obj.any") == s.obj.obj.any

    assert s.get("obj.obj.num") == 42
    assert s.get("obj.obj.num") == s.obj.obj.num

    assert s.get("obj.obj.obj") is None
    assert s.get("obj.obj.obj") == s.obj.obj.obj

    assert s.get("obj").get("obj.num") == 42
    assert s.get("obj").get("obj.num") == s.obj.obj.num

    assert s.get("obj").get("obj").get("num") == 42
    assert s.get("obj").get("obj").get("num") == s.obj.obj.num


def test_nested_settings_get_from_nonexistent_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.get("x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.get("obj.x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)


def test_nested_settings_get_from_unset_should_raise_errors():
    s = Multi()

    with pytest.raises(KeyError) as ex:
        s.get("obj.name")

    assert "'obj'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.get("any.name")

    assert "'any'" in str(ex.value)


def test_nested_settings_get_from_nonobject_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.get("name.x")

    assert "'name'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.get("num.name")

    assert "'num'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.get("obj.name.x")

    assert "'name'" in str(ex.value)


# ----- TESTS FOR Multi TYPE - Nasted Objects and Paths - Set ----- #


def test_nested_settings_set_should_change_property_values():
    s = Multi()
    s.obj = Multi()
    s.obj.obj = Multi()

    s.set("name", "L1")

    assert s.get("name") == "L1"
    assert s.get("name") == s.name
    assert s.is_set("name")

    s.set("obj.name", "L2")

    assert s.get("obj.name") == "L2"
    assert s.get("obj.name") == s.obj.name
    assert s.is_set("obj.name")

    s.set("obj.obj.name", "L3")

    assert s.get("obj.obj.name") == "L3"
    assert s.get("obj.obj.name") == s.obj.obj.name
    assert s.is_set("obj.obj.name")


def test_nested_settings_set_from_nonexistent_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.set("x", 42)

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.set("obj.x", 42)

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)


def test_nested_settings_set_from_unset_should_raise_errors():
    s = Multi()

    with pytest.raises(KeyError) as ex:
        s.set("obj.name", "XXX")

    assert "'obj'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.set("any.name", "XXX")

    assert "'any'" in str(ex.value)


def test_nested_settings_set_from_nonobject_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.set("name.x", 42)

    assert "'name'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.set("num.name", 42)

    assert "'num'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.set("obj.name.x", 42)

    assert "'name'" in str(ex.value)


# ----- TESTS FOR Multi TYPE - Nasted Objects and Paths - IsSet ----- #


def test_nested_settings_is_set_should_return_proper_values():
    s = Multi()
    s.obj = Multi()
    s.obj.num = 42
    s.obj.obj = Multi()

    assert s.is_set("name")
    assert s.is_set("obj.name")
    assert s.is_set("obj.obj.name")

    assert not s.is_set("any")
    assert not s.is_set("obj.any")
    assert not s.is_set("obj.obj.any")

    assert not s.is_set("num")
    assert s.is_set("obj.num")
    assert not s.is_set("obj.obj.num")

    assert s.is_set("obj")
    assert s.is_set("obj.obj")
    assert not s.is_set("obj.obj.obj")


def test_nested_settings_is_set_from_nonexistent_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.is_set("x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.is_set("obj.x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)


def test_nested_settings_is_set_from_unset_should_raise_errors():
    s = Multi()

    with pytest.raises(KeyError) as ex:
        s.is_set("obj.name")

    assert "'obj'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.is_set("any.name")

    assert "'any'" in str(ex.value)


def test_nested_settings_is_set_from_nonobject_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.is_set("name.x")

    assert "'name'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.is_set("num.name")

    assert "'num'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.is_set("obj.name.x")

    assert "'name'" in str(ex.value)


# ----- TESTS FOR Multi TYPE - Nasted Objects and Paths - IsSet ----- #


def test_nested_settings_unset_should_set_properties_to_none():
    s = Multi()
    s.obj = Multi()
    s.obj.obj = Multi()

    assert s.is_set("name")
    s.unset("name")
    assert not s.is_set("name")

    assert s.is_set("obj.name")
    s.unset("obj.name")
    assert not s.is_set("obj.name")

    assert s.is_set("obj.obj.name")
    s.unset("obj.obj.name")
    assert not s.is_set("obj.obj.name")

    s.unset("obj")

    with pytest.raises(KeyError) as ex:
        s.is_set("obj.name")

    assert "'obj'" in str(ex.value)


def test_nested_settings_unset_from_nonexistent_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.unset("x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.unset("obj.x")

    assert "'x'" in str(ex.value)
    assert "Multi" in str(ex.value)


def test_nested_settings_unset_from_unset_should_raise_errors():
    s = Multi()

    with pytest.raises(KeyError) as ex:
        s.unset("obj.name")

    assert "'obj'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.unset("any.name")

    assert "'any'" in str(ex.value)


def test_nested_settings_unset_from_nonobject_should_raise_errors():
    s = Multi()
    s.obj = Multi()

    with pytest.raises(KeyError) as ex:
        s.unset("name.x")

    assert "'name'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.unset("num.name")

    assert "'num'" in str(ex.value)

    with pytest.raises(KeyError) as ex:
        s.unset("obj.name.x")

    assert "'name'" in str(ex.value)
