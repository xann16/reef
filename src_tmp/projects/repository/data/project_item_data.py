from os import path
from typing import Any

class ProjectItemData():
    '''
    Contains data of a project item stored in the project repository.
    '''

    def __init__(self,
                 obj: dict[str, Any], *,
                 name: str | None = None,
                 source_path: str | None = None,
                 config_path: str | None = None,
                 default_module: str | None = None):
        '''
        Constructs ProjectItemData object from item dictionary or manual property value overrides.
        '''
        self.name = name if name is not None else (obj['name'] if 'name' in obj else None)
        self.source_path = source_path if source_path is not None else (obj['source_path'] if 'source_path' in obj else None)
        self.config_path = config_path if config_path is not None else (obj['config_path'] if 'config_path' in obj else None)
        self.default_module = default_module if default_module is not None else (obj['default_module'] if 'default_module' in obj else None)

        
    @property
    def name(self) -> str:
        ''' Project name. '''
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        ''' Project name. '''
        if name is None:
            raise ValueError("'name' property cannot be None.")
        if not isinstance(name, str):
            raise ValueError("'name' property must be a string.")
        if not name:
            raise ValueError("'name' property cannot be an empty string")
        self._name = name


    @property
    def source_path(self) -> str:
        ''' Path to the top-level directory where project's source files are contained. '''
        return self._source_path
    
    @source_path.setter
    def source_path(self, source_path: str) -> None:
        ''' Path to the top-level directory where project's source files are contained. '''
        if source_path is None:
            raise ValueError("'source_path' property cannot be None.")
        if not isinstance(source_path, str):
            raise ValueError("'source_path' property must be a string.")
        if not source_path:
            raise ValueError("'source_path' property cannot be an empty string")
        self._source_path = source_path


    @property
    def config_path(self) -> str:
        ''' Path where project's Reef config files are contained. '''
        return self._config_path if self._config_path is not None else path.join(self._source_path, '.reef')
    
    @config_path.setter
    def config_path(self, config_path: str | None):
        ''' Path where project's Reef config files are contained. '''
        if config_path is not None:
            if not isinstance(config_path, str):
                raise ValueError("'config_path' property must be a string.")
            if not config_path:
                raise ValueError("'config_path' property cannot be an empty string")
        self._config_path = config_path


    @property
    def is_config_inplace(self) -> bool:
        return self._config_path is None or path.commonpath(self.source_path, self.config_path) == self.source_path


    @property
    def default_module(self) -> str | None:
        ''' Module used as default when working with this project. '''
        return self._default_module
    
    @default_module.setter
    def default_module(self, default_module: str | None) -> None:
        ''' Module used as default when working with this project. '''
        if default_module is not None:
            if not isinstance(default_module, str):
                raise ValueError("'default_module' property must be a string.")
            if not default_module:
                raise ValueError("'default_module' property cannot be an empty string")
        self._default_module = default_module


    def to_dict(self) -> dict[str, Any]:
        ''' Returns ProjectItemData as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {
            'name': self.name,
            'source_path': self.source_path
        }
    
        if self._config_path is not None:
            result['config_path'] = self.config_path
        if self._default_module is not None:
            result['default_module'] = self.default_module

        return result