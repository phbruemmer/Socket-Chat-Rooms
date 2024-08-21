import random

import rooms.chat_rooms


used_ports = []


class Lobby:
    def cmd_username(self, user, new_username):
        print(new_username)
        user.username = new_username

    def cmd_create(self, user, create_type, name, password=''):
        def get_available_port():
            new_port = random.randint(3000, 3100)
            while new_port in used_ports:
                new_port = random.randint(3000, 3100)
            print(new_port)
            return new_port
        if create_type == 'chat':
            port = get_available_port()
            new_room = rooms.chat_rooms.Room(port=port, room_name=name, room_password=password, admin=user)
            new_room.start_room()
            user.change_room(new_room)

    def cmd_join(self, user, room):
        pass

    def cmd_list_rooms(self, user):
        pass

    def process_command(self, command, user):
        print(command)
        cmd_instructions = command.split()
        main_cmd = cmd_instructions[0]
        cmd_arguments = cmd_instructions.pop(-1)
        argument_length = len(cmd_instructions)
        print(argument_length)
        if main_cmd == '$username' and argument_length == 1:
            self.cmd_username(user, cmd_arguments)
