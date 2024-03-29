from os import path

import click

from .cli_project import project
from .config import Config

GROUP_COMMANDS = ["init", "project", "module", "component", "extras", "config"]

VERSION = "0.1.0"

CTX = dict(help_option_names=["-h", "--help"])


@click.group(invoke_without_command=True, context_settings=CTX)
@click.pass_context
@click.option("--verbose", "-v", is_flag=True, help="Increase output verbosity level")
@click.option("--version", "-V", is_flag=True, help="Print current version of reef used")
@click.option("--context", "-c", default="", help="Provides context as project::module::component")
def main(ctx, context, verbose, version):
    """
    Strands ecosystem tool for generating project structures, build systems and
    maintain them.
    """
    if version:
        click.echo(f"reef - version {VERSION}")
        click.echo()
        click.echo("Strands ecosystem tool for generating project structures, build systems and")
        click.echo("maintain them.")
        click.echo("                                                Created by Maciej Manna")
        click.echo("                                                  maciejmanna@gmail.com")
        click.echo("                                                      github.com/xann16")
        click.echo()
        return
    if ctx.invoked_subcommand is None:
        click.echo("Specify one of the commands below:")
        for cmd in GROUP_COMMANDS:
            print(cmd, end=" ")
        print()

    context_tokens = context.split("::", 3) if context else []
    ctx.obj["project"] = context_tokens[0] if len(context_tokens) > 0 else ""
    ctx.obj["module"] = context_tokens[1] if len(context_tokens) > 1 else ""
    ctx.obj["component"] = context_tokens[2] if len(context_tokens) > 2 else ""

    ctx.obj["is_verbose"] = verbose
    ctx.obj["config"] = Config.load(VERSION)


@main.command("init", context_settings=CTX)
@click.pass_context
@click.option(
    "--config-path",
    "-p",
    help="Path to directory containing reef config (default: ~/.reef)",
    type=click.Path(exists=False),
    default=path.abspath(path.expanduser("~/.reef")),
)
@click.option(
    "--exec-path",
    "-x",
    help="Path to directory with reef executable shell script (default: current directory)",
    type=click.Path(exists=True),
    default=".",
)
def init(ctx, config_path, exec_path):
    """
    Initialises reef config and environment before first use.
    """

    new_config = Config(config_path, exec_path, VERSION)

    if Config.get_path() and not click.confirm("There is a reef environment already initialised. Continue anyway?"):
        click.echo("Reef init aborted.")
        return

    click.echo("Please review provided config...\n")
    print(new_config)
    if not click.confirm("Confirm provided config?"):
        click.echo("Reef init aborted.")
        return

    new_config.update_shell_config(ctx.obj["VERBOSE"])
    new_config.save_as_json(new_config.config_path, ctx.obj["VERBOSE"])

    click.echo("\nReef init successful.")


main.add_command(project)


@main.command("module", context_settings=CTX)
@click.pass_context
def module(ctx):
    """
    Handles module cration and mainteneance of reef projects.
    """
    config = ctx.obj["config"]

    print("###===================###")
    print("### module subcommand ###")
    print("###===================###")


@main.command("component", context_settings=CTX)
@click.pass_context
def component(ctx):
    """
    Handles component cration and mainteneance of reef projects and modules.
    """
    config = Config.load(VERSION)

    print("###======================###")
    print("### component subcommand ###")
    print("###======================###")


@main.command("extras", context_settings=CTX)
@click.pass_context
def component(ctx):
    """
    Extra features unhandled elsewhere.
    """
    config = Config.load(VERSION)

    print("###===================###")
    print("### extras subcommand ###")
    print("###===================###")


@main.command("config", context_settings=CTX)
@click.pass_context
def component(ctx):
    """
    Handles general reef configuration.
    """
    config = Config.load(VERSION)

    print("###===================###")
    print("### config subcommand ###")
    print("###===================###")
