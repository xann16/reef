from typing import Iterable

from .repository.project_repository import ProjectRepository
from .repository.data.project_item_data import ProjectItemData
from .project import Project

class ProjectFactory():
    ''' Foctory that references project repository and manages creation and loading of project settings data. '''

    def __init__(self, project_repository: ProjectRepository):
        ''' Initializes factory object given Reef project repository. '''
        self._repository: ProjectRepository = project_repository
        self._project_cache: dict[str, Project] = {}

    @property
    def project_items(self) -> Iterable[ProjectItemData]:
        ''' Allows to iterate over project data items registered in project repository. '''
        return iter(self._repository)
    
    def __contains__(self, project_name: str) -> bool:
        ''' Checks whether reef project with given name is registered. '''
        return project_name in self._repository.project_names
    
    def __getitem__(self, project_name: str) -> Project:
        ''' Gets Project object representing reef project with given name. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        return self._get_project_impl(project_name)


    @property
    def default_project_name(self) -> str | None:
        ''' Returns name of a project set as a default, or None if not set. '''
        return self._repository.default_project_name


    @property
    def default_project(self) -> Project | None:
        ''' Returns Project set as a default, or None if not set. '''
        return self._get_project_impl(self.default_project_name) if self.default_project_name is not None else None


    @property
    def change_default_project(self, project_name: str) -> None:
        ''' Changes project set as default to the one given by name. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        if project_name == self.default_project_name:
            return
        
        self._repository.default_project_name = project_name
        self._repository.save()


    def _get_project_impl(self, project_name: str) -> Project:
        ''' Implemets project retrieval using cache. '''
        assert project_name in self
        if project_name not in self._project_cache:
            self._project_cache[project_name] = Project(info=self._repository[project_name])
        return self._project_cache[project_name]
        