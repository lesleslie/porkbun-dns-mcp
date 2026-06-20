# Porkbun DNS MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

MCP server for managing Porkbun DNS records through a FastMCP interface.

**Version:** 0.1.3
**Status:** Internal Bodai integration component

## Quick Links

- [Overview](#overview)
- [Capabilities](#capabilities)
- [Quick Start](#quick-start)
- [MCP Server Configuration](#mcp-server-configuration)
- [Tool Reference](#tool-reference)
- [Configuration](#configuration)
- [Development](#development)

## Quality & CI

Crackerjack is the standard quality-control and CI/CD gate for Porkbun DNS MCP changes. Local verification should mirror the Crackerjack workflow used across the Bodai ecosystem.

______________________________________________________________________

## Overview

Porkbun DNS MCP exposes DNS record management workflows through a FastMCP server. It is focused on record lookup, creation, update, and deletion for domains managed through Porkbun while keeping provider credentials and request validation in a narrow integration boundary.

This server is intentionally separate from `porkbun-domain-mcp`. DNS owns record-level operations; domain owns registration, renewal, transfer, and pricing workflows.

## Capabilities

Implemented tool surface:

- **Record listing**: list all DNS records for a domain
- **Record lookup**: retrieve a specific DNS record by ID
- **Record creation**: create A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, or ALIAS records
- **Record editing**: update selected fields on an existing DNS record
- **Record deletion**: remove a DNS record by ID
- **Credential health metadata**: report whether API credentials are configured
- **HTTP health routes**: `/health` and `/healthz` for MCP client and process supervision checks

## Quick Start

### Prerequisites

- Python 3.13+
- UV package manager
- Porkbun API key and secret key

### Local Setup

```bash
git clone https://github.com/lesleslie/porkbun-dns-mcp.git
cd porkbun-dns-mcp
uv sync --group dev
```

### Run With Credentials

```bash
export PORKBUN_DNS_API_KEY="your-api-key"
export PORKBUN_DNS_SECRET_KEY="your-secret-key"
uv run porkbun-dns-mcp start
uv run porkbun-dns-mcp health
```

The default HTTP bind is `127.0.0.1:3042`.

## CLI Commands

The CLI is built with `mcp-common` and provides the standard lifecycle command surface used by Bodai MCP servers.

```bash
uv run porkbun-dns-mcp start      # Start the HTTP MCP server
uv run porkbun-dns-mcp stop       # Stop the managed server process
uv run porkbun-dns-mcp restart    # Restart the managed server process
uv run porkbun-dns-mcp status     # Show process status
uv run porkbun-dns-mcp health     # Run the local health probe
```

## MCP Server Configuration

### Claude / Codex Style Configuration

Add the server to an MCP client configuration:

```json
{
  "mcpServers": {
    "porkbun-dns": {
      "command": "uv",
      "args": ["run", "porkbun-dns-mcp", "start"],
      "cwd": "/Users/les/Projects/porkbun-dns-mcp",
      "env": {
        "PORKBUN_DNS_API_KEY": "your-api-key",
        "PORKBUN_DNS_SECRET_KEY": "your-secret-key"
      }
    }
  }
}
```

Use your secret manager for live credentials rather than committing them to client config.

### Health Checks

```bash
curl http://127.0.0.1:3042/health
curl http://127.0.0.1:3042/healthz
```

## Tool Reference

| Tool | Purpose | Required Inputs |
|------|---------|-----------------|
| `list_dns_records` | List all DNS records for a domain | `domain` |
| `get_dns_record` | Retrieve one DNS record by ID | `domain`, `record_id` |
| `create_dns_record` | Create a DNS record | `domain`, `record_type`, `name`, `content` |
| `edit_dns_record` | Update selected fields on a DNS record | `domain`, `record_id` |
| `delete_dns_record` | Delete a DNS record | `domain`, `record_id` |

Supported record types are `A`, `AAAA`, `CNAME`, `MX`, `TXT`, `NS`, `SRV`, `CAA`, and `ALIAS`.

Tool responses follow a consistent `ToolResponse` shape:

```json
{
  "success": true,
  "message": "Found 4 DNS records for example.com",
  "data": {},
  "error": null,
  "next_steps": []
}
```

## Configuration

Committed defaults live in `settings/porkbun-dns.yaml`. Runtime overrides should come from environment variables or a local `.env` file that is not committed.

| Setting | Environment Variable | Default |
|---------|----------------------|---------|
| API key | `PORKBUN_DNS_API_KEY` | empty |
| Secret key | `PORKBUN_DNS_SECRET_KEY` | empty |
| Base URL | `PORKBUN_DNS_BASE_URL` | `https://porkbun.com/api/json/v3` |
| Timeout | `PORKBUN_DNS_TIMEOUT` | `30.0` |
| Max retries | `PORKBUN_DNS_MAX_RETRIES` | `3` |
| HTTP host | `PORKBUN_DNS_HTTP_HOST` | `127.0.0.1` |
| HTTP port | `PORKBUN_DNS_HTTP_PORT` | `3042` |
| Log level | `PORKBUN_DNS_LOG_LEVEL` | `INFO` |
| JSON logs | `PORKBUN_DNS_LOG_JSON` | `true` |

## Project Structure

```text
porkbun_dns_mcp/
  cli.py              # mcp-common lifecycle CLI
  client.py           # Porkbun DNS API client boundary
  config.py           # Pydantic settings and logging
  models.py           # Typed DNS record models
  server.py           # FastMCP application factory
  tools/dns_tools.py  # Registered MCP tools
settings/
  porkbun-dns.yaml    # Committed defaults
tests/
  test_schema_validation.py
```

## Development

```bash
uv sync --group dev
uv run pytest
uv run ruff check porkbun_dns_mcp tests
uv run ruff format porkbun_dns_mcp tests
uv run pyright porkbun_dns_mcp
```

Use targeted tests when isolating schema behavior:

```bash
uv run pytest tests/test_schema_validation.py -v
```

## Security Notes

- Do not commit Porkbun API keys, secret keys, real customer domains, or sensitive record values.
- Treat DNS mutations as production-impacting operations.
- Review generated `delete_dns_record` and `edit_dns_record` calls before exposing them to unattended agent workflows.
- Scrub real domain details from fixtures, screenshots, and troubleshooting logs.
