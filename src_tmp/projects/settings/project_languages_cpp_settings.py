from ...settings_base import SettingsBase

class ProjectLanguagesCppSettings(SettingsBase):
    '''
    Contains project settings specific to C++ language.
    '''

    def __init__(self,
                 obj, *,
                 standard=None,
                 allow_extensions=None):
        '''
        Constructs ProjectLanguagesCppSettings object from item dictionary or manual property value overrides.
        '''
        self.standard = standard if standard is not None else (obj['standard'] if 'standard' in obj else None)
        self.allow_extensions = allow_extensions if allow_extensions is not None else (obj['allow_extensions'] if 'allow_extensions' in obj else None)
        
    @property
    def standard(self):
        ''' Required C++ standard. '''
        return self._standard
    
    @standard.setter
    def standard(self, standard):
        ''' Required C++ standard. '''
        # TODO : Add C++ standard validation
        if standard is not None:
            if not isinstance(standard, str):
                raise ValueError("'standard' property must be a string.")
            if not standard:
                raise ValueError("'standard' property cannot be an empty string.")
        self._standard = standard

    @property
    def allow_extensions(self):
        ''' Indicates whether non-standard C++ extensions are allowed. '''
        return self._allow_extensions if self._allow_extensions is not None else False
    
    @allow_extensions.setter
    def allow_extensions(self, allow_extensions):
        ''' Indicates whether non-standard C++ extensions are allowed. '''
        if allow_extensions is not None:
            if not isinstance(allow_extensions, bool):
                raise ValueError("'allow_extensions' property must be a boolean.")
        self._allow_extensions = allow_extensions


    def to_dict(self):
        ''' Returns ProjectLanguagesCppSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}
        
        if self._standard is not None:
            result['standard'] = self.standard
        if self._allow_extensions is not None:
            result['allow_extensions'] = self.allow_extensions

        return result if any(result) else None
    
