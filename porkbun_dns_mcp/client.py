"""Porkbun API client for DNS management.

This module provides an async HTTP client for interacting with the Porkbun DNS API.

API Documentation: https://porkbun.com/api/json/v3/documentation
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx

from .config import PorkbunDNSSettings, get_logger_instance, get_settings
from .models import (
    CreateRecordResponse,
    DNSRecord,
    DNSRecordsResponse,
    PorkbunError,
)

logger = get_logger_instance("porkbun-dns-mcp.client")


class PorkbunClient:
    """Async HTTP client for Porkbun DNS API.

    Provides methods for managing DNS records through the Porkbun API.
    All operations require authentication via API key and secret key.

    Attributes:
        settings: Configuration settings
        client: HTTPX async client

    Example:
        >>> async with PorkbunClient() as client:
        ...     records = await client.list_records("example.com")
        ...     for record in records:
        ...         print(f"{record.name}: {record.content}")
    """

    def __init__(self, settings: PorkbunDNSSettings | None = None) -> None:
        """Initialize the Porkbun client.

        Args:
            settings: Optional settings instance. Uses get_settings() if not provided.
        """
        self.settings = settings or get_settings()
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "PorkbunClient":
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, *args: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized.

        Returns:
            Initialized HTTPX async client
        """
        if self._client is None:
            config = self.settings.http_client_config()
            self._client = httpx.AsyncClient(**config)
            logger.debug(
                "HTTP client initialized",
                base_url=config["base_url"],
                timeout=self.settings.timeout,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.debug("HTTP client closed")

    async def _request(
        self,
        method: str,
        endpoint: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated request to the Porkbun API.

        Args:
            method: HTTP method (POST for all Porkbun endpoints)
            endpoint: API endpoint path
            payload: Request payload (will include auth credentials)

        Returns:
            Parsed JSON response

        Raises:
            PorkbunError: If the API returns an error or request fails
        """
        client = await self._ensure_client()

        # Merge authentication payload with request payload
        full_payload = {**self.settings.auth_payload()}
        if payload:
            full_payload.update(payload)

        # Retry logic with exponential backoff
        last_error: Exception | None = None
        for attempt in range(self.settings.max_retries + 1):
            try:
                response = await client.request(
                    method,
                    endpoint,
                    json=full_payload,
                )
                response.raise_for_status()

                data = response.json()

                # Check Porkbun API status
                if data.get("status", "").upper() != "SUCCESS":
                    message = data.get("message", "Unknown API error")
                    raise PorkbunError(
                        message=message,
                        status=response.status_code,
                        details=data,
                    )

                logger.debug(
                    "API request successful",
                    endpoint=endpoint,
                    attempt=attempt + 1,
                )
                return data

            except httpx.HTTPStatusError as e:
                last_error = e
                logger.warning(
                    "API request failed",
                    endpoint=endpoint,
                    status_code=e.response.status_code,
                    attempt=attempt + 1,
                )
                if attempt < self.settings.max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                else:
                    raise PorkbunError(
                        message=f"HTTP {e.response.status_code}: {e.response.text}",
                        status=e.response.status_code,
                    ) from e

            except httpx.RequestError as e:
                last_error = e
                logger.warning(
                    "API request error",
                    endpoint=endpoint,
                    error=str(e),
                    attempt=attempt + 1,
                )
                if attempt < self.settings.max_retries:
                    await asyncio.sleep(0.5 * (2**attempt))
                else:
                    raise PorkbunError(
                        message=f"Request failed: {e}",
                    ) from e

        # Should not reach here, but just in case
        raise PorkbunError(
            message=f"Request failed after {self.settings.max_retries} retries",
        ) from last_error

    # =========================================================================
    # DNS Record Operations
    # =========================================================================

    async def list_records(self, domain: str) -> list[DNSRecord]:
        """Retrieve all DNS records for a domain.

        Args:
            domain: Domain name (e.g., "example.com")

        Returns:
            List of DNS records

        Raises:
            PorkbunError: If the API request fails
        """
        logger.debug("Listing DNS records", domain=domain)

        data = await self._request("POST", f"/dns/retrieve/{domain}")

        response = DNSRecordsResponse(**data)
        return response.records

    async def get_record(self, domain: str, record_id: int | str) -> DNSRecord:
        """Retrieve a specific DNS record.

        Args:
            domain: Domain name (e.g., "example.com")
            record_id: Record ID

        Returns:
            DNS record

        Raises:
            PorkbunError: If the API request fails or record not found
        """
        logger.debug("Getting DNS record", domain=domain, record_id=record_id)

        data = await self._request(
            "POST",
            f"/dns/retrieve/{domain}/{record_id}",
        )

        response = DNSRecordsResponse(**data)

        if not response.records:
            raise PorkbunError(
                message=f"Record {record_id} not found for domain {domain}",
                status=404,
            )

        return response.records[0]

    async def create_record(
        self,
        domain: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 600,
        priority: int | None = None,
    ) -> DNSRecord:
        """Create a new DNS record.

        Args:
            domain: Domain name (e.g., "example.com")
            record_type: DNS record type (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, ALIAS)
            name: Record name (subdomain or empty/@ for root)
            content: Record content/value
            ttl: Time to live in seconds (default: 600, minimum: 60)
            priority: Priority for MX/SRV records

        Returns:
            Created DNS record with ID

        Raises:
            PorkbunError: If the API request fails
        """
        logger.debug(
            "Creating DNS record",
            domain=domain,
            record_type=record_type,
            name=name,
        )

        payload: dict[str, Any] = {
            "type": record_type.upper(),
            "name": name,
            "content": content,
            "ttl": ttl,
        }

        if priority is not None:
            payload["prio"] = priority

        data = await self._request("POST", f"/dns/create/{domain}", payload)

        response = CreateRecordResponse(**data)

        if response.id is None:
            raise PorkbunError(message="Create record response missing ID")

        # Fetch and return the created record
        return await self.get_record(domain, response.id)

    async def edit_record(
        self,
        domain: str,
        record_id: int | str,
        record_type: str | None = None,
        name: str | None = None,
        content: str | None = None,
        ttl: int | None = None,
        priority: int | None = None,
    ) -> DNSRecord:
        """Edit an existing DNS record.

        Only provided fields will be updated.

        Args:
            domain: Domain name (e.g., "example.com")
            record_id: Record ID to edit
            record_type: New record type (optional)
            name: New record name (optional)
            content: New record content (optional)
            ttl: New TTL value (optional)
            priority: New priority for MX/SRV records (optional)

        Returns:
            Updated DNS record

        Raises:
            PorkbunError: If the API request fails
        """
        logger.debug(
            "Editing DNS record",
            domain=domain,
            record_id=record_id,
        )

        # Get current record for defaults
        current = await self.get_record(domain, record_id)

        payload: dict[str, Any] = {
            "type": record_type or current.type.value,
            "name": name if name is not None else current.name,
            "content": content or current.content,
            "ttl": ttl or current.ttl,
        }

        if priority is not None:
            payload["prio"] = priority
        elif current.priority is not None:
            payload["prio"] = current.priority

        await self._request(
            "POST",
            f"/dns/edit/{domain}/{record_id}",
            payload,
        )

        # Fetch and return the updated record
        return await self.get_record(domain, record_id)

    async def delete_record(self, domain: str, record_id: int | str) -> bool:
        """Delete a DNS record.

        Args:
            domain: Domain name (e.g., "example.com")
            record_id: Record ID to delete

        Returns:
            True if deletion was successful

        Raises:
            PorkbunError: If the API request fails
        """
        logger.debug(
            "Deleting DNS record",
            domain=domain,
            record_id=record_id,
        )

        await self._request("POST", f"/dns/delete/{domain}/{record_id}")

        return True


__all__ = ["PorkbunClient"]
