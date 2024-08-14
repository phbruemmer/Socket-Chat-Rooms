import socket
import struct
import threading
import re
import time

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


def get_username(sock):
    print("# # # # # # # # # # # # # # #\nE N T E R - U S E R N A M E\n")
    username = input("> > > ")
    while not re.match(r"^[A-Za-z0-9]*$", username) or re.match(r'^[\s\t\n]*$', username):
        print("[info] only english letters and numbers from 0 - 9 are allowed.")
        username = input("> > > ")
    print("[info] valid username received.\n[info] sending username for user validation...")
    sock.send(username.encode())
    print("[info] username sent.")


def connected_client(sock):
    connected = threading.Event()

    def receiver():
        print("[info] listening to server...")
        while not connected.is_set():
            data_ = sock.recv(BUFFER)
            while data_:
                print(data_)
                data_ = sock.recv(BUFFER)
    def sender():
        print("[info] chat available.")
        while not connected.is_set():
            msg_ = input("> ")
            if not len(msg_) > 32:
                continue
            print(123)
            msg_ = msg_.encode()
            sock.send(msg_)
            if msg_ == b'$exit':
                connected.set()
                return


    recv_thread = threading.Thread(target=receiver)
    send_thread = threading.Thread(target=sender)
    # recv_thread.start()
    send_thread.start()


def connect_to_lobby(addr, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((addr, port))
        get_username(sock)
        connected_client(sock)
        sock.close()


def client_main():
    addr, port = listen_for_broadcast_message()
    if addr is None:
        return
    connect_to_lobby(addr, port)


if __name__ == "__main__":
    client_main()
