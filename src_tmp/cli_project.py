import click
from os import path

from .config import Config
from .projects.project_manager import ProjectManager

PROJECT_REPOSITORY_JSON_FILEPATH = "projects.json"

def _resolve_project_name(ctx, override=None, is_override_required=False):
    if is_override_required and not override:
        assert False # TODO
    if override:
        return override
    if 'project' in ctx.obj and ctx.obj['project']:
        return ctx.obj['project']
    return None 


@click.group('project')
@click.pass_context
def project(ctx):
    ''' Handles reef project creation and maintenance. '''
    project_repo_path = path.join(ctx.obj['config'].projects_path(), PROJECT_REPOSITORY_JSON_FILEPATH)
    ctx.obj['project_manager'] = ProjectManager(repository_path=project_repo_path)


@project.command('info')
@click.pass_context
def project_info(ctx):
    ''' Displays basic information on current state of reef projects. '''
    items = list(ctx.obj['project_manager'].project_items)

    if not items:
        print("No reef projects are registered.")

    project_name_title = "PROJECT NAME"
    max_project_name_length = max(max(len(name) for name, _, _ in items), len(project_name_title))

    # title and separator line
    print(f"| ### | {project_name_title:max_project_name_length} | CFG | SOURCE PATH ")
    print(f"| --- | {'-' * max_project_name_length} | --- | ----------- ... ")

    # item listing
    for i, (name, source_path, is_config_inplace) in enumerate(items):
        config_label = "IN " if is_config_inplace else "OUT"
        print(f"| {i + 1:3} | {name:max_project_name_length} | {config_label} | {source_path}")


@project.command('list')
@click.pass_context
def project_list(ctx):
    ''' Lists all registered reef projects. '''
    for name, _, _ in ctx.obj['project_manager'].project_items:
        print(name)


@project.command('describe')
@click.option('--project', '-p', default='', help="Name of project to describe")
@click.option('--verbose', '-v', is_flag=True, help="Verbose mode (include unset properties with default values)")
@click.pass_context
def project_describe(project, verbose, ctx):
    ''' Displays more information and settings used in given reef project. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, project)
    manager.describe(project_name, verbose)


@project.command('create')
@click.argument('name')
@click.option('--template', '-t', default='', help="Name of template for created project")
@click.option('--output-path', '-o', default='.', help="Top-level directory where project is to be created")
@click.pass_context
def project_create(name, template, output_path, ctx):
    ''' Creates new reef project. '''
    ctx.obj['project_manager'].create(name, template, output_path)


@project.command('import')
@click.argument('path')
@click.option('--name', '-n', default='', help="Name of imported project (if other than already specified)")
@click.pass_context
def project_import(path, name, ctx):
    ''' Adds an existing reef project to currently used reef repository. '''
    ctx.obj['project_manager'].import_existing(path, name)


@project.command('refresh')
@click.option('--project', '-p', default='', help="Name of project to refresh")
@click.pass_context
def project_refresh(project, ctx):
    ''' Refreshes reef generated files for given project. '''
    ctx.obj['project_manager'].refresh(_resolve_project_name(ctx, project))


@project.command('remove')
@click.argument('name')
@click.option('--remove-files', '-r', is_flag=True, help="Removes all files in addition to removing project from reef repository")
@click.pass_context
def project_remove(name, remove_files, ctx):
    ''' Removes project from reef repository. '''
    ctx.obj['project_manager'].remove(_resolve_project_name(ctx, name, True), remove_files)


@project.command('get-default')
@click.pass_context
def project_get_default(ctx):
    ''' Outputs name of reef project used as a default in current context. '''
    default_project = ctx.obj['project_manager'].default_project_name

    if default_project:
        print(default_project)
    else:
        print("No project currently set as default.")


@project.command('set-default')
@click.argument('name')
@click.pass_context
def project_set_default(name, ctx):
    ''' Sets default reef project to be used in current context. '''
    project_name = _resolve_project_name(ctx, name, True)
    ctx.obj['project_manager'].change_default_project(project_name)


@project.command('get-default-module')
@click.option('--project', '-p', default='', help="Name of project considered")
@click.pass_context
def get_project_default_module(ctx, project):
    ''' Outputs name of a module used as a default for current/given reef project. '''
    project_name = _resolve_project_name(ctx, project)
    default_module = ctx.obj['project_manager'].get_default_module_name_for(project_name)

    if default_module:
        print(default_module)
    else:
        print(f"No module currently set as default for '{project_name}'.")


@project.command('set-default-module')
@click.argument('name')
@click.option('--project', '-p', default='', help="Name of project considered")
@click.pass_context
def project_default_module(name, project, ctx):
    ''' Sets default module for current/given reef project. '''
    project_name = _resolve_project_name(ctx, project)
    default_module = ctx.obj['project_manager'].change_default_module_for(project_name, name)


@project.group('config')
@click.pass_context
def project_config(ctx):
    """
            Handles configuration specific for given reef project.
    """
    pass


@project_config.group('list')
@click.pass_context
def project_config_list(ctx):
    ''' Lists configuration items for given reef project. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_list_entries(project_name)


@project_config.group('get')
@click.argument('key')
@click.pass_context
def project_config_get(key, ctx):
    ''' Gets value of given configuration item. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    print(manager.config_get_entry(key, project_name))


@project_config.group('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_set(key, value, ctx):
    ''' Sets value of given configuration item. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_set_entry(key, value, project_name)


@project_config.group('reset')
@click.argument('key')
@click.pass_context
def project_config_reset(key, ctx):
    ''' Resets given configuration item to its default value. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_reset_entry(key, project_name)


@project_config.group('add-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_add_item(key, value, ctx):
    ''' Adds value to list for given configuration item. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_add_entry_item(key, value, project_name)


@project_config.group('remove-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_remove_item(key, value, ctx):
    ''' Removes value from list for given configuration item. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_remove_entry_item(key, value, project_name)


@project_config.group('clear-items')
@click.argument('key')
@click.pass_context
def project_config_clear_items(key, ctx):
    ''' Removes all values from list for given configuration item. '''
    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_clear_entry_items(key, project_name)

