"""Schema validation tests for Pydantic models in porkbun-dns-mcp.

This module provides tests to ensure Pydantic models properly handle
API responses with extra fields, which is critical for forward compatibility
when Porkbun API adds new fields.

Current Status:
    No Pydantic models exist yet in this project. This file serves as a
    template for when models are added to porkbun_dns_mcp.models.

When models are added:
    1. Import the models from porkbun_dns_mcp.models
    2. Uncomment and adapt the test classes below
    3. Add fixture data matching actual Porkbun API responses

Example model structure expected:
    from pydantic import BaseModel, ConfigDict

    class DNSRecord(BaseModel):
        model_config = ConfigDict(extra="ignore")  # or extra="allow"
        id: str
        name: str
        type: str
        content: str
        ttl: int
        prio: int | None = None
"""

from __future__ import annotations

import pytest


# =============================================================================
# TEMPLATE TEST CLASSES
# Uncomment and adapt these when Pydantic models are added to the project
# =============================================================================


class TestSchemaValidationTemplate:
    """Template tests for schema validation - enable when models exist.

    These tests verify that Pydantic models:
    1. Accept extra fields from API responses (forward compatibility)
    2. Have model_config with extra="ignore" or extra="allow"

    This is critical because:
    - Porkbun API may add new fields without notice
    - We don't want parsing to fail on unknown fields
    - Forward compatibility reduces maintenance burden
    """

    @pytest.fixture
    def sample_dns_record_response(self) -> dict[str, object]:
        """Sample DNS record response from Porkbun API.

        Returns:
            Dict containing a typical DNS record response.
            Add/remove fields as needed based on actual API responses.

        Reference: https://porkbun.com/api/json/v3/documentation
        """
        return {
            "id": "123456",
            "name": "example.com",
            "type": "A",
            "content": "192.168.1.1",
            "ttl": "600",
            "prio": None,
            # Future fields from API would appear here
            # "notes": "Example note",
            # "flags": None,
        }

    @pytest.fixture
    def sample_dns_record_with_extra_fields(self) -> dict[str, object]:
        """DNS record response with extra/unknown fields.

        Returns:
            Dict containing DNS record with hypothetical future fields
            that Porkbun API might add.

        This tests forward compatibility - models should accept unknown
        fields rather than raising validation errors.
        """
        return {
            "id": "789012",
            "name": "www.example.com",
            "type": "CNAME",
            "content": "example.com",
            "ttl": "300",
            "prio": None,
            # Hypothetical future fields
            "notes": "Added by automation",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-20T14:22:00Z",
            "tags": ["production", "verified"],
            "internal_id": "abc123xyz",
        }

    @pytest.mark.skip(reason="No Pydantic models exist yet in porkbun_dns_mcp")
    def test_extra_fields_ignored(self) -> None:
        """Verify model accepts extra fields without raising errors.

        This test ensures that when Porkbun API adds new fields,
        our models won't break. The model should parse successfully
        and ignore any unknown fields.

        Implementation when models exist:

            from porkbun_dns_mcp.models import DNSRecord

            data = self.sample_dns_record_with_extra_fields
            record = DNSRecord.model_validate(data)

            assert record.id == "789012"
            assert record.name == "www.example.com"
            # Should not raise ValidationError
        """
        _ = self.sample_dns_record_with_extra_fields
        pytest.fail("Implement this test when DNSRecord model is created")

    @pytest.mark.skip(reason="No Pydantic models exist yet in porkbun_dns_mcp")
    def test_model_has_extra_ignore(self) -> None:
        """Verify model_config has extra='ignore' or extra='allow'.

        This test ensures the model is explicitly configured to handle
        extra fields, rather than relying on Pydantic's default behavior.

        Implementation when models exist:

            from porkbun_dns_mcp.models import DNSRecord

            config = DNSRecord.model_config
            extra_setting = config.get("extra")

            # Either "ignore" (discard extra fields) or "allow"
            # (keep them) is acceptable
            assert extra_setting in ("ignore", "allow"), (
                f"DNSRecord should have extra='ignore' or extra='allow', "
                f"got extra='{extra_setting}'"
            )
        """
        pytest.fail("Implement this test when DNSRecord model is created")


