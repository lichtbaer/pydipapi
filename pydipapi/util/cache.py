"""
Caching utilities for the DIP API client.
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any, Dict, Optional, cast


class SimpleCache:
    """
    A simple file-based cache for API responses.
    """

    def __init__(self, cache_dir: str = ".cache", ttl: int = 3600):
        """
        Initialize the cache.

        Args:
            cache_dir (str): Directory to store cache files.
            ttl (int): Time to live in seconds.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = ttl

    def _get_cache_key(self, url: str, params: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a cache key for the given URL and parameters.

        Args:
            url (str): The URL.
            params (Optional[Dict[str, Any]]): Query parameters.

        Returns:
            str: The cache key.
        """
        key_data = {"url": url, "params": params or {}}
        key_string = json.dumps(key_data, sort_keys=True)
        # Use SHA256 instead of MD5 for security
        return hashlib.sha256(key_string.encode()).hexdigest()

    def get(
        self, url: str, params: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get a cached response.

        Args:
            url (str): The URL.
            params (Optional[Dict[str, Any]]): Query parameters.

        Returns:
            Optional[Dict[str, Any]]: The cached response or None if not found/expired.
        """
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            with open(cache_file) as f:
                cached_data = json.load(f)

            # Check if cache is expired
            if time.time() - cached_data["timestamp"] > self.ttl:
                cache_file.unlink()
                return None

            data_obj = cached_data.get("data")
            if isinstance(data_obj, dict):
                return cast(Dict[str, Any], data_obj)
            return None

        except (json.JSONDecodeError, KeyError):
            # Invalid cache file, remove it
            if cache_file.exists():
                cache_file.unlink()
            return None

    def set(
        self, url: str, data: Dict[str, Any], params: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Cache a response.

        Args:
            url (str): The URL.
            data (Dict[str, Any]): The response data.
            params (Optional[Dict[str, Any]]): Query parameters.
        """
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"

        cache_data = {"timestamp": time.time(), "data": data}

        try:
            with open(cache_file, "w") as f:
                json.dump(cache_data, f)
        except Exception as e:
            logging.warning(f"Failed to write cache file {cache_file}: {e}")

    def clear(self) -> None:
        """
        Clear all cached data.
        """
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except Exception as e:
                logging.warning(f"Failed to delete cache file {cache_file}: {e}")

    def clear_expired(self) -> None:
        """
        Clear expired cache entries.
        """
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file) as f:
                    cached_data = json.load(f)

                if current_time - cached_data["timestamp"] > self.ttl:
                    cache_file.unlink()

            except Exception as e:
                logging.warning(f"Failed to process cache file {cache_file}: {e}")
