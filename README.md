# Commerzbank Scraper
Python-Scripte, die das Unternehmensregister (https://www.unternehmensregister.de) nach Stimmrechtsmitteilungen durchsuchen, deren Inhalte speichern und als csv-Datei exportieren.

## Abhängigkeiten
Benötigt Pyhton 2.7.10 mit folgenden Paketen:
- mechanize
- bs4

## Verwendung

1. Konfiguration anpassen in config.py (Suchbegriff, Zeitraum, Sprache...)
2. Scrapen: `python scrape.py`
3. Parsen: incl. csv-Export: `python parse.py` (legt eine datei data.csv ins root-Verzeichnis)
