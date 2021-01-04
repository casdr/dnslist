#!/usr/bin/env python3
# by casdr
# Requires the netaddr and pythondns pip packages

import netaddr
import dns.resolver
import sys

class DNSListParser():
    host = ""
    record = ""
    ip4 = []
    ip6 = []

    def __init__(self, host):
        self.host = host
        result = dns.resolver.resolve(host, "TXT")
        for record in result:
            string = ""
            for part in record.strings:
                string += "%s " % (part.decode('utf-8'))
            self.parse(string)
        self.ip4 = list(set(self.ip4))
        self.ip6 = list(set(self.ip6))

    def parse_all(self, value):
        self.ip4.append("0.0.0.0/0")
        self.ip6.append("::/0")

    def parse_ip4(self, value):
        self.ip4.append(value)

    def parse_ip6(self, value):
        self.ip6.append(value)

    def parse_include(self, value):
        result = self.__init__(value)

    def parse_a(self, value):
        if not value:
            value = self.host
        result = dns.resolver.resolve(value, "A")
        for record in result:
            self.ip4.append(record.address)

    def parse_aaaa(self, value):
        if not value:
            value = self.host
        result = dns.resolver.resolve(value, "AAAA")
        for record in result:
            self.ip6.append(record.address)

    def parse(self, record):
        splitted = record.split()
        if splitted[0] != "v=dnslist1":
            return
        for piece in splitted:
            self.parse_piece(piece)

    def parse_piece(self, piece):
        piece = piece.split(":", 1)
        name = piece[0]
        value = ""
        if len(piece) > 1:
            value = piece[1]

        types = {
            "all": self.parse_all,
            "ip4": self.parse_ip4,
            "ip6": self.parse_ip6,
            "include": self.parse_include,
            "a": self.parse_a,
            "aaaa": self.parse_aaaa,
        }
        handler = types.get(name, "none")
        if handler == "none":
            return
        handler(value)

if __name__ == "__main__": 
    parser = DNSListParser(sys.argv[1])
    print("\n".join(parser.ip4))
    print("\n".join(parser.ip6))

