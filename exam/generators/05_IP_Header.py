#!/usr/bin/env python

FILES = ["05_IP_Header.tex"]

class IPv4:
    def __init__(self, rng):
        self.version = 4
        self.ihl = 5
        self.dscp_ecn = 0
        self.length = rng.randint(20,65535)
        self.identification = (rng.getrandbits(16) & 0xFFFF)
        self.flags_and_offset = (rng.getrandbits(15) & 0xFFFF)
        self.ttl = rng.randint(0,255)
        self.protocol = rng.randint(0,143)
        self.checksum = (rng.getrandbits(16) & 0xFFFF)
        self.source = (rng.getrandbits(32) & 0xFFFFFFFF)
        self.destination = (rng.getrandbits(32) & 0xFFFFFFFF)

    def __str__(self):
        lines = "{:02X} {:02X} {:02X} {:02X}\n"*5
        return lines.format(
            self.version*16 + self.ihl, self.dscp_ecn,
            *self.length.to_bytes(2, 'big'),
            *self.identification.to_bytes(2, 'big'),
            *self.flags_and_offset.to_bytes(2, 'big'),
            self.ttl,
            self.protocol,
            *self.checksum.to_bytes(2, 'big'),
            *self.source.to_bytes(4, 'big'),
            *self.destination.to_bytes(4, 'big')
            )

    def get_source(self):
        return self.dotted_decimal(self.source)

    def get_destination(self):
        return self.dotted_decimal(self.destination)

    def dotted_decimal(self, address):
        return "{:d}.{:d}.{:d}.{:d}".format(*address.to_bytes(4, 'big'))

def get_context(rng):
    ctx = {}
    packet = IPv4(rng)
    ctx["packet"] = packet
    source = rng.random() < 0.5
    ctx["srcdst"] = "Absender" if source else "Empfänger"
    ctx["srcdstip"] = packet.get_source() if source else packet.get_destination()
    return ctx
