# https://pymotw.com/3/
import socket
from time import time, sleep
from random import random


def udp_send(bytedata):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # IP_address, Port_No
    server_address = ('localhost', 10000)
    try:
        sent = sock.sendto(bytedata, server_address)
    finally:
        # print('Data sent, closing socket')
        sock.close()


def get_decimal_posix():
    tm = time()
    tm = round(tm, 4)
    return tm


def get_data():
    returnarray = []
    iters = 10 * 10
    for i in range(0, iters):
        t = get_decimal_posix()
        rn = round(random(), 4)
        d = [t, rn]
        returnarray.append(d)
    return returnarray


if __name__ == "__main__":

    # try:
    while True:
        data_to_send = str(get_data())
        # Convert to bytes
        bytearray = data_to_send.encode('utf-8')
        print(len(bytearray))
        udp_send(bytearray)
        sleep(10)
    # except KeyboardInterrupt:
    #     print("Exit on keyboard")

