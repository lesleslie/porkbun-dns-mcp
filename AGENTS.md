# Repository Guidelines

## Project Structure & Module Organization

- `porkbun_dns_mcp/` contains the server package, API client logic, tool implementations, and schema helpers.
- `docs/` and root docs should hold operator-facing guidance; `tests/` should mirror the package structure for DNS record and domain workflow coverage.
- Generated artifacts such as `dist/` and coverage output should not be edited manually.

## Build, Test, and Development Commands

- `uv sync --group dev` installs development dependencies.
- Use the repo's documented local server commands for smoke tests.
- `uv run pytest` runs the test suite.
- `uv run ruff check porkbun_dns_mcp tests` and `uv run ruff format porkbun_dns_mcp tests` cover linting and formatting.
- Run project quality checks through Crackerjack before landing changes.

## Coding Style & Naming Conventions

- Use explicit type hints, validated request models, and small tool handlers.
- Keep modules snake_case and responses predictable and structured.

## Testing Guidelines

- Add tests for record CRUD, validation, and provider error handling.
- Prefer mocked API responses over live-network tests unless the scenario explicitly needs end-to-end verification.

## Commit & Pull Request Guidelines

- Use focused commits such as `fix(records): normalize TXT value quoting`.
- PRs should describe affected tools, commands run, and any API behavior changes.

## Security & Configuration Tips

- Never commit Porkbun credentials.
- Scrub domains, tokens, and sensitive record data from logs or examples.
