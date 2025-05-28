import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Daten einlesen
dataframe = pd.read_csv('../data/activity.csv')

st.title("Analyse der Aktivitätsdaten")
st.header("Bitte die Maximale Herzfrequenz eingeben")

# Maximale Herzfrequenz per App-Eingabe (nur für die Achsenskalierung)
hr_max = st.number_input("Maximale Herzfrequenz (bpm)", min_value=50, max_value=250, value=int(dataframe["HeartRate"].max()))

# Berechnen der Gesamtdauer in Minuten und Sekunden
total_seconds = int(dataframe["Duration"].sum())
minutes = total_seconds // 60
seconds = total_seconds % 60

# Ausgabe von Mittelwert, Maximalwert und Gesamtdauer
st.table({
    "Ø Leistung (Watt)": [f"{dataframe['PowerOriginal'].mean():.1f}"],
    "Max. Leistung (Watt)": [f"{dataframe['PowerOriginal'].max():.0f}"],
    "Gesamtdauer (m:s)": [f"{minutes}:{seconds:02d}"],
})


# Feste Zonen-Grenzen 
zonengrenzen = [90, 110, 140, 160, 180, 210]  

# Farben für die Herzfrequenz-Zonen
farben = [
    "rgba(250,240,255,0.2)",  # Zone 1
    "rgba(200,220,255,0.4)",  # Zone 2
    "rgba(140,200,255,0.6)",  # Zone 3
    "rgba(80,180,255,0.8)",   # Zone 4
    "rgba(20,160,255,1)",   # Zone 5
]

# Funktion zur Zonenzuordnung
def get_zone(hr):
    if hr < zonengrenzen[1]:
        return "Zone1"
    elif hr < zonengrenzen[2]:
        return "Zone2"
    elif hr < zonengrenzen[3]:
        return "Zone3"
    elif hr < zonengrenzen[4]:
        return "Zone4"
    elif hr < zonengrenzen[5]:
        return "Zone5"
    else:
        return "Zone5+"

dataframe["Zone"] = dataframe["HeartRate"].apply(get_zone)


# Plotting mit Plotly
window_size = 30
zeit_achsen = dataframe.index / 60

fig = go.Figure()

# Rechtecke für die festen Zonen zeichnen
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
        range=[0, hr_max]  # Nur die Achse skaliert sich, die Zonen bleiben fix!
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


# Zeit pro Zone berechnen 1 Zeile = 1 Sekunde
zone_counts = dataframe["Zone"].value_counts().sort_index()
zone_minutes = (zone_counts / 60).apply(lambda x: f"{x:.2f}")  # Minuten als String mit 2 Nachkommastellen
zone_percent = (zone_counts / len(dataframe) * 100).apply(lambda x: f"{x:.1f}")  # Prozent als String mit 1 Nachkommastelle

st.write("### Verbrachte Zeit in den Zonen (in Minuten):")
st.table(zone_minutes.to_frame(name="Minuten"))

st.write("### Prozentuale Verteilung der Zeit in den Zonen:")
st.table(zone_percent.to_frame(name="Zeit (%)"))


# Prozentualer Anteil der Leistung pro Zone
zone_power_percent = (dataframe.groupby("Zone")["PowerOriginal"].sum() / dataframe["PowerOriginal"].sum() * 100)
zone_power_percent = zone_power_percent.apply(lambda x: f"{x:.1f}")  # Format als String mit 1 Nachkommastelle
st.write("### Prozentuale Verteilung der Leistung in den Zonen:")
st.table(zone_power_percent.to_frame(name="Leistung (%)"))


