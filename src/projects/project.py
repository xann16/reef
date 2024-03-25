from os import path, mkdir
from typing import Any

from .settings.project_settings import ProjectSettings
from .repository.data.project_item_data import ProjectItemData

class Project():
    ''' Represents data and functionality for Reef projects. '''
    
    def __init__(self, info: ProjectItemData, *, settings: ProjectSettings | None = None):
        ''' Initializes repository given loaded project list data. '''
        self._info: ProjectItemData = info
        self._settings: ProjectSettings | None = settings
        
        if self._settings is None:
            self.reload_settings()

        assert self._settings is not None
        assert self._settings.name == self._info.name


    @property
    def name(self) -> str:
        ''' Name of a project. '''
        return self._info.name

    @property
    def config_path(self) -> str:
        ''' Path where project reef configuration files are located. '''
        return self._info.config_path

    @property
    def source_path(self) -> str:
        ''' Path where reef project source is located. '''
        return self._info.config_path

    @property
    def is_config_inplace(self) -> bool:
        ''' Indicates whether given project stores its reef configuration inplace. '''
        return self._info.is_config_inplace


    def describe(self, verbose: bool = False, config_only: bool = False) -> None:
        if not config_only:
            print(f"NAME:        {self.name}")
            print(f"SOURCE PATH: {self.source_path}")
            print(f"CONFIG PATH: {'(IN)' if self.is_config_inplace else '(OUT)'} {self.config_path}")
            print("PROJECT SETTINGS:")
        self._settings.print_properties(skip_unset=not verbose)

    def get(self, key: str) -> Any:
        ''' Returns value for setting given by key. '''
        return self._settings.get(key)

    def config_set_entry(self, key: str, value: str, project_name: str | None = None) -> None:
        ''' Sets value for a setting given by key. '''
        return self._settings.set(key, value)

    def config_add_entry_item(self, key: str, value: str, project_name: str | None = None):
        ''' Adds an entry to the list-like setting given by key. '''
        raise NotImplementedError("List-like project setting are not yey implemented.")

    def config_remove_entry_item(self, key: str, value: str, project_name: str | None = None):
        ''' Removess an entry from the list-like setting given by key. '''
        raise NotImplementedError("List-like project setting are not yey implemented.")

    def config_clear_entry_items(self, key: str, project_name: str | None = None):
        ''' Clears all items from the list-like setting given by key. '''
        raise NotImplementedError("List-like project setting are not yey implemented.")


    def reload_settings(self) -> None:
        ''' Loads or reloads settings from default JSON config file. '''
        self._settings = ProjectSettings.load_from_json(self.config_path)

    def save_settings(self) -> None:
        ''' Saves current project settings to default JSON config file. '''
        self._settings.save_to_json(self.config_path)

    def initialize_inplace_settings(self) -> None:
        ''' Given proper settings, it initializes proper in-place config directory and settings file there. '''
        if not self.is_config_inplace:
            raise ValueError('Inplace config initialization works only for projects with inplace configuration.')
        if path.exists(self.config_path):
            raise FileExistsError(f"Reef config at '{self.config_path}' already exists.")
        if not path.exists(self.source_path):
            mkdir(self.source_path)
        if not path.exists(self.config_path):
            mkdir(self.config_path)
        self.save_settings()

