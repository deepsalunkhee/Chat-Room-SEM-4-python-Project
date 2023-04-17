import socket
from threading import Thread
from flask import Flask, render_template

# Create a Flask app instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Define host and port for server
HOST = 'localhost'
PORT = 5000

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket option to allow re-use of the address and port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Listen for incoming client connections
server_socket.listen()

# Define list of connected clients
clients = []

# Define function to broadcast message to all connected clients
def broadcast_message(sender, message):
    for client in clients:
        if client != sender:
            try:
                # Send the message to the client
                client.sendall(f' {message}'.encode())
            except socket.error:
                # If there's an error sending the message, remove the client from the list of connected clients
                clients.remove(client)
                print(f'Client {client} disconnected')

# Define function to handle client connection
def handle_client(client_socket, addr):
    print(f'Client connected from {addr}')

    # Add the client socket to the list of connected clients
    clients.append(client_socket)

    while True:
        # Receive data from the client
        data = client_socket.recv(1024)

        # If there's no data, the client has disconnected
        if not data:
            # Remove the client from the list of connected clients and close the connection
            clients.remove(client_socket)
            client_socket.close()
            break

        # Decode the received data into a string
        message = data.decode()

        # Broadcast the message to all connected clients
        broadcast_message(addr, message)

# Define a route for the index page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print(f'Server running on {HOST}:{PORT}')

    # Listen for incoming client connections
    while True:
        # Accept an incoming client connection and create a new thread to handle the connection
        client_socket, addr = server_socket.accept()
        client_thread = Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()
