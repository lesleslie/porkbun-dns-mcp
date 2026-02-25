"""Porkbun DNS MCP - MCP server for Porkbun DNS management.

This package provides an MCP (Model Context Protocol) server for managing
DNS records through the Porkbun API.

Modules:
    models: Pydantic models for API request/response validation
    config: Configuration with Oneiric logging support
    client: HTTP client for Porkbun API communication
    server: FastMCP server implementation
"""

from porkbun_dns_mcp.client import PorkbunClient
from porkbun_dns_mcp.config import PorkbunDNSSettings, get_settings, setup_logging
from porkbun_dns_mcp.models import (
    DNSRecord,
    DNSRecordCreate,
    DNSRecordType,
    DNSRecordUpdate,
    PorkbunError,
)

__version__ = "0.1.1"

__all__ = [
    "PorkbunClient",
    "PorkbunDNSSettings",
    "get_settings",
    "setup_logging",
    "DNSRecord",
    "DNSRecordCreate",
    "DNSRecordType",
    "DNSRecordUpdate",
    "PorkbunError",
    "__version__",
]
