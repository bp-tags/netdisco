"""Discover Daikin devices."""
from . import BaseDiscoverable
from . import ForegroundScanner
from ..daikin import Daikin

class Discoverable(BaseDiscoverable):
    """Add support for discovering a Daikin device."""

    def __init__(self, netdis):
        """Initialize the Daikin discovery."""
        self._netdis = netdis

    def get_entries(self):
        """Get all the Daikin details."""
        return self._netdis.daikin.entries

    def get_scanner(self):
        return ForegroundScanner(Daikin())
