"""FastMCP server for Porkbun DNS management.

This module provides the FastMCP application with HTTP transport support
and Oneiric-style configuration.
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP

from porkbun_dns_mcp import __version__
from porkbun_dns_mcp.client import PorkbunClient
from porkbun_dns_mcp.config import get_logger_instance, get_settings, setup_logging
from porkbun_dns_mcp.tools import register_dns_tools

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

logger = get_logger_instance("porkbun-dns-mcp.server")

APP_NAME = "porkbun-dns-mcp"
APP_VERSION = __version__


def create_app() -> FastMCP:
    """Create and configure the FastMCP application.

    Returns:
        Configured FastMCP application instance
    """
    # Initialize logging with Oneiric
    settings = get_settings()
    setup_logging(settings)

    logger.info(
        "Initializing Porkbun DNS MCP server",
        version=APP_VERSION,
        http_transport=settings.enable_http_transport,
    )

    # Validate credentials
    if not settings.has_credentials():
        logger.warning(
            "API credentials not configured. Set PORKBUN_DNS_API_KEY and "
            "PORKBUN_DNS_SECRET_KEY environment variables."
        )

    # Create FastMCP app
    app = FastMCP(
        name=APP_NAME,
        version=APP_VERSION,
    )

    # Create client
    client = PorkbunClient(settings)

    # Register tools
    register_dns_tools(app, client)

    # Set up lifespan for client cleanup
    original_lifespan = app._mcp_server.lifespan

    @asynccontextmanager
    async def lifespan(server: Any) -> AsyncGenerator[dict[str, Any]]:
        """Manage client lifecycle."""
        async with original_lifespan(server) as state:
            try:
                yield state
            finally:
                await client.close()
                logger.info("Porkbun client closed")

    app._mcp_server.lifespan = lifespan
    app._porkbun_client = client  # type: ignore[attr-defined]

    logger.info("Porkbun DNS MCP server initialized")
    return app


# Lazy initialization for import
_app: FastMCP | None = None


def get_app() -> FastMCP:
    """Get or create the FastMCP application.

    Returns:
        FastMCP application instance
    """
    global _app
    if _app is None:
        _app = create_app()
    return _app


# Export for uvicorn ASGI serving
def __getattr__(name: str) -> Any:
    """Lazy attribute access for app and http_app."""
    if name == "app":
        return get_app()
    if name == "http_app":
        return get_app().http_app
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


__all__ = [
    "create_app",
    "get_app",
    "APP_NAME",
    "APP_VERSION",
]
