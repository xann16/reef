"""Provides base class for objects representing settings data."""

from typing import Any, Iterable, Tuple

_SETTINGS_STR_SPACES_PER_INDENT_LEVEL = 2
_SETTINGS_STR_LIST_POINT_CHARACTER = "-"
_SETTINGS_STR_VALUE_SEPARATOR = ":"


class SettingsBase:
    """A common base class for settings objects.

    It provides certain functionalities that makes easier to handle
    common use cases like:

    - getting and setting its properties using string keys,
    - handling paths for nested objects and arrays,
    - printing contents of settings,
    - facilities to simplify data serialization and deserialization.
    """

    def get(self, path: str) -> Any:
        """Returns value associated with given property path."""
        path_tail, child = self.__expand_path(path)
        return self.__get_value(path) if path_tail is None else child.get(path_tail)

    def set(self, path: str, value: Any) -> None:
        """Sets value of property associated with given path."""
        path_tail, child = self.__expand_path(path)
        if path_tail is None:
            self.__set_value(path, value)
        else:
            child.set(path_tail, value)

    def is_set(self, path: str) -> bool:
        """Checks whether property given by name is set.

        Note, that property is not set when the value of field associated with that property
        (i.e. with '_' prefix) is None. This does not account for any default values.
        """
        path_tail, child = self.__expand_path(path)
        return (not self.__is_property_unset(path)) if path_tail is None else child.is_set(path_tail)

    def unset(self, path: str) -> None:
        """Unsets value of property associated with given path."""
        path_tail, child = self.__expand_path(path)
        if path_tail is None:
            self.__unset_value(path)
        else:
            child.unset(path_tail)

    def to_string(self, *, indent_level: int = 0, skip_unset: bool = False, recurse: bool = True) -> str:
        """Returns stringified representation of all object properties and its values.

        Arguments:

        - indent_level (int) - current level of indentation to be used for nested objects,
        - skip_unset (bool) - if true, unset properties (with value None) are not stringified at all,
        - recurse (bool) - if true, nested objects are also expanded and stringified.
        """
        return self._str_properties(indent_level, skip_unset, recurse)

    def __str__(self):
        """Returns full string representation of a settings object."""
        return self.to_string()

    def __repr__(self):
        """Returns flat string representation of a setting object with basic info."""
        type_str = str(type(self))
        name_str = self.get("name") if self.__is_property("name") else "Unknown"
        return f"Object '{name_str}' of type '{type_str}':\n{self.to_string(recurse=False)}"

    ### IMPLEMENTATION DETAILS:

    def __is_property(self, name: str) -> bool:
        """Checks whether given string is a name of this object's @property field.

        In addition, names starting with underscore ('_') are filtered out as private.
        """
        try:
            return False if name.startswith("_") else isinstance(getattr(type(self), name), property)
        except AttributeError:
            return False

    def __is_property_readonly(self, name: str) -> bool:
        """Checks whether property given by name is read-only.

        Note, that property is read-only if it does not defie a setter.
        """
        return getattr(type(self), name).fset is None

    def __is_property_backed_by_field(self, name: str) -> bool:
        """Checks whether property given by name is backed by data member.

        Note, that property is packed by data member if it defines a field with exactly
        the same ame as the property prefixed with an underscore ('_').
        """
        return ("_" + name) in dir(self)

    def __is_property_unset(self, name: str) -> bool:
        """Checks whether property given by name is unset.

        Note, that property is unset when the value of field associated with that property
        (i.e. with '_' prefix) is None. This does not account for any default values.
        """
        try:
            return getattr(self, "_" + name) is None
        except AttributeError:
            return True

    def __list_property_names(self) -> Iterable[str]:
        """Returns iterable over stringified names of all fields marked as @property."""
        return (name for name in dir(self) if self.__is_property(name))

    def __get_line_header(self, indent_level: int) -> str:
        """Returns initial part of line for string representing a property at given indent level."""
        return f" {'':^{indent_level * _SETTINGS_STR_SPACES_PER_INDENT_LEVEL}}{_SETTINGS_STR_LIST_POINT_CHARACTER}"

    def _str_properties(self, indent_level: int, skip_unset: bool, recurse: bool) -> str:
        """Returns stringified representation of all object properties and its values.

        Arguments:

        - indent_level (int) - current level of indentation to be used for nested objects,
        - skip_unset (bool) - if true, unset properties (with value None) are not stringified at all,
        - recurse (bool) - if true, nested objects are also expanded and stringified.
        """
        result = ""
        for property_name in self.__list_property_names():
            result += f"{self.__str_property(property_name, indent_level, skip_unset, recurse)}\n"
        return result

    def __str_property(self, name: str, indent_level: int, skip_unset: bool, recurse: bool) -> str:
        """Returns stringified representation of object property and its value.

        Arguments:

        - name (string) - name of a property to be stringified,
        - indent_level (int) - current level of indentation to be used for nested objects,
        - skip_unset (bool) - if true, unset properties (with value None) are not stringified at all,
        - recurse (bool) - if true, nested objects are also expanded and stringified.
        """
        if skip_unset and self.__is_property_unset(name):
            return ""

        value = getattr(self, name)
        if isinstance(value, SettingsBase):
            if recurse:
                value_str = f"\n{value._str_properties(indent_level + 1, skip_unset, recurse)}"
            else:
                value_str = f"<object '{type(value)}'>"
        else:
            value_str = str(value)

        return f"{self.__get_line_header(indent_level)} {name}{_SETTINGS_STR_VALUE_SEPARATOR} {value_str}"

    def __assert_has_property(self, name: str) -> None:
        """Checks if property with given name is defined for object and throws if it does not."""
        if not self.__is_property(name):
            raise KeyError(f"No property '{name}' found in class '{type(self)}'")

    def __expand_path(self, path: str) -> Tuple[str, Any]:
        """Helper function to recurse down the nested settings structure.

        Given path returns either (1) None and None - when given object is the target item in the path,
        or otherwise (2) tail of the path (without head) and nested settings object pointed by the head.
        """
        if "." not in path:
            self.__assert_has_property(path)
            return None, None
        tokens = path.split(".", 1)
        self.__assert_has_property(tokens[0])
        child = getattr(self, tokens[0])
        if not isinstance(child, SettingsBase):
            raise KeyError(f"Object '{tokens[0]}' contains no further nested properties.")
        return tokens[1], child

    def __get_value(self, key: str) -> Any:
        """Returns value associated with given property name (key)."""
        self.__assert_has_property(key)
        return getattr(self, key)

    def __set_value(self, key: str, value: Any) -> None:
        """Sets value of property associated with given name (key)."""
        self.__assert_has_property(key)
        if self.__is_property_readonly(key):
            raise RuntimeError(f"Property '{key}' of class '{type(self)}' cannot be set. It is read-only.")
        return setattr(self, key, value)

    def __unset_value(self, key: str) -> None:
        """Unsets value of property associated with given name (key)."""
        self.__assert_has_property(key)
        if self.__is_property_readonly(key):
            raise RuntimeError(f"Property '{key}' of class '{type(self)}' cannot be unset. It is read-only.")
        if not self.__is_property_backed_by_field(key):
            field_name = "_" + key
            raise RuntimeError(
                f"Property '{key}' of class '{type(self)}' cannot be unset."
                + f"It is not backed by the standard '{field_name}' field."
            )
        return setattr(self, "_" + key, None)
