"""Unit tests for config and model coverage.

These tests exercise helper methods and validators that the existing
test suite does not cover, to lift coverage of the small, side-effect-free
modules above the 80% threshold without adding integration surface.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from porkbun_dns_mcp.config import PorkbunDNSSettings
from porkbun_dns_mcp.models import (
    DNSRecord,
    DNSRecordCreate,
    DNSRecordType,
    PorkbunError,
)
from porkbun_dns_mcp.tools.dns_tools import (
    ToolResponse,
    _record_to_dict,
    register_dns_tools,
)


@pytest.mark.unit
class TestPorkbunDNSSettings:
    """Cover helper methods on PorkbunDNSSettings without env-var coupling."""

    def test_has_credentials_both_blank(self) -> None:
        settings = PorkbunDNSSettings(api_key="", secret_key="")
        assert settings.has_credentials() is False

    def test_has_credentials_both_set(self) -> None:
        settings = PorkbunDNSSettings(api_key="pk1", secret_key="sk1")
        assert settings.has_credentials() is True

    def test_has_credentials_only_api_key(self) -> None:
        settings = PorkbunDNSSettings(api_key="pk1", secret_key="")
        assert settings.has_credentials() is False

    def test_get_masked_api_key_empty(self) -> None:
        settings = PorkbunDNSSettings(api_key="", secret_key="")
        assert settings.get_masked_api_key() == "***"

    def test_get_masked_api_key_short(self) -> None:
        settings = PorkbunDNSSettings(api_key="abc", secret_key="")
        assert settings.get_masked_api_key() == "***"

    def test_get_masked_api_key_long(self) -> None:
        settings = PorkbunDNSSettings(api_key="abcdefghij", secret_key="")
        assert settings.get_masked_api_key() == "...ghij"

    def test_validate_base_url_empty_returns_default(self) -> None:
        settings = PorkbunDNSSettings(base_url="", api_key="", secret_key="")
        assert settings.base_url == "https://porkbun.com/api/json/v3"

    def test_validate_base_url_strips_trailing_slash(self) -> None:
        settings = PorkbunDNSSettings(
            base_url="https://example.test/api/",
            api_key="",
            secret_key="",
        )
        assert settings.base_url == "https://example.test/api"

    def test_auth_payload(self) -> None:
        settings = PorkbunDNSSettings(api_key="pk1", secret_key="sk1")
        assert settings.auth_payload() == {
            "apikey": "pk1",
            "secretapikey": "sk1",
        }

    def test_http_client_config_shape(self) -> None:
        settings = PorkbunDNSSettings(api_key="", secret_key="")
        cfg = settings.http_client_config()
        assert cfg["base_url"] == "https://porkbun.com/api/json/v3"
        assert float(cfg["timeout"].read) == 30.0
        assert cfg["headers"]["Content-Type"] == "application/json"
        assert cfg["headers"]["Accept"] == "application/json"

    def test_get_logging_config(self) -> None:
        settings = PorkbunDNSSettings(api_key="", secret_key="")
        log_cfg = settings.get_logging_config()
        assert log_cfg["level"] == "INFO"
        assert log_cfg["emit_json"] is True
        assert log_cfg["service_name"] == "porkbun-dns-mcp"


@pytest.mark.unit
class TestPorkbunError:
    """Cover PorkbunError exception helpers."""

    def test_to_dict_without_details(self) -> None:
        err = PorkbunError(message="boom", status=500)
        assert err.to_dict() == {"error": "boom", "status": 500}

    def test_to_dict_with_details(self) -> None:
        err = PorkbunError(
            message="boom",
            status=400,
            details={"field": "name"},
        )
        assert err.to_dict() == {
            "error": "boom",
            "status": 400,
            "details": {"field": "name"},
        }

    def test_to_dict_none_status(self) -> None:
        err = PorkbunError(message="oops")
        assert err.to_dict() == {"error": "oops", "status": None}


@pytest.mark.unit
class TestDNSRecordNormalizeName:
    """Cover DNSRecord.normalize_name validator."""

    def test_normalize_empty_name_becomes_root(self) -> None:
        rec = DNSRecord(id="1", name="", type=DNSRecordType.A, content="1.2.3.4")
        assert rec.name == "@"

    def test_subdomain_preserved(self) -> None:
        rec = DNSRecord(
            id="2", name="www", type=DNSRecordType.A, content="1.2.3.4"
        )
        assert rec.name == "www"


@pytest.mark.unit
class TestPorkbunResponseSuccess:
    """Cover PorkbunResponse.success property."""

    def test_success_uppercase(self) -> None:
        from porkbun_dns_mcp.models import PorkbunResponse

        resp = PorkbunResponse(status="SUCCESS")
        assert resp.success is True

    def test_success_lowercase(self) -> None:
        from porkbun_dns_mcp.models import PorkbunResponse

        resp = PorkbunResponse(status="success")
        assert resp.success is True

    def test_error_status(self) -> None:
        from porkbun_dns_mcp.models import PorkbunResponse

        resp = PorkbunResponse(status="ERROR", message="nope")
        assert resp.success is False


@pytest.mark.unit
class TestDNSRecordCreate:
    """Cover DNSRecordCreate model with type alias."""

    def test_record_type_via_alias(self) -> None:
        rec = DNSRecordCreate(
            domain="example.com",
            **{"type": "A"},
            name="www",
            content="1.2.3.4",
        )
        assert rec.record_type == DNSRecordType.A

    def test_default_name(self) -> None:
        rec = DNSRecordCreate(
            domain="example.com",
            **{"type": "A"},
            content="1.2.3.4",
        )
        assert rec.name == ""

    def test_default_ttl(self) -> None:
        rec = DNSRecordCreate(
            domain="example.com",
            **{"type": "A"},
            name="www",
            content="1.2.3.4",
        )
        assert rec.ttl == 600


@pytest.mark.unit
class TestToolResponse:
    """Cover ToolResponse model used by dns_tools."""

    def test_minimal(self) -> None:
        resp = ToolResponse(success=True, message="ok")
        assert resp.success is True
        assert resp.message == "ok"
        assert resp.data is None
        assert resp.error is None
        assert resp.next_steps is None

    def test_with_all_fields(self) -> None:
        resp = ToolResponse(
            success=False,
            message="oops",
            data={"k": "v"},
            error="boom",
            next_steps=["retry"],
        )
        assert resp.data == {"k": "v"}
        assert resp.error == "boom"
        assert resp.next_steps == ["retry"]


@pytest.mark.unit
class TestRecordToDict:
    """Cover _record_to_dict helper."""

    def test_includes_all_record_fields(self) -> None:
        rec = DNSRecord(
            id="42",
            name="www",
            type=DNSRecordType.A,
            content="1.2.3.4",
            ttl=300,
            priority=None,
            notes=None,
        )
        out = _record_to_dict(rec)
        assert out == {
            "id": "42",
            "name": "www",
            "type": "A",
            "content": "1.2.3.4",
            "ttl": 300,
            "priority": None,
            "notes": None,
        }


@pytest.mark.unit
class TestCliPorkbunDNSSettings:
    """Cover the CLI-side PorkbunDNSSettings and health_probe_handler."""

    def test_cli_settings_defaults(self) -> None:
        from porkbun_dns_mcp.cli import PorkbunDNSSettings

        s = PorkbunDNSSettings()
        assert s.server_name == "porkbun-dns-mcp"
        assert s.http_port == 3042
        assert s.startup_timeout == 10
        assert s.shutdown_timeout == 10
        assert s.force_kill_timeout == 5

    def test_health_probe_handler_without_credentials(self) -> None:
        from porkbun_dns_mcp.cli import health_probe_handler

        fake_settings = PorkbunDNSSettings(api_key="", secret_key="")
        with patch("porkbun_dns_mcp.config.get_settings", return_value=fake_settings):
            snapshot = health_probe_handler()

        assert snapshot.lifecycle_state["server_name"] == "porkbun-dns-mcp"
        assert snapshot.lifecycle_state["status"] == "healthy"
        assert snapshot.activity_state["credentials_configured"] is False

    def test_health_probe_handler_with_credentials(self) -> None:
        from porkbun_dns_mcp.cli import health_probe_handler

        fake_settings = PorkbunDNSSettings(api_key="pk1", secret_key="sk1")
        with patch("porkbun_dns_mcp.config.get_settings", return_value=fake_settings):
            snapshot = health_probe_handler()

        assert snapshot.activity_state["credentials_configured"] is True
        assert snapshot.activity_state["api_url"] == "https://porkbun.com/api/json/v3"


@pytest.mark.unit
class TestPorkbunClientLifecycle:
    """Cover PorkbunClient constructor and async context manager."""

    def test_init_uses_supplied_settings(self) -> None:
        from porkbun_dns_mcp.client import PorkbunClient

        fake = PorkbunDNSSettings(api_key="pk", secret_key="sk")
        client = PorkbunClient(settings=fake)
        assert client.settings is fake
        assert client._client is None

    def test_init_falls_back_to_get_settings(self) -> None:
        from porkbun_dns_mcp.client import PorkbunClient

        fake = PorkbunDNSSettings(api_key="pk", secret_key="sk")
        with patch("porkbun_dns_mcp.client.get_settings", return_value=fake):
            client = PorkbunClient()
        assert client.settings is fake

    @pytest.mark.asyncio
    async def test_async_context_manager_creates_and_closes_client(self) -> None:
        from porkbun_dns_mcp.client import PorkbunClient

        fake = PorkbunDNSSettings(api_key="pk", secret_key="sk")
        async with PorkbunClient(settings=fake) as client:
            inner = client._client
            assert inner is not None
        assert client._client is None

    @pytest.mark.asyncio
    async def test_close_idempotent_when_never_opened(self) -> None:
        from porkbun_dns_mcp.client import PorkbunClient

        fake = PorkbunDNSSettings(api_key="pk", secret_key="sk")
        client = PorkbunClient(settings=fake)
        await client.close()
        assert client._client is None
