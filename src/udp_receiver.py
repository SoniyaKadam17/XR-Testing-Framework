import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9999))

print("Listening on UDP 9999...")

while True:
    data, addr = sock.recvfrom(4096)
    print(f"Received {len(data)} bytes from {addr}")