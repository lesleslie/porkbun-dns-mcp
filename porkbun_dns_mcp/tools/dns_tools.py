"""DNS record management MCP tools.

This module provides MCP tools for managing DNS records through the Porkbun API.

Tools provided:
- list_dns_records: Retrieve all DNS records for a domain
- get_dns_record: Retrieve a specific DNS record
- create_dns_record: Create a new DNS record
- edit_dns_record: Edit an existing DNS record
- delete_dns_record: Delete a DNS record
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from porkbun_dns_mcp.client import PorkbunClient
from porkbun_dns_mcp.config import get_logger_instance
from porkbun_dns_mcp.models import DNSRecord, DNSRecordType

if TYPE_CHECKING:
    from fastmcp import FastMCP

logger = get_logger_instance("porkbun-dns-mcp.tools")


# =============================================================================
# Tool Input Models
# =============================================================================


class ListDNSRecordsInput(BaseModel):
    """Input for list_dns_records tool."""

    domain: str = Field(description="Domain name (e.g., 'example.com')")


class GetDNSRecordInput(BaseModel):
    """Input for get_dns_record tool."""

    domain: str = Field(description="Domain name (e.g., 'example.com')")
    record_id: int = Field(description="DNS record ID")


class CreateDNSRecordInput(BaseModel):
    """Input for create_dns_record tool."""

    domain: str = Field(description="Domain name (e.g., 'example.com')")
    record_type: str = Field(
        description="DNS record type: A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, or ALIAS"
    )
    name: str = Field(
        description="Record name (subdomain or empty for root domain)"
    )
    content: str = Field(description="Record content/value (IP address, hostname, etc.)")
    ttl: int = Field(
        default=600,
        description="Time to live in seconds (minimum: 60, default: 600)",
    )
    priority: int | None = Field(
        default=None,
        description="Priority for MX/SRV records (0-65535)",
    )


class EditDNSRecordInput(BaseModel):
    """Input for edit_dns_record tool."""

    domain: str = Field(description="Domain name (e.g., 'example.com')")
    record_id: int = Field(description="DNS record ID to edit")
    record_type: str | None = Field(
        default=None,
        description="New record type (optional)",
    )
    name: str | None = Field(
        default=None,
        description="New record name (optional)",
    )
    content: str | None = Field(
        default=None,
        description="New record content (optional)",
    )
    ttl: int | None = Field(
        default=None,
        description="New TTL value (optional)",
    )
    priority: int | None = Field(
        default=None,
        description="New priority for MX/SRV records (optional)",
    )


class DeleteDNSRecordInput(BaseModel):
    """Input for delete_dns_record tool."""

    domain: str = Field(description="Domain name (e.g., 'example.com')")
    record_id: int = Field(description="DNS record ID to delete")


# =============================================================================
# Tool Response Model
# =============================================================================


class ToolResponse(BaseModel):
    """Standardized LLM-friendly tool response.

    Follows the mcp-common ToolResponse pattern for consistency.
    """

    success: bool = Field(description="Whether the operation succeeded")
    message: str = Field(description="Human-readable result message")
    data: dict[str, Any] | None = Field(
        default=None,
        description="Structured output data",
    )
    error: str | None = Field(
        default=None,
        description="Error details if operation failed",
    )
    next_steps: list[str] | None = Field(
        default=None,
        description="Suggested follow-up actions",
    )


def _record_to_dict(record: DNSRecord) -> dict[str, Any]:
    """Convert DNSRecord to dictionary for API response.

    Args:
        record: DNS record to convert

    Returns:
        Dictionary representation
    """
    return {
        "id": record.id,
        "name": record.name,
        "type": record.type.value,
        "content": record.content,
        "ttl": record.ttl,
        "priority": record.priority,
        "notes": record.notes,
    }


# =============================================================================
# Tool Registration
# =============================================================================


def register_dns_tools(app: "FastMCP", client: PorkbunClient) -> None:
    """Register DNS management tools with the FastMCP app.

    Args:
        app: FastMCP application instance
        client: Porkbun API client
    """

    @app.tool()
    async def list_dns_records(domain: str) -> ToolResponse:
        """List all DNS records for a domain.

        Retrieves all DNS records configured for the specified domain
        through the Porkbun API.

        Args:
            domain: Domain name (e.g., 'example.com')

        Returns:
            ToolResponse with list of DNS records
        """
        logger.info("Listing DNS records", domain=domain)

        try:
            records = await client.list_records(domain)

            return ToolResponse(
                success=True,
                message=f"Found {len(records)} DNS records for {domain}",
                data={
                    "domain": domain,
                    "records": [_record_to_dict(r) for r in records],
                    "count": len(records),
                },
                next_steps=[
                    "Review the records for any needed changes",
                    "Use create_dns_record to add new records",
                    "Use edit_dns_record to modify existing records",
                ],
            )

        except Exception as e:
            logger.error("Failed to list DNS records", domain=domain, error=str(e))
            return ToolResponse(
                success=False,
                message=f"Failed to list DNS records for {domain}",
                error=str(e),
                next_steps=[
                    "Verify the domain name is correct",
                    "Check your API credentials are valid",
                    "Ensure you have permission to access this domain",
                ],
            )

    @app.tool()
    async def get_dns_record(domain: str, record_id: int) -> ToolResponse:
        """Get a specific DNS record by ID.

        Retrieves details for a single DNS record.

        Args:
            domain: Domain name (e.g., 'example.com')
            record_id: The DNS record ID

        Returns:
            ToolResponse with the DNS record details
        """
        logger.info("Getting DNS record", domain=domain, record_id=record_id)

        try:
            record = await client.get_record(domain, record_id)

            return ToolResponse(
                success=True,
                message=f"Retrieved DNS record {record_id}",
                data={
                    "domain": domain,
                    "record": _record_to_dict(record),
                },
                next_steps=[
                    "Use edit_dns_record to modify this record",
                    "Use delete_dns_record to remove this record",
                ],
            )

        except Exception as e:
            logger.error(
                "Failed to get DNS record",
                domain=domain,
                record_id=record_id,
                error=str(e),
            )
            return ToolResponse(
                success=False,
                message=f"Failed to get DNS record {record_id}",
                error=str(e),
                next_steps=[
                    "Verify the record ID is correct",
                    "Use list_dns_records to find valid record IDs",
                ],
            )

    @app.tool()
    async def create_dns_record(
        domain: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 600,
        priority: int | None = None,
    ) -> ToolResponse:
        """Create a new DNS record.

        Creates a new DNS record for the specified domain.

        Args:
            domain: Domain name (e.g., 'example.com')
            record_type: DNS record type (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, ALIAS)
            name: Record name (subdomain or empty for root domain)
            content: Record content (IP address, hostname, text, etc.)
            ttl: Time to live in seconds (default: 600, minimum: 60)
            priority: Priority for MX/SRV records (optional)

        Returns:
            ToolResponse with the created record details
        """
        logger.info(
            "Creating DNS record",
            domain=domain,
            record_type=record_type,
            name=name,
        )

        try:
            # Validate record type
            record_type = record_type.upper()
            if record_type not in [t.value for t in DNSRecordType]:
                valid_types = ", ".join([t.value for t in DNSRecordType])
                return ToolResponse(
                    success=False,
                    message=f"Invalid record type: {record_type}",
                    error=f"Valid types are: {valid_types}",
                    next_steps=[f"Use one of: {valid_types}"],
                )

            record = await client.create_record(
                domain=domain,
                record_type=record_type,
                name=name,
                content=content,
                ttl=ttl,
                priority=priority,
            )

            return ToolResponse(
                success=True,
                message=f"Created {record_type} record for {domain}",
                data={
                    "domain": domain,
                    "record": _record_to_dict(record),
                },
                next_steps=[
                    "Verify the record with list_dns_records",
                    "Wait for DNS propagation (may take a few minutes)",
                    "Test the record with dig or nslookup",
                ],
            )

        except Exception as e:
            logger.error(
                "Failed to create DNS record",
                domain=domain,
                record_type=record_type,
                error=str(e),
            )
            return ToolResponse(
                success=False,
                message=f"Failed to create DNS record for {domain}",
                error=str(e),
                next_steps=[
                    "Verify the record content is valid for the type",
                    "Check for duplicate records",
                    "Ensure TTL is at least 60 seconds",
                ],
            )

    @app.tool()
    async def edit_dns_record(
        domain: str,
        record_id: int,
        record_type: str | None = None,
        name: str | None = None,
        content: str | None = None,
        ttl: int | None = None,
        priority: int | None = None,
    ) -> ToolResponse:
        """Edit an existing DNS record.

        Updates specified fields of an existing DNS record.
        Only provided fields will be changed.

        Args:
            domain: Domain name (e.g., 'example.com')
            record_id: The DNS record ID to edit
            record_type: New record type (optional)
            name: New record name (optional)
            content: New record content (optional)
            ttl: New TTL value (optional)
            priority: New priority for MX/SRV records (optional)

        Returns:
            ToolResponse with the updated record details
        """
        logger.info("Editing DNS record", domain=domain, record_id=record_id)

        try:
            record = await client.edit_record(
                domain=domain,
                record_id=record_id,
                record_type=record_type,
                name=name,
                content=content,
                ttl=ttl,
                priority=priority,
            )

            return ToolResponse(
                success=True,
                message=f"Updated DNS record {record_id}",
                data={
                    "domain": domain,
                    "record": _record_to_dict(record),
                },
                next_steps=[
                    "Verify the changes with list_dns_records",
                    "Wait for DNS propagation if content changed",
                ],
            )

        except Exception as e:
            logger.error(
                "Failed to edit DNS record",
                domain=domain,
                record_id=record_id,
                error=str(e),
            )
            return ToolResponse(
                success=False,
                message=f"Failed to edit DNS record {record_id}",
                error=str(e),
                next_steps=[
                    "Verify the record ID exists",
                    "Use list_dns_records to find valid record IDs",
                ],
            )

    @app.tool()
    async def delete_dns_record(domain: str, record_id: int) -> ToolResponse:
        """Delete a DNS record.

        Permanently removes a DNS record from the domain.

        Args:
            domain: Domain name (e.g., 'example.com')
            record_id: The DNS record ID to delete

        Returns:
            ToolResponse confirming deletion
        """
        logger.info("Deleting DNS record", domain=domain, record_id=record_id)

        try:
            await client.delete_record(domain, record_id)

            return ToolResponse(
                success=True,
                message=f"Deleted DNS record {record_id} from {domain}",
                data={
                    "domain": domain,
                    "record_id": record_id,
                    "deleted": True,
                },
                next_steps=[
                    "Verify deletion with list_dns_records",
                    "Update any services that depended on this record",
                ],
            )

        except Exception as e:
            logger.error(
                "Failed to delete DNS record",
                domain=domain,
                record_id=record_id,
                error=str(e),
            )
            return ToolResponse(
                success=False,
                message=f"Failed to delete DNS record {record_id}",
                error=str(e),
                next_steps=[
                    "Verify the record ID exists",
                    "Use list_dns_records to find valid record IDs",
                ],
            )

    logger.info("Registered 5 DNS management tools")
