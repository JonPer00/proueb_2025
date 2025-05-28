# Programmierübung Aufgabe 2 
## Hier werden Daten aus einer CSV-Datei Analysiert und geplottet 


## Umgang mit PDM

- Zum Aufsetzten eines Projektes einmalig `pmd init`
- Zum installieren eines Projektes nach dem clonen `pmd install`
- Zum Hinzufügen eines Paketes `pdm add <packetname>`

- `gitignore` legt fest, was von git ignoriert wird.  Hier muss __immer vor__ dem ersten Comit der Ordner `.venv` drin stehen. 

## Nutzung des Projektes 


Dann nutzt man [`diesen Link`](https://github.com/JonPer00/proueb_2025) um das Repository in Visual Sudio Code zu Klonen. 

Lediglich `pdm install` reicht aus, um alle anderen Datei mitzuinstallieren. 
Nun muss man nurnoch unter Extentions "Streamlit Runner" installieren und dann mittel `pdm add streamlit` die dazugehörigen Dateien installieren. 

Um die Daten aus einer __CSV__ Datei analysieren zu können, muss nun die Datei main_ausgabe.py mittels Streamlit ausgeführt werden. 
Das kann man ganz einfach, indem mann einen rechtklick auf "main_ausgabe.py" macht, und auf "Run with Streamlit" klickt. 

Nun startet die Ausgabe im Browser unter "localhost". 
Bei Veränderung im Code ist ledigliches Speicher und Reloaden der Browserseite nötig, um die Veränderung sehen zu können. 

ps: Die Grafik inst Interaktiv. 

Hier noch eine kleiner prelook auf die Grafik: 
 ![](https://github.com/JonPer00/proueb_2025/blob/main/figures/Plotinter.png?raw=true)
