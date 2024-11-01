from contextlib import contextmanager

import click
from click import UsageError
from rich.console import Console
from rich.table import Table

from sbtse import worm
from sbtse.errors import WormError, WormErrorClientNotRegistered


class PinParamType(click.ParamType):
    name = "pin"

    def convert(self, value, param, ctx):
        if len(value) != 5:
            self.fail(f"{value!r} is not of length 5", param, ctx)
        if not value.isdigit():
            self.fail(f"{value!r} is not only digits", param, ctx)
        return value


class PukParamType(click.ParamType):
    name = "puk"

    def convert(self, value, param, ctx):
        if len(value) != 6:
            self.fail(f"{value!r} is not of length 5", param, ctx)
        if not value.isdigit():
            self.fail(f"{value!r} is not only digits", param, ctx)
        return value


T_PIN = PinParamType()
T_PUK = PukParamType()


@click.group()
@click.option('--path', type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True, writable=True),
              help='TSE mount point')
@click.option('--url', type=str, help='LAN TSE URL')
@click.option('--api-key', type=str, help='LAN TSE API Key')
@click.option('--tse', type=str, help='LAN TSE serial number')
@click.pass_context
def main(ctx, path, url, api_key, tse):
    ctx.ensure_object(dict)
    if not path and not (url and api_key and tse):
        raise UsageError("Please set either --path or --url/--api-key/--tse.")
    ctx.obj["path"] = path
    ctx.obj["url"] = url
    ctx.obj["api_key"] = api_key
    ctx.obj["tse"] = tse


@contextmanager
def _tse_context(ctx):
    if ctx.obj["path"]:
        with worm.LocalWormContext(ctx.obj["path"]) as w:
            yield w
    else:
        with worm.LANWormContext(ctx.obj["url"], ctx.obj["api_key"]) as w:
            w.select_tse(ctx.obj["tse"])
            yield w


@main.command(help="Show info and flash health status")
@click.pass_context
def info(ctx):
    with _tse_context(ctx) as w:
        info = w.info()

        table = Table(title="Information")
        table.add_column("Key", justify="left", no_wrap=True)
        table.add_column("Value", justify="left")
        for k, v in info.items():
            table.add_row(k, str(v))

        console = Console()
        console.print(table)
        info = w.flash_health()

        table = Table(title="Flash health")
        table.add_column("Key", justify="left", no_wrap=True)
        table.add_column("Value", justify="left")
        for k, v in info.items():
            table.add_row(k, str(v))

        console = Console()
        console.print(table)


@main.command(help="Run self-test")
@click.argument("client_id", type=str)
@click.pass_context
def selftest(ctx, client_id):
    with _tse_context(ctx) as w:
        try:
            w.run_self_test(client_id)
        except WormError as e:
            click.echo(click.style(f"Failed with error: {type(e).__name__}", fg="red"))
        else:
            click.echo(click.style("OK", fg="green"))


@main.command(help="Factory reset (development TSE only)")
@click.pass_context
def factory_reset(ctx):
    with _tse_context(ctx) as w:
        w.factory_reset()


@main.command(help="Run setup procedure for a fresh TSE")
@click.argument("client_id", type=str)
@click.argument("admin_pin", type=T_PIN)
@click.argument("admin_puk", type=T_PUK)
@click.argument("time_admin_pin", type=T_PIN)
@click.pass_context
def setup(ctx, client_id, admin_pin, admin_puk, time_admin_pin):
    with _tse_context(ctx) as w:
        try:
            w.run_self_test(client_id)
        except WormErrorClientNotRegistered:
            pass
        else:
            raise UsageError("Client already registered.")
        w.setup(client_id, admin_pin, admin_puk, time_admin_pin)


@main.group("config", help="Manipulate TSE configuration")
@click.pass_context
def config(ctx):
    pass


@config.command(help="Enable CTSS")
@click.argument("admin_pin", type=T_PIN)
@click.pass_context
def ctss_enable(ctx, admin_pin):
    with _tse_context(ctx) as w:
        w.login_as_admin(admin_pin)
        w.ctss_enable()


@config.command(help="Disable CTSS")
@click.argument("admin_pin", type=T_PIN)
@click.pass_context
def ctss_disable(ctx, admin_pin):
    with _tse_context(ctx) as w:
        w.login_as_admin(admin_pin)
        w.ctss_disable()


"""
TODO:
- initialize
- decommission
- firmware update
- enable export if csp test fails
- disable export if csp test fails
- register client
- deregister clients
- list registered clients
- unblock admin
- unblock time admin
- change puk
- change pin
- change time admin pin
- derive initial credentials
- transaction start
- transaction update
- transaction finish
- last transaction
- list started transactions
- list entries
- export tar
"""

if __name__ == '__main__':
    main(obj={})
