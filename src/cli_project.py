import click

from .config import Config


@click.group('project')
@click.pass_context
def project(ctx):
    """
            Handles reef project creation and maintenance.
    """
    pass


@project.command('info')
@click.pass_context
def project_info(ctx):
    """
            Displays basic information on current state of reef projects.
    """

    config = ctx.obj['config']

    print("###=========================###")
    print("### info project subcommand ###")
    print("###=========================###")


@project.command('list')
@click.pass_context
def project_list(ctx):
    """
            Lists all registered reef projects.
    """

    config = ctx.obj['config']

    print("###=========================###")
    print("### list project subcommand ###")
    print("###=========================###")


@project.command('describe')
@click.option('--project', '-p', default='', help="Name of project to describe")
@click.pass_context
def project_describe(project, ctx):
    """
            Displays information on given reef project.
    """

    config = ctx.obj['config']

    print("###=========================###")
    print("### list project subcommand ###")
    print("###=========================###")


@project.command('create')
@click.argument('name')
@click.option('--template', '-t', default='basic', help="Name of template for created project")
@click.option('--output-path', '-o', default='.', help="Top-level directory where project is to be created")
@click.pass_context
def project_create(name, template, output_path, ctx):
    """
            Creates new reef project.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### create project subcommand ###")
    print("###===========================###")


@project.command('import')
@click.argument('path')
@click.option('--name', '-n', default='', help="Name of imported project (if other than top-level directory)")
@click.pass_context
def project_import(path, name, ctx):
    """
            Tries to add existing project to reef repository.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### import project subcommand ###")
    print("###===========================###")


@project.command('refresh')
@click.pass_context
def project_import(path, name, ctx):
    """
            Refresh reef generated files for given project.
    """

    config = ctx.obj['config']

    print("###============================###")
    print("### refresh project subcommand ###")
    print("###============================###")


@project.command('delete')
@click.argument('name')
@click.option('--remove-files', '-r', is_flag=True, help="Removes all files in addition to removing project from reef repository")
@click.pass_context
def project_delete(name, remove_files, ctx):
    """
            Removes project from reef repository.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### remove project subcommand ###")
    print("###===========================###")


@project.command('default')
@click.pass_context
def project_default(ctx):
    """
            Gets name of reef project used as default in current context.
    """

    config = ctx.obj['config']

    print("###============================###")
    print("### default project subcommand ###")
    print("###============================###")


@project.command('set-default')
@click.argument('name')
@click.pass_context
def project_set_default(name, ctx):
    """
            Sets default reef project to be used in current context.
    """

    config = ctx.obj['config']

    print("###================================###")
    print("### set-default project subcommand ###")
    print("###================================###")


@project.command('default-module')
@click.pass_context
def project_default_module(ctx):
    """
            Gets name of default module used with current reef project.
    """

    config = ctx.obj['config']

    print("###===================================###")
    print("### default-module project subcommand ###")
    print("###===================================###")


@project.command('set-default-module')
@click.argument('name')
@click.pass_context
def project_default_module(name, ctx):
    """
            Sets default module to be used with current reef project.
    """

    config = ctx.obj['config']

    print("###=======================================###")
    print("### set-default-module project subcommand ###")
    print("###=======================================###")


@project.group('config')
@click.pass_context
def project_config(ctx):
    """
            Handles configuration specific for given reef project.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### project config subcommand ###")
    print("###===========================###")


@project_config.group('list')
@click.pass_context
def project_config_list(ctx):
    """
            Lists configuration items for given reef project.
    """

    config = ctx.obj['config']

    print("###================================###")
    print("### list project config subcommand ###")
    print("###================================###")


@project_config.group('get')
@click.argument('key')
@click.pass_context
def project_config_get(key, ctx):
    """
            Gets value of given configuration item.
    """

    config = ctx.obj['config']

    print("###===============================###")
    print("### get project config subcommand ###")
    print("###===============================###")


@project_config.group('set')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_set(key, value, ctx):
    """
            Sets value of given configuration item.
    """

    config = ctx.obj['config']

    print("###===============================###")
    print("### set project config subcommand ###")
    print("###===============================###")


@project_config.group('reset')
@click.argument('key')
@click.pass_context
def project_config_reset(key, ctx):
    """
            Resets given configuration item to its default value.
    """

    config = ctx.obj['config']

    print("###=================================###")
    print("### reset project config subcommand ###")
    print("###=================================###")


@project_config.group('add-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_list(key, value, ctx):
    """
            Adds value to list for given configuration item.
    """

    config = ctx.obj['config']

    print("###====================================###")
    print("### add-item project config subcommand ###")
    print("###====================================###")


@project_config.group('remove-item')
@click.argument('key')
@click.argument('value')
@click.pass_context
def project_config_list(key, value, ctx):
    """
            Removes value from list for given configuration item.
    """

    config = ctx.obj['config']

    print("###=======================================###")
    print("### remove-item project config subcommand ###")
    print("###=======================================###")


@project_config.group('clear-items')
@click.argument('key')
@click.pass_context
def project_config_clear_items(key, ctx):
    """
            Removes all values from list for given configuration item.
    """

    config = ctx.obj['config']

    print("###=======================================###")
    print("### clear-items project config subcommand ###")
    print("###=======================================###")

