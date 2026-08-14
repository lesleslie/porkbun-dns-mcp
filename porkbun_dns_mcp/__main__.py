"""Run Porkbun DNS MCP server as a module.

The lifecycle CLI is provided by `mcp-common`'s `MCPServerCLIFactory`.
Available subcommands include `start`, `stop`, `restart`, `status`,
and `health` (see `python -m porkbun_dns_mcp --help` for the canonical
list).

Usage:
    python -m porkbun_dns_mcp start    # Start the HTTP MCP server
    python -m porkbun_dns_mcp stop     # Stop the managed server process
    python -m porkbun_dns_mcp health   # Run the local health probe
    python -m porkbun_dns_mcp --help   # Show all available subcommands
"""

from porkbun_dns_mcp.cli import main

if __name__ == "__main__":
    main()
