import socket
import threading
import time

PORT = 5000
TIMEOUTS = 10
BUFFER = 1024


def listen_for_broadcast_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Address Family, UDP
    sock.bind(('', PORT))
    sock.settimeout(TIMEOUTS)

    listening = True
    addr = None

    try:
        while listening:
            print(f"[info] Listening for beacons on port {PORT}...")
            try:
                data, addr = sock.recvfrom(BUFFER)
                print(f"[info] data received from {addr}: {data.decode()}")
                print("[info] trying to connect...")
            except socket.timeout:
                listening = False
                print("[info] listening timed out.")
            finally:
                sock.close()
    finally:
        sock.close()
    return addr[0] if addr else None


def connect_to_lobby(addr):
    pass


def client_main():
    addr = listen_for_broadcast_message()
    if addr is None:
        return
    connect_to_lobby(addr)


if __name__ == "__main__":
    client_main()
