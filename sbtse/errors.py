class WormError(Exception):
    pass


class WormErrorInvalidParameter(WormError):
    pass


class WormErrorNoWormCard(WormError):
    pass


class WormErrorIO(WormError):
    pass


class WormErrorTimeout(WormError):
    pass


class WormErrorOutOfMem(WormError):
    pass


class WormErrorInvalidResponse(WormError):
    pass


class WormErrorStoreFullInternal(WormError):
    pass


class WormErrorResponseMissing(WormError):
    pass


class WormErrorExportNotInitialized(WormError):
    pass


class WormErrorExportFailed(WormError):
    pass


class WormErrorIncrementalExportInvalidState(WormError):
    pass


class WormErrorIncrementalExportNoData(WormError):
    pass


class WormErrorPowerCycleDetected(WormError):
    pass


class WormErrorFirmwareUpdateNotApplied(WormError):
    pass


class WormErrorThreadStartFailed(WormError):
    pass


class WormErrorNetwork(WormError):
    pass


class WormErrorCmdNotSupported(WormError):
    pass


class WormErrorLanInvalidApiToken(WormError):
    pass


class WormErrorNetworkTimeout(WormError):
    pass


class WormErrorConnectionFailed(WormError):
    pass


class WormErrorLanUnbalancedLocks(WormError):
    pass


class WormErrorLanInvalidServerResponse(WormError):
    pass


class WormErrorInvalidState(WormError):
    pass


class WormErrorTseNotFound(WormError):
    pass


class WormErrorIncrementalExportLimitTooLow(WormError):
    pass


class WormErrorFwuNotAvailable(WormError):
    pass


class WormErrorFromCardFirst(WormError):
    pass


class WormErrorUnknown(WormError):
    pass


class WormErrorNoTimeSet(WormError):
    pass


class WormErrorNoTransactionInProgress(WormError):
    pass


class WormErrorInvalidCmdSyntax(WormError):
    pass


class WormErrorWrongLength(WormError):
    pass


class WormErrorNotEnoughDataWritten(WormError):
    pass


class WormErrorTseInvalidParameter(WormError):
    pass


class WormErrorTransactionNotStarted(WormError):
    pass


class WormErrorMaxParallelTransactions(WormError):
    pass


class WormErrorCertificateExpired(WormError):
    pass


class WormErrorNoLastTransaction(WormError):
    pass


class WormErrorCmdNotAllowed(WormError):
    pass


class WormErrorTransactionSignaturesExceeded(WormError):
    pass


class WormErrorNotAuthorized(WormError):
    pass


class WormErrorMaxRegisteredClientsReached(WormError):
    pass


class WormErrorClientNotRegistered(WormError):
    pass


class WormErrorExportUnacknowledgedData(WormError):
    pass


class WormErrorClientHasUnfinishedTransactions(WormError):
    pass


class WormErrorTseHasUnfinishedTransactions(WormError):
    pass


class WormErrorTseNoResponseToFetch(WormError):
    pass


class WormErrorNotAllowedExportInProgress(WormError):
    pass


class WormErrorStoreFull(WormError):
    pass


class WormErrorWrongStateNeedsPukChange(WormError):
    pass


class WormErrorWrongStateNeedsPinChange(WormError):
    pass


class WormErrorWrongStateNeedsActiveCtss(WormError):
    pass


class WormErrorWrongStateNeedsSelfTest(WormError):
    pass


class WormErrorWrongStateNeedsSelfTestPassed(WormError):
    pass


class WormErrorFwuIntegrityFailure(WormError):
    pass


class WormErrorFwuDecryptionFailure(WormError):
    pass


class WormErrorFwuWrongFormat(WormError):
    pass


class WormErrorFwuInternalError(WormError):
    pass


class WormErrorFwuDowngradeProhibited(WormError):
    pass


class WormErrorTseAlreadyInitialized(WormError):
    pass


class WormErrorTseDecommissioned(WormError):
    pass


class WormErrorTseNotInitialized(WormError):
    pass


class WormErrorAuthenticationFailed(WormError):
    pass


class WormErrorAuthenticationPinBlocked(WormError):
    pass


class WormErrorAuthenticationUserNotLoggedIn(WormError):
    pass


class WormErrorSelfTestFailedFW(WormError):
    pass


class WormErrorSelfTestFailedCSP(WormError):
    pass


class WormErrorSelfTestFailedRNG(WormError):
    pass


class WormErrorFwuBaseFWError(WormError):
    pass


class WormErrorFwuFwextError(WormError):
    pass


class WormErrorFwuCspError(WormError):
    pass


class WormErrorExportNoneInProgress(WormError):
    pass


class WormErrorExportRetry(WormError):
    pass


class WormErrorExportNoDataAvailable(WormError):
    pass


class WormErrorCmdNotFound(WormError):
    pass


class WormErrorSigError(WormError):
    pass


class WormErrorFromCardLast(WormError):
    pass


