import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())


class Room:
    def __init__(self, host=HOST, port=3000, max_users=20,
                 room_name='standard_room', global_room=False, room_password='', admin=None):
        self.host = host
        self.port = port
        self.room_name = room_name
        self.global_room = global_room
        self.room_password = room_password
        self.room_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.room_socket.bind((host, port))
        self.room_socket.listen(max_users)
        self.admin = admin
        print(f"[info-room-class] new room started and listening on {self.host}:{self.port}")

    def start_room(self):
        def run_room():
            try:
                while True:
                    conn, addr = self.room_socket.accept()
                    print(f"[info-room-class] connection established with {addr}")
                    client_handler = threading.Thread(target=self.handle_client)
                    client_handler.start()
            except KeyboardInterrupt:
                print("[info-room-class] stopping server...")
                self.room_socket.close()

        room_thread = threading.Thread(target=run_room)
        room_thread.start()

    def handle_client(self, room_socket):
        with room_socket:
            while True:
                data = room_socket.recv(1024)
                if not data:
                    break
                print(data.decode())
                room_socket.sendall(data)
