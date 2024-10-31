import datetime

from sbtse.errors import WormErrorClientNotRegistered
from sbtse.worm import *

print(get_version())
print(is_online_sdk())
print(signature_algorithm())
print(log_time_format())
client_id = "TEST"

with WormContext("/mnt/tse/") as w:
    w.keepalive_configure(30)
    w.keepalive_disable()
    w.factory_reset()
    print(w.info())
    print(w.derive_initial_credentials())
    print("Running self test...")
    try:
        w.run_self_test(client_id)
    except WormErrorClientNotRegistered:
        print("Not registered.")
    if w.bundled_firmware_update_available():
        w.bundled_firmware_update_apply()
    print(w.flash_health())
    w.setup(client_id, "12345", "123456", "12345")
    w.change_admin_pin("12345", "54321")
    w.change_time_admin_pin("12345", "66666")
    w.change_puk("123456", "999999")
    w.unblock_admin("999999", "22222")
    w.login_as_admin("22222")
    w.login_as_time_admin("66666")
    w.update_time(datetime.datetime(2020, 1, 1, 2, 0, 0, tzinfo=datetime.timezone.utc))
    w.logout_as_time_admin()
    w.register_client("TEST2")
    print(w.list_registered_clients())
    print(w.transaction_start("TEST", "Foobar", "Kassenbeleg"))