class Port(object):
    def __init__(self, device, port_id):
        self.device = device
        self.line = None
        self.id = port_id
        self.is_connected = False

    def disconnect(self):
        if self.line is None:
            raise RuntimeError("Port is not connected to any line")

        self.device.delete_known_addresses(self.id)
        self.line.delete_port(self)
        self.line = None
        self.is_connected = False

    def connect(self, line):
        if self.line is not None:
            raise RuntimeError("dest ports must be disconnected first!")

        line.connect(self)
        self.is_connected = True

    def __repr__(self):
        return "Port(id={}, device={!r}, line={!r})".format(
            self.id, self.device, self.line)

    def send(self, message):
        self.line.send(message, self)

    def handle_message(self, message):
        self.device.handle_message(message, self.id)

