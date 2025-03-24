# Usage

## sterces --help

```sh
Usage: sterces [OPTIONS] COMMAND [ARGS]...

  Command interface for a KeePass database.

Options:
  -d, --debug                     increment debug level
  -D, --db, --database-file TEXT  keepass db file ( default
                                  ~/.sterces/db.kdbx)
  -k, --key-file TEXT             keepass key file (default None)
  -p, --passphrase-file TEXT      passphrase file default ~/.sterces/.ssapeek
  -t, --transformed-key TEXT      keepass transformed key (default None)
  -v, --verbose                   increment verbosity level
  --warn / --no-warn              Warn permissions flag (default True)
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.

Commands:
  entry   Command group for entry management.
  group   Command group for group management.
  lookup  Lookup attribute of an entry.
```

## sterces entry --help

```sh
Usage: sterces entry [OPTIONS] COMMAND [ARGS]...

  Command group for entry management.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add or update an entry.
  dump    Dump specified entry or all entries if path not specified.
  remove  Remove specified entry.
  show    Show specified entry or all entries if path not specified.
  update  Update specified attributes of entry.
```

## sterces group --help

```sh
Usage: sterces entry [OPTIONS] COMMAND [ARGS]...

  Command group for entry management.

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Add or update an entry.
  dump    Dump specified entry or all entries if path not specified.
  remove  Remove specified entry.
  show    Show specified entry or all entries if path not specified.
  update  Update specified attributes of entry.
```

## sterces lookup --help

```sh
Usage: sterces lookup [OPTIONS] PATH [ATTR]

  Lookup attribute of an entry.

  ATTR must be one of: expiry, notes, otp, password, tags, url, username

  ATTR defaults to password when not specified

Options:
  -h, --help  Show this message and exit.
```
