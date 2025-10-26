# https://pymotw.com/3/
import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind the socket to the port - IP_address, Port_No
server_address = ('localhost', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)
    print(f'Received {len(data)} bytes from client {address}')
    # Convert bytearray back to string. this is now something that can be parsed

    d = data.decode("utf-8")
    # print(d)
    if data:
        # On completion send confirmation message back to client
        msg = 'Server received ' + str(len(data)) + ' bytes'
        m = msg.encode('utf-8')
        sent = sock.sendto(m, address)
        # print('sent {} bytes back to {}'.format(
        #     sent, address))