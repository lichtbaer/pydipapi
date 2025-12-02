# Utility package for pydipapi
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

# Re-export selected error utilities for convenience
from .error_handler import (  # noqa: F401
    DipApiConnectionError,
    DipApiError,
    DipApiHttpError,
    handle_api_error,
    handle_api_response,
    handle_async_api_error,
    is_rate_limited,
    should_retry,
    validate_api_key,
)


def redact_query_params(
    url: str, keys_to_redact: Iterable[str] = ("apikey", "api_key", "key", "token", "auth")
) -> str:
    """
    Redact sensitive query parameters in a URL for safe logging.

    Args:
        url: The input URL possibly containing sensitive query parameters.
        keys_to_redact: Iterable of query parameter keys to redact.
                      Default includes: apikey, api_key, key, token, auth.

    Returns:
        A URL string with sensitive values replaced by "***REDACTED***".
    """
    if not url:
        return url
    
    try:
        split = urlsplit(url)
        query_pairs = parse_qsl(split.query, keep_blank_values=True)
        redacted_pairs = []
        keys_to_redact_lower = {k.lower() for k in keys_to_redact}
        
        for k, v in query_pairs:
            if k.lower() in keys_to_redact_lower:
                redacted_pairs.append((k, "***REDACTED***"))
            else:
                redacted_pairs.append((k, v))
        
        redacted_query = urlencode(redacted_pairs)
        return urlunsplit(
            (split.scheme, split.netloc, split.path, redacted_query, split.fragment)
        )
    except Exception:
        # If URL parsing fails, return a safe version
        return url.split("?")[0] + "?***REDACTED***"
