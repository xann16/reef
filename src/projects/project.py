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


    @property
    def config_path(self) -> str:
        ''' Path where project reef configuration files are located. '''
        return self._info.config_path


    def reload_settings(self) -> None:
        ''' Loads or reloads settings from default JSON config file. '''
        self._settings = ProjectSettings.load_from_json(self.config_path)

    def save_settings(self) -> None:
        ''' Saves current project settings to default JSON config file. '''
        self._settings.save_to_json(self.config_path)
