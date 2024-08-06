import socket
import struct

BROADCAST_PORT = 5555
TIMEOUTS = 10
BUFFER = 1024


def listen_for_broadcast_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Address Family, UDP
    sock.bind(('', BROADCAST_PORT))
    sock.settimeout(TIMEOUTS)

    listening = True
    addr = None
    PORT = None

    try:
        while listening:
            print(f"[info] Listening for beacons on port {BROADCAST_PORT}...")
            try:
                PORT, addr = sock.recvfrom(BUFFER)  # receives IP and PORT for the Lobby server.
                PORT = struct.unpack('!I', PORT)[0]
                print(f"[info] data received from {addr}: {PORT}")
                print("[info] trying to connect...")
                listening = False
            except socket.timeout:
                listening = False
                print("[info] listening timed out.")
            finally:
                sock.close()
    finally:
        sock.close()
    return (addr[0], PORT) if addr or PORT else None


def connect_to_lobby(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((addr, port))
        sock.send(b'Test')
        sock.close()


def client_main():
    addr, port = listen_for_broadcast_message()
    if addr is None:
        return
    connect_to_lobby(addr, port)


if __name__ == "__main__":
    client_main()
