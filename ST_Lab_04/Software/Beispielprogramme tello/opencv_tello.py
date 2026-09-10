"""
Streamin a tello video into openCV

There is a time lag of several seconds of the video stream.
By use of grab - retrieve instead of read the frames are discarded unprocessed

Joerg Dahlkemper
2022-07-12
"""


import socket
import cv2

# set to True for takeoff after start and land by pressing 'q' in active video frame
TAKEOFF = False

# for tello access
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
DISCARDED_FRAMES = 2
tello_address = (TELLO_IP, TELLO_PORT)

# for receiving from tello
VS_UDP_IP = '0.0.0.0'
VS_UDP_PORT = 11111

# Create a socket for communication
# Address family: AF_INET (IPv4), Socket type: SOCK_DGRAM (UDP)
socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
# Set to listen
socket.bind (('', TELLO_PORT))

# Throw 'command' text to use command mode
socket.sendto ('command'.encode (' utf-8 '), tello_address)
# take off
if TAKEOFF:
    socket.sendto ('takeoff'.encode (' utf-8 '), tello_address)
# Start video streaming
socket.sendto ('streamon'.encode (' utf-8 '), tello_address)

# udp_video_address = 'udp://' + VS_UDP_IP + ':' + str (VS_UDP_PORT)  # seems not to work in Lab 801
udp_video_address = 'udp://' + TELLO_IP + ':' + str (VS_UDP_PORT)

video_stream = cv2.VideoCapture (udp_video_address)
while True:
    for _ in range(DISCARDED_FRAMES):
        video_stream.grab()
    ret, frame = video_stream.retrieve()
    if ret:
        cv2.imshow('frame', frame)
    if cv2.waitKey(1)&0xFF == ord ('q'):
        break

video_stream.release ()
cv2.destroyAllWindows ()

# Stop video streaming
socket.sendto ('streamoff'.encode (' utf-8 '), tello_address)
# Landing
if TAKEOFF:
    socket.sendto ('land'.encode (' utf-8 '), tello_address)

socket.close()
