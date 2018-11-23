from collections import namedtuple

from scapy.all import Ether

from port import Port
from line import Line


class Address(object):
    def __init__(self, address_bytes):
        self.address_bytes = tuple(address_bytes)

    def __repr__(self):
        return "Address({!r})".format(":".join(self.address_bytes))

    def __hash__(self):
        return hash(self.address_bytes)

    def __ne__(self, other):
        return not self == other

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False

        return self.address_bytes == other.address_bytes


class Switch(object):
    def __init__(self, addr, ports_count=4):
        self.addr = self.parse_addr(addr)
        self.ports = [Port(self, i) for i in range(ports_count)]
        self.known_addresses = {}

    @classmethod
    def parse_addr(cls, addr):
        return Address(addr.split(":"))

    def connect(self, line, port_id):
        port = self.ports[port_id]
        port.connect(line)

    def delete_known_addresses(self, port_id):
        for known_address, port in self.known_addresses.items():
            if port == port_id:
                del self.known_addresses[known_address]

    def handle_message(self, message, from_port):
        print("{!r}: new message recieved, now parsing..".format(
            self))
        eth_message = message[Ether]
        src_address = Address(eth_message.src.split(":"))
        dst_address = Address(eth_message.dst.split(":"))

        if src_address not in self.known_addresses:
            if src_address != self.addr:
                print("{!r}: added {} to known addresses at port {}".format(
                    self, src_address, from_port))
                self.known_addresses[src_address] = from_port

        if dst_address == self.addr:
            self.handle_self_message(message)
            return

        if dst_address in self.known_addresses:
            port_id = self.known_addresses[dst_address]
            if self.ports[port_id].is_connected:
                print("{!r}: found {} in known addresses sending through port {}".format(
                    self, dst_address, port_id))
                self.ports[port_id].send(message)

        else:
            # boardcast the message if dst is unknown
            print("{!r}: unknown {} broadcasting to all ports!".format(self,
                dst_address))
            message_sent = False
            for port in self.ports:
                if port.id == from_port:
                    continue
                if port.is_connected:
                    message_sent = True
                    print("{!r}: sending to {}".format(self, port))
                    port.send(message)

            if not message_sent:
                print("{!r}: packet dropped!".format(self))

    def handle_self_message(self, message):
        print("{!r}: received message to self!".format(self))

    def send_message(self, message):
        pass

    def connect_device(self, device, port_id, dest_port):
        line = Line()
        port = self.ports[port_id]
        port.connect(line)
        try:
            device.connect(line, dest_port)

        except RuntimeError:
            port.disconnect()
            raise

        return line

    def __repr__(self):
        return "Switch({!r})".format(self.addr)

