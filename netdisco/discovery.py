"""Combine all the different protocols into a simple interface."""
from __future__ import print_function
import logging
import os
import importlib
import threading

from .ssdp import SSDP
from .mdns import MDNS
from .gdm import GDM
from .lms import LMS
from .tellstick import Tellstick
from .flux_led import FluxLed
from .daikin import Daikin
# from .samsungac import SamsungAC
from .philips_hue_nupnp import PHueNUPnPDiscovery

_LOGGER = logging.getLogger(__name__)


class NetworkDiscovery(object):
    """Scan the network for devices.

    mDNS scans in a background thread.
    SSDP scans in the foreground.
    GDM scans in the foreground.
    LMS scans in the foreground.
    Tellstick scans in the foreground

    start: is ready to scan
    scan: scan the network
    discover: parse scanned data
    get_in
    """

    # pylint: disable=too-many-instance-attributes
    def __init__(self, limit_discovery=None):
        """Initialize the discovery."""
        self.limit_discovery = limit_discovery

        self.discoverables = {}
        self.scanners = []
        self.protocols = {}

        self._load_device_support()

        unique_scanners = {discoverable.get_scanner() for discoverable in self.discoverables.values()}

        for scanner in unique_scanners:
            self.scanners.append(scanner)

        self.is_discovering = False

    def get_protocol(self, protocol_type, protocol_class):
        if not self.protocols[protocol_type]:
            self.protocols[protocol_type] = protocol_class()
        return self.protocols[protocol_type]

    def scan(self):
        """Start and tells scanners to scan."""
        if not self.is_discovering:
            # Start all discovery processes in parallel
            for scanner in self.scanners:
                scanner.start()
            self.is_discovering = True

        # Wait for all foreground discovery processes to complete
        for scanner in self.scanners:
            scanner.join()

    def stop(self):
        """Turn discovery off."""
        if not self.is_discovering:
            return

        # Stop all background scanners
        for scanner in self.scanners:
            scanner.stop()

        self.is_discovering = False

    def discover(self):
        """Return a list of discovered devices and services."""
        self._check_enabled()

        return [dis for dis, checker in self.discoverables.items()
                if checker.is_discovered()]

    def get_info(self, dis):
        """Get a list with the most important info about discovered type."""
        return self.discoverables[dis].get_info()

    def get_entries(self, dis):
        """Get a list with all info about a discovered type."""
        return self.discoverables[dis].get_entries()

    def _check_enabled(self):
        """Raise RuntimeError if discovery is disabled."""
        if not self.is_discovering:
            raise RuntimeError("NetworkDiscovery is disabled")

    def _load_device_support(self):
        """Load the devices and services that can be discovered."""
        self.discoverables = {}

        discoverables_format = __name__.rsplit('.', 1)[0] + '.discoverables.{}'

        for module_name in os.listdir(os.path.join(os.path.dirname(__file__),
                                                   'discoverables')):
            if module_name[-3:] != '.py' or module_name == '__init__.py':
                continue

            module_name = module_name[:-3]

            if self.limit_discovery is not None and \
               module_name not in self.limit_discovery:
                continue

            module = importlib.import_module(
                discoverables_format.format(module_name))

            self.discoverables[module_name] = module.Discoverable(self)

    def print_raw_data(self):
        """Helper method to show what is discovered in your network."""
        from pprint import pprint

        print("Zeroconf")
        pprint(self.mdns.entries)
        print("")
        print("SSDP")
        pprint(self.ssdp.entries)
        print("")
        print("GDM")
        pprint(self.gdm.entries)
        print("")
        print("LMS")
        pprint(self.lms.entries)
        print("")
        print("Tellstick")
        pprint(self.tellstick.entries)
        print("")
        print("Fluxled")
        pprint(self.fluxled.entries)
        print("Philips Hue N-UPnP")
        pprint(self.phue.entries)
