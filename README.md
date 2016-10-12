# Commerzbank Scraper
Python-Script, mit dem das Unternehmensregister (https://www.unternehmensregister.de) nach Dokumenten durchsucht wird, die die Commerzbank betreffen.

## Voraussetzungen
Benötigt Pyhton 2.7.10 mit folgenden Paketen:
- mechanize
- bs4

## Verwendung

- Konfiguration anpassen in `config.py` (Suchbegriff, Zeitraum, Sprache...)
- zum Srcapen der Seiten: `python scrape.py`
- zum Parsen der Seiten incl. csv-Export: `python parse.py` (legt eine datei data.csv ins root-Verzeichnis)
