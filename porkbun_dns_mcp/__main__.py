"""Run Porkbun DNS MCP server as a module.

Usage:
    python -m porkbun_dns_mcp serve --http
    python -m porkbun_dns_mcp serve  # stdio mode
    python -m porkbun_dns_mcp --help
"""

from porkbun_dns_mcp.cli import main

if __name__ == "__main__":
    main()
