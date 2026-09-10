#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Einlesen von Sensordaten ueber eine serielle Schnittstelle

Liest eine definerte Anzahl von Datenwerten aus einer seriellen Schnittstelle ein.
Mehrere Datenwerte in einer Zeile müssen durch ein Komma getrennt sein.

Voraussetzungen:
Installation von PySerial ueber conda install pyserial

Die Parameter sind entsprechend der Messaufgabe anzupassen:
LENGTH:   Anzahl der Werte, nach der die Daten gespeichert und das Programm beendet werden
PORT:     Schnittstelle, diese darf nicht gleichzeitig durch den seriellen Monitor belegt sein
BAUD:     muss der im Arduino-Programm gewaehlten Baudrate entsprechend
HEADERS:  je nach Anzahl der durch Komma getrennten Datenwerte anpassen und benennen
CSV_FILE: Name der CSV-Datei fuer die Datenspeicherung, falls vorhanden, wird ueberschrieben
COLORS:   unterschiedliche Linientypen fuer bis zu 6 Diagramme
"""


import time
from datetime import datetime
import serial
import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters


__author__ = "Joerg Dahlkemper"
__version__ = "200703"


LENGTH = 10
PORT = "COM4"
BAUD = 115200
HEADERS = ["Temperature", "Humidity", "Timestamp"]
CSV_FILE = "measurement.csv"
COLORS = ['b', 'g--', 'r:', 'k-.', 'c', 'm']

def main():
    """ Hauptfunktion zum Einlesen der Werte der Schnittstelle """

    ser = serial.Serial(PORT, BAUD)
    time.sleep(1)

    data = []

    for i in range(LENGTH):
        line = ser.readline()
        values = [float(str) for str in line.decode().rstrip().split(',')]  # Werte anhaengen
        values.append(datetime.now())  # Zeitstempel hinzufuegen
        data.append(values)
        print(i, values[:-1])  # Kontrollausgabe ohne Zeitstempel
        time.sleep(0.1)  # idle time, um Rechner nicht voll auszulasten
    ser.close()

    # fuer komfortable Datenanlyse Nutzung von pandas
    # see https://pandas.pydata.org/getting_started.html
    dataframe = pd.DataFrame(data, columns=HEADERS)

    print("\n", dataframe)
    dataframe.to_csv(CSV_FILE)  # CSV-Datei speichern

    # Anzeige aller in HEADERS genannten Datenreihen
    register_matplotlib_converters()
    for k, header in enumerate(HEADERS[:-1]):
        plt.plot(dataframe['Timestamp'], dataframe[header], COLORS[k], label=header)
    plt.xlabel("Zeit")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()
