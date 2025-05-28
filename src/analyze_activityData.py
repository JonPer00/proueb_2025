#%% Zelle 1
import pandas as pd

dataframe = pd.read_csv('../data/activity.csv')
dataframe
dataframe.columns

# %%
print(dataframe["HeartRate"].min())
dataframe["HeartRate"].max()
dataframe["HeartRate"].mean()
df_statistics = dataframe[["HeartRate", "PowerOriginal"]].describe()

# %% Mittelwert PowerOriginal und HeartRate auf Zeit
print(dataframe["PowerOriginal"].mean())
dataframe["PowerOriginal"].max()
print(dataframe["Duration"].sum)
print(darafr)


# %%
untergrenzen_zonen = {}
hr_max = dataframe["HeartRate"].max()
zone = 1
for faktor in [0.5, 0.6, 0.7, 0.8, 0.9]:
    untergrenzen_zonen["Zone" + str(zone)] = float(hr_max * faktor/1)
    #print("Zone:", zone)
    #print(hr_max * faktor)
    zone = zone + 1

untergrenzen_zonen
# %%
list_zone = []
dataframe["Zone"] = None

for index, row in dataframe.iterrows():
    #print(index)
    print(row["HeartRate"])
    current_hr = row["HeartRate"]
    
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
dataframe["Zone"].value_counts()


# %%
dataframe

dataframe.groupby("Zone").mean()
# %%
df_group = dataframe.groupby("Zone").mean()
df_group[["HeartRate", "PowerOriginal"]]


# %% Grafik erstellen mittels matplotlib
import matplotlib.pyplot as plt

window_size = 30  # Fenstergröße für gleitenden Mittelwert

plt.figure(figsize=(12, 5))

# X-Achse in Minuten umrechnen
zeit_achsen = dataframe.index / 60  # Annahme: 1 Zeile = 1 Sekunde

# Gleitende Mittelwerte plotten
plt.plot(zeit_achsen, dataframe["HeartRate"].rolling(window=window_size).mean(), label="HeartRate")
plt.plot(zeit_achsen, dataframe["PowerOriginal"].rolling(window=window_size).mean(), label="PowerOriginal")

# Zonengrenzen als horizontale Linien auf der Y-Achse markieren
for i in range(1, 6):
    y = untergrenzen_zonen[f"Zone{i}"]
    plt.axhline(y, color='grey', linestyle='--', linewidth=0.5)
    plt.text(0, y, f'Zone {i}', va='bottom', ha='left', color='grey', fontsize=9, backgroundcolor='white')

plt.title("Durchschnitt Herzfrequenz und Power")
plt.xlabel("Zeit [Minuten]")
plt.ylabel("Watt/Herzfrequenz")
plt.legend()
plt.tight_layout()
plt.show()

#%% grafik mittels plotly 
import plotly.graph_objects as go

# Fenstergröße für den Mittelwert
window_size = 30

# Zeit in Minuten (statt Index)
zeit_achsen = dataframe.index / 60

# Plot-Objekt erstellen
fig = go.Figure()

# Farben für die Herzfrequenz-Zonen
farben = [
    "rgba(250,240,255,0.3)",  # Zone 1
    "rgba(200,220,255,0.3)",  # Zone 2
    "rgba(140,200,255,0.3)",  # Zone 3
    "rgba(80,180,255,0.3)",   # Zone 4
    "rgba(20,160,255,0.3)",   # Zone 5
]

# Zonen als farbige Rechtecke im Hintergrund
zonengrenzen = [0] + [untergrenzen_zonen[f"Zone{i}"] for i in range(1, 6)] + [dataframe["HeartRate"].max() + 10]
for i in range(1, 6):
    fig.add_shape(
        type="rect",
        x0=zeit_achsen.min(), x1=zeit_achsen.max(),
        y0=zonengrenzen[i-1], y1=zonengrenzen[i],
        fillcolor=farben[i-1],
        line=dict(width=0),
        layer="below",
        yref="y2"  # Rechte Y-Achse (Herzfrequenz)
    )
    # Zonen-Text an der Y-Achse
    fig.add_annotation(
        x=zeit_achsen.min(),
        y=(zonengrenzen[i-1] + zonengrenzen[i]) / 2,
        text=f"Zone {i}",
        showarrow=False,
        font=dict(color="grey", size=10),
        bgcolor="white",
        opacity=0.7,
        xanchor="left",
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
    xaxis_title="Zeit [Minuten]",
    yaxis=dict(
        title="Leistung [Watt]",
        side="left"
    ),
    yaxis2=dict(
        title="Herzfrequenz [bpm]",
        overlaying="y",
        side="right"
    ),
    legend=dict(
        orientation="h",      # horizontal
        x=0.5, y=0.97,        # ganz oben zentriert
        xanchor="right",
        yanchor="bottom",
        font=dict(size=10),
        bordercolor="LightGray",
        borderwidth=1
    ),
    template="simple_white"
)

fig.show()

# %%
