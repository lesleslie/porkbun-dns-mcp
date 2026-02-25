"""Pydantic models for Porkbun DNS API request/response validation.

This module defines all the data models used for interacting with the
Porkbun DNS API, including DNS record types and API responses.

API Documentation: https://porkbun.com/api/json/v3/documentation
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DNSRecordType(str, Enum):
    """Supported DNS record types.

    Porkbun supports the following record types:
    - A: IPv4 address
    - AAAA: IPv6 address
    - CNAME: Canonical name (alias)
    - MX: Mail exchange
    - TXT: Text record (SPF, DKIM, etc.)
    - NS: Name server
    - SRV: Service record
    - CAA: Certificate Authority Authorization
    - ALIAS: ANAME record (root domain CNAME alternative)
    """

    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    NS = "NS"
    SRV = "SRV"
    CAA = "CAA"
    ALIAS = "ALIAS"


class DNSRecord(BaseModel):
    """A DNS record from Porkbun API.

    Attributes:
        id: Unique record identifier
        name: Record name (subdomain or @ for root)
        type: DNS record type (A, AAAA, CNAME, etc.)
        content: Record content/value
        ttl: Time to live in seconds
        priority: Priority for MX/SRV records (optional)
        notes: Optional notes for the record
    """

    id: str = Field(description="Unique record identifier")
    name: str = Field(description="Record name (subdomain or @ for root)")
    type: DNSRecordType = Field(description="DNS record type")
    content: str = Field(description="Record content/value")
    ttl: int = Field(default=600, description="Time to live in seconds", ge=60)
    priority: int | None = Field(
        default=None,
        description="Priority for MX/SRV records (0-65535)",
        ge=0,
        le=65535,
    )
    notes: str | None = Field(default=None, description="Optional notes")

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Normalize record name - empty string becomes @ for root domain."""
        return v if v else "@"


class DNSRecordCreate(BaseModel):
    """Request model for creating a new DNS record.

    Attributes:
        domain: Domain name (e.g., "example.com")
        record_type: DNS record type
        name: Record name (subdomain or @ for root)
        content: Record content/value
        ttl: Time to live in seconds (default: 600)
        priority: Priority for MX/SRV records (optional)
    """

    domain: str = Field(description="Domain name (e.g., 'example.com')")
    record_type: DNSRecordType = Field(
        alias="type",
        description="DNS record type (A, AAAA, CNAME, MX, TXT, NS, SRV, CAA, ALIAS)",
    )
    name: str = Field(
        default="",
        description="Record name (subdomain or empty/@ for root domain)",
    )
    content: str = Field(description="Record content/value (IP address, hostname, etc.)")
    ttl: int = Field(
        default=600,
        description="Time to live in seconds (minimum: 60)",
        ge=60,
        le=604800,  # Max 7 days
    )
    priority: int | None = Field(
        default=None,
        description="Priority for MX/SRV records (0-65535)",
        ge=0,
        le=65535,
    )

    model_config = {"populate_by_name": True}


class DNSRecordUpdate(BaseModel):
    """Request model for updating an existing DNS record.

    All fields are optional - only provided fields will be updated.

    Attributes:
        name: New record name
        type: New DNS record type
        content: New record content
        ttl: New TTL value
        priority: New priority value
    """

    name: str | None = Field(default=None, description="New record name")
    type: DNSRecordType | None = Field(default=None, description="New DNS record type")
    content: str | None = Field(default=None, description="New record content")
    ttl: int | None = Field(
        default=None,
        description="New TTL value (60-604800)",
        ge=60,
        le=604800,
    )
    priority: int | None = Field(
        default=None,
        description="New priority for MX/SRV records",
        ge=0,
        le=65535,
    )


class PorkbunResponse(BaseModel):
    """Base response from Porkbun API.

    Porkbun API returns a consistent response structure with status
    and optional message for errors.

    Attributes:
        status: "SUCCESS" or "ERROR"
        message: Error message (if status is ERROR)
    """

    status: str = Field(description="Response status: SUCCESS or ERROR")
    message: str | None = Field(
        default=None,
        description="Error message when status is ERROR",
    )

    @property
    def success(self) -> bool:
        """Check if the response indicates success."""
        return self.status.upper() == "SUCCESS"


class DNSRecordsResponse(PorkbunResponse):
    """Response containing DNS records.

    Attributes:
        records: List of DNS records
    """

    records: list[DNSRecord] = Field(
        default_factory=list,
        description="List of DNS records",
    )


class DNSRecordResponse(PorkbunResponse):
    """Response for a single DNS record operation.

    Attributes:
        record: The DNS record (for retrieve operations)
    """

    record: DNSRecord | None = Field(
        default=None,
        description="The DNS record",
    )


class CreateRecordResponse(PorkbunResponse):
    """Response after creating a DNS record.

    Attributes:
        id: ID of the newly created record
    """

    id: int | None = Field(
        default=None,
        description="ID of the newly created record",
    )


class PorkbunError(Exception):
    """Exception raised for Porkbun API errors.

    Attributes:
        message: Error message from the API
        status: HTTP status code (if available)
        details: Additional error details
    """

    def __init__(
        self,
        message: str,
        status: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize the exception.

        Args:
            message: Error message
            status: HTTP status code
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.status = status
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API responses.

        Returns:
            Dictionary representation of the error
        """
        result: dict[str, Any] = {
            "error": self.message,
            "status": self.status,
        }
        if self.details:
            result["details"] = self.details
        return result


__all__ = [
    "DNSRecordType",
    "DNSRecord",
    "DNSRecordCreate",
    "DNSRecordUpdate",
    "PorkbunResponse",
    "DNSRecordsResponse",
    "DNSRecordResponse",
    "CreateRecordResponse",
    "PorkbunError",
]
