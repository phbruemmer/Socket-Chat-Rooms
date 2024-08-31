import socket
import struct


def check_ip(addr):
    """
    - This function checks IP addresses and returns True when a valid ipv4 address is found.
    :param addr:
    :return:
    """
    addr = addr.split('.')
    if not len(addr) == 4:
        return False

    for i in range(0, 4):
        if not addr[i].isdigit():
            return False
    return True


def check_port(port):
    valid_port = True
    if not isinstance(port, int):
        valid_port = False
    if not port >= 3000 and port <= 9000:
        valid_port = False
    return valid_port


class Instruction:
    def __init__(self, sock):
        self.sock = sock

    def username(self):
        pass

    def change_room(self, instructions):
        print("[instruction-info] changing to new room...")

        self.sock.send(struct.pack('?', True))
        self.sock.shutdown()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((instructions[1], instructions[2]))

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
    print(check_ip('192.168.115.2x0'))



