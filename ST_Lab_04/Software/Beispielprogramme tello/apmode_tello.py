"""
Tello Python3 Control for AP mode to enable formation flight

author: Joerg Dahlkemper
date: 2020-01-25

Preparation
-----------
Drones must be connected to Access point by sending the commands:
command
ap <SSID> <PASSWORD>
to retrieve the serial number use sn?

Usage
-----
To send a command to the first drone use "1>command", to the 2nd "2>command" and to all "*>command".
"""

import threading 
import socket
import sys
import time


HOST = ''
PORT = 9000
DRONE_IPS = ["192.168.179.20", "192.168.179.21"]
DRONE_PORT = 8889



# Create UDP sockets
localaddr = (HOST,PORT)
tello_addresses = [] 
for drone_ip in DRONE_IPS:
    tello_addresses.append((drone_ip, DRONE_PORT))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(localaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print('\r\nControl multiple Tello Drones connected to the same Access Point')
print('----------------------------------------------------------------')
print('\n[i] start a command with "1>" for the 1st drone, "2>" for the 2nd and "*>" for all drones')
print('[i] To quit the demo type "end" and <CTRL>+C.\n')
drone_count = len(DRONE_IPS)
for i, ip in enumerate(DRONE_IPS):
    print('[i] Drone #%d expected at IP %s' %(i+1, ip))
print('[i] Ready to execute commands ...\n')


# Create recvThread for asynchronous response check
recvThread = threading.Thread(target=recv)
recvThread.start()

while True: 

    try:
        msg = input("");

        if not msg:
            break  

        if 'end' in msg:
            print('[i] User request to quit')
            break

        if '>' in msg:
            [id, cmd] = msg.split(">", 1) # split into id and rest
            # Send data
            cmd_encoded = cmd.encode(encoding="utf-8")
            if id.isdigit():
                drone_id = int(id)
                if drone_id>0 and drone_id<=drone_count:
                    sent = sock.sendto(cmd_encoded, tello_addresses[drone_id-1])
                else:
                    print('[!] %d is not a valid id, must be "*" or a number between 1 and %d' %(drone_id, drone_count))
                
            elif id == "*":
                for tello_address in tello_addresses:
                    sent = sock.sendto(cmd_encoded, tello_address)
            else:
                print('[!] %s is not a valid id, must be "*" or a number between 1 and %d' %(id, drone_count))
        else:
            print('[i] Command must start with "1>" to specify drone or "*>" for all drones')
            
    except KeyboardInterrupt:
        print ('[i] Keyboard Interrupt')
        break

print ('[i] Closing socket and exiting')
sock.close()
exit(0)
