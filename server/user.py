import time

from server import CLIENTS

class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def change_room(self, room):
        print(f"[info] changing room to {room.room_name}...")
        conn = CLIENTS[self.user_id]
        change_room_msg = b'$change_room$'
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
