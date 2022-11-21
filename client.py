import socket
import json
import sys

host = socket.gethostname()  # as both code is running on same pc
port = 8728  # socket server port number
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((host, port))  # connect to the server

# This is where the sequence will begin, client waits for intro message
print(client_socket.recv(3000).decode()) 
client_socket.send('OK'.encode())  # Send OK message

# This is where the registration and authentication will happen
print(client_socket.recv(3000).decode()) # Asks if user is registered
user = input() #takes Y/N from user accordingly
client_socket.send(user.encode()) #sends Y/N to server
print()
with open("users.json", "r") as jsonFile:
        users = json.load(jsonFile)

if(user == 'N'  or user == "n"):
    print(client_socket.recv(3000).decode()) #asks for email
    email = input() #takes email from user
    client_socket.send(email.encode()) #sends email to server
    print()
    if email in users:
        print(client_socket.recv(3000).decode())
        print() 
        sys.exit(0)
    if email.endswith('@ashoka.edu.in'):
        print(client_socket.recv(3000).decode()) #asks for password
        password = input()
        client_socket.send(password.encode()) #sends password to server
        print()
        print(client_socket.recv(3000).decode()) #logged in message
        client_socket.send('OK'.encode())  # Send OK message
    else:
        print(client_socket.recv(3000).decode()) #prints error mesage
        sys.exit(0)
elif(user == 'Y' or user == "y"):
    print(client_socket.recv(3000).decode()) #asks for email
    email = input() #takes email from user
    client_socket.send(email.encode()) #sends email to server
    print()
    if email.endswith('@ashoka.edu.in'):
        print(client_socket.recv(3000).decode()) #asks for password
        password = input()
        client_socket.send(password.encode()) #sends password to server
        print()
        print(client_socket.recv(3000).decode()) #logged in message
        client_socket.send('OK'.encode())  # Send OK message
    else:
        print(client_socket.recv(3000).decode()) #prints error mesage
        sys.exit(0)
else: 
    #wait for error message
    print()
    print(client_socket.recv(3000).decode())
    sys.exit(0)

# This is where the client will receive the service options
options = client_socket.recv(3000).decode() 
options = json.loads(options) # Gets options Prereqs and Semester

print("We offer the following services: ")
for option in options:
    print(option) # check if this is correct

print('\nWhat would you like to view? (Prereqs/Sem): ', end='')  # show in terminal
choice = input()
client_socket.send(choice.encode())
print()

if choice == 'Prereqs':
    #wait for outro
    var = input(client_socket.recv(3000).decode())
    client_socket.send(var.encode())
    print() #print ok
    print(client_socket.recv(3000).decode())
elif choice == 'Sem':
    #wait for service request
    var = input(client_socket.recv(3000).decode())
    #send service needed 
    client_socket.send(var.encode())
    #wait for ok response
    print() 
    print(client_socket.recv(3000).decode())
else: 
    #wait for error message
    print()
    print(client_socket.recv(3000).decode())

client_socket.close()  # close the connection