import argparse
import socket
import sys

from IPy import IP

from resolver import DNSResolver

MIN_PORT = 0
MAX_PORT = 65536


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help='server port')
    parser.add_argument('-f', help='IP:Port for forwarder. Example: 8.8.8.8:53')

    args = parser.parse_args()
    port, forwarder = args.p, args.f

    if port is None and forwarder is None:
        print('Unfilled params. Check help.')
        sys.exit(0)

    if ':' in forwarder:
        forwarder = tuple(forwarder.split(':'))
    else:
        forwarder = (forwarder, 53)
    forwarder = (socket.gethostbyname(forwarder[0]), int(forwarder[1]))
    try:
        IP(forwarder[0])
    except ValueError:
        print('Invalid forwarder\'s IP')
        sys.exit()

    try:
        port = int(port)
        if port < MIN_PORT or port > MAX_PORT:
            print('Invalid port')
            sys.exit()
    except ValueError:
        print('Invalid port')
        sys.exit()

    dns_server = DNSResolver(port, forwarder)
    dns_server.run()


if __name__ == '__main__':
    try:
        main()
    except PermissionError:
        print('PermissionError: administrator rights required')
        sys.exit(0)
