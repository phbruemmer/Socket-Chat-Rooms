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
