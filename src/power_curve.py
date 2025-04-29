import numpy as np
from sort import bubble_sort
import matplotlib.pyplot as plt

def load_data(file_path):
    """
    Load data from a CSV file and return it as a dictionary.
    Assumes the CSV file has a column 'PowerOriginal'.
    """
    import pandas as pd
    data = pd.read_csv(file_path)
    return {'PowerOriginal': data['PowerOriginal'].tolist()}

def plot_power_curve(file_path):
    # Daten laden
    data = load_data(file_path)
    power_W = data['PowerOriginal']

    # Daten sortieren
    sorted_power_W = bubble_sort(power_W)
    sorted_power_W = sorted_power_W[::-1]  # Umkehren für die Grafik
    time = list(range(len(sorted_power_W)))  # Zeit in Minuten
    time = np.array(time)/60

    # Grafik erstellen
    plt.figure(figsize=(10, 6))
    plt.fill_between(time, sorted_power_W, color='lightgray', alpha=0.5)
    plt.plot(time, sorted_power_W, linestyle='-', color='r', label='Power Curve')
    plt.title('Power Curve')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Power (W)')
    plt.grid(True)
    plt.legend()
    plt.xlim(left=0)  # x-Achse bei 0 starten
    plt.ylim(bottom=0) # y-Achse bei 0 starten
    plt.savefig('figures/leistungskurve1.png')
    plt.close()


if __name__ == "__main__":
    plot_power_curve('data/activity.csv')
