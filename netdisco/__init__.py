"""Module to scan the network using uPnP and mDNS for devices and services."""

class Scanner(object):
    def start(self):
        pass

    def join(self):
        pass

    def stop(self):
        pass


class ForegroundScanner(Scanner):
    def __init__(self, base):
        self.base = base
        self.thread = threading.Thread(target=self.base.scan)

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()


class BackgroundScanner(Scanner):
    def __init__(self, base):
        self.base = base

    def start(self):
        self.base.start()

    def stop(self):
        self.base.stop()
