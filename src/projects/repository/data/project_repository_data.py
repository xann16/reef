from collections import abc
from typing import Any, Iterable

from .project_item_data import ProjectItemData

class ProjectRepositoryData():
    '''
    Contains data of projects managed by reef repository.
    '''

    def __init__(self,
                 obj: dict[str, Any], *,
                 projects: Iterable[ProjectItemData] | None = None,
                 default_project: str | None = None):
        ''' Constructs ProjectRepositoryData object from item dictionary or manual property value overrides. '''
        self._projects = {}
        self.add_projects(projects)
        self.add_projects(obj['projects'] if 'projects' in obj else [])
        
        self.default_project = default_project if default_project is not None else (obj['default_project'] if 'default_project' in obj else None)


    def __contains__(self, project_name: str) -> bool:
        '''  Checks if project with given name is contained in the repository. '''
        return project_name in self._projects
    
    def __iter__(self) -> Iterable[ProjectItemData]:
        ''' Lists all project items. '''
        return iter(self._projects.values)

    def add_projects(self, projects: Iterable[ProjectItemData] | None) -> None:
        ''' Adds project items from an iterable collection. '''
        if projects is None:
            return
        if not isinstance(projects, abc.Iterable):
            raise ValueError("'projects' parameter must be iterable.")
        for project in projects:
            self.add_project(project)

    def add_project(self, project: ProjectItemData) -> None:
        ''' Adds a single project item. '''
        if project is None:
            raise ValueError("'project' item cannot be None.")
        if not isinstance(project, ProjectItemData):
            raise ValueError("'project' item must be a ProjectItemData object.")
        if project.name in self:
            raise ValueError(f"'project' cannot be added, as it has name ('{project.name}') that already exists in the repository.")
        self._projects[project.name] = project

    def remove_project(self, project_name: str) -> None:
        '''  Removes a project with given name from the repository (raises error if name is not found). '''
        if project_name not in self:
            raise KeyError(f"Project with name '{project_name}' does not exist.")
        del self._projects[project_name]
        if self.default_project == project_name:
            self.default_project = None        

    def clear_projects(self) -> None:
        ''' Removes all projects from repository. '''
        self._projects = {}

    def __get_item_(self, project_name: str) -> ProjectItemData:
        ''' Returns project item with given name. '''
        if project_name not in self:
            raise KeyError(f"Project with name '{project_name}' does not exist.")
        return self._projects[project_name]

        
    @property
    def default_project(self) -> str | None:
        ''' Project used as default when working with this repository. '''
        return self._default_project
    
    @default_project.setter
    def default_project(self, default_project: str | None) -> None:
        ''' Project used as default when working with this repository. '''
        if default_project is not None:
            if not isinstance(default_project, str):
                raise ValueError("'default_module' property must be a string.")
            if not default_project:
                raise ValueError("'default_module' property cannot be an empty string")
        self.default_project = default_project


    def to_dict(self) -> dict[str, Any]:
        ''' Returns ProjectRepositoryData as a dictionary with its properties (convenient for conversion to JSON). '''
        result = {
            'project': list(self),
        }

        if self._default_project is not None:
            result['default_project'] = self.default_project
    
        return result
