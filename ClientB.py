import tkinter as tk
from tkinter import ttk
import threading
import socket

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define host and port for server
HOST = 'localhost'
PORT = 5000

# Connect to the server
client_socket.connect((HOST, PORT))

# Define function to send message to server
def send_message():
    message = message_entry.get()
    sender = sender_entry.get()
    data = {'message': message, 'sender': sender}
    client_socket.sendall(str(data).encode())
    message_entry.delete(0, tk.END)
    if not sender_entry['state'] == 'disabled':
        sender_entry.config(state='disabled')

# Create the GUI
root = tk.Tk()
root.title('Chat App')
root.geometry('500x500')
root.configure(bg='black')

# Create widgets
sender_label = ttk.Label(root, text='Name:', foreground='white', background='black')
sender_entry = ttk.Entry(root)
message_label = ttk.Label(root, text='Message:', foreground='white', background='black')
message_entry = ttk.Entry(root)
send_button = ttk.Button(root, text='Send', command=send_message)
chat_box = tk.Text(root, height=20, width=60, foreground='white', background='black')
scrollbar = ttk.Scrollbar(root, command=chat_box.yview)
chat_box.config(yscrollcommand=scrollbar.set, state='disabled')

# Add widgets to grid
sender_label.grid(row=0, column=0, pady=10, padx=10)
sender_entry.grid(row=0, column=1, pady=10, padx=10)
message_label.grid(row=1, column=0, pady=10, padx=10)
message_entry.grid(row=1, column=1, pady=10, padx=10)
send_button.grid(row=2, column=1, pady=10, padx=10, sticky='e')
chat_box.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
scrollbar.grid(row=3, column=2, sticky='ns', pady=10)

# Define function to update chat box with received messages
def update_chat_box(message):
    chat_box.config(state='normal')
    chat_box.insert(tk.END, message + '\n')
    chat_box.config(state='disabled')

# Define function to receive messages from server
def receive_messages():
    while True:
        data = client_socket.recv(1024)
        message = data.decode()
        update_chat_box(message)

# Create a new thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Run the GUI
root.mainloop()
