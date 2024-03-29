from ...settings_base import SettingsBase

def __is_int(value):
    try:
        int(value)
        return True
    except:
        return False


class ProjectCMakeSettings(SettingsBase):
    '''
    Contains project settings specific for CMake.
    '''

    def __init__(self,
                 obj, *,
                 version_required=None):
        '''
        Constructs ProjectCMakeSettings object from item dictionary or manual property value overrides.
        '''
        self.version_required = version_required if version_required is not None else (obj['version_required'] if 'version_required' in obj else None)
        
    @property
    def version_required(self):
        ''' Override for minimum required version of CMake. '''
        return self._version_required if self._version_required is not None else "3.21"

    @property
    def version_required_major(self):
        ''' Major part of an override for minimum required version of CMake. '''
        return int(self.version.split('.')[0])

    @property
    def version_required_minor(self):
        ''' Minor part of an override for minimum required version of CMake. '''
        return int(self.version.split('.')[1])

    @version_required.setter
    def version_required(self, version_required):
        ''' Override for minimum required version of CMake. '''
        # TODO: proper version string validation - type-dependent. 
        if version_required is not None:
            if not isinstance(version_required, str):
                raise ValueError("'version_required' property must be a string.")
            tokens = version_required.split('.')
            if len(tokens) != 2 or not all(__is_int(t) for t in tokens):
                raise ValueError("'version_required' must have proper format: '[INT].[INT]'.")
        self._version_required = version_required


    def to_dict(self):
        ''' Returns ProjectCMakeSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}

        if self._version_required is not None:
            result['version_required'] = self.version_required

        return result if any(result) else None

