---
description: Retrieve a single DNS record from a Porkbun-managed domain by record ID, returning type, name, content, TTL, priority, and notes.
argument-hint: <domain> <record-id>
allowed-tools: mcp__porkbun-dns__get_dns_record, mcp__porkbun-dns__list_dns_records
---

# /porkbun-dns-list

Look up a single DNS record by its Porkbun record ID.

## Usage

`/porkbun-dns-list <domain> <record-id>`

Arguments:

- `<domain>`: the fully-qualified domain name registered in Porkbun (e.g. `example.com`).
- `<record-id>`: the integer ID returned by `mcp__porkbun-dns__list_dns_records`.

## Workflow

1. If the user does not know the record ID, call `mcp__porkbun-dns__list_dns_records` first to surface candidates.
2. Call `mcp__porkbun-dns__get_dns_record` with `<domain>` and `<record-id>`.
3. Report `id`, `name`, `type`, `content`, `ttl`, `priority`, and `notes`.
4. Suggest `mcp__porkbun-dns__edit_dns_record` or `mcp__porkbun-dns__delete_dns_record` as the natural follow-up actions.

## Example

`/porkbun-dns-list example.com 123456789`
