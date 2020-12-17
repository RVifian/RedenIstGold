## Testdaten aufbereiten:

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

Resemblyzer braucht den Algorithmus von von: https://github.com/google/uis-rnn 

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

Die Audiodatei haben wir mit Hilfe von https://mp3cut.net/ gekürzt.
 

 **15min Version**
Kann nicht direkt auf Github gespeichert aber von hier heruntergeladen werden: https://zhaw-my.sharepoint.com/:u:/g/personal/vifiarob_students_zhaw_ch/ERTnmpq_daZCqeFg9BhK5KcB8BAnm4q5osEHQwZu-2jLng?e=9e0wze

```Python
segments = [[113, 140], [34, 50], [190, 230], [873, 910], [764, 800], [672, 720]] 
speaker_names = ["Sandro Botz Moderator", "Backgroundinfo Sprecherin", "Karin Keller-Sutter, Bundesrätin", "Martin Landolt, Präsident BDP", "Gerhard Pfister, Präsident CVP", "Daniel Jositsch, Ständerat SP"] 
speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments] 
```
 
 **1min Version**
```Python
segments = [[00, 11], [14, 30]]
speaker_names = ["Sandro Botz, Moderator", "Karin Keller-Sutter, Bundesrätin"]
speaker_wavs = [
    wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]
```
