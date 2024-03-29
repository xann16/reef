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

    def item_for(self, project_name: str) -> ProjectItemData:
        ''' Gets project data item for given registered project in repository. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        return self._repository[project_name]


    def __contains__(self, project_name: str) -> bool:
        ''' Checks whether reef project with given name is registered. '''
        return project_name in self._repository.project_names
    
    def __getitem__(self, project_name: str) -> Project:
        ''' Gets Project object representing reef project with given name. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        return self._get_project_impl(project_name)


    def add(self, project: Project) -> None:
        ''' Adds given project to the repository. '''
        if project.name in self._repository:
            raise KeyError(f"Project with name '{project.name}' is already registered in reef project repository.")
        self._repository.add_project_from_data(project.info)
        self._repository.save()
        self._project_cache[project.name] = project
        

    def remove(self, project_name: str) -> None:
        ''' Removes named project to the repository. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        self._repository.remove_project(project_name)
        self._repository.save()


    @property
    def default_project_name(self) -> str | None:
        ''' Returns name of a project set as a default, or None if not set. '''
        return self._repository.default_project_name


    @property
    def default_project(self) -> Project | None:
        ''' Returns Project set as a default, or None if not set. '''
        return self._get_project_impl(self.default_project_name) if self.default_project_name is not None else None


    def change_default_project(self, project_name: str) -> None:
        ''' Changes project set as default to the one given by name. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        if project_name == self.default_project_name:
            return
        
        self._repository.default_project_name = project_name
        self._repository.save()


    def get_default_module_name_for(self, project_name: str) -> str | None:
        ''' Returns name of a module set as a default for a project, or None if not set. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        return self._repository[project_name].default_module


    def change_default_module_for(self, project_name: str, module_name: str) -> None:
        ''' Changes module set as default for a project to the one given by name. '''
        if project_name not in self._repository:
            raise KeyError(f"Project '{project_name}' is not registered in reef project repository.")
        if module_name == self.get_default_module_name_for(project_name):
            return
        
        self._repository[project_name].default_module = module_name
        self._repository.save()


    def _get_project_impl(self, project_name: str) -> Project:
        ''' Implemets project retrieval using cache. '''
        assert project_name in self
        if project_name not in self._project_cache:
            self._project_cache[project_name] = Project(info=self._repository[project_name])
        return self._project_cache[project_name]
        