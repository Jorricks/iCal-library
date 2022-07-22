"""
The ICal reader module provides easy access to iCalenders with full support for recurring events,
following the RFC 5545 <https://www.ietf.org/rfc/rfc5545.txt>, available in Python.
"""
__version__ = "0.0.1a0"

from ical_library.cache_client import CacheClient
from ical_library.exceptions import *
