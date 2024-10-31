import datetime
import logging
from _ctypes import POINTER, byref
from ctypes import c_ubyte, c_uint32, c_uint8, c_int, c_char_p
from typing import List

from . import _worm
from .errors import guard

logger = logging.getLogger(__name__)


def get_version() -> str:
    """
    Returns the library version.
    """
    return _worm.worm_getVersion().decode()


def is_online_sdk() -> bool:
    """
    Returns whether this SDK is an online SDK or not.
    """
    return bool(_worm.worm_isOnlineSdk())


def signature_algorithm() -> str:
    """
    Returns the signature algorithm that is used by the TSE.
    """
    return _worm.worm_signatureAlgorithm().decode()


def log_time_format() -> str:
    """
    Returns the log time format used by the TSE.
    """
    return _worm.worm_logTimeFormat().decode()


def _c_ubyte(bs):
    return (c_ubyte * len(bs))(*bs)


class WormContext:
    def __init__(self, mount_point: str):
        self._ctx = POINTER(_worm.WormContext)()
        guard(_worm.worm_init(byref(self._ctx), mount_point.encode()))

    def close(self):
        _worm.worm_cleanup(self._ctx)
        del self._ctx

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def keepalive_configure(self, seconds: int):
        guard(_worm.worm_keepalive_configure(self._ctx, seconds))

    def keepalive_disable(self):
        guard(_worm.worm_keepalive_disable(self._ctx))

    def info(self) -> dict:
        i = _worm.worm_info_new(self._ctx)
        guard(_worm.worm_info_read(i))

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_info_tsePublicKey(i, byref(val_res), byref(val_len))
        pubkey = bytes([val_res[i] for i in range(val_len.value)])

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_info_tseSerialNumber(i, byref(val_res), byref(val_len))
        serial = bytes([val_res[i] for i in range(val_len.value)])

        info = {
            "isDevelopmentFirmware": bool(_worm.worm_info_isDevelopmentFirmware(i)),
            "capacity": _worm.worm_info_capacity(i),
            "size": _worm.worm_info_size(i),
            "hasValidTime": _worm.worm_info_hasValidTime(i),
            "hasPassedSelfTest": _worm.worm_info_hasPassedSelfTest(i),
            "isCtssInterfaceActive": _worm.worm_info_isCtssInterfaceActive(i),
            "isExportEnabledIfCspTestFails": _worm.worm_info_isExportEnabledIfCspTestFails(
                i
            ),
            "initializationState": _worm.worm_info_initializationState(i),
            "hasChangedPuk": _worm.worm_info_hasChangedPuk(i),
            "hasChangedAdminPin": _worm.worm_info_hasChangedAdminPin(i),
            "timeUntilNextSelfTest": _worm.worm_info_timeUntilNextSelfTest(i),
            "startedTransactions": _worm.worm_info_startedTransactions(i),
            "maxStartedTransactions": _worm.worm_info_maxStartedTransactions(i),
            "createdSignatures": _worm.worm_info_createdSignatures(i),
            "maxSignatures": _worm.worm_info_maxSignatures(i),
            "remainingSignatures": _worm.worm_info_remainingSignatures(i),
            "maxTimeSynchronizationDelay": _worm.worm_info_maxTimeSynchronizationDelay(
                i
            ),
            "maxUpdateDelay": _worm.worm_info_maxUpdateDelay(i),
            "tsePublicKey": pubkey,
            "timeUntilNextTimeSynchronization": _worm.worm_info_timeUntilNextTimeSynchronization(
                i
            ),
            "tseSerialNumberBytes": serial,
            "tseSerialNumberHex": serial.hex(),
            "tseDescription": _worm.worm_info_tseDescription(i),
            "registeredClients": _worm.worm_info_registeredClients(i),
            "maxRegisteredClients": _worm.worm_info_maxRegisteredClients(i),
            "certificateExpirationDate": datetime.datetime.fromtimestamp(
                _worm.worm_info_certificateExpirationDate(i), datetime.timezone.utc
            ),
            "tarExportSizeInSectors": _worm.worm_info_tarExportSizeInSectors(i),
            "tarExportSize": _worm.worm_info_tarExportSize(i),
            "hardwareVersion": _worm.worm_info_hardwareVersion(i),
            "softwareVersion": _worm.worm_info_softwareVersion(i),
            "formFactor": _worm.worm_info_formFactor(i),
        }
        _worm.worm_info_free(i)
        return info

    def flash_health(self) -> dict:
        val_errors = c_uint32()
        val_spare = c_uint8()
        val_erase = c_uint8()
        val_retention = c_uint8()
        guard(
            _worm.worm_flash_health_summary(
                self._ctx,
                byref(val_errors),
                byref(val_spare),
                byref(val_erase),
                byref(val_retention),
            )
        )
        needs_replacement = bool(
            _worm.worm_flash_health_needs_replacement(val_errors, val_spare, val_erase)
        )
        return {
            "uncorrectableEccErrors": val_errors,
            "percentageRemainingSpareBlocks": val_spare,
            "percentageRemainingEraseCounts": val_erase,
            "percentageRemainingTenYearsDataRetention": val_retention,
            "needsReplacement": needs_replacement,
        }

    def run_self_test(self, client_id):
        guard(_worm.worm_tse_runSelfTest(self._ctx, client_id))

    def factory_reset(self):
        # Works only on development TSEs (pre-2020).
        guard(_worm.worm_tse_factoryReset(self._ctx))

    def setup(
        self,
        client_id: str,
        admin_pin: str,
        admin_puk: str,
        time_admin_pin: str,
        credential_seed="SwissbitSwissbit",
    ):
        assert len(admin_pin) == 5
        assert len(admin_puk) == 6
        assert len(time_admin_pin) == 5
        guard(
            _worm.worm_tse_setup(
                self._ctx,
                _c_ubyte(credential_seed.encode()),
                len(credential_seed),
                _c_ubyte(admin_puk.encode()),
                len(admin_puk),
                _c_ubyte(admin_pin.encode()),
                len(admin_pin),
                _c_ubyte(time_admin_pin.encode()),
                len(time_admin_pin),
                client_id,
            )
        )

    def ctss_enable(self):
        guard(_worm.worm_tse_ctss_enable(self._ctx))

    def ctss_disable(self):
        guard(_worm.worm_tse_ctss_disable(self._ctx))

    def initialize(self):
        guard(_worm.worm_tse_initialize(self._ctx))

    def decommission(self):
        guard(_worm.worm_tse_decommission(self._ctx))

    def update_time(self, time=None):
        if not time:
            time = datetime.datetime.now(datetime.timezone.utc)
        if not isinstance(time, int):
            time = int(time.astimezone(datetime.timezone.utc).timestamp())
        guard(_worm.worm_tse_updateTime(self._ctx, time))

    def bundled_firmware_update_available(self) -> bool:
        val = _worm.WormTseFirmwareUpdate()
        guard(_worm.worm_tse_firmwareUpdate_isBundledAvailable(self._ctx, byref(val)))
        return val.value != _worm.WORM_FW_NONE

    def bundled_firmware_update_apply(self):
        guard(_worm.worm_tse_firmwareUpdate_applyBundled(self._ctx))

    def enable_export_if_csp_test_fails(self):
        guard(_worm.worm_tse_enableExportIfCspTestFails(self._ctx))

    def disable_export_if_csp_test_fails(self):
        guard(_worm.worm_tse_disableExportIfCspTestFails(self._ctx))

    def register_client(self, client_id: str):
        guard(_worm.worm_tse_registerClient(self._ctx, client_id))

    def deregister_client(self, client_id: str):
        guard(_worm.worm_tse_deregisterClient(self._ctx, client_id))

    def list_registered_clients(self) -> List[str]:
        result = []
        skip = 0
        while True:
            clients = _worm.WormRegisteredClients()
            guard(_worm.worm_tse_listRegisteredClients(self._ctx, skip, byref(clients)))
            print(clients.amount, clients.clientIds)
            result += [
                c.raw.decode().rstrip('\x00') for c in
                clients.clientIds[:clients.amount]
            ]
            if clients.amount == 16:
                skip += 16
            else:
                break
        return result

    def _login(self, user: _worm.WormUserId, pin: str):
        val_remaining_retries = c_int()
        ret = _worm.worm_user_login(
            self._ctx,
            user,
            _c_ubyte(pin.encode()),
            len(pin.encode()),
            byref(val_remaining_retries),
        )
        if ret:
            logger.warning("Remaining retries: %d", val_remaining_retries.value)
        guard(ret)

    def login_as_admin(self, pin: str):
        self._login(_worm.WORM_USER_ADMIN, pin)

    def login_as_time_admin(self, pin: str):
        self._login(_worm.WORM_USER_TIME_ADMIN, pin)

    def logout_as_admin(self):
        guard(_worm.worm_user_logout(self._ctx, _worm.WORM_USER_ADMIN))

    def logout_as_time_admin(self):
        guard(_worm.worm_user_logout(self._ctx, _worm.WORM_USER_TIME_ADMIN))

    def _unblock(self, user: _worm.WormUserId, puk: str, new_pin: str):
        val_remaining_retries = c_int()
        assert len(new_pin) == 5
        assert len(puk) == 6
        ret = _worm.worm_user_unblock(
            self._ctx,
            user,
            _c_ubyte(puk.encode()),
            len(puk),
            _c_ubyte(new_pin.encode()),
            len(new_pin),
            byref(val_remaining_retries),
        )
        if ret:
            logger.warning("Remaining retries: %d", val_remaining_retries.value)
        guard(ret)

    def unblock_admin(self, puk: str, new_pin: str):
        self._unblock(_worm.WORM_USER_ADMIN, puk, new_pin)

    def unblock_time_admin(self, puk: str, new_pin: str):
        self._unblock(_worm.WORM_USER_TIME_ADMIN, puk, new_pin)

    def change_puk(self, puk: str, new_puk: str):
        val_remaining_retries = c_int()
        assert len(puk) == 6
        assert len(new_puk) == 6
        ret = _worm.worm_user_change_puk(
            self._ctx,
            _c_ubyte(puk.encode()),
            len(puk),
            _c_ubyte(new_puk.encode()),
            len(new_puk),
            byref(val_remaining_retries),
        )
        if ret:
            logger.warning("Remaining retries: %d", val_remaining_retries.value)
        guard(ret)

    def _change_pin(self, user: _worm.WormUserId, pin: str, new_pin: str):
        val_remaining_retries = c_int()
        assert len(new_pin) == 5
        assert len(pin) == 5
        ret = _worm.worm_user_change_pin(
            self._ctx,
            user,
            _c_ubyte(pin.encode()),
            len(pin),
            _c_ubyte(new_pin.encode()),
            len(new_pin),
            byref(val_remaining_retries),
        )
        if ret:
            logger.warning("Remaining retries: %d", val_remaining_retries.value)
        guard(ret)

    def change_admin_pin(self, pin: str, new_pin: str):
        self._change_pin(_worm.WORM_USER_ADMIN, pin, new_pin)

    def change_time_admin_pin(self, pin: str, new_pin: str):
        self._change_pin(_worm.WORM_USER_TIME_ADMIN, pin, new_pin)

    def derive_initial_credentials(self, credential_seed="SwissbitSwissbit") -> dict:
        _worm.worm_user_deriveInitialCredentials.argtypes = [
            # This is easier to handle than what ctypesgen generates
            POINTER(_worm.WormContext),
            POINTER(c_ubyte),
            c_int,
            c_char_p,
            c_int,
            c_char_p,
            c_int,
            c_char_p,
            c_int,
        ]
        val_res_puk = c_char_p(b"******")
        val_res_pin = c_char_p(b"*****")
        val_res_tapin = c_char_p(b"*****")

        guard(
            _worm.worm_user_deriveInitialCredentials(
                self._ctx,
                _c_ubyte(credential_seed.encode()),
                len(credential_seed),
                val_res_puk,
                6,
                val_res_pin,
                5,
                val_res_tapin,
                5,
            )
        )
        return {
            "adminPuk": val_res_puk.value.decode(),
            "adminPin": val_res_pin.value.decode(),
            "timeAdminPin": val_res_tapin.value.decode(),
        }

    def transaction_start(self, client_id: str, process_data: str, process_type: str):
        resp = _worm.worm_transaction_response_new(self._ctx)
        guard(
            _worm.worm_transaction_start(
                self._ctx,
                client_id,
                _c_ubyte(process_data.encode()),
                len(process_data.encode()),
                process_type,
                resp,
            )
        )

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_transaction_response_serialNumber(
            resp, byref(val_res), byref(val_len)
        )
        serial = bytes([val_res[i] for i in range(val_len.value)])

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_transaction_response_signature(resp, byref(val_res), byref(val_len))
        signature = bytes([val_res[i] for i in range(val_len.value)])

        data = {
            "logTime": _worm.worm_transaction_response_logTime(resp),
            "serialNumberHex": serial.hex(),
            "serialNumberBytes": serial,
            "signatureCounter": _worm.worm_transaction_response_signatureCounter(resp),
            "transactionNumber": _worm.worm_transaction_response_transactionNumber(
                resp
            ),
            "signature": signature,
        }
        _worm.worm_transaction_response_free(resp)
        return data

    # todo: transactions
