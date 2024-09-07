import random
import re
import rooms.chat_rooms


used_ports = []


class Lobby:
    def server_side_input_checks(self, data):
        if not re.match(r"^[A-Za-z0-9]*$", data) or re.match(r'^[\s\t\n]*$', data):
            return False
        else:
            return True

    def cmd_username(self, user, new_username):
        if self.server_side_input_checks(new_username):
            user.username = new_username
            user.send_success()
        else:
            user.send_failure()

    def cmd_create(self, user, create_type, name, password=''):
        def get_available_port():
            new_port = random.randint(3000, 3100)
            while new_port in used_ports:
                new_port = random.randint(3000, 3100)
            print(new_port)
            return new_port

        if create_type == 'chat':
            port = get_available_port()
            user.disconnect()
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
        argument_length = len(cmd_instructions) - 1
        print(argument_length)
        if main_cmd == '$username' and argument_length == 1:
            self.cmd_username(user, cmd_instructions[1])
        elif main_cmd == '$create' and (argument_length == 2 or argument_length == 3):
            if argument_length < 3:
                cmd_instructions.append('')
            self.cmd_create(user, cmd_instructions[1], cmd_instructions[2], cmd_instructions[3])
        else:
            user.send_failure()

