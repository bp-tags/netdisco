"""Discover Logitech Media Server."""
from . import BaseDiscoverable
from . import ForegroundScanner
from ..lms import LMS

class Discoverable(BaseDiscoverable):
    """Add support for discovering Logitech Media Server."""

    def __init__(self, netdis):
        """Initialize Logitech Media Server discovery."""
        self.netdis = netdis

    def get_entries(self):
        """Get all the Logitech Media Server details."""
        return self.netdis.lms.entries

    def get_scanner(self):
        return ForegroundScanner(LMS())
