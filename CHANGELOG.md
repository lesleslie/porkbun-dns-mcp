# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
