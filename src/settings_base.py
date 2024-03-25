from typing import Iterable, Any

_SPACES_PER_INDENT_LEVEL = 2
_LIST_POINT_CHARACTER = '-'
_VALUE_SEPARATOR = ':'

class SettingsBase():

    def print_properties(self, *, 
                         indent_level: int = 0, 
                         skip_unset: bool = True,
                         recurse: bool = True) -> None:
        for property_name in self.__list_property_names():
            self.__print_property(property_name, indent_level, skip_unset, recurse)

    def __list_property_names(self) -> Iterable[str]:
        return (name for name in dir(self) if self.__is_property(name))

    def __print_property(self, property_name: str, indent_level: int, skip_unset: bool, recurse: bool) -> None:
        if not skip_unset and not self.__is_underlying_field_not_none(property_name):
            return
        self.__print_prefix(indent_level)
        print(property_name, end=_VALUE_SEPARATOR)

        value = getattr(self, property_name)
        if isinstance(value, SettingsBase):
            if recurse:
                print()
                value._print_properties(indent_level=indent_level + 1, skip_unset=skip_unset)
            else:
                print(f"<object {type(value)}>")
        else:
            print(' ' + str(value))

    def __is_property(self, name):
        if name.startswith('_'):
            return False
        try:
            return isinstance(getattr(type(self), name), property)
        except AttributeError:
            return False

    def __is_underlying_field_not_none(self, property_name: str) -> bool:
        field_name = '_' + property_name
        try:
            return getattr(self, field_name) is not None
        except AttributeError:
            return True

    def __print_prefix(self, indent_level: int) -> None:
        print((' ' * ((_SPACES_PER_INDENT_LEVEL * indent_level) + 1)) + _LIST_POINT_CHARACTER, end=' ')

    def __get_value(self, property_name: str) -> Any:
        if not self.__is_property(property_name):
            raise KeyError(f"No property '{property_name}' found in class '{type(self)}'")
        return getattr(self, property_name)

    def __set_value(self, property_name:str , value: Any) -> None:
        if not self.__is_property(property_name):
            raise KeyError(f"No property '{property_name}' found in class '{type(self)}'")
        return setattr(self, property_name, value)

    def get(self, path: str) -> Any:
        if '.' not in path:
            return self.__get_value(path)
        tokens = path.split('.', 2)
        child = getattr(self, tokens[0])
        if not isinstance(child, SettingsBase):
            raise KeyError(f"Object {tokens[0]} contains no further nested properties.")
        return child.get(tokens[1])

    def set(self, path: str, value: Any) -> None:
        if '.' not in path:
            return self.__set_value(path, value)
        tokens = path.split('.', 2)
        child = getattr(self, tokens[0])
        if not isinstance(child, SettingsBase):
            raise KeyError(f"Object {tokens[0]} contains no further nested properties.")
        child.set(tokens[1], value)

