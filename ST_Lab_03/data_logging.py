import csv
import serial
import sys
import time

ARDUINO_PORT = 'COM7'  # Passe den COM-Port an deinen Arduino an
ARDUINO_BAUDRATE = 115200
LOG_FILE = 'sensor_data_log.csv'

# Arduino-Serial-Verbindung herstellen
try:
    arduino = serial.Serial(ARDUINO_PORT, ARDUINO_BAUDRATE, timeout=1)
    print(f"Mit Arduino auf {ARDUINO_PORT} verbunden.")
except Exception as e:
    print(f"Fehler beim Verbinden mit Arduino: {e}")
    sys.exit(1)

# CSV-Logger initialisieren
try:
    with open(LOG_FILE, mode='w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Header in die CSV schreiben
        csvwriter.writerow([
            "Timestamp", "Acc X", "Acc Y", "Acc Z", "Gyro X", "Gyro Y", "Gyro Z", "Roll Raw", "Pitch Raw", "Kalman Roll", "Kalman Pitch", 
            "Complementary Roll", "Complementary Pitch", "Joystick X", "Joystick Y", 
            "Joystick Button", "Emergency Button"
        ])
except Exception as e:
    print(f"Fehler beim Initialisieren der CSV-Datei: {e}")
    sys.exit(1)

while True:
    try:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            data = line.split(',')

            accX = float(data[0])
            accY = float(data[1])
            accZ = float(data[2])
            gyroX = float(data[3])
            gyroY = float(data[4])
            gyroZ = float(data[5])
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

            # Aktuelle Zeit holen
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

            # Daten in die CSV schreiben
            with open(LOG_FILE, mode='a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([
                    timestamp, accX, accY, accZ, gyroX, gyroY, gyroZ, roll_raw, pitch_raw, kalRoll, kalPitch, 
                    complRoll, complPitch, joystick_x, joystick_y, 
                    joystick_button, emergency_button
                ])

            # Daten optional ausgeben
            print(f"Daten geloggt: {timestamp}, Roll Raw: {roll_raw}, Pitch Raw: {pitch_raw}")

    except KeyboardInterrupt:
        print("Programm beendet.")
        break
    except Exception as e:
        print(f"Fehler: {e}")

# Ressourcen freigeben
arduino.close()