# =============================================================================
# ADDITIONAL MODEL TEMPLATES
# Copy and adapt these for other model types as needed
# =============================================================================


class TestDomainRecordTemplate:
    """Template tests for Domain-related models."""

    @pytest.fixture
    def sample_domain_response(self) -> dict[str, object]:
        """Sample domain listing response."""
        return {
            "domain": "example.com",
            "status": "ACTIVE",
            "tld": "com",
            "createDate": "2020-01-15",
            "expireDate": "2025-01-15",
        }

    @pytest.mark.skip(reason="No Domain model exists yet")
    def test_extra_fields_ignored(self) -> None:
        """Placeholder for Domain model extra fields test."""
        pytest.fail("Implement when Domain model is created")

    @pytest.mark.skip(reason="No Domain model exists yet")
    def test_model_has_extra_ignore(self) -> None:
        """Placeholder for Domain model config test."""
        pytest.fail("Implement when Domain model is created")


class TestAPIResponseTemplate:
    """Template tests for generic API response wrapper models."""

    @pytest.fixture
    def sample_api_response(self) -> dict[str, object]:
        """Sample API response structure."""
        return {
            "status": "SUCCESS",
            "message": "Record created successfully",
            "records": [],
        }

    @pytest.mark.skip(reason="No APIResponse model exists yet")
    def test_extra_fields_ignored(self) -> None:
        """Placeholder for APIResponse model extra fields test."""
        pytest.fail("Implement when APIResponse model is created")

    @pytest.mark.skip(reason="No APIResponse model exists yet")
    def test_model_has_extra_ignore(self) -> None:
        """Placeholder for APIResponse model config test."""
        pytest.fail("Implement when APIResponse model is created")


# =============================================================================
# DISCOVERY TESTS
# These tests can run now to help identify what models exist
# =============================================================================


class TestModelDiscovery:
    """Tests to discover and document existing models.

    These tests help track when models are added to the project
    and serve as documentation for the expected model structure.
    """

    def test_models_module_exists(self) -> None:
        """Check if the models module exists.

        This test documents the expected location for Pydantic models.
        When models are added, they should be placed in:
            porkbun_dns_mcp/models.py
        or
            porkbun_dns_mcp/models/__init__.py
        """
        import importlib.util

        spec = importlib.util.find_spec("porkbun_dns_mcp.models")
        # Currently expected to fail - update when models are added
        assert spec is None, (
            "Models module found! Update test_schema_validation.py "
            "to enable model-specific tests."
        )

    def test_porkbun_dns_mcp_package_structure(self) -> None:
        """Document the expected package structure for models.

        Expected structure:
            porkbun_dns_mcp/
            |-- __init__.py
            |-- models.py          # or models/
            |   |-- __init__.py    # if using package
            |   |-- dns_record.py
            |   |-- domain.py
            |   |-- api_response.py
            |-- client.py
            |-- server.py
        """
        from pathlib import Path

        package_dir = Path(__file__).parent.parent / "porkbun_dns_mcp"
        assert package_dir.exists(), "porkbun_dns_mcp package directory exists"

        # List current contents for documentation
        contents = list(package_dir.iterdir()) if package_dir.exists() else []
        python_files = [f.name for f in contents if f.suffix == ".py"]

        # Document current state
        print(f"Current Python files in porkbun_dns_mcp: {python_files}")

        # This assertion will pass now; update when models are added
        assert True


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Add markers to tests based on their class names.

    This allows running specific test categories:
        pytest -m unit          # Run unit tests
        pytest -m "not slow"    # Skip slow tests
    """
    for item in items:
        # Mark all tests in this file as unit tests
        if "test_schema_validation" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
