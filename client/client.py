import socket
import struct
import threading
import re
import instruction_handler

BROADCAST_PORT = 5555
TIMEOUTS = 10
BUFFER = 1024


def listen_for_broadcast_message():
    """
    - This function listens to UDP Broadcasts on Broadcast Port 5555.
    - The UDP Broadcast message from the server contains the port for the TCP connection for the lobby server.
    - If the address and port exists the function returns it
    :return:
    """
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
    """
    - This function determines the username and checks whether the username consists of valid characters (only english
        letters)
    - The username is sent to the server if it is valid, in case of an invalid username the request will be repeated
    :param sock:
    :return:
    """
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
    print_event = threading.Event()

    def receiver(connection):
        """
        - This function receives data from the server and follows the instructions if given.
        :param connection:
        :return:
        """
        instruction = instruction_handler.Instruction(sock)
        print("[info] listening to server...")
        try:
            while not connection.is_set():
                data_ = sock.recv(BUFFER)
                if not data_:
                    print("[info] no data received, server might have closed the connection.")
                    connection.set()
                    break
                print(data_.decode())
                print_event.set()

                valid_instruction = instruction.detect_instruction(data_)

                if valid_instruction:
                    continue

                validation_code = struct.unpack('?', data_)
                if validation_code:
                    print("[client-info] command executed on server-side.")
                elif not validation_code:
                    print("[client-info] command could not be executed on server-side.")
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
    """
    - This function simply connects the client to the server using the TCP protocol with ipv4 address and port
    :param addr:
    :param port:
    :return:
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((addr, port))
        get_username(sock)
        connected_client(sock)
        sock.close()


def client_main():
    """
    - Main function to connect the client to the server.
    :return:
    """
    addr, port = listen_for_broadcast_message()
    if addr is None:
        return
    connect_to_lobby(addr, port)


if __name__ == "__main__":
    client_main()
