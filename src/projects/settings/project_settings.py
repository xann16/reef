from .project_advanced_settings import ProjectAdvancedSettings
from .project_details_settings import ProjectDetailsSettings
from .project_cmake_settings import ProjectCMakeSettings
from .project_languages_settings import ProjectLanguagesSettings
from .project_temp_settings import ProjectTempSettings

class ProjectSettings():
    '''
    Contains project settings data.
    '''

    _SUPPORTED_LANGUAGES = ["cpp"]

    def __init__(self,
                 obj, *,
                 name=None,
                 name_short=None,
                 default_language=None,
                 details=None,
                 advanced=None,
                 languages=None,
                 cmake=None,
                 temp=None):
        '''
        Constructs ProjectSettings object from item dictionary or manual property value overrides.
        '''
        self.name = name if name is not None else (obj['name'] if 'name' in obj else None)
        self.name_short = name_short if name_short is not None else (obj['name_short'] if 'name_short' in obj else None)
        self.default_language = default_language if default_language is not None else (obj['default_language'] if 'default_language' in obj else None)
        self.details = details if details is not None else (ProjectDetailsSettings(obj['details']) if 'details' in obj else None)
        self.advanced = advanced if advanced is not None else (ProjectAdvancedSettings(obj['advanced']) if 'advanced' in obj else None)
        self.languages = languages if languages is not None else (ProjectLanguagesSettings(obj['languages']) if 'languages' in obj else None)
        self.cmake = cmake if cmake is not None else (ProjectCMakeSettings(obj['cmake']) if 'cmake' in obj else None)
        self.temp = temp if temp is not None else (ProjectTempSettings(obj['temp']) if 'temp' in obj else None)

        
    @property
    def name(self):
        ''' Project name. '''
        return self._name
    
    @name.setter
    def name(self, name):
        ''' Project name. '''
        if name is None:
            raise ValueError("'name' property cannot be None.")
        if not isinstance(name, str):
            raise ValueError("'name' property must be a string.")
        if not name:
            raise ValueError("'name' property cannot be an empty string")
        self._name = name

    @property
    def name_short(self):
        ''' Short version of project name. '''
        return self._name_short if self._name_short is not None else self.name
    
    @name_short.setter
    def name_short(self, name_short):
        ''' Short version of project name. '''
        if name_short is not None:
            if not isinstance(name_short, str):
                raise ValueError("'name_short' property must be a string.")
            if not name_short:
                raise ValueError("'name_short' property cannot be an empty string")
        self._name_short = name_short

    @property
    def default_language(self):
        ''' Default language used by the project. '''
        return self._default_language if self._default_language is not None else self._SUPPORTED_LANGUAGES[0]
    
    @default_language.setter
    def default_language(self, default_language):
        ''' Default language used by the project. '''
        if default_language is not None:
            if not isinstance(default_language, str):
                raise ValueError("'default_language' property must be a string.")
            if not default_language:
                raise ValueError("'default_language' property cannot be an empty string.")
            if default_language not in self._SUPPORTED_LANGUAGES:
                raise ValueError(f"'default_language' cannot be '{default_language}' (supported values include: {', '.join(self._SUPPORTED_LANGUAGES)} ).")
        self._default_language = type

    @property
    def details(self):
        ''' Contains detailed info project settings. '''
        return self._details if self._details is not None else ProjectDetailsSettings()
    
    @details.setter
    def details(self, details):
        ''' Contains detailed info project settings. '''
        if details is not None:
            if not isinstance(details, ProjectDetailsSettings):
                raise ValueError("'details' property must be an instance of ProjectDetailsSettings class.")
        self._details = details

    @property
    def advanced(self):
        ''' Contains advanced settings for a project. '''
        return self._advanced if self._advanced is not None else ProjectAdvancedSettings()
    
    @advanced.setter
    def advanced(self, advanced):
        ''' Contains advanced settings for a project. '''
        if advanced is not None:
            if not isinstance(advanced, ProjectAdvancedSettings):
                raise ValueError("'advanced' property must be an instance of ProjectAdvancedSettings class.")
        self._advanced = advanced

    @property
    def languages(self):
        ''' Contains language-specific settings for a project. '''
        return self._languages if self._languages is not None else ProjectLanguagesSettings()
    
    @languages.setter
    def languages(self, languages):
        ''' Contains language-specific settings for a project. '''
        if languages is not None:
            if not isinstance(languages, ProjectLanguagesSettings):
                raise ValueError("'languages' property must be an instance of ProjectLanguagesSettings class.")
        self._languages = languages

    @property
    def cmake(self):
        ''' Contains CMake-specific settings for a project. '''
        return self._cmake if self._cmake is not None else ProjectCMakeSettings()
    
    @cmake.setter
    def cmake(self, cmake):
        ''' Contains CMake-specific settings for a project. '''
        if cmake is not None:
            if not isinstance(cmake, ProjectCMakeSettings):
                raise ValueError("'cmake' property must be an instance of ProjectCMakeSettings class.")
        self._cmake = cmake

    @property
    def temp(self):
        ''' Contains temporary settings for a project. '''
        return self._temp if self._temp is not None else ProjectTempSettings()
    
    @temp.setter
    def temp(self, temp):
        ''' Contains temporary settings for a project. '''
        if temp is not None:
            if not isinstance(temp, ProjectTempSettings):
                raise ValueError("'temp' property must be an instance of ProjectTempSettings class.")
        self._temp = temp

    def to_dict(self):
        ''' Returns ProjectSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {
            "name": self.name
        }
    
        if self._name_short is not None:
            result['name_short'] = self.name_short
        if self._default_language is not None:
            result['default_language'] = self.default_language
        if self._details is not None:
            result['details'] = self.details.to_dict()
        if self._advanced is not None:
            result['advanced'] = self.advanced.to_dict()
        if self._languages is not None:
            result['languages'] = self.languages.to_dict()
        if self._cmake is not None:
            result['cmake'] = self.cmake.to_dict()
        if self._temp is not None:
            result['temp'] = self.temp.to_dict()

        return result