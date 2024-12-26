import datetime
import os
from contextlib import contextmanager

import click
import dateutil.parser
import uvicorn
from click import UsageError
from rich.console import Console
from rich.table import Table

from sbtse import worm
from sbtse.errors import (
    WormError,
    WormErrorClientNotRegistered,
    WormErrorWrongStateNeedsSelfTest,
)


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
            self.fail(f"{value!r} is not of length 6", param, ctx)
        if not value.isdigit():
            self.fail(f"{value!r} is not only digits", param, ctx)
        return value


class DateTimeParamType(click.ParamType):
    name = "datetime"

    def convert(self, value, param, ctx):
        return dateutil.parser.parse(value)


T_PIN = PinParamType()
T_PUK = PukParamType()
T_DATETIME = DateTimeParamType()


@click.group()
@click.option(
    "--path",
    type=click.Path(
        exists=True, dir_okay=True, file_okay=False, readable=True, writable=True
    ),
    help="TSE mount point",
)
@click.option("--url", type=str, help="LAN TSE URL")
@click.option("--api-key", type=str, help="LAN TSE API Key")
@click.option("--tse", type=str, help="LAN TSE serial number")
@click.pass_context
def main(ctx, path, url, api_key, tse):
    ctx.ensure_object(dict)
    if not path and not (url and api_key and tse) and ctx.invoked_subcommand != "mock":
        raise UsageError("Please set either --path or --url/--api-key/--tse.")
    ctx.obj["path"] = path
    ctx.obj["url"] = url
    ctx.obj["api_key"] = api_key
    ctx.obj["tse"] = tse


@contextmanager
def _tse_context(ctx, admin_pin=None, time_admin_pin=None, self_test_client=None):
    if ctx.obj["path"]:
        with worm.LocalWormContext(ctx.obj["path"]) as w:
            info = w.info()
            if not info["hasPassedSelfTest"] and self_test_client:
                try:
                    w.run_self_test(self_test_client)
                except WormErrorClientNotRegistered:
                    pass
            if admin_pin:
                w.login_as_admin(admin_pin)
            if time_admin_pin:
                w.login_as_time_admin(time_admin_pin)
                if info["isDevelopmentFirmware"] and info[
                    "certificateExpirationDate"
                ] < datetime.datetime.now(datetime.timezone.utc):
                    # Development TSEs expired 2020-01, so let's backdate so we can still use them for testing
                    w.update_time(
                        datetime.datetime.now(datetime.timezone.utc).replace(year=2019)
                    )
                else:
                    w.update_time()
            yield w
    else:
        with worm.LANWormContext(ctx.obj["url"], ctx.obj["api_key"]) as w:
            info = w.info()
            w.select_tse(ctx.obj["tse"])
            if not info["hasPassedSelfTest"] and self_test_client:
                try:
                    w.run_self_test(self_test_client)
                except WormErrorClientNotRegistered:
                    pass
            if admin_pin:
                w.login_as_admin(admin_pin)
            if time_admin_pin:
                w.login_as_time_admin(time_admin_pin)
                if info["isDevelopmentFirmware"] and info[
                    "certificateExpirationDate"
                ] < datetime.datetime.now(datetime.timezone.utc):
                    # Development TSEs expired 2020-01, so let's backdate so we can still use them for testing
                    w.update_time(
                        datetime.datetime.now(datetime.timezone.utc).replace(year=2019)
                    )
                else:
                    w.update_time()
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

        try:
            info = w.flash_health()
        except WormErrorWrongStateNeedsSelfTest:
            click.echo(
                click.style("Flash health can only be shown after selftest.", fg="red")
            )
            return

        table = Table(title="Flash health")
        table.add_column("Key", justify="left", no_wrap=True)
        table.add_column("Value", justify="left")
        for k, v in info.items():
            table.add_row(k, str(v))

        console = Console()
        console.print(table)


