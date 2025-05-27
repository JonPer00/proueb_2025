import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import os
import json

# Hilfsfunktion: Absoluten Pfad erstellen
def resolve_path(relative_path):
    """Erstellt einen absoluten Pfad basierend auf dem Skriptverzeichnis."""
    base_path = os.path.dirname(__file__)  # Verzeichnis des aktuellen Skripts
    return os.path.join(base_path, relative_path)

# JSON-Datei laden
def load_person_db():
    """Lädt die person_db.json und gibt die Daten zurück."""
    try:
        with open(resolve_path('../data/person_db.json'), 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Die Datei '../data/person_db.json' wurde nicht gefunden.")
        return []
    except json.JSONDecodeError:
        st.error("Fehler beim Lesen der JSON-Datei.")
        return []

# EKG-Daten plotten
def plot_ekg_data(file_path):
    """Lädt und plottet die EKG-Daten aus einer .txt-Datei."""
    try:
        data = np.loadtxt(file_path)  # EKG-Daten aus der Datei laden
        plt.figure(figsize=(10, 4))
        plt.plot(data, label="EKG-Daten")
        plt.title("EKG-Daten")
        plt.xlabel("Zeit")
        plt.ylabel("Amplitude")
        plt.legend()
        st.pyplot(plt)  # Plot in Streamlit anzeigen
    except FileNotFoundError:
        st.error(f"Die Datei '{file_path}' wurde nicht gefunden.")
    except ValueError:
        st.error(f"Die Datei '{file_path}' konnte nicht gelesen werden. Überprüfen Sie das Format.")

# Streamlit-Seite
def main():
    st.title("EKG-Daten Plotter")
    st.write("Wählen Sie einen Probanten und einen EKG-Test aus, um die Daten zu plotten.")

    # Personendaten laden
    person_db = load_person_db()

    if person_db:
        # Dropdown-Menü für Probanten
        probanten_namen = [f"{person['firstname']} {person['lastname']}" for person in person_db]
        selected_person = st.selectbox("Probant auswählen:", probanten_namen)

        # Ausgewählten Probanten finden
        probant = next((p for p in person_db if f"{p['firstname']} {p['lastname']}" == selected_person), None)

        if probant:
            st.write(f"**Name:** {probant['firstname']} {probant['lastname']}")
            st.write(f"**Geburtsjahr:** {probant['date_of_birth']}")

            # Dropdown-Menü für EKG-Tests
            ekg_tests = probant["ekg_tests"]
            test_options = [f"Test-ID: {test['id']} - Datum: {test['date']}" for test in ekg_tests]
            selected_test = st.selectbox("EKG-Test auswählen:", test_options)

            # Ausgewählten Test finden
            test = next((t for t in ekg_tests if f"Test-ID: {t['id']} - Datum: {t['date']}" == selected_test), None)

            if test:
                st.write(f"**Test-ID:** {test['id']}")
                st.write(f"**Datum:** {test['date']}")

                # Plot-Button
                if st.button("EKG-Daten plotten"):
                    plot_ekg_data(resolve_path(test["result_link"]))
    else:
        st.warning("Keine Probanten verfügbar.")

if __name__ == "__main__":
    main()