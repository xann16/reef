from typing import Iterable
from os import path

from .project_factory import ProjectFactory
from .repository.project_repository import ProjectRepository
from .project import Project

class ProjectManager():
    ''' Manages all operations concerning the management of Reef projects. '''

    def __init__(self, 
                 factory: ProjectFactory | None = None, 
                 repository_path: str | None = None):
        ''' Creates project manager with injected project factory, or path to the underlying project data repository. '''
        if factory is None and repository_path is None:
            raise ValueError("Project manager must be initialized with either Project Factory or path to project repository source.")
        if factory is not None:
            if not isinstance(factory, ProjectFactory):
                raise ValueError("Project factory has to be the object of 'ProjectFactory' type.")
            self._factory = factory
            if repository_path is not None:
                print("WARNING: [ProjectManager] Project repository path was provided while injecting ProjectFactory object. Injected object is used.")
        else:
            repository = ProjectRepository(repository_path)
            self._factory = ProjectFactory(repository)

        assert self._factory is not None

    @property
    def project_items(self) -> Iterable[tuple[str, str, bool]]:
        ''' Allows to iterate over basic informaton for registered Reef projects including: name, source path and whether config is inplace. '''
        return ((p.name, p.source_path, p.is_config_inplace) for p in self._factory)

    @property
    def default_project(self) -> Project | None:
        ''' Returns Project set as a default, or None if not set. '''
        return self._factory.default_project

    @property
    def default_project_name(self) -> str | None:
        ''' Returns name of a project set as a default, or None if not set. '''
        return self._factory.default_project_name

    @property
    def change_default_project(self, project_name: str) -> None:
        ''' Changes project set as default to the one given by name. '''
        return self._factory.change_default_project(project_name)




    def describe(self, project_name=None):
        """
            describe
        """
        pass

    def create(self, project_name, project_template_name, base_path):
        """
            create
        """
        pass

    def import_from(self, base_path, project_name=None):
        """
        import
        """
        pass

    def refresh(self, project_name=None):
        """
            refresh
        """
        pass

    def delete(self, project_name, are_files_removed=False):
        """
            delete
        """
        pass


    def get_default_module(self, project_name):
        """
            get_default_module
        """
        pass

    def set_default_module(self, module_name, project_name=None):
        """
            set_default_module
        """
        pass

    def config_get_entry(self, key, project_name=None):
        """
            config_get_entry
        """
        pass

    def config_set_entry(self, key, value, project_name=None):
        """
            config_set_entry
        """
        pass

    def config_list_entries(self, key, project_name=None):
        """
            config_list_entries
        """
        pass

    def config_reset_entry(self, key, project_name=None):
        """
            config_reset_entry
        """
        pass

    def config_add_entry_item(self, key, value, project_name=None):
        """
            config_add_entry_item
        """
        pass

    def config_remove_entry_item(self, key, value, project_name=None):
        """
            config_remove_entry_item
        """
        pass

    def config_clear_entry_items(self, key, project_name=None):
        """
            config_clear_entry_items
        """
        pass


