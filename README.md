# Porkbun DNS MCP Server

[![Code style: crackerjack](https://img.shields.io/badge/code%20style-crackerjack-000042)](https://github.com/lesleslie/crackerjack)
[![Runtime: oneiric](https://img.shields.io/badge/runtime-oneiric-6e5494)](https://github.com/lesleslie/oneiric)
[![Framework: FastMCP](https://img.shields.io/badge/framework-FastMCP-0ea5e9)](https://github.com/jlowin/fastmcp)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Python: 3.13+](https://img.shields.io/badge/python-3.13%2B-green)](https://www.python.org/downloads/)

MCP server for managing Porkbun DNS records through a FastMCP interface.

## Overview

This repository provides a focused DNS-management server for Porkbun domains. It is intended for record lookup, creation, updates, and deletion workflows, with typed validation around provider requests and responses.

## Installation

```bash
uv sync --group dev
```

## Usage

### Stdio Mode

```bash
uv run porkbun-dns-mcp
```

### HTTP Mode

```bash
uv run porkbun-dns-mcp serve --http --port 3042
```

## Development

```bash
uv run pytest
uv run ruff check porkbun_dns_mcp tests
uv run ruff format porkbun_dns_mcp tests
```

## Project Structure

- `porkbun_dns_mcp/`: server package, API client, tools, and schemas
- `tests/`: record workflow and provider error-path coverage
- `docs/`: operator-facing guidance and examples

## Security Notes

- Keep Porkbun credentials in environment variables or local config only.
- Avoid putting real domains, tokens, or sensitive record values in examples or logs.
