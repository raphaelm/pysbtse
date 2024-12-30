import asyncio
import base64
import contextlib
import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional, List

from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from sbtse import errors
from sbtse.worm import (
    BaseWormContext,
    LocalWormContext,
    LANWormContext,
    log_time_format,
    signature_algorithm,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global worm_context

    loop_task = asyncio.create_task(_update_time_loop())
    yield
    loop_task.cancel()
    try:
        if worm_context:
            worm_context.close()
            worm_context = None
    except errors.WormError:
        pass


app = FastAPI(lifespan=lifespan)
worm_context: Optional[BaseWormContext] = None
worm_lock = asyncio.Lock()
last_time_update: float = 0.0
loop_task = None
logger = logging.getLogger(__name__)


def _update_time(info):
    global last_time_update

    worm_context.login_as_time_admin(os.environ["SBTSE_TAPIN"])

    if info["isDevelopmentFirmware"] and info[
        "certificateExpirationDate"
    ] < datetime.now(timezone.utc):
        # Development TSEs expired 2020-01, so let's backdate so we can still use them for testing
        worm_context.update_time(datetime.now(timezone.utc).replace(year=2019))
    else:
        worm_context.update_time()
    last_time_update = time.time()
    logger.info("Time update sent.")


async def _update_time_loop():
    global last_time_update, worm_context

    while True:
        try:
            if worm_context:
                info = worm_context.info()
                _update_time(info)
                await asyncio.sleep(info["maxTimeSynchronizationDelay"] * 0.8)
            else:
                await asyncio.sleep(10)
        except asyncio.CancelledError:
            pass
        except:
            logger.exception("Error updating time.")
            await asyncio.sleep(10)
            pass


@contextlib.asynccontextmanager
async def _worm_context(client_id, require_self_test=True) -> BaseWormContext:
    global worm_context

    async with worm_lock:
        if not worm_context:
            logger.info("Connecting to TSE…")
            if os.environ["SBTSE_PATH"]:
                worm_context = LocalWormContext(os.environ["SBTSE_PATH"])
            else:
                worm_context = LANWormContext(
                    os.environ["SBTSE_URL"], os.environ["SBTSE_API_KEY"]
                )
                worm_context.select_tse(os.environ["SBTSE_TSE"])
            worm_context.keepalive_configure(2000)
            logger.info("Connected to TSE.")

        info = worm_context.info()

        if not info["hasPassedSelfTest"] and require_self_test:
            if client_id:
                logger.info(f"Running self test with client ID {client_id}...")
                worm_context.run_self_test(client_id)
                logger.info("Self test completed.")
                _update_time(info)
            else:
                logger.info(f"Running self test with client ID FAKE...")
                try:
                    worm_context.run_self_test("FAKE")
                except errors.WormErrorClientNotRegistered:
                    pass
                logger.info("Self test completed.")
                _update_time(info)

        if time.time() - last_time_update > info["maxTimeSynchronizationDelay"] * 0.8:
            _update_time(info)

        try:
            yield worm_context
        except errors.WormErrorNoTimeSet:
            # self heal attempt
            _update_time(info)
            raise
        except errors.WormErrorWrongStateNeedsSelfTestPassed:
            # self heal attempt
            if client_id:
                logger.info(f"Running self test with client ID {client_id}...")
                worm_context.run_self_test(client_id)
                logger.info("Self test completed.")
                _update_time(info)
            raise


class InfoResponse(BaseModel):
    isDevelopmentFirmware: bool
    capacity: int
    size: int
    hasValidTime: bool
    hasPassedSelfTest: bool
    isCtssInterfaceActive: bool
    isExportEnabledIfCspTestFails: bool
    initializationState: str
    hasChangedPuk: bool
    hasChangedAdminPin: bool
    timeUntilNextSelfTest: int
    startedTransactions: int
    maxStartedTransactions: int
    createdSignatures: int
    maxSignatures: int
    remainingSignatures: int
    maxTimeSynchronizationDelay: int
    maxUpdateDelay: int
    tsePublicKey: str
    timeUntilNextTimeSynchronization: int
    tseSerialNumberBytes: str
    tseSerialNumberHex: str
    tseDescription: str
    registeredClients: int
    maxRegisteredClients: int
    certificateExpirationDate: datetime
    tarExportSizeInSectors: int
    tarExportSize: int
    hardwareVersion: int
    softwareVersion: int
    formFactor: str
    logTimeFormat: str
    signatureAlgorithm: str


@app.get("/info", summary="Retrieve information about the TSE")
async def info() -> InfoResponse:
    async with _worm_context("TESTCLIENT", require_self_test=False) as worm:
        return InfoResponse(
            **{
                k: base64.b64encode(v) if isinstance(v, bytes) else v
                for k, v in {
                    **worm.info(),
                    **worm.flash_health(),
                    "logTimeFormat": log_time_format(),
                    "signatureAlgorithm": signature_algorithm(),
                }.items()
            }
        )


class HealthResponse(BaseModel):
    uncorrectableEccErrors: int
    percentageRemainingSpareBlocks: int
    percentageRemainingEraseCounts: int
    percentageRemainingTenYearsDataRetention: int
    needsReplacement: bool


@app.get("/health", summary="Retrieve flash health information about the TSE")
async def health() -> HealthResponse:
    async with _worm_context(None, require_self_test=True) as worm:
        return HealthResponse(**{k: v for k, v in worm.flash_health().items()})


@app.get("/certificate", summary="Retrieve the certificate used for signing")
async def info():
    async with _worm_context("TESTCLIENT", require_self_test=False) as worm:
        return Response(
            worm.get_log_message_certificate(), headers={"Content-Type": "text/plain"}
        )


class TransactionInput(BaseModel):
    client_id: str
    process_data: str
    process_type: str


class TransactionResponse(BaseModel):
    logTime: int
    serialNumberHex: str
    signatureCounter: int
    transactionNumber: int
    signatureBase64: str


@app.post("/transactions/", summary="Start a transaction")
async def tx_start(inp: TransactionInput) -> TransactionResponse:
    async with _worm_context(client_id=inp.client_id) as worm:
        resp = worm.transaction_start(
            client_id=inp.client_id,
            process_data=inp.process_data,
            process_type=inp.process_type,
        )
        return TransactionResponse(
            **{k: v for k, v in resp.items() if not isinstance(v, bytes)}
        )


@app.post("/transactions/{transaction_id}/update", summary="Update a transaction")
async def tx_update(inp: TransactionInput, transaction_id: int) -> TransactionResponse:
    async with _worm_context(client_id=inp.client_id) as worm:
        resp = worm.transaction_update(
            client_id=inp.client_id,
            transaction_id=transaction_id,
            process_data=inp.process_data,
            process_type=inp.process_type,
        )
        return TransactionResponse(
            **{k: v for k, v in resp.items() if not isinstance(v, bytes)}
        )


@app.post("/transactions/{transaction_id}/finish", summary="Finish a transaction")
async def tx_finish(inp: TransactionInput, transaction_id: int) -> TransactionResponse:
    async with _worm_context(client_id=inp.client_id) as worm:
        resp = worm.transaction_finish(
            client_id=inp.client_id,
            transaction_id=transaction_id,
            process_data=inp.process_data,
            process_type=inp.process_type,
        )
        return TransactionResponse(
            **{k: v for k, v in resp.items() if not isinstance(v, bytes)}
        )


@app.exception_handler(errors.WormError)
async def unicorn_exception_handler(request: Request, exc: errors.WormError):
    logger.error(f"Error: {type(exc).__name__}")
    if isinstance(
        exc,
        (
            errors.WormErrorInvalidParameter,
            errors.WormErrorExportNotInitialized,
            errors.WormErrorIncrementalExportInvalidState,
            errors.WormErrorIncrementalExportNoData,
            errors.WormErrorCmdNotSupported,
            errors.WormErrorLanInvalidApiToken,
            errors.WormErrorTseNotFound,
            errors.WormErrorWrongLength,
            errors.WormErrorTransactionNotStarted,
            errors.WormErrorMaxParallelTransactions,
            errors.WormErrorNoLastTransaction,
            errors.WormErrorCmdNotAllowed,
            errors.WormErrorCmdNotFound,
            errors.WormErrorNotAuthorized,
            errors.WormErrorClientNotRegistered,
            errors.WormErrorExportUnacknowledgedData,
            errors.WormErrorClientHasUnfinishedTransactions,
            errors.WormErrorTseHasUnfinishedTransactions,
            errors.WormErrorAuthenticationFailed,
            errors.WormErrorAuthenticationPinBlocked,
            errors.WormErrorAuthenticationUserNotLoggedIn,
        ),
    ):
        return JSONResponse(
            status_code=400,
            content={"message": type(exc).__name__},
        )
    return JSONResponse(
        status_code=500,
        content={"message": type(exc).__name__},
    )


@app.get("/transactions/{client_id}/open/", summary="List of started transactions for client ID")
async def tx_started_for_client(client_id: str) -> List[int]:
    async with _worm_context(client_id=client_id) as worm:
        resp = worm.list_started_transactions(
            client_id=client_id,
        )
        return resp
