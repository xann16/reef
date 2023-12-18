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
@click.pass_context
def project_describe(ctx):
    """
            Displays information on given reef project.
    """

    config = ctx.obj['config']

    print("###=========================###")
    print("### list project subcommand ###")
    print("###=========================###")


@project.command('create')
@click.pass_context
def project_create(ctx):
    """
            Creates new reef project.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### create project subcommand ###")
    print("###===========================###")


@project.command('import')
@click.pass_context
def project_import(ctx):
    """
            Tries to add existing project to reef repository.
    """

    config = ctx.obj['config']

    print("###===========================###")
    print("### import project subcommand ###")
    print("###===========================###")


@project.command('delete')
@click.pass_context
def project_delete(ctx):
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
@click.pass_context
def project_set_default(ctx):
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
@click.pass_context
def project_default_module(ctx):
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
@click.pass_context
def project_config_get(ctx):
    """
            Gets value of given configuration item.
    """

    config = ctx.obj['config']

    print("###===============================###")
    print("### get project config subcommand ###")
    print("###===============================###")


@project_config.group('set')
@click.pass_context
def project_config_set(ctx):
    """
            Sets value of given configuration item.
    """

    config = ctx.obj['config']

    print("###===============================###")
    print("### set project config subcommand ###")
    print("###===============================###")


@project_config.group('reset')
@click.pass_context
def project_config_reset(ctx):
    """
            Reets given configuration item to its default value.
    """

    config = ctx.obj['config']

    print("###=================================###")
    print("### reset project config subcommand ###")
    print("###=================================###")


@project_config.group('add-item')
@click.pass_context
def project_config_list(ctx):
    """
            Adds value to list for given configuration item.
    """

    config = ctx.obj['config']

    print("###====================================###")
    print("### add-item project config subcommand ###")
    print("###====================================###")


@project_config.group('remove-item')
@click.pass_context
def project_config_list(ctx):
    """
            Removes value from list for given configuration item.
    """

    config = ctx.obj['config']

    print("###=======================================###")
    print("### remove-item project config subcommand ###")
    print("###=======================================###")

