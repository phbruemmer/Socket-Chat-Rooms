import struct


class User:
    def __init__(self, username, user_id, conn):
        self.username = username
        self.user_id = user_id
        self.conn = conn

    def change_room(self, room):
        print(f"[info-user-class] changing room to {room.room_name}...")
        conn = self.conn
        change_room_msg = f'change_room${room.host}${room.port}'
        conn.send(change_room_msg)
        valid_cmd = struct.unpack('?', conn.recv(1))
        if not valid_cmd:
            print("[user-info] failed to change room.\n[user-info] returning to lobby...")
            return
        else:
            self.disconnect()

    def disconnect(self):
        print("[user-info] shutting down connection...")
        self.conn.shutdown()

    def send_success(self):
        print("[user-class] sending success...")
        self.conn.send(struct.pack('?', True))

    def send_failure(self):
        print("[user-class] sending failure...")
        self.conn.send(struct.pack('?', False))
