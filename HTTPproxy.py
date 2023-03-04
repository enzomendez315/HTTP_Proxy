# Place your imports here
import signal
import socket
from socket import *
from optparse import OptionParser
import sys
from threading import Thread
from time import *

# Signal handler for pressing ctrl-c
def ctrl_c_pressed(signal, frame):
	sys.exit(0)

# Proxy should handle both DNS and IPv4 URLs. When it starts,
# the first thing it does is to establish a socket that it can use
# to listen for incoming connections. Port is specified on command line

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

# Set up signal handling (ctrl-c)
signal.signal(signal.SIGINT, ctrl_c_pressed)

# Once a client has connected, the proxy should read data from the client
# and check for a properly formatted HTTP request. 
# aka <METHOD> <URL> <HTTP VERSION>
# For other headers: <HEADER NAME>: <HEADER VALUE>

# “400 Bad Request” for malformed requests or if headers are not properly 
# formatted for parsing.
# "501 Not Implemented” for valid HTTP methods other than GET.
# TODO: Set up sockets to receive requests
def handle_client(client_socket, client_addr):
    # recv request
    # parse request
    # fetch data from origin
    # send response
    for i in range(10):
        sleep(1)
        print(f'Handling request from client {client_addr}')
    print('Client request handled')
    client_socket.close()

server_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', 2100))
server_socket.listen()

# IMPORTANT!
# Immediately after you create your proxy's listening socket add
# the following code (where "skt" is the name of the socket here):
# skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Without this code the autograder may cause some tests to fail
# spuriously.

while True:
    client_socket, client_addr = server_socket.accept()
    # Use this line to handle each connection in a single thread.
    # handle_client(client_socket, client_addr)
    # Use this line to handle each connection in a separate thread.
    Thread(target=handle_client, args=(client_socket, client_addr)).start()


# Example, accept from client:
    # GET http://www.google.com/ HTTP/1.0

# Send to origin server:
    # GET / HTTP/1.0
    # Host: www.google.com
    # Connection: close
    # (Additional client-specified headers, if any.)
