from ...settings_base import SettingsBase


class ProjectTempHierarchySettings(SettingsBase):
    """
    Contains temporary project settings related to project's directory structure.
    """

    _HIERARCHY_TYPES = ["default"]

    def __init__(self, obj, *, type=None, is_multiproject=None, separate_public_includes=None):
        """
        Constructs ProjectTempHierarchySettings object from item dictionary or manual property value overrides.
        """
        self.type = type if type is not None else (obj["type"] if "type" in obj else None)
        self.is_multiproject = (
            is_multiproject
            if is_multiproject is not None
            else (obj["is_multiproject"] if "is_multiproject" in obj else None)
        )
        self.separate_public_includes = (
            separate_public_includes
            if separate_public_includes is not None
            else (obj["separate_public_includes"] if "separate_public_includes" in obj else None)
        )

    @property
    def type(self):
        """Directory hierarchy type."""
        return self._type if self._type is not None else self._HIERARCHY_TYPES[0]

    @type.setter
    def type(self, type):
        """Directory hierarchy type."""
        if type is not None:
            if not isinstance(type, str):
                raise ValueError("'type' property must be a string.")
            if not type:
                raise ValueError("'type' property cannot be an empty string.")
            if type not in self._HIERARCHY_TYPES:
                raise ValueError(
                    f"'type' cannot be '{type}' (supported values include: {', '.join(self._HIERARCHY_TYPES)} )."
                )
        self._type = type

    @property
    def is_multiproject(self):
        """Indicates whether project hierarchy allows for multiple modules or just one."""
        return self._is_multiproject if self._is_multiproject else True

    @is_multiproject.setter
    def is_multiproject(self, is_multiproject):
        """Indicates whether project hierarchy allows for multiple modules or just one."""
        if is_multiproject is not None:
            if not isinstance(is_multiproject, bool):
                raise ValueError("'is_multiproject' property must be a boolean.")
        self._is_multiproject = is_multiproject

    @property
    def separate_public_includes(self):
        """Indicates whether project uses separate directory for public includes (headers) or not."""
        return self._separate_public_includes if self._separate_public_includes else True

    @separate_public_includes.setter
    def separate_public_includes(self, separate_public_includes):
        """Indicates whether project uses separate directory for public includes (headers) or not."""
        if separate_public_includes is not None:
            if not isinstance(separate_public_includes, bool):
                raise ValueError("'separate_public_includes' property must be a boolean.")
        self._separate_public_includes = separate_public_includes

    def to_dict(self):
        """Returns ProjectTempHierarchySettings as a dictionary with its properties (convenient for conversion to JSON)."""
        result = {}

        if self._type is not None:
            result["type"] = self.type
        if self._is_multiproject is not None:
            result["is_multiproject"] = self.is_multiproject
        if self._separate_public_includes is not None:
            result["separate_public_includes"] = self.separate_public_includes

        return result if any(result) else None
