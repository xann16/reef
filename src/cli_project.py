import click

from .config import Config
from .projects.project_manager import ProjectManager

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
    """
        Handles reef project creation and maintenance.
    """

    ctx.obj['project_manager'] = ProjectManager()


@project.command('info')
@click.pass_context
def project_info(ctx):
    """
        Displays basic information on current state of reef projects.
    """

    manager = ctx.obj['project_manager']
    manager.info()


@project.command('list')
@click.pass_context
def project_list(ctx):
    """
            Lists all registered reef projects.
    """

    manager = ctx.obj['project_manager']
    manager.get_list()


@project.command('describe')
@click.option('--project', '-p', default='', help="Name of project to describe")
@click.pass_context
def project_describe(project, ctx):
    """
            Displays information on given reef project.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, project)
    manager.describe(project_name)


@project.command('create')
@click.argument('name')
@click.option('--template', '-t', default='', help="Name of template for created project")
@click.option('--output-path', '-o', default='.', help="Top-level directory where project is to be created")
@click.pass_context
def project_create(name, template, output_path, ctx):
    """
            Creates new reef project.
    """

    manager = ctx.obj['project_manager']
    manager.create(name, template if template else None, output_path)


@project.command('import')
@click.argument('path')
@click.option('--name', '-n', default='', help="Name of imported project (if other than top-level directory)")
@click.pass_context
def project_import(path, name, ctx):
    """
            Tries to add existing project to reef repository.
    """

    manager = ctx.obj['project_manager']
    manager.import_from(path, name if name else None)


@project.command('refresh')
@click.option('--project', '-p', default='', help="Name of project to describe")
@click.pass_context
def project_refresh(project, ctx):
    """
            Refresh reef generated files for given project.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, project)
    manager.refresh(project_name)


@project.command('delete')
@click.argument('name')
@click.option('--remove-files', '-r', is_flag=True, help="Removes all files in addition to removing project from reef repository")
@click.pass_context
def project_delete(name, remove_files, ctx):
    """
            Removes project from reef repository.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, name, True)
    manager.describe(project_name)


@project.command('default')
@click.pass_context
def project_default(ctx):
    """
            Gets name of reef project used as default in current context.
    """

    manager = ctx.obj['project_manager']
    print(manager.get_default())


@project.command('set-default')
@click.argument('name')
@click.pass_context
def project_set_default(name, ctx):
    """
            Sets default reef project to be used in current context.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, name, True)
    manager.set_default(project_name)


@project.command('default-module')
@click.pass_context
def project_default_module(ctx):
    """
            Gets name of default module used with current reef project.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    print(manager.get_default_module(project_name))


@project.command('set-default-module')
@click.argument('name')
@click.pass_context
def project_default_module(name, ctx):
    """
            Sets default module to be used with current reef project.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.set_default_module(name, project_name)


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
    """
            Lists configuration items for given reef project.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_list_entries(project_name)


@project_config.group('get')
@click.argument('key')
@click.pass_context
def project_config_get(key, ctx):
    """
            Gets value of given configuration item.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    print(manager.config_get_entry(key, project_name))


@project_config.group('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_set(key, value, ctx):
    """
            Sets value of given configuration item.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_set_entry(key, value, project_name)


@project_config.group('reset')
@click.argument('key')
@click.pass_context
def project_config_reset(key, ctx):
    """
            Resets given configuration item to its default value.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_reset_entry(key, project_name)


@project_config.group('add-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_add_item(key, value, ctx):
    """
            Adds value to list for given configuration item.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_add_entry_item(key, value, project_name)


@project_config.group('remove-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_remove_item(key, value, ctx):
    """
            Removes value from list for given configuration item.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_remove_entry_item(key, value, project_name)


@project_config.group('clear-items')
@click.argument('key')
@click.pass_context
def project_config_clear_items(key, ctx):
    """
            Removes all values from list for given configuration item.
    """

    manager = ctx.obj['project_manager']
    project_name = _resolve_project_name(ctx, '')
    manager.config_clear_entry_items(key, project_name)

