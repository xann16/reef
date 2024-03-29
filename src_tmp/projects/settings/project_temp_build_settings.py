from ...settings_base import SettingsBase


class ProjectTempBuildSettings(SettingsBase):
    '''
    Contains temporary project settings related to build options.
    '''

    _BUILD_MODES = ['default']

    def __init__(self,
                 obj, *,
                 mode=None):
        '''
        Constructs ProjectTempBuildSettings object from item dictionary or manual property value overrides.
        '''
        self.mode = mode if mode is not None else (obj['mode'] if 'mode' in obj else None)

    @property
    def mode(self):
        ''' Build mode. '''
        return self._mode if self._mode is not None else self._BUILD_MODES[0]

    @mode.setter
    def mode(self, mode):
        ''' Build mode. '''
        if mode is not None:
            if not isinstance(mode, str):
                raise ValueError("'mode' property must be a string.")
            if not mode:
                raise ValueError("'mode' property cannot be an empty string.")
            if mode not in self._BUILD_MODES:
                raise ValueError(f"'mode' cannot be '{mode}' (supported values include: {', '.join(self._BUILD_MODES)} ).")
        self._mode = mode

    def to_dict(self):
        ''' Returns ProjectTempBuildSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}

        if self._mode is not None:
            result['mode'] = self.mode

        return result if any(result) else None

