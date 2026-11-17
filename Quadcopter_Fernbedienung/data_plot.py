import csv
import matplotlib.pyplot as plt

LOG_FILE = 'transl_fast.csv'

# CSV-Datei einlesen
def read_csv(file_path):
    data = {
        "Timestamp": [], "Roll Raw": [], "Kalman Roll": [], "Complementary Roll": [], "Gyro Y": []
    }
    try:
        with open(file_path, mode='r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                data["Timestamp"].append(row["Timestamp"])
                data["Roll Raw"].append(float(row["Roll Raw"]))
                data["Kalman Roll"].append(float(row["Kalman Roll"]))
                data["Complementary Roll"].append(float(row["Complementary Roll"]))
                data["Gyro Y"].append(float(row["Gyro Y"]))  # Gyro Y in den Joystick Y-Feld geloggt
    except Exception as e:
        print(f"Fehler beim Lesen der CSV-Datei: {e}")
        return None
    return data

# Daten plotten
def plot_data(data):
    if data is None:
        print("Keine Daten zum Plotten verfügbar.")
        return

    plt.figure(figsize=(12, 6))

    # Diagramme hinzufügen
    plt.plot(data["Roll Raw"], label="Roll Raw")
    plt.plot(data["Kalman Roll"], label="Kalman Roll")
    plt.plot(data["Complementary Roll"], label="Complementary Roll")
    plt.plot(data["Gyro Y"], label="Gyro Y")

    # Plot konfigurieren
    plt.xlabel("Sample")
    plt.ylabel("Wert")
    plt.title("Roll-Winkel Plot")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

if __name__ == "__main__":
    data = read_csv(LOG_FILE)
    plot_data(data)