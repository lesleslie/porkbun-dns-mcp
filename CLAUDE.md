# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

For a shorter, tool-neutral bootstrap document, start with `AGENTS.md`.

## Project Overview

This is an MCP (Model Context Protocol) server for managing Porkbun DNS records.

## Development Guidelines

### Code Quality

This project uses crackerjack for quality assurance. Run checks before committing:

```bash
# Run all quality checks
crackerjack check

# Run specific checks
ruff check .
ruff format --check .
pytest --cov
bandit -r porkbun_dns_mcp
```

### Testing

- Write unit tests for all core functionality
- Use pytest markers: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.network`
- Target 80%+ code coverage
- Mock external API calls (Porkbun API)

### Type Safety

- Use strict type checking (`pyright` with `typeCheckingMode = "strict"`)
- All functions must have type hints
- Run `pyright` to verify types

<!-- CRACKERJACK_START -->

## Crackerjack Integration

This project is configured with crackerjack for automated quality checks and AI-powered code analysis.

### Quality Tools

- **Ruff**: Fast Python linter and formatter (line-length 88)
- **Pytest**: Testing framework with coverage reporting (target: 80%)
- **Pyright**: Static type checker (strict mode)
- **Bandit**: Security linter for Python
- **Coverage.py**: Code coverage measurement

### Running Quality Checks

```bash
# Full quality check
crackerjack check

# Individual tools
ruff check .           # Linting
ruff format .          # Formatting
pytest --cov           # Tests with coverage
pyright                # Type checking
bandit -r porkbun_dns_mcp  # Security scan
```

### Fixing Issues Automatically

Crackerjack can automatically fix many common issues:

```bash
crackerjack fix --all
```

### Skill System Access

This project has access to Crackerjack's AI agent skill system via MCP:

- **12 Specialized Agents**: RefactoringAgent, SecurityAgent, PerformanceAgent, etc.
- **Smart Issue Matching**: Automatically finds the best agent for any code issue
- **Confidence-Based Execution**: Agents provide confidence scores for suggestions

Example usage via MCP:

```python
# List available skills
await mcp.call_tool("list_skills", {"skill_type": "all"})

# Find skills for an issue
await mcp.call_tool("get_skills_for_issue", {"issue_type": "security"})

# Execute a skill
await mcp.call_tool("execute_skill", {
    "skill_id": "skill_abc123",
    "issue_type": "security",
    "issue_data": {"message": "...", "file_path": "..."}
})
```

<!-- CRACKERJACK_END -->

### Tool Profile System

Tool registration is gated by `PORKBUN_DNS_TOOL_PROFILE`
(case-insensitive):

| Profile | Tools exposed |
|-----------|--------------------------------------------------------------------------------------------------------|
| `MINIMAL` | `health_check` (MCP) + `discover_tools` (W0 meta). HTTP `/health` + `/healthz` routes always available. |
| `STANDARD` | All 5 `porkbun-dns-mcp` tools + `health_check` + `discover_tools` (same as FULL — Tier-A trivial). |
| `FULL` | All 5 `porkbun-dns-mcp` tools + `health_check` + `discover_tools`. Default when no env var is set. |

The dispatch surface lives in `porkbun_dns_mcp/tools/profiles.py`:

- `_GROUP_REGISTRY: list[tuple[str, str]]` is the SSOT — every register
  fn has a uniform `(mcp, settings, client)` signature.
- `apply_porkbun_dns_tool_profile(server, settings, client)` is the
  async entry point consumed by `create_app`. It calls
  `_apply_tool_profile` (the async helper from `mcp-common` 0.18.0) —
  NOT the sync `apply_tool_profile` wrapper (which raises `RuntimeError`
  in event loops; the W2b.3 keystone).
- `essential_tool_names={"health_check"}` enforces the invariant at
  every profile via the W0 helper's subset check.

The caller-supplied `settings` + `client` are forwarded through every
registration path via lambda default-arg capture (the W4.1 + W4.3
reviewer fixes — silent env reload and dropped `await client.close()`
are both regression-tested in `tests/unit/test_tool_profile.py`).

See `docs/architecture/tool-profile-rationale.md` for full rationale.
