import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Daten einlesen
dataframe = pd.read_csv('../data/activity.csv')

# Maximale Herzfrequenz per App-Eingabe
hr_max = st.number_input("Maximale Herzfrequenz (bpm)", min_value=100, max_value=250, value=int(dataframe["HeartRate"].max()))

# Zonen berechnen (verschieben sich mit hr_max)
untergrenzen_zonen = {}
zone = 1
for faktor in [0.5, 0.6, 0.7, 0.8, 0.9]:
    untergrenzen_zonen["Zone" + str(zone)] = float(hr_max * faktor)
    zone = zone + 1

# Einteilung der Zonen
list_zone = []
for current_hr in dataframe["HeartRate"]:
    if current_hr >= untergrenzen_zonen["Zone5"]:
        list_zone.append("Zone5")
    elif current_hr >= untergrenzen_zonen["Zone4"]:
        list_zone.append("Zone4")
    elif current_hr >= untergrenzen_zonen["Zone3"]:
        list_zone.append("Zone3")
    elif current_hr >= untergrenzen_zonen["Zone2"]:
        list_zone.append("Zone2")
    elif current_hr >= untergrenzen_zonen["Zone1"]:
        list_zone.append("Zone1")
    else:
        list_zone.append("Zone0")

dataframe["Zone"] = list_zone

# Zeit pro Zone berechnen (Annahme: 1 Zeile = 1 Sekunde)
zone_counts = dataframe["Zone"].value_counts().sort_index()
zone_minutes = (zone_counts / 60).round(2)
zone_percent = (zone_counts / len(dataframe) * 100).round(1)

# Ausgabe: Zeit pro Zone
st.write("### Verbrachte Zeit in den Zonen (in Minuten):")
st.write(zone_minutes)

st.write("### Prozentuale Verteilung der Zeit in den Zonen:")
st.write(zone_percent)

# Ausgabe von Mittelwert, Maximalwert und Gesamtdauer
st.write("Mittelwert PowerOriginal:", dataframe["PowerOriginal"].mean())
st.write("Maximalwert PowerOriginal:", dataframe["PowerOriginal"].max())
st.write("Gesamtdauer (Summe Duration):", dataframe["Duration"].sum())

# Plotting mit Plotly
window_size = 30
zeit_achsen = dataframe.index / 60

fig = go.Figure()

# Farben für die Herzfrequenz-Zonen
farben = [
    "rgba(250,240,255,0.3)",  # Zone 1
    "rgba(200,220,255,0.3)",  # Zone 2
    "rgba(140,200,255,0.3)",  # Zone 3
    "rgba(80,180,255,0.3)",   # Zone 4
    "rgba(20,160,255,0.3)",   # Zone 5
]

# Zonen als farbige Rechtecke im Hintergrund (rechte Y-Achse)
zonengrenzen = [0] + [untergrenzen_zonen[f"Zone{i}"] for i in range(1, 5)] + [hr_max]

for i in range(1, 6):
    fig.add_shape(
        type="rect",
        x0=zeit_achsen.min(), x1=zeit_achsen.max(),
        y0=zonengrenzen[i-1], y1=zonengrenzen[i],
        fillcolor=farben[i-1],
        line=dict(width=0),
        layer="below",
        yref="y2"
    )
    fig.add_annotation(
        x=zeit_achsen.max(),
        y=(zonengrenzen[i-1] + zonengrenzen[i]) / 2,
        text=f"Zone {i}",
        showarrow=False,
        font=dict(color="grey", size=10),
        bgcolor="white",
        opacity=0.7,
        xanchor="right",
        yref="y2"
    )

# Power (linke Achse)
fig.add_trace(go.Scatter(
    x=zeit_achsen,
    y=dataframe["PowerOriginal"].rolling(window=window_size).mean(),
    mode='lines',
    name='Leistung',
    yaxis='y1'
))

# HeartRate (rechte Achse)
fig.add_trace(go.Scatter(
    x=zeit_achsen,
    y=dataframe["HeartRate"].rolling(window=window_size).mean(),
    mode='lines',
    name='Herzfrequenz',
    yaxis='y2'
))

# Layout: Achsen, Titel, Legende
fig.update_layout(
    title="Durchschnitt Herzfrequenz und Leistung",
    xaxis_title="Zeit (Minuten)",
    yaxis=dict(
        title="Leistung (Watt)",
        side="left",
        range=[0, dataframe["PowerOriginal"].max()]
    ),
    yaxis2=dict(
        title="Herzfrequenz (bpm)",
        overlaying="y",
        side="right",
        range=[0, hr_max]
    ),
    legend=dict(
        orientation="h",
        x=1.0, y=1.0,
        xanchor="right",
        yanchor="bottom",
        font=dict(size=10),
        bordercolor="LightGray",
        borderwidth=1
    ),
    template="simple_white"
)

st.plotly_chart(fig, use_container_width=True)