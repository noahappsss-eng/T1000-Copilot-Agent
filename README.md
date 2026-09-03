# T1000 Copilot Agent – Skripte zur Datenaufbereitung

## Über dieses Repository

Dieses Repository enthält die Python-Skripte, die im Rahmen der Projektarbeit zur Untersuchung eines Microsoft 365 Copilot-Agents für die Informationssuche im Product Data Management verwendet wurden. Die Skripte dienten der technischen Aufbereitung des abgegrenzten Datenbestands vor dessen Bereitstellung in SharePoint.

Enthalten sind ausschließlich die Skripte und die zu ihrer Ausführung erforderlichen Abhängigkeiten. Der betriebliche Datenbestand, die erzeugten Ausgabedateien und weitere unternehmensinterne Informationen sind aus Vertraulichkeitsgründen nicht Bestandteil dieses Repositories.

## Enthaltene Dateien

| Datei | Funktion |
|---|---|
| `jpg_zu_pdf.py` | Sucht rekursiv nach JPG- und JPEG-Dateien und wandelt diese in PDF-Dateien um. |
| `csv_aufteilen.py` | Teilt eine zusammenhängende CSV-Stücklistendatei anhand der Gerätezeilen in einzelne gerätespezifische CSV-Dateien auf. |
| `requirements.txt` | Enthält die zusätzlich benötigten Python-Abhängigkeiten. |

## Voraussetzungen

- Python 3.9 oder neuer
- Python-Paket `Pillow` für die Bildkonvertierung

Die übrigen verwendeten Module sind Bestandteil der Python-Standardbibliothek.

## Installation

Repository klonen und in den Projektordner wechseln:

```bash
git clone https://github.com/noahappsss-eng/T1000-Copilot-Agent.git
cd T1000-Copilot-Agent
```

Abhängigkeiten installieren:

```bash
python -m pip install -r requirements.txt
```

## Verwendung von `jpg_zu_pdf.py`

Das Skript durchsucht den angegebenen Ordner einschließlich aller Unterordner nach Dateien mit den Endungen `.jpg` und `.jpeg`. Für jedes gefundene Bild wird im selben Verzeichnis eine PDF-Datei mit identischem Dateinamensstamm erstellt. Bereits vorhandene PDF-Dateien werden nicht überschrieben.

Aufruf:

```bash
python jpg_zu_pdf.py "/pfad/zum/hauptordner"
```

Beispiel unter Windows:

```powershell
python .\jpg_zu_pdf.py "C:\Pfad\zum\Hauptordner"
```

> **Achtung:** Nach erfolgreicher Erstellung und Prüfung der PDF-Datei wird die jeweilige ursprüngliche JPG- oder JPEG-Datei gelöscht. Das Skript sollte daher zunächst mit einer Sicherungskopie des Datenbestands getestet werden.

Nach Abschluss gibt das Skript die Anzahl der ersetzten Dateien sowie gegebenenfalls aufgetretene Fehler aus.

## Verwendung von `csv_aufteilen.py`

Das Skript liest eine zusammenhängende CSV-Datei ein und erkennt neue Geräte daran, dass die Spalte `Baustufe` den Wert `0` enthält. Für jedes erkannte Gerät wird eine eigene CSV-Datei erzeugt. Der Tabellenkopf der Ausgangsdatei wird in jede Ausgabedatei übernommen.

Grundlegender Aufruf:

```bash
python csv_aufteilen.py "/pfad/zur/stueckliste.csv" --ausgabe "/pfad/zum/ausgabeordner"
```

Beispiel unter Windows:

```powershell
python .\csv_aufteilen.py "C:\Pfad\zur\stueckliste.csv" --ausgabe "C:\Pfad\zum\Ausgabeordner"
```

Optionale Parameter:

| Parameter | Beschreibung | Standardwert |
|---|---|---:|
| `-o`, `--ausgabe` | Verzeichnis für die erzeugten CSV-Dateien | `aufgeteilte_stuecklisten_MRF` |
| `--baustufe-spalte` | Nummer der Spalte mit der Baustufe, gezählt wie in Excel | `1` |
| `--artikel-spalte` | Nummer der Spalte mit der Artikelbezeichnung, gezählt wie in Excel | `9` |

Beispiel mit abweichenden Spaltenpositionen:

```bash
python csv_aufteilen.py "stueckliste.csv" --ausgabe "ausgabe" --baustufe-spalte 2 --artikel-spalte 5
```

Das Skript erkennt UTF-8- und Windows-1252-kodierte Dateien sowie gängige Trennzeichen automatisch. Die erzeugten Dateien werden im Format UTF-8 mit BOM gespeichert.

## Datengrundlage und Vertraulichkeit

Die Skripte enthalten keine für die Evaluation verwendeten Produktdaten. Für eine eigene Ausführung müssen geeignete Eingabedateien bereitgestellt werden. Insbesondere die Funktionsweise von `csv_aufteilen.py` setzt voraus, dass die Gerätezeilen durch den Wert `0` in der festgelegten Baustufenspalte gekennzeichnet sind.

## Autor

Noah Junginger, 2026
