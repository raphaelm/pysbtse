# pysbtse

Python bindings and command-line tool for the Swissbit TSE. 

## Setup

Install ``sbtse`` like any Python package, e.g. with pip. Additionally, you need ``libWormAPI.so`` for your architecture
in your library path or your working directory. We are not allowed to distribute this library here, so please try to
find it on the internet or request it from a Swissbit TSE seller.

## Capabilities

This module includes an auto-generated ctypes wrapper for the `libWormAPI.so` from Swissbit SDK 5.9.1.
On top of that, it includes a high-level Python interface to work with the TSE.
The Python interface supports all features of the offline SDK except for:

- Online firmware updates and manual firmware transfer (bundled firmware updates are supported)
- Incremental TAR exports
- Export lifetime monitoring information

LAN TSE support is implemented but not tested.


## Command line usage

```
Usage: sbtse [OPTIONS] COMMAND [ARGS]...

Options:
  --path DIRECTORY  TSE mount point
  --url TEXT        LAN TSE URL
  --api-key TEXT    LAN TSE API Key
  --tse TEXT        LAN TSE serial number
  --help            Show this message and exit.

Commands:
  config           Manipulate TSE configuration
  delete           Delete stored data.
  entries          Query log entries
  export           Export stored data.
  factory-reset    Factory reset (development TSE only)
  firmware-update  Update firmware to version bundled with SDK.
  info             Show info and flash health status
  mock             Run mock API server (development only)
  pin              Manage Admin PIN
  puk              Manage PUK
  selftest         Run self-test
  serve            Run local API server
  setup            Run setup procedure for a fresh TSE
  time-admin-pin   Manage Time Admin PIN
  transaction      Create and query transactions
```

Run ``sbtse --path /mnt/tse COMMAND --help`` for the options and subcommands of the commands.

## Python library usage

Example:

```python
from sbtse import worm, errors

client_id = "TEST"
admin_pin = "12345"
admin_puk = "123456"
time_admin_pin = "12345"

print("SDK version:", worm.get_version())

with worm.LocalWormContext("/mnt/tse/") as w:
    info = w.info()
    print("Info:", info)
    print("Initial credentials:", w.derive_initial_credentials())
    print("Running self test...")
    try:
        w.run_self_test(client_id)
    except errors.WormErrorClientNotRegistered:
        print("Not registered.")
        if info["hasChangedAdminPin"]:
            w.login_as_admin(admin_pin)
            w.register_client(client_id)
        else:
            w.setup(client_id, admin_pin, admin_puk, time_admin_pin)
        
    if w.bundled_firmware_update_available():
        print("Updating firmware...")
        w.bundled_firmware_update_apply()
    
    print("Flash health:", w.flash_health())
    w.login_as_time_admin(time_admin_pin)
    w.update_time()
    
    print("Registered clients:", w.list_registered_clients())
    
    # Transaction handling
    print("Performing transaction...")
    tx = w.transaction_start(client_id, "", "")
    print("Started transactions:", w.list_started_transactions())
    print("Finished transaction:", w.transaction_finish(client_id, tx["transactionNumber"], "Foobar", "Kassenbeleg"))
    
    # Export capabilities
    print("Last transaction:", w.last_transaction())
    for tx in w.iterate_entries():
        print("Entry:", tx)
    print("Certificate:", w.get_log_message_certificate())
    
    print("Exporting TAR…")
    with open("export.tar", "wb") as f:
        w.export_tar(f)

    print("Exporting filtered TAR…")
    with open("export_tx_filtered.tar", "wb") as f:
        w.export_tar(f, start_transaction=0, end_transaction=2, client_id=client_id)
```

The example does not show all features. Have a look at ``help(LocalWormContext)`` for a full list of methods.

For LAN TSE (untested):

```python
from sbtse import worm

with worm.LANWormContext("https://10.1.1.1:9000", "api_key") as w:
    tses = w.list_connected_tses()
    print("TSEs:", tses)
    w.select_tse(tses[0])
    with w.lock_tse():
        w.setup(...)
    ...
```

## API Usage

The API is executed as a single-thread single-process worker to avoid concurrent access to the TSE which might be problematic.
However, this also means that the API might be slow to respond under concurrent access. This is intentional.

| Method | Path                                                                           | Description                                      |
| --- |--------------------------------------------------------------------------------|--------------------------------------------------|
| GET | [/info](#getinfo)                                                              | Retrieve information about the TSE               |
| GET | [/health](#gethealth)                                                          | Retrieve health status information about the TSE |
| GET | [/certificate](#getcertificate)                                                | Retrieve the certificate used for signing        |
| POST | [/transactions/](#posttransactions)                                            | Start a transcation                              |
| POST | [/transactions/{transaction_id}/update](#posttransactionstransaction_idupdate) | Update a transaction                             |
| POST | [/transactions/{transaction_id}/finish](#posttransactionstransaction_idfinish) | Finish a transaction                             |

### [GET] /info

Retrieve information about the TSE

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  isDevelopmentFirmware: boolean
  capacity: integer
  size: integer
  hasValidTime: boolean
  hasPassedSelfTest: boolean
  isCtssInterfaceActive: boolean
  isExportEnabledIfCspTestFails: boolean
  initializationState: string
  hasChangedPuk: boolean
  hasChangedAdminPin: boolean
  timeUntilNextSelfTest: integer
  startedTransactions: integer
  maxStartedTransactions: integer
  createdSignatures: integer
  maxSignatures: integer
  remainingSignatures: integer
  maxTimeSynchronizationDelay: integer
  maxUpdateDelay: integer
  tsePublicKey: string
  timeUntilNextTimeSynchronization: integer
  tseSerialNumberBytes: string
  tseSerialNumberHex: string
  tseDescription: string
  registeredClients: integer
  maxRegisteredClients: integer
  certificateExpirationDate: string
  tarExportSizeInSectors: integer
  tarExportSize: integer
  hardwareVersion: integer
  softwareVersion: integer
  formFactor: string
  logTimeFormat: str
  signatureAlgorithm: str
}
```

### [GET] /health

Retrieve health information about the TSE

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  uncorrectableEccErrors: integer
  percentageRemainingSpareBlocks: integer
  percentageRemainingEraseCounts: integer
  percentageRemainingTenYearsDataRetention: integer
  needsReplacement: boolean
}
```

### [GET] /certificate

Retrieve the certificate used for signing

### [POST] /transactions/

Start a transaction

#### Request body

- application/json

```ts
{
  client_id: string
  process_data: string
  process_type: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  logTime: integer
  serialNumberHex: string
  signatureCounter: integer
  transactionNumber: integer
  signatureBase64: string
}
```

### [POST] /transactions/{transaction_id}/update

Update a transaction

#### Request body

- application/json

```ts
{
  client_id: string
  process_data: string
  process_type: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  logTime: integer
  serialNumberHex: string
  signatureCounter: integer
  transactionNumber: integer
  signatureBase64: string
}
```

### [POST] /transactions/{transaction_id}/finish

Finish a transaction

#### Request body

- application/json

```ts
{
  client_id: string
  process_data: string
  process_type: string
}
```

#### Responses

- 200 Successful Response

`application/json`

```ts
{
  logTime: integer
  serialNumberHex: string
  signatureCounter: integer
  transactionNumber: integer
  signatureBase64: string
}
```


## License

The code in this library is licensed under the Apache 2.0 license.
Note that the binary library and documentation provided by Swissbit is provided under the "Swissbit Device Driver Adaptation & Distribution License" and therefore not shared in this repository.