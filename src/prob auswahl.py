import streamlit as st
import json
import matplotlib.pyplot as plt
import numpy as np

# Session State initialisieren
if "state" not in st.session_state:
    st.session_state.state = "start"  # Standardzustand ist die Startseite
if "selected_test" not in st.session_state:
    st.session_state.selected_test = None  # Standardwert für den ausgewählten Test

# Callback-Funktionen
def go_to_probantenauswahl():
    st.session_state.state = "probantenauswahl"

def go_to_start():
    st.session_state.state = "start"

def go_to_plot(test_data):
    st.session_state.state = "plot"
    st.session_state.selected_test = test_data

# State Machine
def start_page():
    """Startseite"""
    st.title("Willkommen zur EKG-Datenanalyse")
    st.write("Gedacht zur Analyse von EKG-Daten und um die Daten von Probanten zu verwalten.")
    st.button("Zur Auswahl", on_click=go_to_probantenauswahl)  # Callback verwenden  
    st.image("../data/pictures/startgif.gif", use_container_width=True, caption="EKG-Datenanalyse")

def probantenauswahl_page():
    """Probantenauswahl-Seite"""
    st.title("Probantenauswahl")
    st.write("Bitte wählen Sie einen Probanten aus der Liste aus:")

    # JSON-Datei laden
    try:
        with open('../data/person_db.json', 'r', encoding='utf-8') as file:
            probanten_data = json.load(file)
            probanten = [
                {
                    "id": person["id"],
                    "name": f"{person['firstname']} {person['lastname']}",
                    "date_of_birth": person["date_of_birth"],
                    "picture_path": person["picture_path"],
                    "ekg_tests": person["ekg_tests"]
                }
                for person in probanten_data
            ]
    except FileNotFoundError:
        st.error("Die Datei '../data/person_db.json' wurde nicht gefunden.")
        probanten = []
    except json.JSONDecodeError:
        st.error("Fehler beim Lesen der JSON-Datei.")
        probanten = []

    # Dropdown-Menü zur Auswahl eines Probanten
    if probanten:
        probanten_namen = [probant["name"] for probant in probanten]
        auswahl = st.selectbox("Probant auswählen:", probanten_namen)

        # Details des ausgewählten Probanten anzeigen
        ausgewählter_probant = next((probant for probant in probanten if probant["name"] == auswahl), None)

        if ausgewählter_probant:
            # Spalten erstellen mit Abstand
            col1, spacer, col2, col3 = st.columns([1, 0.5, 2, 2])  # Abstand zwischen Bild und Details

            # Spalte 1: Bild anzeigen
            with col1:
                if ausgewählter_probant["picture_path"]:
                    try:
                        st.image(f"../{ausgewählter_probant['picture_path']}", caption="Probantenbild", width=150)
                    except FileNotFoundError:
                        st.warning("Das Bild konnte nicht geladen werden.")

            # Spalte 2: Details anzeigen
            with col2:
                st.write(f"**ID:** {ausgewählter_probant['id']}")
                st.write(f"**Name:** {ausgewählter_probant['name']}")
                st.write(f"**Geburtsjahr:** {ausgewählter_probant['date_of_birth']}")

            # Spalte 3: EKG-Tests anzeigen
            with col3:
                st.write("### EKG-Tests:")
                for test in ausgewählter_probant["ekg_tests"]:
                    if "result_link" in test:
                        if st.button(f"Ergebnis anzeigen (ID: {test['id']}) - {test['date']}", key=test['id']):
                            # Testdaten in den Session State speichern und zur Plot-Seite wechseln"):
                            go_to_plot(test)
        else:
            st.warning("Kein passender Probant gefunden.")
    else:
        st.write("Keine Probanten verfügbar.")

    # Zurück zur Startseite
    st.button("Zurück zur Startseite", on_click=go_to_start)  # Callback verwenden

def plot_page():
    """Seite zum Plotten der EKG-Daten"""
    st.title("EKG-Daten Plot")
    test_data = st.session_state.selected_test

    if test_data:
        st.write(f"**Test-ID:** {test_data['id']}")
        st.write(f"**Datum:** {test_data['date']}")

        # EKG-Daten laden und plotten
        try:
            with open(test_data["result_link"], 'r') as file:
                data = np.loadtxt(file)  # Annahme: EKG-Daten sind als Textdatei gespeichert
                plt.figure(figsize=(10, 4))
                plt.plot(data, label="EKG-Daten")
                plt.title(f"EKG-Daten für Test-ID {test_data['id']}")
                plt.xlabel("Zeit")
                plt.ylabel("Amplitude")
                plt.legend()
                st.pyplot(plt)
        except FileNotFoundError:
            st.error("Die EKG-Daten konnten nicht geladen werden.")
    else:
        st.warning("Keine Testdaten ausgewählt.")

    # Zurück zur Probantenauswahl
    st.button("Zurück zur Probantenauswahl", on_click=go_to_probantenauswahl)

# State Machine Logik
if st.session_state.state == "start":
    start_page()
elif st.session_state.state == "probantenauswahl":
    probantenauswahl_page()
elif st.session_state.state == "plot":
    plot_page()