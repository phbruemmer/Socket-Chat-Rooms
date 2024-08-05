import socket
import threading

HOST = socket.gethostbyname(socket.gethostname)


class Room:
    def __init__(self, host=HOST, port=5000, max_users=20):
        self.host = host
        self.port = port
        self.room_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.room_socket.bind((host, port))
        self.room_socket.listen(max_users)
        print(f"[info] new room started and listening on {self.host}:{self.port}")

    def start_room(self):
        try:
            while True:
                conn, addr = self.room_socket.accept()
                print(f"[info] connection established with {addr}")
                client_handler = threading.Thread(target=self.handle_client)
                client_handler.start()
        except KeyboardInterrupt:
            print("[info] stopping server...")
            self.room_socket.close()

    def handle_client(self):
        pass
