"""
Caching utilities for the DIP API client.
"""

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, Optional, cast

logger = logging.getLogger(__name__)


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

        Raises:
            OSError: If the cache directory cannot be created or accessed.
            PermissionError: If write permissions are not available.
        """
        self.cache_dir = Path(cache_dir).resolve()
        self.ttl = ttl

        # Validate and create cache directory with better error handling
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            # Test write permissions
            test_file = self.cache_dir / ".write_test"
            try:
                test_file.touch()
                test_file.unlink()
            except (OSError, PermissionError) as e:
                raise PermissionError(
                    f"Cannot write to cache directory {self.cache_dir}: {e}"
                ) from e
        except (OSError, PermissionError) as e:
            logger.error(f"Failed to initialize cache directory {cache_dir}: {e}")
            raise

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
            with open(cache_file, encoding="utf-8") as f:
                cached_data = json.load(f)

            # Validate cache data structure
            if not isinstance(cached_data, dict):
                logger.warning(f"Invalid cache file format: {cache_file}")
                cache_file.unlink()
                return None

            # Check if cache is expired
            timestamp = cached_data.get("timestamp")
            if not isinstance(timestamp, (int, float)):
                logger.warning(f"Invalid timestamp in cache file: {cache_file}")
                cache_file.unlink()
                return None

            if time.time() - timestamp > self.ttl:
                cache_file.unlink()
                return None

            data_obj = cached_data.get("data")
            if isinstance(data_obj, dict):
                return cast(Dict[str, Any], data_obj)
            return None

        except (json.JSONDecodeError, KeyError) as e:
            # Invalid cache file, remove it
            logger.warning(f"Invalid cache file {cache_file}: {e}")
            if cache_file.exists():
                try:
                    cache_file.unlink()
                except OSError:
                    pass
            return None
        except (OSError, PermissionError) as e:
            logger.warning(f"Cannot read cache file {cache_file}: {e}")
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
            # Use atomic write: write to temp file first, then rename
            temp_file = cache_file.with_suffix(".tmp")
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f)
            # Atomic rename on POSIX systems
            temp_file.replace(cache_file)
        except (OSError, PermissionError) as e:
            logger.warning(f"Failed to write cache file {cache_file}: {e}")
        except Exception as e:
            logger.warning(f"Unexpected error writing cache file {cache_file}: {e}")
            # Clean up temp file if it exists
            temp_file = cache_file.with_suffix(".tmp")
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except OSError:
                    pass

    def clear(self) -> None:
        """
        Clear all cached data.

        Raises:
            OSError: If cache files cannot be deleted.
        """
        cleared_count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
                cleared_count += 1
            except Exception as e:
                logger.warning(f"Failed to delete cache file {cache_file}: {e}")
        logger.debug(f"Cleared {cleared_count} cache files")

    def clear_expired(self) -> None:
        """
        Clear expired cache entries.
        """
        current_time = time.time()
        cleared_count = 0

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, encoding="utf-8") as f:
                    cached_data = json.load(f)

                timestamp = cached_data.get("timestamp")
                if isinstance(timestamp, (int, float)) and current_time - timestamp > self.ttl:
                    cache_file.unlink()
                    cleared_count += 1

            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Invalid cache file, remove it
                logger.warning(f"Invalid cache file {cache_file}: {e}")
                try:
                    cache_file.unlink()
                    cleared_count += 1
                except OSError:
                    pass
            except Exception as e:
                logger.warning(f"Failed to process cache file {cache_file}: {e}")

        logger.debug(f"Cleared {cleared_count} expired cache files")
