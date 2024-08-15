import random
import socket
import struct
import threading
import time

import lobby_console as lc
import user

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
BROADCAST_PORT = 5555
PORT = 5000
BUFFER = 1024

CLIENTS = {}

SEND_BROADCAST_EVENT = threading.Event()
TCP_CONNECTION_EVENT = threading.Event()
WAIT_FOR_CONNECTION_EVENT = threading.Event()
LISTEN_FOR_CMD = threading.Event()

lobby = lc.Lobby()


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

    def random_user_id():
        while True:
            random_num = random.randint(1, 999999)
            if random_num not in CLIENTS:
                break
        return random_num

    def command_line(user_):
        while True:
            data_ = conn.recv(BUFFER)
            while data_:
                data_ += conn.recv(BUFFER)
                if not data_:
                    break
            print(data_.decode())
            lobby.process_command(command=data_, user=user_)
    user_id = random_user_id()
    CLIENTS[user_id] = conn
    print(CLIENTS)

    username_ = conn.recv(BUFFER).decode()
    print(username_)
    cur_user = user.User(username_, user_id)
    command_line(cur_user)


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