@main.command(help="Run self-test")
@click.option("--client-id", "-c", prompt=True, type=str, help="Client ID")
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
@click.option("--client-id", "-c", prompt=True, type=str, help="Client ID")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.option("--admin-puk", prompt=True, type=T_PUK, help="Admin PUK")
@click.option("--time-admin-pin", prompt=True, type=T_PIN, help="Time Admin PIN")
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
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def ctss_enable(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.ctss_enable()


@config.command(help="Disable CTSS")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selfest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def ctss_disable(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.ctss_disable()


@config.command(help="Final step for TSE initialization")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def initialize(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.initialize()


@config.command(help="Register client")
@click.option("--client-id", "-c", prompt=True, type=str, help="Client ID")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def register_client(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.register_client(client_id)


@config.command(help="Deregister client")
@click.option("--client-id", "-c", prompt=True, type=str, help="Client ID")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def deregister_client(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.deregister_client(client_id)


@config.command(help="List of registered clients")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def list_clients(ctx, admin_pin):
    with _tse_context(ctx, admin_pin=admin_pin) as w:
        for c in w.list_registered_clients():
            print(c)


@config.command(help="Enable export if CSP test fails")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def enable_export_if_csp_test_fails(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.enable_export_if_csp_test_fails()


@config.command(help="Disable export if CSP test fails")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def disable_export_if_csp_test_fails(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.disable_export_if_csp_test_fails()


@config.command(help="Decommission (irrevocably disable) TSE")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def decommission(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        w.update_time()
        w.decommission()


@main.command(help="Update firmware to version bundled with SDK.")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.pass_context
def firmware_update(ctx, client_id, admin_pin):
    with _tse_context(ctx, self_test_client=client_id, admin_pin=admin_pin) as w:
        if w.bundled_firmware_update_available():
            click.echo("Applying firmware update...")
            w.bundled_firmware_update_apply()
            click.echo(click.style("OK", fg="green"))
        else:
            click.echo(click.style("No update available.", fg="red"))


@main.group("pin", help="Manage Admin PIN")
@click.pass_context
def pin(ctx):
    pass


@pin.command(help="Unblock Admin PIN")
@click.option("--admin-puk", prompt=True, type=T_PUK, help="Admin PUK")
@click.option("--new-pin", prompt=True, type=T_PIN, help="New PIN")
@click.pass_context
def unblock(ctx, admin_puk, new_pin):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        w.unblock_admin(admin_puk, new_pin)


@pin.command(help="Change Admin PIN")
@click.option("--old-pin", prompt=True, type=T_PIN, help="Old PIN")
@click.option("--new-pin", prompt=True, type=T_PIN, help="New PIN")
@click.pass_context
def change(ctx, old_pin, new_pin):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        w.change_admin_pin(old_pin, new_pin)


@main.group("time-admin-pin", help="Manage Time Admin PIN")
@click.pass_context
def time_admin_pin(ctx):
    pass


@time_admin_pin.command(help="Unblock Time Admin PIN")
@click.option("--admin-puk", prompt=True, type=T_PUK, help="Admin PUK")
@click.option("--new-pin", prompt=True, type=T_PIN, help="New PIN")
@click.pass_context
def unblock(ctx, admin_puk, new_pin):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        w.unblock_time_admin(admin_puk, new_pin)


@time_admin_pin.command(help="Change Time Admin PIN")
@click.option("--old-pin", prompt=True, type=T_PIN, help="Old PIN")
@click.option("--new-pin", prompt=True, type=T_PIN, help="New PIN")
@click.pass_context
def change(ctx, old_pin, new_pin):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        w.change_time_admin_pin(old_pin, new_pin)


@main.group("puk", help="Manage PUK")
@click.pass_context
def puk(ctx):
    pass


@puk.command(help="Change PUK")
@click.option("--old-puk", prompt=True, type=T_PUK, help="Old PUK")
@click.option("--new-puk", prompt=True, type=T_PUK, help="New PUK")
@click.pass_context
def change(ctx, old_puk, new_puk):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        w.change_puk(old_puk, new_puk)


@puk.command(help="Show initial credentials")
@click.pass_context
def initial(ctx):
    with _tse_context(ctx, self_test_client="UNKNOWN") as w:
        for k, v in w.derive_initial_credentials().items():
            print(f"{k}: {v}")


@main.group("transaction", help="Create and query transactions")
@click.pass_context
def transaction(ctx):
    pass


def _print_tx(tx):
    table = Table(title="Transaction")
    table.add_column("Key", justify="left", no_wrap=True)
    table.add_column("Value", justify="left")
    for k, v in tx.items():
        table.add_row(k, str(v))

    console = Console()
    console.print(table)


@transaction.command(help="Start transaction")
@click.option("--time-admin-pin", prompt=True, type=T_PIN, help="Time Admin PIN")
@click.argument("client_id")
@click.argument("process_type", required=False)
@click.argument("process_data", required=False)
@click.pass_context
def start(ctx, client_id, process_type, process_data, time_admin_pin):
    with _tse_context(
        ctx, self_test_client=client_id, time_admin_pin=time_admin_pin
    ) as w:
        tx = w.transaction_start(client_id, process_data or "", process_type or "")
        _print_tx(tx)


@transaction.command(help="Update transaction")
@click.option("--time-admin-pin", prompt=True, type=T_PIN, help="Time Admin PIN")
@click.argument("client_id")
@click.argument("transaction_id", type=int)
@click.argument("process_type")
@click.argument("process_data")
@click.pass_context
def update(ctx, client_id, transaction_id, process_type, process_data, time_admin_pin):
    with _tse_context(
        ctx, self_test_client=client_id, time_admin_pin=time_admin_pin
    ) as w:
        tx = w.transaction_update(client_id, transaction_id, process_data, process_type)
        _print_tx(tx)


@transaction.command(help="Finish transaction")
@click.option("--time-admin-pin", prompt=True, type=T_PIN, help="Time Admin PIN")
@click.argument("client_id")
@click.argument("transaction_id", type=int)
@click.argument("process_type")
@click.argument("process_data")
@click.pass_context
def finish(ctx, client_id, transaction_id, process_type, process_data, time_admin_pin):
    with _tse_context(
        ctx, self_test_client=client_id, time_admin_pin=time_admin_pin
    ) as w:
        tx = w.transaction_finish(client_id, transaction_id, process_data, process_type)
        _print_tx(tx)


@transaction.command(help="Show details of last transaction")
@click.argument("client_id", required=False)
@click.pass_context
def last(ctx, client_id):
    with _tse_context(ctx, self_test_client=client_id) as w:
        _print_tx(w.last_transaction(client_id))


@transaction.command(help="List started transaction IDs")
@click.argument("client_id", required=False)
@click.pass_context
def list_started(ctx, client_id):
    with _tse_context(ctx, self_test_client=client_id) as w:
        for tx in w.list_started_transactions(client_id):
            print(tx)


@main.group("entries", help="Query log entries")
@click.pass_context
def entries(ctx):
    pass


@entries.command(help="Retrieve entry by ID")
@click.argument("entry_id", type=int)
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.pass_context
def get(ctx, admin_pin, client_id, entry_id):
    with _tse_context(ctx, admin_pin=admin_pin, self_test_client=client_id) as w:
        entry = w.entry_by_id(entry_id)
        table = Table(title="Flash health")
        table.add_column("Key", justify="left", no_wrap=True)
        table.add_column("Value", justify="left")
        for k, v in entry.items():
            table.add_row(k, str(v))

        console = Console()
        console.print(table)


@entries.command(help="List entries")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.pass_context
def list(ctx, admin_pin, client_id):
    with _tse_context(ctx, admin_pin=admin_pin, self_test_client=client_id) as w:
        table = Table(title="Entries")
        table.add_column("ID", justify="left", no_wrap=True)
        table.add_column("Valid", justify="left")
        table.add_column("Type", justify="left")
        table.add_column("Message", justify="left")
        table.add_column("Process Data", justify="left")
        for entry in w.iterate_entries():
            table.add_row(
                str(entry["id"]),
                str(entry["isValid"]),
                entry["type"],
                str(entry["message"]),
                str(entry["processData"]),
            )

        console = Console()
        console.print(table)


@main.command(help="Delete stored data. Requires a full export first.")
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.option(
    "--client-id", "-c", prompt=True, type=str, help="Client ID (for selftest)"
)
@click.pass_context
def delete(ctx, admin_pin, client_id):
    with _tse_context(ctx, admin_pin=admin_pin, self_test_client=client_id) as w:
        w.delete_stored_data()


@main.command(help="Export stored data.")
@click.argument("outfile", type=click.File("wb"))
@click.option("--admin-pin", prompt=True, type=T_PIN, help="Admin PIN")
@click.option(
    "--client-id",
    "-c",
    prompt=True,
    type=str,
    help="Client ID (for selftest, if necessary)",
)
@click.option("--filter-client-id", type=str, help="Client ID (for filtering)")
@click.option("--start-date", type=T_DATETIME, help="Start date (inclusively)")
@click.option("--end-date", type=T_DATETIME, help="End date (inclusively)")
@click.option("--start-transaction", type=int, help="Start transaction (inclusive)")
@click.option("--end-transaction", type=int, help="End transaction (inclusive)")
@click.pass_context
def export(
    ctx,
    outfile,
    admin_pin,
    client_id,
    filter_client_id,
    start_date,
    end_date,
    start_transaction,
    end_transaction,
):
    with _tse_context(ctx, admin_pin=admin_pin, self_test_client=client_id) as w:
        w.export_tar(
            outfile,
            start_date=start_date,
            end_date=end_date,
            client_id=filter_client_id,
            start_transaction=start_transaction,
            end_transaction=end_transaction,
        )


@main.command(help="Run local API server")
@click.option("--reload", is_flag=True, help="Auto-reload code (development only)")
@click.option("--debug", is_flag=True, help="Debug log")
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Host to listen to (default: 127.0.0.1)",
)
@click.option(
    "--port", type=int, default=9873, help="Host to listen to (default: 9873)"
)
@click.option("--time-admin-pin", prompt=True, type=T_PIN, help="Time Admin PIN")
@click.pass_context
def serve(ctx, host, port, reload, time_admin_pin, debug):
    _serve(ctx, host, port, reload, time_admin_pin, debug, "sbtse.api:app")


@main.command(help="Run mock API server (development only)")
@click.option("--reload", is_flag=True, help="Auto-reload code (development only)")
@click.option("--debug", is_flag=True, help="Debug log")
@click.option(
    "--host",
    type=str,
    default="127.0.0.1",
    help="Host to listen to (default: 127.0.0.1)",
)
@click.option(
    "--port", type=int, default=9873, help="Host to listen to (default: 9873)"
)
@click.pass_context
def mock(ctx, host, port, reload, debug):
    _serve(ctx, host, port, reload, "12345", debug, "sbtse.mockapi:app")


def _serve(ctx, host, port, reload, time_admin_pin, debug, app):
    os.environ.update(
        {
            "SBTSE_PATH": ctx.obj["path"] or "",
            "SBTSE_URL": ctx.obj["url"] or "",
            "SBTSE_API_KEY": ctx.obj["api_key"] or "",
            "SBTSE_TSE": ctx.obj["tse"] or "",
            "SBTSE_TAPIN": time_admin_pin,
        }
    )
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"][
        "fmt"
    ] = "%(asctime)s - %(levelname)s - %(name)s - thread=%(thread)s - %(message)s"
    log_config["formatters"]["default"][
        "fmt"
    ] = "%(asctime)s - %(levelname)s - %(name)s - thread=%(thread)s - %(message)s"
    log_config["loggers"][""] = {
        "handlers": ["default"],
        "level": "DEBUG" if debug else "INFO",
        "propagate": False,
    }
    uvicorn.run(
        app,
        host=host,
        port=port,
        workers=1,  # No concurrent access to TSE allowed!
        reload=reload,
        log_config=log_config,
    )


if __name__ == "__main__":
    main(obj={})
