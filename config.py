# -*- coding: utf-8 -*-
from datetime import datetime
import os

#####################
### SUCH-OPTIONEN ###
#####################

suchbegriff = 'Commerzbank'
bereich = '81' # = Stimmrechtsmitteilungen
language = 'de'

# von
start_day = '1'
start_month = '1'
start_year = '2013'
# bis
now = datetime.now()
end_day = str(now.day)
end_month = str(now.month)
end_year = str(now.year)


# Ordner-Struktur erzeugen

if not os.path.exists("Sites/"):
	os.makedirs("Sites/")
if not os.path.exists("Sites/manuell"):
	os.makedirs("Sites/manuell/")
if not os.path.exists("Sites/" + suchbegriff):
	os.makedirs("Sites/" + suchbegriff)
