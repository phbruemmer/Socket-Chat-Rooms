class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def change_room(self, room):
        print(f"[info] changing room to {room.room_name}...")
