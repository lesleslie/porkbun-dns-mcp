# Python Coding Standards for porkbun-dns-mcp

## Type Hints

- **All functions must have type hints** for parameters and return values
- Use `from typing import ...` for complex types (Optional, List, Dict, etc.)
- Use `|` syntax for unions with Python 3.10+ (e.g., `str | None`)
- Never use `Any` without a compelling reason documented in a comment

## Docstrings

- **All public functions, classes, and modules must have docstrings**
- Use Google-style docstrings (preferred) or reStructuredText
- Document parameters, returns, and raised exceptions
- Keep docstrings concise but informative

## Error Handling

- **Never use `except Exception` or `except:` without specific exception types**
- Never suppress exceptions with `pass`
- Use specific exception types (ValueError, KeyError, custom exceptions)
- Always include error messages that explain what went wrong
- Log errors before raising if appropriate

## Async/Await

- Use `async def` for I/O-bound operations (API calls, database queries)
- Always use `await` when calling async functions
- Use `asyncio.gather()` for concurrent independent operations
- Use `async with` for async context managers

## Code Style

- Follow PEP 8 guidelines (enforced by ruff)
- Maximum line length: 88 characters
- Use f-strings for string formatting
- Use descriptive variable names (avoid single letters except for loop variables)

## Testing

- Write unit tests for all non-trivial functions
- Use descriptive test names that explain what is being tested
- Use pytest fixtures for setup/teardown
- Mock external dependencies (API calls, file I/O)
- Aim for 80%+ code coverage

## Security

- Never hardcode credentials or API keys
- Use environment variables for configuration
- Validate all user inputs
- Use HTTPS for all network requests
- Keep dependencies updated

## Examples

### Good Function with Type Hints and Docstring

```python
async def create_dns_record(
    domain: str,
    record_type: str,
    name: str,
    content: str,
    ttl: int = 300,
) -> dict[str, str]:
    """Create a new DNS record via Porkbun API.

    Args:
        domain: The domain name (e.g., "example.com")
        record_type: Record type (A, AAAA, CNAME, MX, TXT)
        name: Record name/subdomain
        content: Record content/value
        ttl: Time to live in seconds (default: 300)

    Returns:
        dict with API response including record ID

    Raises:
        ValueError: If record_type is invalid
        ConnectionError: If API request fails
    """
    if record_type not in {"A", "AAAA", "CNAME", "MX", "TXT"}:
        raise ValueError(f"Invalid record type: {record_type}")

    # API call implementation...
```

### Bad Examples (What to Avoid)

```python
# NO: Missing type hints
def create_record(domain, name, content):
    pass

# NO: Bare except
try:
    api_call()
except:
    pass

# NO: Vague error message
if not domain:
    raise ValueError("Invalid")

# NO: Using Any
from typing import Any
def process(data: Any) -> Any:
    return data
```
