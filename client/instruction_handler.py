class Instruction:
    def __init__(self, sock):
        self.sock = sock

    def username(self):
        pass

    def change_room(self, instructions):
        pass


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
    Instruction().detect_instruction("change_room$129.168.115.200:3053")

