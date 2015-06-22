# Use those functions to enumerate all interfaces available on the system using Python.
# found on <http://code.activestate.com/recipes/439093/#c1>
# Thanks to Philipp Klaus - https://gist.github.com/pklaus

# Remove this - Only to run tests on Windows
import sys
if sys.platform.startswith('linux'):
    import fcntl

import socket
import struct
import array
import subprocess

class Sysnet:

    def all_interfaces(self):
        max_possible = 128
        bytes = max_possible * 32
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        names = array.array('B', '\0' * bytes)
        outbytes = struct.unpack('iL', fcntl.ioctl(
            s.fileno(),
            0x8912,  # SIOCGIFCONF
            struct.pack('iL', bytes, names.buffer_info()[0])
        ))[0]
        namestr = names.tostring()
        lst = []
        for i in range(0, outbytes, 40):
            name = namestr[i:i+16].split('\0', 1)[0]
            ip   = namestr[i+20:i+24]
            lst.append((name, ip))
        return lst

    def format_ip(self, addr):
        return str(ord(addr[0])) + '.' + \
               str(ord(addr[1])) + '.' + \
               str(ord(addr[2])) + '.' + \
               str(ord(addr[3]))

    def allInterfaces(self):
        all_int = []
        if sys.platform.startswith('linux'):
            ifs = self.all_interfaces()
        else:
            ifs = (('io','1.0.0.127'),('eth0','1.0.0.10'), ('eth0','11.34.23.10'))
        for i in ifs:
            all_int.append((i[0],self.format_ip(i[1])))
            print "%12s   %s" % (i[0], self.format_ip(i[1]))

        return all_int

    @staticmethod
    def listRoutes():
        routes = subprocess.check_output(["netstat", "-rn"])
        return routes

    @staticmethod
    def listInterfaces(self):
        interfaces = subprocess.check_output(["ifconfig", "-a"])
        return interfaces

    @staticmethod
    def listConnections():
        connections = subprocess.check_output(["netstat", "-an"])
        return connections

    @staticmethod
    def listProcesses():
        processes = subprocess.check_output(["top", "-n 1"])
        return processes