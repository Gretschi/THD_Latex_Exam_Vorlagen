#!/usr/bin/env python

TEMPLATE_PKT = """\\begin{{verbatim}}\n{}\\end{{verbatim}}"""
TEMPLATE_PARTS = """
\\part[1] Handelt es sich hierbei um ein IPv4 oder ein IPv6 Paket? \\answerline[4]
\\part[1] Nach wie vielen Schritten wird dieses Paket verworfen? \\answerline[{ttl}]
\\part[3] Wie lautet der {srcdst} des Pakets?
\\begin{{solutionbox}}{{1cm}}
                {srcdstip}
\\end{{solutionbox}}
"""

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

def get_packet_str(ip_packet):
    return TEMPLATE_PKT.format(ip_packet)

def get_parts_str(ip_packet, rng):
    source = rng.random() < 0.5
    srcdst = "Absender" if source else "Empfänger"
    srcdstip = ip_packet.get_source() if source else ip_packet.get_destination()
    return(TEMPLATE_PARTS.format(
        ttl=ip_packet.ttl,
        srcdst=srcdst,
        srcdstip=srcdstip))

def print_tex(ip_packet, rng):
    print(get_packet_str(ip_packet))
    print(get_parts_str(ip_packet, rng))

def write_tex(ip_packet, rng):
    with open("IP_Header_packet.tex", "w") as packetfile:
        packetfile.write(get_packet_str(ip_packet))
    with open("IP_Header_parts.tex", "w") as partsfile:
        partsfile.write(get_parts_str(ip_packet, rng))

def generate(rng):
    packet = IPv4(rng)
    write_tex(packet, rng)
    files = ["IP_Header_packet.tex", "IP_Header_parts.tex"]
    return files

if __name__ == "__main__":
    import random
    packet = IPv4(random)
    print_tex(packet, random)
