import socket
import json 
import random
import string
import smtplib, ssl
import sys   

hostIP = '127.0.0.1'
#hostIP = '0.0.0.0'
port=8728
ServerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ServerSocket.bind((hostIP,port)) #binds the socket to the port
ServerSocket.listen(3)
print("Server is up!")

options = ["Prerequisites for courses", "Semester-wise courses"]
pre_req = {"CS-1101" : "None", "CS-1104" : "None", "CS-1209" : "None", "CS-1216" : "CS-1101 Introduction to Computer Programming", "CS-1203" : "CS-1101 Introduction to Computer Programming", "CS-1205" : "CS-1101 Introduction to Computer Programming", "CS-1217" : "CS-1101 Introduction to Computer Programming and CS-1216 Computer Organization and Systems", "CS-1390" : "CS-1101 Introduction to Computer Programming and CS-1209 Probability and Statistics", "CS-1340" : "CS-1101 Introduction to Computer Programming and CS-1216 Computer Organization and Systems", "CS-1319" : "CS-1101 Introduction to Computer Programming, CS-1216 Computer Organization and Systems, and CS-1203 Data Structures"}
sem = {"Monsoon 2022" : "CS-1101 Introduction to Computer Programming, CS-1216 Computer Organisation and Systems, CS- 1203 Data Structures, CS-1209 Probability and Statistics, CS-1390 Introduction to Machine Learning, CS-1340 Computer Networks, CS-1319 Programming Language Design and Implementation",
"Spring 2022" : "CS-1101 Introduction to Computer Programming, CS-1104 Discrete Mathematics, CS-1217 Operating Systems, CS-1205 Algorithm Design and Analysis"}

def handle_new_client(ClientSocket,Address):
    global options
    global pre_req
    global sem

    # Response is ok, so sends service options
    data = json.dumps(options)
    ClientSocket.send(data.encode()) #send options i.e. Prereqs or Sem

    #send available information
    choice = ClientSocket.recv(3000).decode() #Prereq or Sem
    if choice == 'Prereqs':
        ClientSocket.send("Send us the course for which you'd like prerequisites! (CS-1101/CS-1104/CS-1209/CS-1216/CS-1203/CS-1205/CS-1217/CS-1390/CS-1340/CS-1319):\n".encode()) 
        #wait for response
        code = ClientSocket.recv(3000).decode()
        if(code in pre_req.keys()):
            data_sent = pre_req[code]
            ClientSocket.send(str(data_sent).encode())
    elif choice == "Sem":
        ClientSocket.send("Send us the semester for which you'd like courses! (Monsoon 2022/Spring 2022):\n".encode()) 
        #wait for response
        sems = ClientSocket.recv(3000).decode()
        if(sems in sem.keys()):
            data_sent = sem[sems]
            ClientSocket.send(str(data_sent).encode())
    else:
        ClientSocket.send("Invalid choice! Disconnecting...".encode())

while True:
    (ClientSocket,Address) = ServerSocket.accept() #wait until client connectss

    print("New client connected!")
    intro = "\nWelcome to the Course Catalogue!\n"
    ClientSocket.send(intro.encode())
    # Sends intro message

    # Wait for OK response
    # If response not ok thesn
    if(ClientSocket.recv(3000).decode() != "OK"):
        print("Disconnecting! Error!!")
        ClientSocket.close()

    # Open users file here
    with open("users.json", "r") as jsonFile:
        users = json.load(jsonFile)

    # This is where we add registration and authentication with ashoka ID
    ClientSocket.send("Hello! Are you a registered user? (Y/N):".encode()) #Ask if user is registered
    user = ClientSocket.recv(3000).decode()
    
    if(user == "N" or user == "n"):
        ClientSocket.send("Enter your Ashoka email:".encode())
        #wait for response
        email = ClientSocket.recv(3000).decode() #gets email from client
        if email in users:
            ClientSocket.send("You are already registered, please reconnect to server with existing password!".encode())
            sys.exit(0)
        # if email doesnt already exit in users.json then continue, send error message and exists
        if email.endswith('@ashoka.edu.in'):
            letters = string.ascii_lowercase
            num = ''.join(random.choice(letters) for i in range(10))
            
            sender_email = "coursecatalogue2022@gmail.com" 
            password = "jsqejhqylkftfypv" 
            receiver_email = [f"{email}"]
            message = """\
From: Course Catalogue
To: %s
Subject: Authentication

Your password is %s. This will remain your password for every login attempt.""" % (email, num)

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls(context=context)
                    server.login(sender_email, password) 
                    server.sendmail(sender_email, receiver_email, message)
                    server.close()
                    server.set_debuglevel(True)
                    ClientSocket.send("A password has been sent to your email; if not recieved, please reconnect to server. Enter your password:".encode())
                    password = ClientSocket.recv(3000).decode()
            except Exception as ex:
                ClientSocket.send("Something went wrong….",ex.encode())

            if password == num:
                users[email] = password
                ClientSocket.send("You have been logged in successfully.\n".encode())
                if(ClientSocket.recv(3000).decode() != "OK"):
                    print("Disconnecting! Error!!")
                    ClientSocket.close()
                handle_new_client(ClientSocket,Address)
            else:
                ClientSocket.send("Incorrect password! Disconnecting...".encode())
                sys.exit(0)
        else:
            ClientSocket.send("Invalid email".encode())
            sys.exit(0)

    elif (user == "Y" or user == "y"):
        ClientSocket.send("Enter your Ashoka email:".encode())
        #wait for response
        email = ClientSocket.recv(3000).decode() #gets email from client
        if email.endswith('@ashoka.edu.in'):
            ClientSocket.send("Enter your password:".encode())
            #generate and send password to email
            password = ClientSocket.recv(3000).decode()
            #check if password is valid
            if(users[email] == password):
                ClientSocket.send("You have been logged in successfully.".encode())
                if(ClientSocket.recv(3000).decode() != "OK"):
                    print("Disconnecting! Error!!")
                    ClientSocket.close()
                handle_new_client(ClientSocket,Address)
            else:
                ClientSocket.send("Incorrect password! Disconnecting...".encode())
                sys.exit(0)
        else:
            ClientSocket.send("Invalid email".encode())
            sys.exit(0)
    else:
        ClientSocket.send("Invalid choice! Disconnecting...".encode())
        sys.exit(0)

    with open("users.json", "w") as jsonFile:
        json.dump(users, jsonFile)

    ClientSocket.close()

print("Server is going down!")
ServerSocket.close()


### Sequence of events
# Client connects to server
# Server accepts connection

# (Interaction begins)
# 1.Server sends intro message -> Welcome to course catalogue
# 2.Client sends OK response 
# 3.Server asks if user already registered
# 4.Client sends yes or no:
# 5.a) If no, server asks for email
# 5.b) Client sends email address
# 5.c) Server checks if email already registered, if yes then exists with error message
# 5.d) Server then checks if email has Ashoka domain, if yes then sends password to email address
# 5.e) Client sends password
# 5.f) Server checks if password is correct, gets OK from client, then calls handle_new_client, else throws error
# 6.a) If yes, server asks for email
# 6.b) Client sends email, server checks if ashoka domain 
# 6.c) Server asks for password if domain is ashoka
# 6.d) Client sends password
# 6.e) Server checks if password is correct using users.json, gets OK from client, then calls handle_new_client, else throws error
# 7. handle_new_client:
# 7.a) Server sends services offered
# 7.b) Client sends choice of service, Prereqs or Sem
# 7.c) If Prereqs, server asks for course code, then sends data to client
# 7.d) If Sem, server asks for semester, then sends data to client
# 7.e) Client decodes and prints requested data