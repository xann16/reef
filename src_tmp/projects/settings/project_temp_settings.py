from ...settings_base import SettingsBase
from .project_temp_build_settings import ProjectTempBuildSettings
from .project_temp_hierarchy_settings import ProjectTempHierarchySettings


def __is_int(value):
    try:
        int(value)
        return True
    except:
        return False


class ProjectTempSettings(SettingsBase):
    """
    Contains temporary project settings.
    """

    def __init__(self, obj, *, version=None, build=None, hierarchy=None):
        """
        Constructs ProjectTempSettings object from item dictionary or manual property value overrides.
        """
        self.version = version if version is not None else (obj["version"] if "version" in obj else None)
        self.build = (
            build if build is not None else (ProjectTempBuildSettings(obj["build"]) if "build" in obj else None)
        )
        self.hierarchy = (
            hierarchy
            if hierarchy is not None
            else (ProjectTempHierarchySettings(obj["hierarchy"]) if "hierarchy" in obj else None)
        )

    @property
    def version(self):
        """Constant project version if used."""
        return self._version if self._version is not None else "0.1.0"

    @property
    def version_major(self):
        """Major part of a constant project version if used."""
        return int(self.version.split(".")[0])

    @property
    def version_minor(self):
        """Minor part of a constant project version if used."""
        return int(self.version.split(".")[1])

    @property
    def version_patch(self):
        """Patch part of a constant project version if used."""
        return int(self.version.split(".")[2])

    @version.setter
    def version(self, version):
        """Constant project version if used."""
        # TODO: proper version string validation - type-dependent.
        if version is not None:
            if not isinstance(version, str):
                raise ValueError("'version' property must be a string.")
            tokens = version.split(".")
            if len(tokens) != 3 or not all(__is_int(t) for t in tokens):
                raise ValueError("'version' must have proper format: '[INT].[INT].[INT]'.")
        self._version = version

    @property
    def build(self):
        """Contains temporary build settings for a project."""
        return self._build if self._build is not None else ProjectTempBuildSettings()

    @build.setter
    def build(self, build):
        """Contains temporary build settings for a project."""
        if build is not None:
            if not isinstance(build, ProjectTempBuildSettings):
                raise ValueError("'build' property must be an instance of ProjectTempBuildSettings class.")
        self._build = build

    @property
    def hierarchy(self):
        """Contains temporary directory structure settings for a project."""
        return self._hierarchy if self._hierarchy is not None else ProjectTempHierarchySettings()

    @hierarchy.setter
    def hierarchy(self, hierarchy):
        """Contains temporary build settings for a project."""
        if hierarchy is not None:
            if not isinstance(hierarchy, ProjectTempHierarchySettings):
                raise ValueError("'hierarchy' property must be an instance of ProjectTempHierarchySettings class.")
        self._hierarchy = hierarchy

    def to_dict(self):
        """Returns ProjectTempHierarchySettings as a dictionary with its properties (convenient for conversion to JSON)."""
        result = {}

        if self._version is not None:
            result["version"] = self.version
        if self._build is not None:
            result["build"] = self.build.to_dict()
        if self._hierarchy is not None:
            result["hierarchy"] = self.hierarchy.to_dict()

        return result if any(result) else None
