import socket
import json 
import random
import string
import smtplib, ssl   

hostIP = '0.0.0.0'
port=8728
ServerSocket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ServerSocket.bind((hostIP,port)) #binds the socket to the port
ServerSocket.listen(3)
print("Server is up!")

options = ["Prerequisites for courses", "Semester-wise courses"]
pre_req = {"CS-1101" : "None", "CS-1104" : "None", "CS-1209" : "None", "CS-1216" : "Introduction to Computer Programming", "CS-1203" : "Introduction to Computer Programming", "CS-1205" : "Introduction to Computer Programming", "CS-1217" : "Introduction to Computer Programming and Computer Organization and Systems", "CS-1390" : "Introduction to Computer Programming and Probability and Statistics", "CS-1340" : "Introduction to Computer Programming and Computer Organization and Systems", "CS-1319" : "Introduction to Computer Programming, Computer Organization and Systems, and Data Structures"}
sem = {"Monsoon 2022" : "CS-1101 Introduction to Computer Programming, Computer Organisation and Systems, Data Structures, CS-1209 Probability and Statistics, CS-1390 Introduction to Machine Learning, CS-1340 Computer Networks, CS-1319 Programming Language Design and Implementation",
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

    # OPEN USERS FILE HERE
    with open("users.json", "r") as jsonFile:
        users = json.load(jsonFile)

    #this is where we add registration and authentication with ashoka ID
    ClientSocket.send("Hello! Are you a registered user? (Y/N):".encode()) #Ask if user is registered
    user = ClientSocket.recv(3000).decode()
    
    if(user == "N"):
        ClientSocket.send("Enter your Ashoka email:".encode())
        #wait for response
        email = ClientSocket.recv(3000).decode() #gets email from client
        # if email doesnt already exit in users.json then continue, else move to elif block
        if email.endswith('@ashoka.edu.in'):
            letters = string.ascii_lowercase
            num = ''.join(random.choice(letters) for i in range(10))
            #num = "10"
            
            #check if email actually exists
            sender_email = "coursecatalogue2022@gmail.com" 
            password = "jsqejhqylkftfypv" 
            receiver_email = [f"{email}"]
            message = """\
From: Course Catalogue
To: %s
Subject: Authentication

Your password is %s. This will remain your password for every login attempt""" % (email, num)

            context = ssl.create_default_context()
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls(context=context)
                    server.login(sender_email, password) 
                    server.sendmail(sender_email, receiver_email, message)
                    server.close()
                    server.set_debuglevel(True)
                    ClientSocket.send("A password has been sent to your email. Enter your password:".encode())
                        #HOW TO CHECK IF EMAIL EXISTS OR NOT
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
        else:
            ClientSocket.send("Invalid email".encode())
            #do equivalent of return 0

    elif (user == "Y"):
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
            ClientSocket.send("Invalid email".encode())
    else:
        ClientSocket.send("Invalid choice! Disconnecting...".encode())

    with open("users.json", "w") as jsonFile:
        json.dump(users, jsonFile)

    ClientSocket.close()

print("Server is going down!")
ServerSocket.close()


#Sequence of events
#Client connects to server
#Server accepts connection

#(Interaction begins)
#Server sends intro message -> welcome to ams
#Client sends OK response 
#Server sends list of services
#Client sends choice
#If n, server sends outro message??
#If prereqs, server sends prereqs request
#Client sends sem/course code
#Server sends OK response -- has to return data
#If choice invalid, server sends error message