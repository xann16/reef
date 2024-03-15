from typing import Iterable
from os import path
from shutil import rmtree

from .project_factory import ProjectFactory
from .repository.project_repository import ProjectRepository
from .repository.data.project_item_data import ProjectItemData
from .project import Project
from .project_templates.project_template_repository import ProjectTemplateRepository
from .settings.project_settings import ProjectSettings

class ProjectManager():
    ''' Manages all operations concerning the management of Reef projects. '''

    def __init__(self, 
                 factory: ProjectFactory | None = None, 
                 repository_path: str | None = None,
                 template_repository: ProjectTemplateRepository | None = None):
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

        self._templates = template_repository if template_repository is not None else ProjectTemplateRepository()

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

    def change_default_project(self, project_name: str) -> None:
        ''' Changes project set as default to the one given by name. '''
        return self._factory.change_default_project(project_name)

    def refresh(self, project_name: str) -> None:
        ''' Regenerate project files handled by reef. '''
        ### TODO
        raise NotImplementedError("Refresh functionality not yet implemented.")


    def describe(self, project_name=None):
        """
            describe
        """
        pass

    def create(self, project_name: str, project_template_name: str, base_path: str) -> None:
        ''' Creates a new project with config based on given template in new directory named as project located in bae path given. '''
        
        if not project_name:
            raise ValueError('Projecn name cannot be empty')
        if project_template_name:
            raise NotImplementedError('Currently, handling of non-default templates is not supported')
        if not base_path or not path.isdir(base_path):
            raise FileNotFoundError(f"Base path for project creation, '{base_path}', does not exist")

        root_path = path.abspath(path.realpath(path.expanduser(base_path)))
        project_path = path.join(root_path, project_name)
        info = ProjectItemData(None, name=project_name, source_path=project_path)
        
        config_data = self._templates.empty
        config_data['name'] = project_name
        settings = ProjectSettings(config_data)

        project = Project(info, settings=settings)
        project.initialize_inplace_settings()

        self._factory.add(project)

    def import_existing(self, base_path: str, project_name: str):
        ''' Imports an existing reef project with its config at given location. '''

        if not base_path or not path.isdir(base_path):
            raise FileNotFoundError(f"Base path for project import, '{base_path}', does not exist")

        project_path = path.abspath(path.realpath(path.expanduser(base_path)))
        config_path = path.join(project_path, '.reef')              # TODO: extract magic strings            
        config_file_path = path.join(config_path, 'project.json')   # TODO: extract magic strings            
        
        if not path.exists(config_file_path):
            raise FileNotFoundError(f"Config file could not be found at: '{config_file_path}'. Given path does not seem to contain a reef project.")
        
        settings = ProjectSettings.load_from_json(config_path)
        if project_name:
            settings.name = project_name
            settings.name_short = None

        info = ProjectItemData(None, name=settings.name, source_path=project_path)
        project = Project(info, settings=settings)

        self._factory.add(project)


    def remove(self, project_name: str, are_files_removed: bool = False):
        ''' Removes project from repository (and optionally removes all project files). '''
        if project_name not in self._factory:
            raise KeyError(f"Project with name '{project_name}' not found. Cannot be removed")
        info = self._factory.item_for(project_name)

        self._factory.remove(project_name)

        if are_files_removed:
            rmtree(info.source_path)
            if not info.is_config_inplace:
                rmtree(info.config_path)


    def get_default_module_name_for(self, project_name: str) -> str | None:
        ''' Returns name of a module set as a default for a given project, or None if not set. '''
        return self._factory.get_default_module_name_for(project_name)

    def change_default_module_for(self, project_name: str, module_name: str) -> None:
        ''' Changes module set as default for a project to the one given by name. '''
        return self._factory.change_default_module_for(project_name, module_name)


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


