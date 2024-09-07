import socket
import struct
import check_data


class Instruction:
    def __init__(self, sock):
        self.sock = sock

    def username(self):
        pass

    def change_room(self, instructions):
        print("[instruction-info] changing to new room...")
        if not check_data.check_ip(instructions[1]) and check_data.check_port(instructions[2]):
            return False
        self.sock.disconnect()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((instructions[1], instructions[2]))

    def join_threads(self, threads):
        for thread in threads:
            thread.join()

    def detect_instruction(self, instructions):
        instructions = instructions.decode()
        if isinstance(instructions, (bytes, bytearray, memoryview)):
            return False
        instruction = instructions.split('$')
        valid_instruction = True
        match instruction[0]:
            case 'username':
                print("displaying username...")
            case 'change_room':
                print("changing room...")
            case _:
                print("No such instruction found...")
                valid_instruction = False
        return valid_instruction


if __name__ == '__main__':
    print(check_data.check_ip('192.168.115.2x0'))



