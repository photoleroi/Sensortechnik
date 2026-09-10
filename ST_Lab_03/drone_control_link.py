import serial
import socket
import threading
import time
import sys

#59d6f5

#control_source = "STICK"
control_source = "MPU"
mpu_mode = "RAW"
#mpu_mode = "KALMAN"
#mpu_mode = "COMPLEMENTARY"
#mpu_mode = "KALMAN"

# Konfiguration
TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
LOCAL_PORT = 9000
ARDUINO_PORT = 'COM7'  # Passe den COM-Port an deinen Arduino an
ARDUINO_BAUDRATE = 115200

# Tello UDP-Socket erstellen
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', LOCAL_PORT))

def send_command(command):
    try:
        sock.sendto(command.encode('utf-8'), (TELLO_IP, TELLO_PORT))
    except Exception as e:
        print(f"Fehler beim Senden des Befehls: {e}")

def receive_response():
    while True:
        try:
            response, _ = sock.recvfrom(1024)
            print(f"Tello: {response.decode('utf-8')}")
        except Exception as e:
            print(f"Fehler beim Empfang der Antwort: {e}")
            break

# Empfangsthread starten
recv_thread = threading.Thread(target=receive_response)
recv_thread.daemon = True
recv_thread.start()

# Arduino-Serial-Verbindung herstellen
try:
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
    print(f"Mit Arduino auf {ARDUINO_PORT} verbunden.")
except Exception as e:
    print(f"Fehler beim Verbinden mit Arduino: {e}")
    sys.exit(1)

# Drohne initialisieren
send_command("command")
time.sleep(1)

drone_state = "ground"
last_joystick_button_state = 1

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            data = line.split(',')

            roll_raw = float(data[6])
            pitch_raw = float(data[7])
            kalRoll = float(data[8])
            kalPitch = float(data[9])
            complRoll = float(data[10])
            complPitch = float(data[11])
            joystick_x = int(data[12])
            joystick_y = int(data[13])
            joystick_button = int(data[14])
            emergency_button = int(data[15])

            # Notaus
            if emergency_button == 0:
                send_command("emergency")
                print("NOTAUS aktiviert! Alle Motoren gestoppt.")

            # Starten und Landen
            if joystick_button == 0 and last_joystick_button_state == 1:
                if drone_state == "ground":
                    send_command("takeoff")
                    print("Drohne gestartet.")
                    time.sleep(1)  # Verhindert mehrfaches Auslösen
                    drone_state = "air"
                elif drone_state == "air":
                    send_command("land")
                    print("Drohne gelandet.")
                    time.sleep(1)  # Verhindert mehrfaches Auslösen
                    drone_state = "ground"

            last_joystick_button_state = joystick_button

            if control_source == "STICK":
                scaling = 1/100
                midpoint = 13000
                roll = joystick_y
                pitch = joystick_x
            else:
                scaling = 100/45 # scale to 100 at 45 degrees
                midpoint = 0
                if mpu_mode == "RAW":
                    roll = roll_raw
                    pitch = pitch_raw
                elif mpu_mode == "KALMAN":
                    roll = kalRoll
                    pitch = kalPitch
                elif mpu_mode == "COMPLEMENTARY":
                    roll = complRoll
                    pitch = complPitch


            left_right = (roll - midpoint) * scaling
            if left_right > 100:
                left_right = 100
            elif left_right < -100:
                left_right = -100

            forward_backward = (pitch - midpoint) * scaling
            if forward_backward > 100:
                forward_backward = 100
            elif forward_backward < -100:
                forward_backward = -100

            # rc-Befehl senden
            rc_command = f"rc {int(left_right)} {int(forward_backward)} 0 0"
            send_command(rc_command)
            print(f"RC-Befehl gesendet: {rc_command}")

    except KeyboardInterrupt:
        print("Programm beendet.")
        break
    except Exception as e:
        print(f"Fehler: {e}")

# Ressourcen freigeben
arduino.close()
sock.close()
