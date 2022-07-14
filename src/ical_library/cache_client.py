import hashlib
import os
from pathlib import Path
from typing import Any, Union
from urllib import request

from pendulum import DateTime, Duration

from ical_library import client
from ical_library.ical_components import VCalendar


class CacheClient:
    """
    A iCalendar client which takes care of caching the result for you.
    This avoids you needing to handle the caching.

    :param cache_location: A path to the cache. Can be relative or absolute references. When you pass in a value with
    a file extension, it is considered to be a directory, otherwise it's considered as a file reference.
    :param cache_ttl: The time-to-live for the cache. The cache will be deleted/refreshed once it is older than the TTL.
    :param verbose: Print verbose messages regarding cache usage.
    :param url: The URL to the iCalendar file.
    """

    def __init__(
        self,
        url: str,
        cache_location: Union[Path, str],
        cache_ttl: Union[Duration] = Duration(hours=1),
        verbose: bool = True,
    ):
        self.url: str = url
        self.cache_location: Path = Path(cache_location)
        self.cache_ttl: Duration = cache_ttl
        self.verbose = verbose

    @property
    def cache_file_path(self) -> Path:
        """Return the filepath to the cache for the given URL."""
        if self.cache_location.suffix == "":
            return self.cache_location / hashlib.md5(self.url.encode()).hexdigest()
        return self.cache_location

    def get_icalendar(self, **kwargs: Any) -> VCalendar:
        """
        Get a parsed VCalendar instance. If there is an active cache, return that, otherwise fetch and cache the result.
        :param kwargs: Any keyword arguments to pass onto the `urllib.request.urlopen` call.
        :return: a VCalendar instance with all it's iCalendar components like VEvents, VToDos, VTimeZones etc.
        """
        if not self._is_cache_expired():
            if self.verbose:
                print("Using cache to remove this folder.")
            return client.parse_icalendar_file(self.cache_file_path)

        self._purge_icalendar_cache()
        response = request.urlopen(self.url, **kwargs)
        if not (200 <= response.getcode() < 400):
            raise ValueError(f"Unable to execute request at {self.url=}. Response code was: {response.getcode()}.")
        text = response.read().decode("utf-8")
        self._write_response_to_cache(text)

        lines = text.split("\n")
        return client.parse_lines_into_calendar(lines)

    def _write_response_to_cache(self, text: str) -> None:
        """
        Write the response of the fetched URL to cache.
        :param text: The fetched result.
        """
        if self.verbose:
            print(f"Successfully loaded new iCalendar data and stored it at {self.cache_file_path}.")
        self.cache_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file_path, "w") as file:
            file.write(text)

    def _purge_icalendar_cache(self) -> None:
        """Purge the cache we have for this Calendar."""
        if self.verbose:
            print(f"Cache was expired. Removed {self.cache_file_path}.")
        return self.cache_file_path.unlink()

    def _is_cache_expired(self) -> bool:
        """Return whether the cache is passed its expiration date."""
        cutoff = DateTime.utcnow() - self.cache_ttl
        mtime = DateTime.utcfromtimestamp(os.path.getmtime(self.cache_file_path))
        return mtime < cutoff
