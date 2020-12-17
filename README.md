## Reden ist Gold
Ein Python Script mit welchem Speaker Diarization auf .wav Dateien ausgeführt werden kann. Die Scripts basieren auf dem Resemblyzer Algorithmus von https://github.com/resemble-ai/Resemblyzer, welche von uns für unser spezifisches Problem angepasst wurden.

Wie können die Scripts genutzt werden? Folgend eine Step-by-Step Anleitung für einen einfachen Einstieg.

## Testdaten aufbereiten und Tools installieren:

Source: https://www.srf.ch/play/tv/arena/video/abstimmungs-arena-zur-konzernverantwortungsinitiative?urn=urn:srf:video:a1a54687-eae7-4579-9735-07a1a4227899 

Heruntergeladen und konvertiert mit youtube-dl https://youtube-dl.org/. 

Für die Konvertierung des Videos in eine Audiodatei wird ffmpeg benötigt. 

Installation von Chocolately (Windows Package Manager) für eine einfache spätere Installation von ffmpeg: 
Powershell:
```Powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = 
[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; 
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')) 
```

Poswershell: 
```Powershell 
choco install ffmpeg 
Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')) 
```

In cmd: 
```
Youtubedl.exe https://www.srf.ch/play/tv/arena/video/abstimmungs-arena-zur-konzernverantwortungsinitiative?urn=urn:srf:video:a1a54687-eae7-4579-9735-07a1a4227899 
-x --audio-format wav 
```
 
## Dependecies installieren:

Repository von Resemblyzer: https://github.com/resemble-ai/Resemblyzer 

Resemblyzer braucht den Algorithmus von: https://github.com/google/uis-rnn 

Als Vorgabe wird Visual Studio 2019 mit vollständiger C++ Umgebung benötigt: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community&rel=16 

 
![alt text](plots/C++_Dependency.PNG?raw=true)
 

Als Haupt IDE haben wurde jedoch Visual Studio Code verwendet: https://code.visualstudio.com/docs/?dv=win  

Installation von Python 3.8 (3.9 ist noch nicht für alle dependecies unterstützt): https://www.python.org/downloads/release/python-386/  

Clonen unseres Resemblyzer Repositories: 

Visual Studio Code: git clone https://github.com/NosGigu/RedenIstGold

 

**Installieren einiger weitere Python Pakages:** 

Pytorch: 
```Python
pip install torch===1.7.0 torchvision===0.8.1 torchaudio===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html 
```
Und die anderen requirements des repos: 
```Python
pip install -r .\requirements_demos.txt 
pip install -r .\requirements_package.txt 
```
 

## Versuch mit der erstellten wav Datei der Arena Aufzeichnung: 

Da die komplette Länge unsere Kapazität von Rechenleistung deutlich überschreitet haben wir eine 15 min Version und eine 1 min Version erstellt.
Error bei voller länge:
```
RuntimeError: [enforce fail at ..\c10\core\CPUAllocator.cpp:73] data. DefaultCPUAllocator: not enough memory: you tried to allocate 45909278720 bytes. Buy new RAM! 
```

Die Audiodatei haben wir mit Hilfe von https://mp3cut.net/ gekürzt auf 15 und auf 1 min gekürzt.

Die 15 min Version kann nicht direkt auf Github gespeichert werden aber kann von hier heruntergeladen werden: https://zhaw-my.sharepoint.com/:u:/g/personal/vifiarob_students_zhaw_ch/ERTnmpq_daZCqeFg9BhK5KcB8BAnm4q5osEHQwZu-2jLng?e=9e0wze




## Code Erweiterung durch uns

Im folgenden Abschnitt werden alle Änderungen und Erweiterungen des originalen Codes beschreiben.
Der Originale Code kann dabei unter https://github.com/resemble-ai/Resemblyzer abgerufen werden.


## Arena_1min.py

In dieser Variable wav_fpath wird das Audiofile angegeben:
```Python
wav_fpath = Path(
    "audio_data", "Abstimmungs-Arena» zur Konzernverantwortungsinitiative-a1a54687-eae7-4579-9735-07a1a4227899_1min.wav")
wav = preprocess_wav(wav_fpath)
```