def _guard(rescode, allow=0):
    if rescode == allow:
        return
    if rescode == 1:
        raise WormErrorInvalidParameter()
    if rescode == 2:
        raise WormErrorNoWormCard()
    if rescode == 3:
        raise WormErrorIO()
    if rescode == 4:
        raise WormErrorTimeout()
    if rescode == 5:
        raise WormErrorOutOfMem()
    if rescode == 6:
        raise WormErrorInvalidResponse()
    if rescode == 7:
        raise WormErrorStoreFullInternal()
    if rescode == 8:
        raise WormErrorResponseMissing()
    if rescode == 9:
        raise WormErrorExportNotInitialized()
    if rescode == 10:
        raise WormErrorExportFailed()
    if rescode == 11:
        raise WormErrorIncrementalExportInvalidState()
    if rescode == 12:
        raise WormErrorIncrementalExportNoData()
    if rescode == 13:
        raise WormErrorPowerCycleDetected()
    if rescode == 14:
        raise WormErrorFirmwareUpdateNotApplied()
    if rescode == 15:
        raise WormErrorThreadStartFailed()
    if rescode == 16:
        raise WormErrorNetwork()
    if rescode == 17:
        raise WormErrorCmdNotSupported()
    if rescode == 18:
        raise WormErrorLanInvalidApiToken()
    if rescode == 19:
        raise WormErrorNetworkTimeout()
    if rescode == 20:
        raise WormErrorConnectionFailed()
    if rescode == 21:
        raise WormErrorLanUnbalancedLocks()
    if rescode == 22:
        raise WormErrorLanInvalidServerResponse()
    if rescode == 23:
        raise WormErrorInvalidState()
    if rescode == 24:
        raise WormErrorTseNotFound()
    if rescode == 25:
        raise WormErrorIncrementalExportLimitTooLow()
    if rescode == 26:
        raise WormErrorFwuNotAvailable()
    if rescode == 0x1000:
        raise WormErrorFromCardFirst()
    if rescode == 0x1001:
        raise WormErrorUnknown()
    if rescode == 0x1002:
        raise WormErrorNoTimeSet()
    if rescode == 0x1004:
        raise WormErrorNoTransactionInProgress()
    if rescode == 0x1005:
        raise WormErrorInvalidCmdSyntax()
    if rescode == 0x1006:
        raise WormErrorNotEnoughDataWritten()
    if rescode == 0x1007:
        raise WormErrorTseInvalidParameter()
    if rescode == 0x1008:
        raise WormErrorTransactionNotStarted()
    if rescode == 0x1009:
        raise WormErrorMaxParallelTransactions()
    if rescode == 0x100A:
        raise WormErrorCertificateExpired()
    if rescode == 0x100C:
        raise WormErrorNoLastTransaction()
    if rescode == 0x100D:
        raise WormErrorCmdNotAllowed()
    if rescode == 0x100E:
        raise WormErrorTransactionSignaturesExceeded()
    if rescode == 0x100F:
        raise WormErrorNotAuthorized()
    if rescode == 0x1010:
        raise WormErrorMaxRegisteredClientsReached()
    if rescode == 0x1011:
        raise WormErrorClientNotRegistered()
    if rescode == 0x1012:
        raise WormErrorExportUnacknowledgedData()
    if rescode == 0x1013:
        raise WormErrorClientHasUnfinishedTransactions()
    if rescode == 0x1014:
        raise WormErrorTseHasUnfinishedTransactions()
    if rescode == 0x1015:
        raise WormErrorTseNoResponseToFetch()
    if rescode == 0x1016:
        raise WormErrorNotAllowedExportInProgress()
    if rescode == 0x1017:
        raise WormErrorStoreFull()
    if rescode == 0x1050:
        raise WormErrorWrongStateNeedsPukChange()
    if rescode == 0x1051:
        raise WormErrorWrongStateNeedsPinChange()
    if rescode == 0x1053:
        raise WormErrorWrongStateNeedsActiveCtss()
    if rescode == 0x1054:
        raise WormErrorWrongStateNeedsSelfTest()
    if rescode == 0x1055:
        raise WormErrorWrongStateNeedsSelfTestPassed()
    if rescode == 0x1061:
        raise WormErrorFwuIntegrityFailure()
    if rescode == 0x1062:
        raise WormErrorFwuDecryptionFailure()
    if rescode == 0x1064:
        raise WormErrorFwuWrongFormat()
    if rescode == 0x1065:
        raise WormErrorFwuInternalError()
    if rescode == 0x1067:
        raise WormErrorFwuDowngradeProhibited()
    if rescode == 0x10FD:
        raise WormErrorTseAlreadyInitialized()
    if rescode == 0x10FE:
        raise WormErrorTseDecommissioned()
    if rescode == 0x10FF:
        raise WormErrorTseNotInitialized()
    if rescode == 0x1100:
        raise WormErrorAuthenticationFailed()
    if rescode == 0x1201:
        raise WormErrorAuthenticationPinBlocked()
    if rescode == 0x1202:
        raise WormErrorAuthenticationUserNotLoggedIn()
    if rescode == 0x1300:
        raise WormErrorSelfTestFailedFW()
    if rescode == 0x1310:
        raise WormErrorSelfTestFailedCSP()
    if rescode == 0x1320:
        raise WormErrorSelfTestFailedRNG()
    if rescode == 0x1400:
        raise WormErrorFwuBaseFWError()
    if rescode == 0x1500:
        raise WormErrorFwuFwextError()
    if rescode == 0x1600:
        raise WormErrorFwuCspError()
    if rescode == 0x2001:
        raise WormErrorExportNoneInProgress()
    if rescode == 0x2002:
        raise WormErrorExportRetry()
    if rescode == 0x2003:
        raise WormErrorExportNoDataAvailable()
    if rescode == 0xF000:
        raise WormErrorCmdNotFound()
    if rescode == 0xFF00:
        raise WormErrorSigError()
    if rescode == 0xFFFF:
        raise WormErrorFromCardLast()
    raise WormError(f"Unknown error ID {rescode}")
