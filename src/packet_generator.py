import socket


class PacketGenerator:

    def __init__(
        self,
        host="127.0.0.1",
        port=9999
    ):

        self.host = host
        self.port = port

        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

    def send_packet(
        self,
        payload
    ):

        self.socket.sendto(
            payload,
            (self.host, self.port)
        )