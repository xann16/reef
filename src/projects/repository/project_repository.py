from os import path
from typing import Iterable
import json

from .data.project_repository_data import ProjectRepositoryData, ProjectItemData

class ProjectRepository:

    def __init__(self, projects_data_source_path: str):
        ''' Initializes project repository with path to underlying JSON source file to be used. '''
        if projects_data_source_path is None or not isinstance(projects_data_source_path, str):
            raise ValueError("Project Repository source path must be a valid string.")
        self._projects_source_path = projects_data_source_path

        self._initialize_data()
        assert self._data is not None

    @property
    def projects_data_source_path(self) -> str:
        ''' Path to data source JSON file for given project repository. '''
        return self._projects_data_source_path

    @property
    def default_project_name(self) -> str | None:
        ''' Name of the project set as default. '''
        return self._data.default_project

    @default_project_name.setter
    def default_project_name(self, project_name: str | None) -> None:
        ''' Name of the project set as default. '''
        self._data.default_project = project_name

    @property
    def default_project(self) -> ProjectItemData | None:
        ''' Project item for the project set as default. '''
        return self[self.default_project_name()] if self.default_project_name() is not None else None

    @property
    def project_names(self) -> Iterable[str]:
        "Lists all project names in the repository. "
        return (item.name for item in self._data)

    def __contains__(self, project_name: str) -> bool:
        ''' Returns whether project with given name is present in the repository. '''
        return project_name in self._data

    def __get_item__(self, project_name: str) -> ProjectItemData:
        ''' Returns data for project in the repository with given name. '''
        if project_name not in self._data:
            raise KeyError(f"Project with name '{project_name}' not found")
        return self._data[project_name]

    def __iter__(self) -> Iterable[ProjectItemData]:
        ''' Lists all project items. '''
        return iter(self._data)

    def add_project(self, project_name: str, project_source_path: str, *, 
                    project_config_path: str| None = None) -> None:
        ''' Adds new project to repository with given name and source path (optionally, a non-standard config path). '''
        if project_name in self:
            raise KeyError(f"Project with name '{project_name}' already exists.")
        self._data.add_project(ProjectItemData({}, name=project_name, source_path=project_source_path, config_path=project_config_path))

    def remove_project(self, project_name: str) -> None:
        ''' Removes project with given name to the repository. '''
        if project_name not in self._data:
            raise KeyError(f"Project with name '{project_name}' not found")
        del self._data[project_name]

    def reload(self) -> None:
        ''' Reloads repository data from the underlying JSON source file. '''
        if not path.exists(self.projects_source_path()):
            raise FileNotFoundError(f"Project repository source file '{self.projects_source_path()}' does not exist.")
        with open(self.projects_source_path(), 'r', encoding='utf-8') as fp:
            self._data = ProjectRepositoryData(json.load(fp))

    def save(self) -> None:
        ''' Saves repository data to the underlying JSON source file. '''
        with open(self.projects_source_path(), 'w', encoding='utf-8') as fp:
            json.dump(self._data.to_dict(), fp, indent=2)

    def _initialize_data(self) -> None:
        ''' Initializes repository data from existing JSON source or creates an new empty one. '''
        assert self.projects_source_path() is not None and isinstance(self.projects_source_path(), str)

        if path.exists(self.projects_source_path()):
            self.reload()
        else:
            self._data = ProjectRepositoryData()
            self.save()
