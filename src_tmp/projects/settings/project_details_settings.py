from ...settings_base import SettingsBase

class ProjectDetailsSettings(SettingsBase):
    '''
    Contains data on project info details.
    '''

    def __init__(self,
                 obj, *,
                 description=None,
                 homepage=None):
        '''
        Constructs ProjectDetailsSettings object from item dictionary or manual property value overrides.
        '''
        self.name = description if description is not None else (obj['description'] if 'description' in obj else None)
        self.homepage = homepage if homepage is not None else (obj['homepage'] if 'homepage' in obj else None)

        
    @property
    def description(self):
        ''' Project description. '''
        return self._description
    
    @description.setter
    def description(self, description):
        ''' Project description. '''
        if description is not None:
            if not isinstance(description, str):
                raise ValueError("'description' property must be a string.")
            if not description:
                raise ValueError("'description' property cannot be an empty string")
        self._description = description


    @property
    def homepage(self):
        ''' URI to project's homepage. '''
        return self._homepage
    
    @homepage.setter
    def homepage(self, homepage):
        ''' URI to project's homepage. '''
        if homepage is not None:
            # TODO : Add extra URI validation
            if not isinstance(homepage, str):
                raise ValueError("'homepage' property must be a string.")
            if not homepage:
                raise ValueError("'homepage' property cannot be an empty string")
        self._homepage = homepage

    def to_dict(self):
        ''' Returns ProjectDetailsSettings as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {}
    
        if self._description is not None:
            result['description'] = self.description
        if self._homepage is not None:
            result['homepage'] = self.homepage

        return result if any(result) else None