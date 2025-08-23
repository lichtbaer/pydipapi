"""
Shared pagination helpers for DIP API clients.
"""

from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


def fetch_paginated_sync(
    build_url: Callable[..., str],
    make_request: Callable[[str], Optional[Dict[str, Any]]],
    endpoint: str,
    count: int,
    **params: Any,
) -> List[Dict[str, Any]]:
    """
    Fetch paginated data synchronously using provided URL builder and request function.

    Args:
        build_url: Callable to build endpoint URLs.
        make_request: Callable to perform the HTTP request and return JSON data.
        endpoint: API endpoint name.
        count: Number of items to fetch.
        **params: Additional query parameters.

    Returns:
        A list of document dictionaries.
    """
    logger.debug(
        f"[sync] Fetching paginated data from endpoint: {endpoint}, count: {count}, params: {params}"
    )
    documents: List[Dict[str, Any]] = []
    cursor: str = ""

    while len(documents) < count:
        # Add cursor to parameters if we have one
        if cursor:
            params["cursor"] = cursor

        url = build_url(endpoint, **params)
        logger.debug(f"[sync] Making request to URL: {url}")

        data = make_request(url)
        if data is None:
            logger.error("[sync] No response received from make_request")
            break

        logger.debug(f"[sync] Response data type: {type(data)}")
        logger.debug(
            f"[sync] Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}"
        )

        if not data:
            logger.warning("[sync] Empty response data")
            break

        new_documents = data.get("documents", []) if isinstance(data, dict) else []
        logger.debug(f"[sync] Retrieved {len(new_documents)} new documents")
        documents.extend(new_documents)

        # Update cursor for next page
        cursor = data.get("cursor", "") if isinstance(data, dict) else ""
        logger.debug(f"[sync] Next cursor: {cursor}")

        # If no more documents or no cursor, break
        if not new_documents or not cursor:
            logger.debug("[sync] No more documents or no cursor, stopping pagination")
            break

    logger.info(f"[sync] Total documents retrieved: {len(documents)}")
    return documents[:count]


async def fetch_paginated_async(
    build_url: Callable[..., str],
    make_request_async: Callable[[str], Awaitable[Optional[Dict[str, Any]]]],
    endpoint: str,
    count: int,
    **params: Any,
) -> List[Dict[str, Any]]:
    """
    Fetch paginated data asynchronously using provided URL builder and request coroutine.

    Args:
        build_url: Callable to build endpoint URLs.
        make_request_async: Coroutine to perform the HTTP request and return JSON data.
        endpoint: API endpoint name.
        count: Number of items to fetch.
        **params: Additional query parameters.

    Returns:
        A list of document dictionaries.
    """
    logger.debug(
        f"[async] Fetching paginated data from endpoint: {endpoint}, count: {count}, params: {params}"
    )
    documents: List[Dict[str, Any]] = []
    cursor: str = ""

    while len(documents) < count:
        # Add cursor to parameters if we have one
        if cursor:
            params["cursor"] = cursor

        url = build_url(endpoint, **params)
        logger.debug(f"[async] Making request to URL: {url}")

        data = await make_request_async(url)
        if data is None:
            logger.error("[async] No response received from make_request_async")
            break

        logger.debug(f"[async] Response data type: {type(data)}")
        logger.debug(
            f"[async] Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Not a dict'}"
        )

        if not data:
            logger.warning("[async] Empty response data")
            break

        new_documents = data.get("documents", []) if isinstance(data, dict) else []
        logger.debug(f"[async] Retrieved {len(new_documents)} new documents")
        documents.extend(new_documents)

        # Update cursor for next page
        cursor = data.get("cursor", "") if isinstance(data, dict) else ""
        logger.debug(f"[async] Next cursor: {cursor}")

        # If no more documents or no cursor, break
        if not new_documents or not cursor:
            logger.debug("[async] No more documents or no cursor, stopping pagination")
            break

    logger.info(f"[async] Total documents retrieved: {len(documents)}")
    return documents[:count]
