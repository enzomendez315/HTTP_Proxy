# Place your imports here
import signal
import socket
from socket import *
from optparse import OptionParser
import sys
from threading import *
from time import *
from urllib.parse import urlparse

# Start of program execution
# Parse out the command line server address and port number to listen to
parser = OptionParser()
parser.add_option('-p', type='int', dest='serverPort')
parser.add_option('-a', type='string', dest='serverAddress')
(options, args) = parser.parse_args()

port = options.serverPort
address = options.serverAddress
if address is None:
    address = 'localhost'
if port is None:
    port = 2100

# Set up listening socket for incoming connections
listening_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
listening_socket.bind((address, port))
listening_socket.listen()
listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
	sys.exit(0)

# Set up signal handling (ctrl-c)
signal.signal(signal.SIGINT, ctrl_c_pressed)

# Receives data from client and parses it to check that it is a valid request.
# Sets up the server socket and sends the client request, then listens for 
# the reply and sends it back to the client.
def handle_client(client_socket, client_addr):
    # recv request
    request = client_socket.recv(4096)
    while True:
        temp = client_socket.recv(4096)
        request += temp
        if request.endswith(b'\r\n\r\n'):
            break

    # Parse request
    parsed_request = parse_request(request)

    # Set up server socket
    server_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(address, port)

    while True:
        # Fetch data from origin
        server_socket.sendall(parsed_request)
        data = server_socket.recv(4096)

        # Send response
        client_socket.sendall(data)

        for i in range(10):
            sleep(1)
            print(f'Handling request from client {client_addr}')
        print('Client request handled')
        client_socket.close()

# Once a client has connected, the proxy should read data from the client
# and check for a properly formatted HTTP request. 
# aka <METHOD> <URL> <HTTP VERSION>
# For other headers: <HEADER NAME>: <HEADER VALUE>
##########################################################################
# Checks that the request is properly formatted.
# Returns error messages otherwise.
# “400 Bad Request” for malformed requests or if headers are not properly 
# formatted for parsing.
# "501 Not Implemented” for valid HTTP methods other than GET.
def parse_request(request):
    list = request.split(" ")
    if (list[0] != "GET"):
        return "501 Not Implemented"

    if (list[2] != "HTTP/1.0"):
        return "400 Bad Request"

    new_request = list[0] + " / " + list[2] + "\nHost: " + urlparse(list[1]).hostname
    + "\nConnection: close"

    return new_request

    """
    Example, accept from client:
        GET http://www.google.com/ HTTP/1.0

    Send to origin server:
        GET / HTTP/1.0
        Host: www.google.com
        Connection: close
        (Additional client-specified headers, if any.)
    """

# Receive loop from client to proxy. This gathers requests that
# will eventually be sent to the origin server.
while True:
    # Wait for an incoming connection
    client_socket, client_addr = listening_socket.accept()

    # Handle each connection in a single thread.
    #handle_client(client_socket, client_addr)

    # Handle each connection in a separate thread.
    Thread(target=handle_client, args=(client_socket, client_addr)).start()


"""
# recv request from client
request = b''
while True:
    temp = client_socket.recv(1024)
    request += temp
    if request.endswith(b'\r\n\r\n'):
        break

# recv response from origin
while True:
    origin_socket.sendall(request)
    temp = origin_socket.recv(1024)
    if temp == b'':
        break
    request += temp
"""
