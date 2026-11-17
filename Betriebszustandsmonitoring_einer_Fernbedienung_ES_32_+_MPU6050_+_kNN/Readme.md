# Betriebszustandsmonitoring einer Fernbedienung (ESP32 + MPU6050 + kNN)

Praktikumsprojekt im Modul **Sensortechnik** (Studiengang Informations- und Kommunikationstechnik).

Ziel ist ein Betriebszustandsmonitoring für eine Fernbedienung. Mit einem ESP32 und dem Bewegungssensor MPU6050 werden Beschleunigungs- und Gyroskopdaten erfasst. Ein k-Nearest-Neighbor-Klassifikator (kNN) erkennt daraus automatisch den aktuellen Zustand:

| Zustand | Beschreibung |
|---|---|
| **Ruhe** | Fernbedienung liegt still |
| **Transport** | Fernbedienung wird getragen / bewegt |
| **Betrieb** | Fernbedienung wird aktiv benutzt |

## Inhalt

- [Hardware](#hardware)
- [Signalverarbeitung und Merkmale](#signalverarbeitung-und-merkmale)
- [Klassifikation mit kNN](#klassifikation-mit-knn)
- [Echtzeit-Vorhersage](#echtzeit-vorhersage)
- [Ergebnisse](#ergebnisse)
- [Korrelationsanalyse](#korrelationsanalyse)
- [Projekt starten](#projekt-starten)

## Hardware

**Benötigtes Material**

- ESP32-Board
- MPU6050 (3-Achsen-Beschleunigungssensor + 3-Achsen-Gyroskop)
- Computer
- Breadboard und Jumperkabel

**Pinbelegung**

| MPU6050 | ESP32 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SDA | G21 |
| SCL | G22 |

Der ESP32 arbeitet mit 3,3 V und wird über USB (5 V) versorgt. Die Kommunikation mit dem Sensor läuft über I²C (Standard-Pins G21 = SDA, G22 = SCL). Der MPU6050 liefert 16-Bit-Rohwerte (Zweierkomplement) mit 10 Hz. Der ESP32 sendet die Messwerte über die serielle Schnittstelle an den Computer, auf dem die Auswertung und der kNN-Klassifikator laufen.

## Signalverarbeitung und Merkmale

Die Zeitreihen der sechs Kanäle (`AccX`, `AccY`, `AccZ`, `GyroX`, `GyroY`, `GyroZ`) werden in Zeitfenster (30 Messwerte) unterteilt. Pro Fenster und Kanal werden vier statistische Merkmale berechnet:

- **Mittelwert**: durchschnittliche Bewegung im Fenster
- **Standardabweichung**: Streuung der Daten
- **Maximum** und **Minimum**: Extremwerte der Bewegung

Daraus ergibt sich ein Merkmalsvektor mit 24 Merkmalen, z. B. `mean_x`, `std_x`, `max_x`, `min_x`, `mean_gyro_x`, …

## Klassifikation mit kNN

- Die Merkmalsvektoren werden in Trainings- und Testdaten aufgeteilt und skaliert.
- Der kNN-Klassifikator bestimmt die euklidische Distanz zwischen einem neuen Datenpunkt und allen Trainingspunkten. Die Klasse ergibt sich aus der Mehrheit der `k` nächsten Nachbarn.
- Für `k` wurde durch Experimente der Wert **k = 20** gewählt. Das ist ein Kompromiss zwischen Varianz (kleines k, Overfitting) und Bias (großes k, Mehrheitsklasse dominiert).

Bestimmung des optimalen k:

```python
from sklearn.neighbors import KNeighborsClassifier

for k in range(1, 30):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    print(f"Genauigkeit für k={k}:", knn.score(X_test, y_test))
```

Zusätzlich wird ein zweites Modell direkt mit den **Rohdaten** trainiert (gleiche Skalierung), um den Nutzen der Merkmalsberechnung direkt zu vergleichen.

## Echtzeit-Vorhersage

Die Sensordaten werden kontinuierlich über die serielle Schnittstelle (`pyserial`) empfangen und in einem Puffer (`deque`) mit den letzten 120 Messungen gehalten. Sobald der Puffer voll ist, werden Merkmale berechnet, skaliert und an das kNN-Modell übergeben. Der vorhergesagte Zustand wird in der Konsole ausgegeben.

Ausschnitt (gekürzt):

```python
def calculate_features(df):
    features = []
    window_size = 30
    for i in range(0, len(df), window_size):
        window = df.iloc[i:i + window_size]
        mean_x = window['AccX'].mean()
        std_x = window['AccX'].std()
        # ... weitere Merkmale für alle Kanäle (max, min, Gyroskop)
        features.append([mean_x, std_x, ...])
    return pd.DataFrame(features, columns=['mean_x', 'std_x', ...])


def read_serial_data():
    global current_state
    while running:
        line = ser.readline().decode('utf-8').strip()
        values = [float(x) for x in line.split(",")]
        data_queue.append(values)
        if len(data_queue) == 120:
            window = pd.DataFrame(list(data_queue), columns=["AccX", ...])
            features_df = calculate_features(window)
            scaled_features = scaler_loaded.transform(features_df)
            prediction = knn_loaded.predict(scaled_features)
            current_state = prediction[0]
            print(f"Vorhergesagter Zustand: {current_state}")
```

## Ergebnisse

| Eingabe | Accuracy |
|---|---|
| Rohdaten | 98,03 % |
| Berechnete Merkmale | **99,44 %** |

**Konfusionsmatrix mit Merkmalen** (Zeilen = wahr, Spalten = vorhergesagt)

| | Betrieb | Ruhe | Transport |
|---|---|---|---|
| **Betrieb** | 71 | 1 | 0 |
| **Ruhe** | 0 | 36 | 0 |
| **Transport** | 0 | 0 | 72 |

**Konfusionsmatrix mit Rohdaten**

| | Betrieb | Ruhe | Transport |
|---|---|---|---|
| **Betrieb** | 3520 | 76 | 4 |
| **Ruhe** | 78 | 1713 | 8 |
| **Transport** | 11 | 0 | 3589 |

Die Merkmalsextraktion verbessert die Trennbarkeit der Zustände, reduziert Fehlklassifikationen und macht das Modell weniger anfällig für Rauschen. Die meisten Verwechslungen treten bei Rohdaten zwischen „Betrieb“ und „Ruhe“ auf.

## Korrelationsanalyse

Eine Korrelationsmatrix (Pearson) der Merkmale dient dazu, redundante Merkmale zu erkennen. Stark korrelierte Merkmale (Betrag nahe 1) enthalten ähnliche Informationen und können entfernt werden. Weitere Ansätze für die Weiterentwicklung:

- Prüfung der statistischen Signifikanz (p-Wert < 0,05)
- Hauptkomponentenanalyse (PCA), falls Achsen physikalisch zusammenhängen
- Feature-Wichtigkeit z. B. mit Random Forest oder Gradient Boosting

## Projekt starten

1. Hardware gemäß Pinbelegung aufbauen und den Arduino-Code auf den ESP32 laden.
2. Python-Abhängigkeiten installieren:
   ```bash
   pip install pyserial pandas numpy scikit-learn matplotlib seaborn
   ```
3. Serielle Schnittstelle im Python-Skript anpassen (z. B. `COM3` oder `/dev/ttyUSB0`).
4. Skript starten. Der aktuell erkannte Zustand erscheint in der Konsole.

## Quellen

- [datascientest: kNN-Algorithmus](https://datascientest.com/en/knn-what-is-the-knn-algorithm)
- [datatab: Pearson-Korrelation](https://datatab.de/tutorial/pearson-korrelation)
- [IBM: kNN](https://www.ibm.com/topics/knn)
