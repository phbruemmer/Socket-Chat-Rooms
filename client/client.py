import socket
import struct
import threading
import re

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
    #
    # Maybe insecure because of client-side manipulation and no server-side checks
    #
    while not re.match(r"^[A-Za-z0-9]*$", username) or re.match(r'^[\s\t\n]*$', username):
        print("[info] only english letters and numbers from 0 - 9 are allowed.")
        username = input("> > > ")
    print("[info] valid username received.\n[info] sending username for user validation...")
    sock.send(username.encode())
    print("[info] username sent.")


def connected_client(sock):
    connected = threading.Event()
    print_event = threading.Event()

    def receiver(connection):
        print("[info] listening to server...")
        try:
            while not connection.is_set():
                data_ = sock.recv(BUFFER)
                if not data_:
                    print("[info] no data received, server might have closed the connection.")
                    connection.set()
                    break
                print_event.set()

                """
                    ADD:
                        - Function that identifies commands from the server and executes the right instructions.
                        - If no command was found, continue by checking the validation code.
                """

                validation_code = struct.unpack('?', data_)
                if validation_code:
                    print("[client-info] command executed on server-side.")
                elif not validation_code:
                    print("[client-info] ")
                print(data_.decode())
        except ConnectionResetError:
            print("[error] Connection was reset by the server.")
        except Exception as e:
            print(f"[error] Unexpected error in receiver: {e}")
        finally:
            connection.set()
            print("[info] receiver thread closing.")

    def sender(connection):
        print("[info] chat available.")
        try:
            while not connection.is_set():
                print_event.wait()
                print("\n")
                msg_ = input("> ")
                sock.send(msg_.encode())
                print_event.clear()
                if msg_ == "$exit":
                    connection.set()
                    return
        except BrokenPipeError:
            print("[error] Cannot send data, connection closed.")
        except Exception as e:
            print(f"[error] Unexpected error in sender: {e}")
        finally:
            connection.set()
            print("[info] sender thread closing.")

    recv_thread = threading.Thread(target=receiver, args=(connected,))
    recv_thread.start()
    sender(connected)

    # recv_thread.join()
    print("[info] Client disconnected.")


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
