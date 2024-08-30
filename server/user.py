import time
import struct
from server import CLIENTS

class User:
    def __init__(self, username, user_id, conn):
        self.username = username
        self.user_id = user_id
        self.conn = conn

    def change_room(self, room):
        print(f"[info-user-class] changing room to {room.room_name}...")
        conn = self.conn
        change_room_msg = b'change_room$'
        conn.send(change_room_msg)
        valid_cmd = conn.recv(1).decode()
        if not valid_cmd:
            return
        conn.send(room.host)
        valid_cmd = conn.recv(1).decode()
        if not valid_cmd:
            return
        conn.send(room.port)
        valid_cmd = conn.recv(1).decode()
        if not valid_cmd:
            return

    def send_success(self):
        print("[user-class] sending success...")
        self.conn.send(struct.pack('?', True))

    def send_failure(self):
        print("[user-class] sending failure...")
        self.conn.send(struct.pack('?', False))
