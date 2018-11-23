from port import Port


class Line(object):
    def __init__(self):
        self.ports = []

    def delete_port(self, port):
        if port not in self.ports:
            raise RuntimeError("trying to disconnect unknown port!")

        self.ports.remove(port)
        port.is_connected = False

    def connect(self, other_port):
        if not isinstance(other_port, Port):
            raise RuntimeError("line can be connected only to ports")

        if other_port.line is not None:
            raise RuntimeError("Port must be disconnected first!")

        if other_port not in self.ports:
            self.ports.append(other_port)
            other_port.line = self
            other_port.is_connected = True

    def send(self, message, from_port):
        for port in self.ports:
            if port is from_port:
                continue

            port.handle_message(message)

    def __repr__(self):
        return "Line(connections={})".format(len(self.ports))

