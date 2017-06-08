# Commerzbank Scraper
Python-Scripte, die das Unternehmensregister (https://www.unternehmensregister.de) nach Stimmrechtsmitteilungen durchsuchen, deren Inhalte speichern und als csv-Datei exportieren.

## Abhängigkeiten
Benötigt Pyhton 2.7.10 mit folgenden Paketen:
- mechanize
- bs4

## Verwendung
1. Repository klonen `git clone https://...`.
2. Erforderliche Module installieren `pip install mechanize`, `pip install beautifulsoup4`.
3. Konfiguration anpassen in `config.py`, scrapen mit `python scrape.py`, anschließend parsen mit `python parse.py`.


## Workflow
1. **config.py** legt den Namen der Firma fest, nach deren Meldungen gesucht wird, sowie den zu durchsuchenden Veröffentlichungszeitraum.
2. **scrape.py** speichert die gefunden Meldungen im Verzeichnis `/Sites`.
3. **parse.py** sucht nach folgenden Inhalten der Stimmrechtsmitteilung:  
    - Name des Unternehmens, dessen Anteile ge- oder verkauft wurden
    - Datum des Kaufs/ Verkaufs
    - Art (Über- oder Unterschreitung eines Stimmrechtsanteils)
    - Schwelle des Stimmrechtsanteils
    - Stimmrechtsanteil
    
  Das Skript speichert die Informationen in `/data.csv`.
  Die Meldungen sind unterschiedlich formatiert und bei manchen funtioniert das automatisierte Auslesen nicht. In diesem Fall verschiebt das Skript die Meldung in den Ordner `/Sites/manuell` und macht einen Vermerk in `/data.csv`.
