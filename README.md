# Commerzbank Scraper
Jedes Jahr entgehen dem Bund Millionen, weil Banken Steuerschlupflöcher nutzen. Die Commerzbank nutzte sogenannte Cum/Cum-Geschäfte, um Steuern zu sparen. Die dazu getätigten Aktienkäufe hinterlassen Spuren im Unternehmensregister. [BR Data](http://www.br.de/br-data/) und [BR Recherche](http://www.br.de/recherche/) haben diese untersucht.

Diese Sammlung an Python-Skripten dient dazu, das Unternehmensregister (https://www.unternehmensregister.de) nach Stimmrechtsmitteilungen zu durchsuchen, deren Inhalte zu erfassen und strukturiert abzuspeichern.

- **Artikel:** [Cum/Cum - Die Steuertricks der Commerzbank](http://www.br.de/nachrichten/commerzbank-steuertricks-100.html)

## Schnellstart
1. Repository klonen `git clone https://...`.
2. Erforderliche Pakete installieren `pip install -r requirements.txt`
3. Konfiguration anpassen in `config.py`
4. Scrapen mit `python scrape.py`
5. Parsen mit `python parse.py`

## Abhängigkeiten
Die Skripte benötigt [Python 2.7](https://www.python.org/download/releases/2.7/) und die Python-Paketverwaltung [pip](https://pypi.python.org/pypi/pip?). Zum Auslesen des Unternehmensregisters verwenden wir [mechanize](https://pypi.python.org/pypi/mechanize/) und [Beautiful Soup](https://pypi.python.org/pypi/beautifulsoup4/).

Alle erforderlichen Pakete können mit pip installiert werden:

```
$ pip install -r requirements.txt
```

## Funktionen
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
