# python-eml-parser

Three Python scripts that read one `.eml` file and print parts of it. Use them to inspect a saved message: the raw header block, a few address fields plus the body, and the `Received` path with a registrar abuse contact when `whois` returns one.

The scripts use only the Python standard library. They open the file as text, split it on the first blank line, and match header text. They do not use the `email` package.

## Prerequisites

- Python 3.7 or newer. `email-hops.py` calls `subprocess.run` with `capture_output` and `text`, which need 3.7.
- A `whois` executable on `PATH` for `email-hops.py`. `email-headers.py` and `email-body.py` do not call it.
- No third-party packages. There is no `requirements.txt` and nothing to install with pip.

## Install, build, run, and test

There is no install step and no build step. From the repository root, pass the path to an `.eml` file:

```bash
python3 email-headers.py message.eml
python3 email-body.py message.eml
python3 email-hops.py message.eml
```

If the `python` command on your machine is Python 3.7 or newer, you can use `python` in place of `python3`.

This repository has no test suite and no test command.

## Usage

Each script expects one argument, the path to the `.eml` file. If you omit it, the script prints:

```text
Please provide the path to the .eml file as an argument.
```

### Print the header block

`email-headers.py` prints every line before the first blank line.

```bash
python3 email-headers.py message.eml
```

### Print From, Delivered-To, To, CC, and the body

`email-body.py` prints those five fields. It keeps the value from the first header line that starts with `From:`, `Delivered-To:`, `To:`, or `CC:` (that spelling and case). If there is no `CC:` line, CC is an empty string. The body is the text after the first blank line.

```bash
python3 email-body.py message.eml
```

Example output shape:

```text
From:  sender@example.com
Delivered-To:  recipient@example.com
To:  recipient@example.com
CC:  copy@example.com
Body:  This is the body.
```

### Print Received hops and a registrar abuse contact

`email-hops.py` collects hostnames from lines that match `Received: from <hostname>`, where the hostname has at least two dots. It prints that list. It then shortens the last hop to its last two labels (for example `outbound.mail.example.net` becomes `example.net`) and runs:

```bash
whois example.net
```

It looks for a line matching `Registrar Abuse Contact Email:` followed by an address. When that field is present it prints the address. When it is missing or empty, it prints that it could not find the field and suggests running `whois` on the domain yourself.

```bash
python3 email-hops.py message.eml
```

Example output shape when hops are found and the abuse field is not:

```text
Hops:  ['mail.sender.example.com', 'example.net']
Couldn't find the Registrar Abuse Contact Email field for example.net
Try running 'whois example.net' to see if an alternate whois database exists
```

If no matching `Received: from` hostnames are found, it prints `No hops found in headers` and does not run `whois`.

## Layout

| File | Role |
| --- | --- |
| `email-body.py` | Prints From, Delivered-To, To, CC, and the body |
| `email-headers.py` | Prints the raw header block |
| `email-hops.py` | Prints Received hops and looks up a registrar abuse contact |
| `README.md` | This file |

## License

This repository does not include a license file.
