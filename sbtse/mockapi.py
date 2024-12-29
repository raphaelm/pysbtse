import base64
import datetime
import logging
import time
from textwrap import dedent
from typing import List

from fastapi import FastAPI, Response

from sbtse.api import (
    InfoResponse,
    HealthResponse,
    TransactionInput,
    TransactionResponse,
)

app = FastAPI()
loop_task = None
logger = logging.getLogger(__name__)


@app.get("/info", summary="Retrieve information about the TSE")
def info() -> InfoResponse:
    return InfoResponse(
        isDevelopmentFirmware=True,
        capacity=1_000_000,
        size=1_000_000,
        hasValidTime=True,
        hasPassedSelfTest=True,
        isCtssInterfaceActive=True,
        isExportEnabledIfCspTestFails=True,
        initializationState="WORM_INIT_INITIALIZED",
        hasChangedPuk=True,
        hasChangedAdminPin=True,
        timeUntilNextSelfTest=1_000_000,
        startedTransactions=0,
        maxStartedTransactions=128,
        createdSignatures=12345,
        maxSignatures=10_000_000,
        remainingSignatures=10_000_000 - 12345,
        maxTimeSynchronizationDelay=1000,
        maxUpdateDelay=1000,
        tsePublicKey="BLeuznbtm+K5m+o54L0MWSXR7TG5s0c7fKUdE2TLezRhgamafgOb+T55Hc2OXJlsH6c1FdmR6DplsFz1F6Z+TsvjgbO0vL2i"
        "IiST8sXEkXsZYzDP7tVX2rQE8eTbw1wzXg==",
        timeUntilNextTimeSynchronization=100,
        tseSerialNumberBytes="KDAILaThJz2IOeRs0i0AKbiIhOEcoXbqF5PcBe5yUo8=",
        tseSerialNumberHex="2830082da4e1273d8839e46cd22d0029b88884e11ca176ea1793dc05ee72528f",
        tseDescription="TR-00TEST-12345",
        registeredClients=2,
        maxRegisteredClients=128,
        certificateExpirationDate=datetime.datetime(
            datetime.date.today().year + 1,
            month=12,
            day=31,
            hour=12,
            minute=0,
            second=0,
        ),
        tarExportSizeInSectors=0,
        tarExportSize=0,
        hardwareVersion=1,
        softwareVersion=1,
        formFactor="USB",
        logTimeFormat="unixTime",
        signatureAlgorithm="ecdsa-plain-SHA384",
    )


@app.get("/health", summary="Retrieve flash health information about the TSE")
def health() -> HealthResponse:
    return HealthResponse(
        uncorrectableEccErrors=0,
        percentageRemainingSpareBlocks=100,
        percentageRemainingEraseCounts=0,
        percentageRemainingTenYearsDataRetention=99,
        needsReplacement=False,
    )


@app.get("/certificate", summary="Retrieve the certificate used for signing")
def info():
    return Response(
        dedent(
            """
        -----BEGIN CERTIFICATE-----
        MIIBkTCCATegAwIBAgIGAWzYF5flMAoGCCqGSM49BAMCMBYxFDASBgNVBAMMC1N3
        aXNzYml0IENBMB4XDTE5MDgyODExNTc1MFoXDTIwMDEzMDIzMDAwMFowEzERMA8G
        A1UEAwwIU3dpc3NiaXQwejAUBgcqhkjOPQIBBgkrJAMDAggBAQsDYgAEAUDr4gWW
        Z7CHTUOUZRgPE8+47qkHkYEE0Fuekq36+n6gZ81xUF3W0AECdp7GZwGxSLxP2MTN
        yEg1sga1dm3zVOp7jY7pChDhhcxbCUDsnjKuPiniBdGvT2T9WZI6laoNo1MwUTAM
        BgNVHRMBAf8EAjAAMA4GA1UdDwEB/wQEAwIFoDAWBgNVHSUBAf8EDDAKBggrBgEF
        BQcDATAZBgNVHREEEjAQgQ50ZXN0QHRlc3QudGVzdDAKBggqhkjOPQQDAgNIADBF
        AiBez72a1IeRrlM8QsvYxUc8iw/zmFQRJxkHAMpR/0T0TQIhAJBjMvO379XMREps
        fC9gNQASHAmPoPeose+TUjeM0iSk
        -----END CERTIFICATE-----
        -----BEGIN CERTIFICATE-----
        MIIBGTCBvwIGAWzYF5hWMAoGCCqGSM49BAMCMBYxFDASBgNVBAMMC1N3aXNzYml0
        IENBMB4XDTE5MDgyODExNTc1MFoXDTIwMDEzMDIzMDAwMFowFjEUMBIGA1UEAwwL
        U3dpc3NiaXQgQ0EwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNCAAS5sidpYfxFQfXw
        K/WQztoUhW2azT08pe/UIRMYXz5e2KbKWBuIi2UycvIb0eZgBKMC9r5UA+aI9Ujr
        XqcOOilmMAoGCCqGSM49BAMCA0kAMEYCIQDTggzzDCFWUHUcI+KbHKMh7XRd8fPW
        ELrz1hhguX+UHwIhAMh1UTHBZ6ggfkiDFKv2FOVaqtwj+fvvV+TRNMEUjg4t
        -----END CERTIFICATE-----
        """
        ).strip(),
        headers={"Content-Type": "text/plain"},
    )


@app.post("/transactions/", summary="Start a transaction")
def tx_start(inp: TransactionInput) -> TransactionResponse:
    txcnt = int(time.time())
    time.sleep(0.2)
    logger.info(f"Received input: {inp}")
    return TransactionResponse(
        logTime=int(datetime.datetime.now().timestamp()),
        serialNumberHex="2830082da4e1273d8839e46cd22d0029b88884e11ca176ea1793dc05ee72528f",
        transactionNumber=txcnt,
        signatureCounter=txcnt * 2 - 1,
        signatureBase64=base64.b64encode(b"Not a real signature, development only!"),
    )


@app.post("/transactions/{transaction_id}/update", summary="Update a transaction")
def tx_update(inp: TransactionInput, transaction_id: int) -> TransactionResponse:
    time.sleep(0.2)
    logger.info(f"Received input: {inp}")
    return TransactionResponse(
        logTime=int(datetime.datetime.now().timestamp()),
        serialNumberHex="2830082da4e1273d8839e46cd22d0029b88884e11ca176ea1793dc05ee72528f",
        transactionNumber=transaction_id,
        signatureCounter=transaction_id * 2 - 1,
        signatureBase64=base64.b64encode(b"Not a real signature, development only!"),
    )


@app.post("/transactions/{transaction_id}/finish", summary="Finish a transaction")
def tx_finish(inp: TransactionInput, transaction_id: int) -> TransactionResponse:
    time.sleep(0.2)
    logger.info(f"Received input: {inp}")
    return TransactionResponse(
        logTime=int(datetime.datetime.now().timestamp()),
        serialNumberHex="2830082da4e1273d8839e46cd22d0029b88884e11ca176ea1793dc05ee72528f",
        transactionNumber=transaction_id,
        signatureCounter=transaction_id * 2,
        signatureBase64=base64.b64encode(b"Not a real signature, development only!"),
    )


@app.get("/transactions/{client_id}/open/", summary="List of started transactions for client ID")
async def tx_started_for_client(client_id: str) -> List[int]:
    return [1, 2]
