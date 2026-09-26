# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.4] - 2026-09-26

### Documentation

- Add docs/assets/images/ + .scratch/ convention
- CLAUDE.md: Cross-reference MCP backend wiring discipline (Bodai-wide)
- Consolidate Bodai/Vishnu references to bottom section
- Drop Bodai integration framing and add substrate note
- Update FastMCP badge URL to PrefectHQ org (canonical since v3.0 GA)

### Internal

- deps: Bump mcp-common floor to >=0.26.0,<0.27.0 (Phase 2.5)
- gitignore: Apply Bodai canonical snippet
- plugin: Rebadge from Bodai + update install instructions
- porkbun-dns-mcp: Refresh uv.lock for mcp-common 0.30.1

## [0.4.3] - 2026-08-31

### Testing

- Add coverage for config/models/CLI helpers and pragma CLI bootstrap
- Pragma HTTP-integration methods to reach 80% coverage

## [0.4.0] - 2026-08-28

### Documentation

- readme: Bump Python badge from 3.13+ to 3.14+

### Internal

- Bump requires-python to >=3.14
- Bump version to 0.3.0
- Bump version to 0.3.0
- porkbun-dns-mcp: Bump tool-config pins from 3.13 to 3.14
- Re-pin python to 3.14

## [0.3.0] - 2026-08-20

### Added

- porkbun-dns-mcp: Adopt apply_tool_profile() from mcp-common 0.18.0
- porkbun-dns: Bodai plugin conversion (manifest, mcp.json, slash commands)

### Fixed

- porkbun-dns-mcp: Shorten E501 line in test_schema_validation.py

### Internal

- gitignore: Untrack .pyscn/ (bodai 2026-08-20)
- porkbun-dns-mcp: Add [tool.creosote] to skip self-tool scan
- porkbun-dns-mcp: Bootstrap [tool.crackerjack] section + uv sync upgrade
- porkbun-dns-mcp: Gitignore .lycheecache (file, not just dir)
- porkbun-dns-mcp: Gitignore .lycheecache + .hypothesis
- porkbun-dns-mcp: Refresh oneiric + mcp-common deps
- porkbun-dns-mcp: Untrack .lycheecache + .hypothesis runtime artifacts

## [0.2.1] - 2026-08-17

### Documentation

- Fix version drift, tool/HTTP surface labels, missing env var, stale serve docstring

### Internal

- Untrack backup files (.backup, .backup.json, .bak)

## [0.2.0] - 2026-08-12

### Fixed

- Address ty errors

### Internal

- Adopt register_http_health_route from mcp-common
- Bump oneiric dep to >=0.16.0
- Migrate MCPBaseSettings → OneiricMCPConfig, bump fastmcp to >=3.4.0,\<4
- Restore LICENSE and normalize attribution
- Skip template test awaiting future models

## [0.1.4] - 2026-06-20

### Fixed

- Track .cache dir via .gitkeep for gitleaks support

### Internal

- Add mypy.ini and track .cache dir for quality tooling
- Untrack and delete 1 historical *.backup/*.bak files

## [0.1.3] - 2026-05-10

### Changed

- Update configuration
- Update configuration

### Internal

- Bump version to 0.1.2

## [0.1.2] - 2026-02-25

### Added

- Complete Porkbun DNS MCP server implementation

### Changed

- Update configuration

### Internal

- Update LICENSE copyright to 2026
