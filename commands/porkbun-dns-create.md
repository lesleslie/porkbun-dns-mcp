---
description: Create or update a DNS record for a Porkbun-managed domain, supporting A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, and ALIAS record types.
argument-hint: <domain> <action:create|edit> <record-id-if-editing> <type> <name> <content> [--ttl N] [--priority N]
allowed-tools: mcp__porkbun-dns__create_dns_record, mcp__porkbun-dns__edit_dns_record, mcp__porkbun-dns__list_dns_records, mcp__porkbun-dns__get_dns_record
---

# /porkbun-dns-create

Create a new DNS record, or update an existing one by record ID, on a Porkbun-managed domain.

## Usage

`/porkbun-dns-create <domain> create <type> <name> <content> [--ttl N] [--priority N]`
`/porkbun-dns-create <domain> edit <record-id> [--type T] [--name N] [--content C] [--ttl N] [--priority N]`

Arguments:

- `<domain>`: the fully-qualified domain name registered in Porkbun (e.g. `example.com`).
- `create|edit`: choose whether to add a new record or update an existing one.
- `<type>` (create, required): one of `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`, `CAA`, `ALIAS`.
- `<name>` (create, required): the record name (subdomain or empty string for the root domain).
- `<content>` (create, required): the record value (IP, hostname, text, etc.).
- `<record-id>` (edit, required): the integer ID of an existing record. Look it up first with `/porkbun-dns-records` or `mcp__porkbun-dns__list_dns_records` if needed.
- `--ttl N`: optional integer seconds (minimum 60, default 600).
- `--priority N`: optional 0-65535 priority for `MX` and `SRV` records.
- For `edit`, only the flags supplied are changed; omitted flags keep their current state.

## Workflow

1. Confirm the user's intent (`create` vs `edit`) and the relevant record identifiers.
2. For `create`: validate the record type against the supported set, then call `mcp__porkbun-dns__create_dns_record` with `domain`, `record_type`, `name`, `content`, `ttl`, and `priority` as appropriate.
3. For `edit`: if the record ID is unknown, call `mcp__porkbun-dns__list_dns_records` first; then call `mcp__porkbun-dns__edit_dns_record` with `domain`, `record_id`, and any provided optional fields.
4. Confirm the result and remind the user that DNS propagation may take a few minutes.

## Examples

`/porkbun-dns-create example.com create A www 192.0.2.10 --ttl 300`
`/porkbun-dns-create example.com edit 123456789 --content 192.0.2.11 --ttl 300`