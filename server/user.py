import rooms.chat_rooms

class User:
    def __init__(self, username, user_id):
        self.username = username
        self.user_id = user_id

    def change_room(self, room=rooms.chat_rooms.Room):
        pass
