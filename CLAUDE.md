# Porkbun DNS MCP Server

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
