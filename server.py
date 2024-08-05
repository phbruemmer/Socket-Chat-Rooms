import socket
import threading
import time

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 5000
BUFFER = 1024

CLIENTS = []

SEND_BROADCAST_EVENT = threading.Event()
TCP_CONNECTION_EVENT = threading.Event()
WAIT_FOR_CONNECTION_EVENT = threading.Event()


def broadcast_beacon():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # Address Family, UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)   # True -> Activates message broadcast ability
    """
    setsockopt = method to set the value of a socket option
    SOL_SOCKET = refers to socket-level options
    SO_BROADCAST = enables or disables the ability to send broadcast messages on the socket.
    """
    msg = "Server Beacon"

    try:
        while not SEND_BROADCAST_EVENT.is_set():
            sock.sendto(msg.encode(), ('<broadcast>', PORT))
            print(f"[broadcast] Broadcast message sent: {msg}")
            time.sleep(5)
    except Exception as e:
        print(f"[ERROR] Broadcast error: {e}")
    except KeyboardInterrupt:
        print(f"[info] stopping...")
    finally:
        SEND_BROADCAST_EVENT.set()
        sock.close()


def server_main_lobby():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(20)
    print(f"[TCP] listening for connections on {HOST}:{PORT}")
    try:
        while not TCP_CONNECTION_EVENT.is_set():
            sock.settimeout(1)
            try:
                conn, addr = sock.accept()
                print(f"[info] connection from {addr}")
                CLIENTS.append(conn)
            except socket.timeout:
                continue
    except Exception as e:
        print(f"[ERROR] connection handling error: {e}")
    finally:
        TCP_CONNECTION_EVENT.set()
        sock.close()
        print("[info] server socket closed.")


def server_main():
    broadcast_thread = threading.Thread(target=broadcast_beacon)
    broadcast_thread.start()
    while True:
        lobby_thread = threading.Thread(target=server_main_lobby)
        lobby_thread.start()
        WAIT_FOR_CONNECTION_EVENT.wait()
        WAIT_FOR_CONNECTION_EVENT.clear()


if __name__ == "__main__":
    broadcast_beacon()

"""
# # # SERVER - STRUCTURE # # #

-> Send Broadcast Beacon
-> Client gets IP and connects with TCP to the server...
-> TCP connection established
-> "Lobby" - available commands: 
                -> list_chats
                -> join {ip/name} [username]
                -> create [room] 
                    room: [name] [encryption_type] [allowed user number] [only chat / only voice / both] [open/closed]
                        -> encryption_type:
                            - encryption with own key
                            - encryption based on own script
                            - open-encryption (saved on server)
-> "room" - available commands:
                -> !leave
                -> !ban (only admins)
                -> !kick (only admins)
                -> !add_admin [name] (only admins)
                -> !rm_admin [name] (only admins) [OWNER EXCLUDED]
                -> !mute
                -> !unmute
                -> !deaf -> [name] (only admins)
                -> !terminate
"""

