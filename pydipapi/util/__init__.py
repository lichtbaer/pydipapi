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
    is_rate_limited,
    should_retry,
    validate_api_key,
)


def redact_query_params(url: str, keys_to_redact: Iterable[str] = ("apikey",)) -> str:
    """
    Redact sensitive query parameters in a URL for safe logging.

    Args:
        url: The input URL possibly containing sensitive query parameters.
        keys_to_redact: Iterable of query parameter keys to redact.

    Returns:
        A URL string with sensitive values replaced by "***".
    """
    split = urlsplit(url)
    query_pairs = parse_qsl(split.query, keep_blank_values=True)
    redacted_pairs = []
    for k, v in query_pairs:
        if k in keys_to_redact:
            redacted_pairs.append((k, "***"))
        else:
            redacted_pairs.append((k, v))
    redacted_query = urlencode(redacted_pairs)
    return urlunsplit(
        (split.scheme, split.netloc, split.path, redacted_query, split.fragment)
    )
