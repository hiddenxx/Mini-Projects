import socket
import struct

class Ethernet:

    def __init__(self, raw_data):

        dest, src, prototype = struct.unpack('! 6s 6s H', raw_data[:14])

        self.dest_mac = get_mac_addr(dest)
        self.src_mac = get_mac_addr(src)
        self.proto = socket.htons(prototype)
        self.data = raw_data[14:]

def get_mac_addr(mac_raw):
    bytes_str = map('{:02x}'.format,mac_raw)
    return ':'.join(bytes_str).upper()
