import struct
import threading


class User:
    def __init__(self, username, user_id, conn):
        self.username = username
        self.user_id = user_id
        self.conn = conn

    cmd_line_event = threading.Event()
    def change_room(self, room):
        print(f"[info-user-class] changing room to {room.room_name}...")
        conn = self.conn
        change_room_msg = f'change_room${room.host}${room.port}'.encode()
        conn.send(change_room_msg)
        self.disconnect()

    def disconnect(self):
        print("[user-info] shutting down connection...")
        self.conn.close()


    def send_success(self):
        print("[user-class] sending success...")
        self.conn.send(struct.pack('?', True))

    def send_failure(self):
        print("[user-class] sending failure...")
        self.conn.send(struct.pack('?', False))
