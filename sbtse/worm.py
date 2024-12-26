import base64
import contextlib
import datetime
import logging
from _ctypes import POINTER, byref
from ctypes import c_ubyte, c_uint32, c_uint8, c_int, c_char_p, cast, c_uint, c_void_p
from typing import List, BinaryIO

from . import _worm
from .errors import _guard
from .utils import log_execution

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


class BaseWormContext:
    def __init__(self):
        self._ctx = None

    def close(self):
        _worm.worm_cleanup(self._ctx)
        del self._ctx

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def keepalive_configure(self, seconds: int):
        _guard(_worm.worm_keepalive_configure(self._ctx, seconds))

    def keepalive_disable(self):
        _guard(_worm.worm_keepalive_disable(self._ctx))

    @log_execution
    def info(self) -> dict:
        i = _worm.worm_info_new(self._ctx)
        _guard(_worm.worm_info_read(i))

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_info_tsePublicKey(i, byref(val_res), byref(val_len))
        pubkey = bytes([val_res[i] for i in range(val_len.value)])

        val_res = POINTER(c_ubyte)()
        val_len = _worm.worm_uint()
        _worm.worm_info_tseSerialNumber(i, byref(val_res), byref(val_len))
        serial = bytes([val_res[i] for i in range(val_len.value)])
        states = {
            _worm.WORM_INIT_UNINITIALIZED: "WORM_INIT_UNINITIALIZED",
            _worm.WORM_INIT_INITIALIZED: "WORM_INIT_INITIALIZED",
            _worm.WORM_INIT_DECOMMISSIONED: "WORM_INIT_DECOMMISSIONED",
        }

        info = {
            "isDevelopmentFirmware": bool(_worm.worm_info_isDevelopmentFirmware(i)),
            "capacity": _worm.worm_info_capacity(i),
            "size": _worm.worm_info_size(i),
            "hasValidTime": bool(_worm.worm_info_hasValidTime(i)),
            "hasPassedSelfTest": bool(_worm.worm_info_hasPassedSelfTest(i)),
            "isCtssInterfaceActive": bool(_worm.worm_info_isCtssInterfaceActive(i)),
            "isExportEnabledIfCspTestFails": bool(
                _worm.worm_info_isExportEnabledIfCspTestFails(i)
            ),
            "initializationState": states[_worm.worm_info_initializationState(i)],
            "hasChangedPuk": bool(_worm.worm_info_hasChangedPuk(i)),
            "hasChangedAdminPin": bool(_worm.worm_info_hasChangedAdminPin(i)),
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
            "tseDescription": _worm.worm_info_tseDescription(i).decode(),
            "registeredClients": _worm.worm_info_registeredClients(i),
            "maxRegisteredClients": _worm.worm_info_maxRegisteredClients(i),
            "certificateExpirationDate": datetime.datetime.fromtimestamp(
                _worm.worm_info_certificateExpirationDate(i), datetime.timezone.utc
            ),
            "tarExportSizeInSectors": _worm.worm_info_tarExportSizeInSectors(i),
            "tarExportSize": _worm.worm_info_tarExportSize(i),
            "hardwareVersion": _worm.worm_info_hardwareVersion(i),
            "softwareVersion": _worm.worm_info_softwareVersion(i),
            "formFactor": _worm.worm_info_formFactor(i).decode(),
        }
        _worm.worm_info_free(i)
        return info

    @log_execution
    def flash_health(self) -> dict:
        val_errors = c_uint32()
        val_spare = c_uint8()
        val_erase = c_uint8()
        val_retention = c_uint8()
        _guard(
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
            "uncorrectableEccErrors": val_errors.value,
            "percentageRemainingSpareBlocks": val_spare.value,
            "percentageRemainingEraseCounts": val_erase.value,
            "percentageRemainingTenYearsDataRetention": val_retention.value,
            "needsReplacement": needs_replacement,
        }

    @log_execution
    def run_self_test(self, client_id):
        _guard(_worm.worm_tse_runSelfTest(self._ctx, client_id))

    @log_execution
    def factory_reset(self):
        # Works only on development TSEs (pre-2020).
        _guard(_worm.worm_tse_factoryReset(self._ctx))

    @log_execution
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
        _guard(
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

    @log_execution
    def ctss_enable(self):
        _guard(_worm.worm_tse_ctss_enable(self._ctx))

    @log_execution
    def ctss_disable(self):
        _guard(_worm.worm_tse_ctss_disable(self._ctx))

    @log_execution
    def initialize(self):
        _guard(_worm.worm_tse_initialize(self._ctx))

    @log_execution
    def decommission(self):
        _guard(_worm.worm_tse_decommission(self._ctx))

    @log_execution
    def update_time(self, time=None):
        if not time:
            time = datetime.datetime.now(datetime.timezone.utc)
        if not isinstance(time, int):
            time = int(time.astimezone(datetime.timezone.utc).timestamp())
        _guard(_worm.worm_tse_updateTime(self._ctx, time))

    @log_execution
    def bundled_firmware_update_available(self) -> bool:
        val = _worm.WormTseFirmwareUpdate()
        _guard(_worm.worm_tse_firmwareUpdate_isBundledAvailable(self._ctx, byref(val)))
        return val.value != _worm.WORM_FW_NONE

    @log_execution
    def bundled_firmware_update_apply(self):
        _guard(_worm.worm_tse_firmwareUpdate_applyBundled(self._ctx))

    @log_execution
    def enable_export_if_csp_test_fails(self):
        _guard(_worm.worm_tse_enableExportIfCspTestFails(self._ctx))

    @log_execution
    def disable_export_if_csp_test_fails(self):
        _guard(_worm.worm_tse_disableExportIfCspTestFails(self._ctx))

    @log_execution
    def register_client(self, client_id: str):
        _guard(_worm.worm_tse_registerClient(self._ctx, client_id))

    @log_execution
    def deregister_client(self, client_id: str):
        _guard(_worm.worm_tse_deregisterClient(self._ctx, client_id))

    @log_execution
    def list_registered_clients(self) -> List[str]:
        result = []
        skip = 0
        while True:
            clients = _worm.WormRegisteredClients()
            _guard(
                _worm.worm_tse_listRegisteredClients(self._ctx, skip, byref(clients))
            )
            result += [
                c.raw.decode().rstrip("\x00")
                for c in clients.clientIds[: clients.amount]
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
        _guard(ret)

    @log_execution
    def login_as_admin(self, pin: str):
        self._login(_worm.WORM_USER_ADMIN, pin)

    @log_execution
    def login_as_time_admin(self, pin: str):
        self._login(_worm.WORM_USER_TIME_ADMIN, pin)

    @log_execution
    def logout_as_admin(self):
        _guard(_worm.worm_user_logout(self._ctx, _worm.WORM_USER_ADMIN))

    @log_execution
    def logout_as_time_admin(self):
        _guard(_worm.worm_user_logout(self._ctx, _worm.WORM_USER_TIME_ADMIN))

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
        _guard(ret)

    @log_execution
    def unblock_admin(self, puk: str, new_pin: str):
        self._unblock(_worm.WORM_USER_ADMIN, puk, new_pin)

    @log_execution
    def unblock_time_admin(self, puk: str, new_pin: str):
        self._unblock(_worm.WORM_USER_TIME_ADMIN, puk, new_pin)

    @log_execution
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
        _guard(ret)

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
        _guard(ret)

    @log_execution
    def change_admin_pin(self, pin: str, new_pin: str):
        self._change_pin(_worm.WORM_USER_ADMIN, pin, new_pin)

    @log_execution
    def change_time_admin_pin(self, pin: str, new_pin: str):
        self._change_pin(_worm.WORM_USER_TIME_ADMIN, pin, new_pin)

    @log_execution
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

        _guard(
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

    def _transaction_response_to_dict(self, resp):
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

        return {
            "logTime": _worm.worm_transaction_response_logTime(resp),
            "serialNumberHex": serial.hex(),
            "serialNumberBytes": serial,
            "signatureCounter": _worm.worm_transaction_response_signatureCounter(resp),
            "transactionNumber": _worm.worm_transaction_response_transactionNumber(
                resp
            ),
            "signatureBytes": signature,
            "signatureBase64": base64.b64encode(signature).decode(),
        }

    @log_execution
    def transaction_start(self, client_id: str, process_data: str, process_type: str):
        resp = _worm.worm_transaction_response_new(self._ctx)
        _guard(
            _worm.worm_transaction_start(
                self._ctx,
                client_id,
                _c_ubyte(process_data.encode()),
                len(process_data.encode()),
                process_type,
                resp,
            )
        )
        data = self._transaction_response_to_dict(resp)
        _worm.worm_transaction_response_free(resp)
        return data

    @log_execution
    def transaction_update(
        self, client_id: str, transaction_id: int, process_data: str, process_type: str
    ):
        resp = _worm.worm_transaction_response_new(self._ctx)
        _guard(
            _worm.worm_transaction_update(
                self._ctx,
                client_id,
                transaction_id,
                _c_ubyte(process_data.encode()),
                len(process_data.encode()),
                process_type,
                resp,
            )
        )
        data = self._transaction_response_to_dict(resp)
        _worm.worm_transaction_response_free(resp)
        return data

    @log_execution
    def transaction_finish(
        self, client_id: str, transaction_id: int, process_data: str, process_type: str
    ):
        resp = _worm.worm_transaction_response_new(self._ctx)
        _guard(
            _worm.worm_transaction_finish(
                self._ctx,
                client_id,
                transaction_id,
                _c_ubyte(process_data.encode()),
                len(process_data.encode()),
                process_type,
                resp,
            )
        )
        data = self._transaction_response_to_dict(resp)
        _worm.worm_transaction_response_free(resp)
        return data

    @log_execution
    def last_transaction(self, client_id: str = None):
        resp = _worm.worm_transaction_response_new(self._ctx)
        _guard(
            _worm.worm_transaction_lastResponse(
                self._ctx,
                client_id,
                resp,
            )
        )
        data = self._transaction_response_to_dict(resp)
        _worm.worm_transaction_response_free(resp)
        return data

    @log_execution
    def list_started_transactions(self, client_id: str = None):
        result = []
        skip = 0
        while True:
            val_res = cast((_worm.worm_uint * 62)(), POINTER(_worm.worm_uint))
            val_len = c_int()
            _guard(
                _worm.worm_transaction_listStartedTransactions(
                    self._ctx, client_id, skip, val_res, 62, byref(val_len)
                )
            )
            result += [val_res[i] for i in range(val_len.value)]
            if val_len.value == 62:
                skip += 62
            else:
                break
        return result

    def _entry_to_dict(self, entry: _worm.WormEntry) -> dict:
        types = {
            _worm.WORM_ENTRY_TYPE_TRANSACTION: "WORM_ENTRY_TYPE_TRANSACTION",
            _worm.WORM_ENTRY_TYPE_SYSTEM_LOG_MESSAGE: "WORM_ENTRY_TYPE_SYSTEM_LOG_MESSAGE",
            _worm.WORM_ENTRY_TYPE_SE_AUDIT_LOG_MESSAGE: "WORM_ENTRY_TYPE_SE_AUDIT_LOG_MESSAGE",
        }
        val_len = _worm.worm_entry_logMessageLength(entry)
        val_res = cast((c_ubyte * val_len)(), POINTER(c_ubyte))
        _guard(_worm.worm_entry_readLogMessage(entry, val_res, val_len))

        val_len_pd = _worm.worm_entry_processDataLength(entry)
        val_res_pd = cast((c_ubyte * val_len)(), POINTER(c_ubyte))
        _guard(_worm.worm_entry_readProcessData(entry, 0, val_res_pd, val_len_pd))

        return {
            "isValid": bool(_worm.worm_entry_isValid(entry)),
            "id": _worm.worm_entry_id(entry),
            "type": types[_worm.worm_entry_type(entry)],
            "message": bytes([val_res[i] for i in range(val_len)]),
            "processData": bytes([val_res_pd[i] for i in range(val_len_pd)]),
        }

    @log_execution
    def first_entry(self) -> dict:
        entry = _worm.worm_entry_new(self._ctx)
        _guard(_worm.worm_entry_iterate_first(entry))
        d = self._entry_to_dict(entry)
        _worm.worm_entry_free(entry)
        return d

    @log_execution
    def last_entry(self) -> dict:
        entry = _worm.worm_entry_new(self._ctx)
        _guard(_worm.worm_entry_iterate_last(entry))
        d = self._entry_to_dict(entry)
        _worm.worm_entry_free(entry)
        return d

    @log_execution
    def entry_by_id(self, entry_id: int) -> dict:
        entry = _worm.worm_entry_new(self._ctx)
        _guard(_worm.worm_entry_iterate_id(entry, entry_id))
        d = self._entry_to_dict(entry)
        _worm.worm_entry_free(entry)
        return d

    @log_execution
    def iterate_entries(self, start_at: int = 0):
        entry = _worm.worm_entry_new(self._ctx)
        if start_at:
            _guard(_worm.worm_entry_iterate_id(entry, start_at))
        else:
            _guard(_worm.worm_entry_iterate_first(entry))
        try:
            if _worm.worm_entry_isValid(entry):
                yield self._entry_to_dict(entry)

                while True:
                    _guard(_worm.worm_entry_iterate_next(entry))
                    if not _worm.worm_entry_isValid(entry):
                        break
                    yield self._entry_to_dict(entry)
        finally:
            _worm.worm_entry_free(entry)

    @log_execution
    def get_log_message_certificate(self) -> str:
        val_len = c_uint(
            1024 * 16
        )  # 16 kb buffer should be enough. it if is not, the function will fail.
        val_res = cast((c_ubyte * val_len.value)(), POINTER(c_ubyte))
        _guard(_worm.worm_getLogMessageCertificate(self._ctx, val_res, byref(val_len)))
        return bytes([val_res[i] for i in range(val_len.value)]).decode()

    @log_execution
    def export_tar(
        self,
        target: BinaryIO,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None,
        client_id: str = None,
        start_transaction: int = None,
        end_transaction: int = None,
    ):
        def py_write(chunk, chunk_length, callback_data):
            data = bytes([chunk[i] for i in range(chunk_length)])
            target.write(data)
            return 0

        write = _worm.WormExportTarCallback(py_write)

        if start_date is not None or end_date is not None:
            if start_transaction or end_transaction:
                raise ValueError("You can either filter by date or transaction")
            if isinstance(start_date, datetime.datetime):
                start_date = int(
                    start_date.astimezone(datetime.timezone.utc).timestamp()
                )
            elif start_date is None:
                start_date = None
            if isinstance(end_date, datetime.datetime):
                end_date = int(end_date.astimezone(datetime.timezone.utc).timestamp())
            elif end_date is None:
                end_date = 0xFFFFFFFFFFFFFFFF

            _guard(
                _worm.worm_export_tar_filtered_time(
                    self._ctx, start_date, end_date, client_id, write, c_void_p()
                )
            )
        elif start_transaction is not None or end_transaction is not None:
            if start_date or end_date:
                raise ValueError("You can either filter by date or transaction")

            if start_transaction is None:
                start_transaction = 0
            if end_transaction is None:
                end_transaction = 0xFFFFFFFFFFFFFFFF

            _guard(
                _worm.worm_export_tar_filtered_transaction(
                    self._ctx,
                    start_transaction,
                    end_transaction,
                    client_id,
                    write,
                    c_void_p(),
                )
            )
        else:
            if client_id:
                _guard(
                    _worm.worm_export_tar_filtered_time(
                        self._ctx, 0, 0xFFFFFFFFFFFFFFFF, client_id, write, c_void_p()
                    )
                )
            else:
                _guard(_worm.worm_export_tar(self._ctx, write, c_void_p()))

    @log_execution
    def delete_stored_data(self):
        _guard(_worm.worm_export_deleteStoredData(self._ctx))


class LocalWormContext(BaseWormContext):
    @log_execution
    def __init__(self, mount_point: str):
        super().__init__()
        self._ctx = POINTER(_worm.WormContext)()
        _guard(_worm.worm_init(byref(self._ctx), mount_point.encode()))


class LANWormContext(BaseWormContext):
    @log_execution
    def __init__(self, url: str, api_token: str):
        super().__init__()
        self._ctx = POINTER(_worm.WormContext)()
        _guard(_worm.worm_init_lan(byref(self._ctx), url, api_token))

    def select_tse(self, serial_number: str):
        _guard(
            _worm.worm_lantse_select(
                self._ctx,
                c_ubyte(serial_number.encode()),
                len(serial_number.encode()),
            )
        )

    @contextlib.contextmanager
    def lock_tse(self):
        _guard(_worm.worm_lantse_lock(self._ctx))
        try:
            yield
        finally:
            _guard(_worm.worm_lantse_unlock(self._ctx))

    def list_connected_tses(self) -> List[str]:
        result = []
        skip = 0
        while True:
            tses = _worm.WormSerialNumberList()
            _guard(_worm.worm_lantse_listConnectedTses(self._ctx, skip, byref(tses)))
            result += [
                c.raw.decode().rstrip("\x00") for c in tses.serialNumber[: tses.amount]
            ]
            if tses.amount == 16:
                skip += 16
            else:
                break
        return result