Danach werden die Segmente der Speaker definiert  die der Algorithmus zum trainieren des RNN benötigt.
Ausserdem werden hier auch die Labels der Speaker definiert.
Die Segmente bilden dabei die Abschnitte in Sekunden innerhalb der Audiodatei wo die entsprechende Person bestensfalls alleine am sprechen ist.
```Python
segments = [[00, 11], [14, 30]]
speaker_names = ["Sandro Botz, Moderator", "Karin Keller-Sutter, Bundesrätin"]
speaker_wavs = [
    wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]
```

## Arena_15min.py

Hier parellel zu oben, nur mit der 15 minütigen AudioSource und mehreren Sprechern.

```Python
wav_fpath = Path(
    "audio_data", "Abstimmungs-Arena» zur Konzernverantwortungsinitiative-a1a54687-eae7-4579-9735-07a1a4227899_15min.wav")
wav = preprocess_wav(wav_fpath)
```

```Python
segments = [[113, 140], [34, 50], [190, 230], [873, 910], [764, 800], [672, 720]] 
speaker_names = ["Sandro Botz Moderator", "Backgroundinfo Sprecherin", "Karin Keller-Sutter, Bundesrätin", "Martin Landolt, Präsident BDP", "Gerhard Pfister, Präsident CVP", "Daniel Jositsch, Ständerat SP"] 
speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments] 
```


## demo_utils_1min.py

Abgesehen von cm brauchen wir auch colors von matplotlib.
```Python
from matplotlib import cm, colors
```


Ausserdem benötigen wir auch die datetime library.
```Python
import datetime
```

Dann brauchen wir noch einige zusätzliche Variablen.
Karintime und sandrotime wird benötigt um die Sprechdauer hochzuzählen.
Die Speaker Diarization läuft mit 16 Frames, also alle 0.0625 wird ein Frame erzeigt. 
Die Variable timeFrameMultiplier benötigen wir damit wir später einfach darauf zugreifen können um von der Anzahl Frames auf Sekunden zu gelangen.
```Python
# speakers
karinTime = 0
sandroTime = 0

# needed to multiply frames by time
timeFrameMultiplier = 0.0625
```

Die "interactive_diarization" Funktion haben wir so erweitert, dass uns auf der x-Achse die aktuelle Sekunde angezeigt wo die Animation gerade steht in der Diarization des Audiofiles. Da die Animation auf unserer Hardware teilweise verzögert läuft hilft uns dies bei der Analyse.
Ausserdem wird die matplotlib definition so angepasst, dass neu eine zweite "row" ausgegeben wird.
Original:
```Python
def interactive_diarization(similarity_dict, wav, wav_splits, x_crop=5, show_time=False):
    fig, ax = plt.subplots()
```
Modifikation:
```Python
def interactive_diarization(similarity_dict, wav, wav_splits, x_crop=5, show_time=True):    
    fig, (ax, pie) = plt.subplots(1, 2)
```

Danach haben wir noch einen Haupttitel über die beiden neuen Graphen erstellt und den Ttiel der eigentlichen Speaker Diarization noch genauer definiert:
```Python
fig.suptitle("Diarization by Patrik, Dejan & Robin", fontsize=14, fontweight='bold')
ax.set_title("Speaker Diarization")
```

In der Unterfunktion "update" haben wir die zu Anfangs erstellten Variablen mittels "global" für uns verfügbar gemacht und die Labels und Werte für das Pie chart definiert.
```Python
global sandroTime
global karinTime
labels = 'Sandro Botz, Moderator', 'Karin Keller-Sutter, Bundesrätin'
nums = [sandroTime, karinTime]
```

