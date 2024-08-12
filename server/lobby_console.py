class Lobby:
    def cmd_username(self, user, new_username):
        print(new_username)

    def cmd_create(self, user, create_type, name, password=''):
        pass

    def cmd_join(self, user, room):
        pass

    def cmd_list_rooms(self, user):
        pass

    def process_command(self, command, user=''):
        cmd_instructions = command.split()
        main_cmd = cmd_instructions[0]
        cmd_arguments = cmd_instructions.pop(-1)
        argument_length = len(cmd_instructions)
        print(argument_length)
        if main_cmd == '$username' and argument_length == 1:
            self.cmd_username(user, cmd_arguments)
