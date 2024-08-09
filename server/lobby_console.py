import os
import time


class Lobby:
    def __init__(self, command, conn):
        self.command = command
        self.conn = conn

    def cmd_username(self, new_username):
        pass

    def cmd_create(self, create_type, name, password=''):
        pass

    def cmd_join(self, room):
        pass

    def cmd_list_rooms(self):
        pass

    def process_command(self):
        cmd_instructions = self.command.split()
        main_cmd = cmd_instructions[0]
        cmd_arguments = cmd_instructions.pop(0)
        argument_length = len(cmd_arguments)
        print(main_cmd)
        if main_cmd == '$username' and argument_length == 1:
            self.cmd_username(cmd_arguments)


if __name__ == '__main__':
    lobby = Lobby('join [name]', "connection")
    lobby.process_command()
    
# Add cmd variable to arguments in process_command() -method
# Remove __init__ 