Das Pie chart selber ist hier definiert.
Mit "pie" wird der neue Subplot eröffnet welcher oben in der "interactive_diarization" Funktion definiert wurde
"pie.clear()" wird benötigt damit in jedem Frame die Werte des pie chart gelöscht und anschliessend neu geladen werden können.
Das muss so gemacht werden, da matplotlib von sich aus keine update funktion für das pie chart zur verfügung stellt, wir unser pie chart aber in realtime auffüllen wollen.
"pie.pie" definiert das eigentlich piechart mit "nums" als die oben definierten Werte, "autopct" damit wir Prozentzahlen erhalten, "shadow" für Schatten und "startangle" für den Startwinkel.
"pie.set_title" definierten den Titel des charts.
"pie.legend" definiert die Legende an den x und y Koordinaten (0.5, 0.95), "loc" die location, "borderaxespad" den pad zwischen den Achsen und den Border der Legende und mit labels werden die oben definierten labels definiert.
Die 3 "pie.text" Befehle ertstellen uns die  Textboxen wo die Gesamtzeit der Sprecher aufaddiert wird.
Die erste definiert dabei lediglich den Titel.
Die anderen beiden sind gleich aufgebaut.
Zuersten werden alle Frames in denen der definierte Sprecher gesprochen hat mit dem timeFrameMultiplier 0.0625 addiert um Sekunden zu erhalten.
Diese werden als Sekunden der datetime.timedelta übergeben welche den Wert nach der Zeitdarstellung 00:00:00.000000 formatiert.
Mit "[:-4]" werden die letzen 4 Stellen der Milisekunden abgeschnitten damit wir auf eine Dartstellung von 00:00:00.00 kommen welche für uns vollkommen ausreicht und ansprechender aussieht.
Das ganze wird hübsch verpackt in einer roten Textbox im Beispiel von "Sandro Botz: 00:00:00.00 Sekunden" ausgegeben.

```Python
pie
pie.clear()
pie.axis('equal')
pie.pie(nums, autopct='%1.1f%%', shadow=True, startangle=140)
pie.set_title("Sprechverteilung")
# Place a legend to the right of this smaller subplot.
pie.legend(bbox_to_anchor=(0.5, 0.95), loc='upper left', borderaxespad=0., labels=labels)
pie.text(-1, -1.3, 'Total Talk Time:', fontsize=15)
pie.text(-1, -1.5, 'Sandro Botz: ' + str(datetime.timedelta(seconds=(sandroTime * timeFrameMultiplier)))[:-4] + " Sekunden", style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
pie.text(-1, -1.7, 'Karin Keller-Sutter: ' + str(datetime.timedelta(seconds=(karinTime * timeFrameMultiplier)))[:-4] + " Sekunden", style='italic', bbox={'facecolor': 'red', 'alpha': 0.5, 'pad': 10})
```


Damit die beiden Variablen sandroTime und karinTime auf die korrekte Anzahl Frames kommen in denen sie gesprochen haben, haben wir die beiden bestehenden if-Anweisungen erweitert.
Bestehende if Schleifen:
```Python
if similarity > 0.75:
    message = "Speaker: %s (confident)" % name
    color = _default_colors[best]
```
und
```Python
elif similarity > 0.65:
    message = "Speaker: %s (uncertain)" % name
    color = _default_colors[best]
```
Wenn der Algorithmus eine similarität von mehr als 75 % oder bei einer definierten Unsicherheit von immer noch über 65% hat, wird auch unser Codeteil ausgeführt 
Wenn die "name" im aktuellen Frame "Sandro Botz, Moderator" enthält, wird die Variable "sandroTime" um eins erhöht und bei "Karin Keller-Sutter, Bundesrätin" "karinTime" entsprechend um 1. Die print Befehle sind lediglich für uns um den Prozess besser kontrollieren zu können.

```Python
if name == "Sandro Botz, Moderator":
    sandroTime += 1
    print(sandroTime)
if name == "Karin Keller-Sutter, Bundesrätin":
    karinTime += 1
    print(karinTime)
print(name) # print the name of the speaker every update
```

Ganz am Ende wird auch für uns nochmals die Variablen geprintet damit wir auch in der Console nachvollziehen können, dass alles richtig funktioniert hat:

```Python
    # print total amount of talked seconds each candidate
    global karinTime
    global sandroTime
    print(karinTime * timeFrameMultiplier)
    print(sandroTime * timeFrameMultiplier)
```



