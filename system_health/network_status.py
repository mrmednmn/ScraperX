import sys
sys.dont_write_bytecode = True
from socket import create_connection

class NetworkStatusChecker:
    def __init__(self):
        self.ip="8.8.8.8"
        self.port=53
        self.timeout=0.5

    def can_connect(self):
        try:
            #Try to connect to Google's DNS server
            create_connection((self.ip, self.port), timeout=self.timeout)
            return True
        except OSError:
            return False