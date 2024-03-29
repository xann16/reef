from ...settings_base import SettingsBase
from .project_languages_cpp_settings import ProjectLanguagesCppSettings


class ProjectLanguagesSettings(SettingsBase):
    '''
    Contains project settings specific to programming languages.
    '''

    def __init__(self,
                 obj, *,
                 cpp=None):
        '''
        Constructs ProjectLanguagesSettings object from item dictionary or manual property value overrides.
        '''
        self.cpp = cpp if cpp is not None else (ProjectLanguagesCppSettings(obj['cpp']) if 'cpp' in obj else None)

    @property
    def cpp(self):
        ''' Contains project settings specific for the C++ language. '''
        return self._cpp if self._cpp is not None else ProjectLanguagesCppSettings()

    @cpp.setter
    def cpp(self, cpp):
        ''' Contains temporary build settings for a project. '''
        if cpp is not None:
            if not isinstance(cpp, ProjectLanguagesCppSettings):
                raise ValueError("'cpp' property must be an instance of ProjectLanguagesCppSettings class.")
        self._cpp = cpp


    def to_dict(self):
        ''' Returns ProjectLanguagesSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}

        if self._cpp is not None:
            result['cpp'] = self.cpp.to_dict()

        return result if any(result) else None

