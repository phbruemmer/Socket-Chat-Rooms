import socket
import struct
import threading
import time

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
BROADCAST_PORT = 5555
PORT = 5000
BUFFER = 1024

CLIENTS = []

SEND_BROADCAST_EVENT = threading.Event()
TCP_CONNECTION_EVENT = threading.Event()
WAIT_FOR_CONNECTION_EVENT = threading.Event()
LISTEN_FOR_CMD = threading.Event()


def broadcast_beacon():
    """
    - sends the Port of the Lobby server to everyone listening on BROADCAST_PORT.
    :return:
    """
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
            sock.sendto(struct.pack('!I', PORT), ('<broadcast>', BROADCAST_PORT))
                                        # ! - specifies network byte order
                                        # I - specifies an unsigned int (4 bytes)
            print(f"\n[broadcast] Broadcast message sent: {msg}")
            time.sleep(5)
    except Exception as e:
        print(f"[ERROR] Broadcast error: {e}")
    except KeyboardInterrupt:
        print(f"[info] stopping...")
    finally:
        SEND_BROADCAST_EVENT.set()
        sock.close()


def server_lobby_cmd(conn):
    """
    - function to handle new client.
    :param conn:
    :return:
    """
    while True:
        data_ = conn.recv(BUFFER).decode()
        if not data_:
            break
        print(data_)


def server_main_lobby():
    """
    - accepts TCP connections and starts new thread to handle new client.
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(20)
        print(f"[TCP] listening for connections on {HOST}:{PORT}")
        try:
            while not TCP_CONNECTION_EVENT.is_set():
                conn, addr = sock.accept()
                print(f"[info] connection from {addr}")
                CLIENTS.append(conn)
                server_lobby_thread = threading.Thread(target=server_lobby_cmd, args=(conn,))
                server_lobby_thread.start()
        except socket.timeout:
            print("[info] socket timeout.")
        except Exception as e:
            print(f"[ERROR] connection handling error: {e}")
        finally:
            TCP_CONNECTION_EVENT.set()
            sock.close()
            print("[info] server socket closed.")


def server_main():
    """
    main-routine:
        - broadcast thread is always running.
        - server_main_lobby handles own threads for the clients
    :return:
    """
    broadcast_thread = threading.Thread(target=broadcast_beacon)
    broadcast_thread.start()
    server_main_lobby()


if __name__ == "__main__":
    server_main()






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

