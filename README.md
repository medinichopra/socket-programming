# socket-programming
Client- Server Application to display courses and their prerequisites

# Course Catalogue

This client-server program offers two service: the prerequisites of a course, and the courses offered in a semester. In order to access these services, one must login/sign up for the same.

## Note

Make sure to have all three files in the same folder, namely server.py, client.py and users.json. In order to use, one must have Python installed and running.

## Usage

```bash
# in one terminal
python3 server.py

# open another terminal and run
python3 client.py
```

The server will output:

```bash
Server is up!
```
Once the client program is running, you will see:

```python
Welcome to the Course Catalogue!

Hello! Are you a registered user? (Y/N):
```
*The options given in the bracket are what the user can choose from, and they are case sensitive. So y is not the same as Y. <br>

An example input is 'y', and it will go as follows:
```bash
Hello! Are you a registered user? (Y/N):
Y

Enter your Ashoka email:
```
The program will only accept email IDs with the domain @ashoka.edu.in, and will throw an error for any other domain named email.

Post this, it will prompt for your email and password. You

```bash
Enter your Ashoka email:
medini.chopra_ug23@ashoka.edu.in

Enter your password:
hgyushjndg

You have been logged in successfully.
We offer the following services:
Prerequisites for courses
Semester-wise courses

What would you like to view? (Prereqs/Sem):
```

Finally, the program will continue as the prompts provided, but it is important for the user to note that all the inputs are **case sensitive**. 

```bash
What would you like to view? (Prereqs/Sem): Sem

Send us the semester for which you'd like courses! (Monsoon 2022/Spring 2022):
Monsoon 2022

CS-1101 Introduction to Computer Programming, CS-1216 Computer Organisation and Systems, CS- 1203 Data Structures, CS-1209 Probability and Statistics, CS-1390 
Introduction to Machine Learning, CS-1340 Computer Networks, CS-1319 Programming Language Design and Implementation
```
