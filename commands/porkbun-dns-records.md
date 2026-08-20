---
description: List every DNS record configured for a Porkbun-managed domain, grouped by record type, with type, name, content, TTL, and record ID.
argument-hint: <domain>
allowed-tools: mcp__porkbun-dns__list_dns_records, mcp__porkbun-dns__get_dns_record
---

# /porkbun-dns-records

List all DNS records for a domain managed by Porkbun.

## Usage

`/porkbun-dns-records <domain>`

Arguments:

- `<domain>`: the fully-qualified domain name registered in Porkbun (e.g. `example.com`).

## Workflow

1. Call `mcp__porkbun-dns__list_dns_records` with `<domain>` to retrieve the full record set.
2. Group the records by `type` (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, ALIAS) for the report.
3. For each record, surface `id`, `name`, `content`, `ttl`, and `priority` (when set).
4. Call `mcp__porkbun-dns__get_dns_record` only when the user asks for a deeper look at a single record id.
5. Suggest `mcp__porkbun-dns__create_dns_record` or `mcp__porkbun-dns__edit_dns_record` for follow-up changes.

## Example

`/porkbun-dns-records example.com`