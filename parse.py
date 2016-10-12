# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as BS
from datetime import datetime
import re
import os
import csv
import config


########################
### DOKUMENTE PARSEN ###
########################

def parse_document(doc, doc_name):

	soup = BS(doc.decode('utf-8'), "html.parser")
	table = soup.find('table', attrs={'id': 'begin_pub'})
	tableText = soup.find('table', attrs={'id': 'begin_pub'}).getText()
	tableTextBlank = tableText.replace(" ", "").replace("\n", "").replace("\t","")
	tableTextBlank = tableTextBlank.replace("Januar","01.").replace("Februar","02.").replace("Mrz","03.").replace("April","04.").replace("Mai","05.").replace("Juni","06.").replace("Juli","07.").replace("August","08.").replace("September","09.").replace("Oktober","10.").replace("November","11.").replace("Dezember","12.")
	tableTextBlank = tableTextBlank.replace("Prozent","%")
	
	# Mitteilungen ueber Stimmrechtsanteile an der firma rausfiltern
	if bool(re.search("Inhalt der[\n \s]*Stimmrechtsmitteilung:?[\n \s]*" + config.suchbegriff, tableText, re.I)): return "selber_emittent"

	# Daten per regex-Suche finden

	kommentar = ""
	try:
		name = re.compile("Emittent[\w\s\n]*:\s*(.*\n?.*),?", re.I).search(tableText).group(1).encode("utf-8").replace("\n", "")
		name = " ".join(name.split())

	except AttributeError:
		name = "???"
	try: 
		datum = re.compile("Schwellenber[\w]hrung:([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4})", re.I|re.U).search(tableTextBlank).group(1).encode("utf-8")
	except AttributeError:
		try:
			datum = re.compile("am([0-9]{1,2}\.[0-9]{1,2}\.[0-9]{2,4})").findall(tableTextBlank)
			if len(datum) == 1: datum = datum[0]
			elif len(datum) > 1:
				kommentar += "mehrere Daten, " 
				list_of_dates = []
				for d in datum: 
					list_of_dates.append(datetime.strptime(d, "%d.%m.%Y"))
				datum = datetime.strftime(min(list_of_dates), "%d.%m.%Y")
				#datum = min(list_of_dates)
				#richtiges format ausgeben
			else: 
				datum = "???"
		except AttributeError:
			datum= "???"
			kommentar += "Datum unklar"
	try:

		schwelle = re.compile("BetroffeneMeldeschwelle.?:?([\w %]{1,50}%)", re.I).search(tableTextBlank).group(1).encode("utf-8")
	except AttributeError:
		try:
			schwelle = re.compile("Schwellen?von([\w %]{1,30}%)", re.I).search(tableTextBlank).group(1).encode("utf-8")
		except AttributeError:
			schwelle = "???"
			kommentar += "Schwelle unklar, "
	schwelle = schwelle.replace("und", ", ")	
	#print schwelle
	try:
		anteil = re.compile("mitteilungspflichtigerstimmrechtsanteil:[Stimmrechtsanteil:]*([\w,.]{1,50}%)", re.I).search(tableTextBlank).group(1).encode("utf-8")
	except AttributeError:
		try:
			anteil = re.compile("und[betr]*.?[gt]*(andiesem|zudiesem|zumheutigen)Tag([\w,.\s\t]{0,40}%)", re.I|re.U).search(tableTextBlank).group(2).encode("utf-8")
		except AttributeError:
			try:
				anteil = re.compile("undbetrug(zudiesemZeitpunkt|)([\w,.\s]{1,20}%)", re.I).search(tableTextBlank).group(2).encode("utf-8")

			except AttributeError:
				try:
					anteil = re.compile("schrittenundh.lt([\d.,]*%)derStimmrechte", re.I).search(tableTextBlank).group(1).encode("utf-8")
				except AttributeError:
					anteil="???"
					kommentar += "anteil unklar, "
					#print tableText + "\n"
	anteil = anteil.replace(",", ".")
	try: # für dokumente der tabellarischen form
		anteil21_22 = re.compile("Stimmrechtsanteilenach[§]*21,22WpHG:([\d,.]*%)", re.I).search(tableTextBlank).group(1).encode("utf-8")

	except AttributeError:
		try: #erst nach § 22 Abs.1 suchen
			anteil21_22 = re.compile("(\d[\d,.]*%)derStimmrechte[\w().,]{0,80}sindder[\w().,]{0,170}(gem..|gem\.)[§]*22", re.I|re.U).search(tableTextBlank).group(1).encode("utf-8")
			#kommentar += "betrifft §22 ABs. 1, "
		except AttributeError:
			try:
				anteil21_22 = re.compile("Davonsindihr([\d,.]*%)[\w().,]{0,50}nach[§]*22", re.I).search(tableTextBlank).group(1).encode("utf-8") + " §22 ABs. 1"
				# kommentar += "betrifft §22 ABs. 1, "
			except AttributeError:
				try:
					anteil21_22 = re.compile("gem..[§]*22Abs\.1\,Satz1Nr\.1sindihr([\d,.]*%)", re.I).search(tableTextBlank).group(1).encode("utf-8") + " §22 ABs. 1"
					#kommentar += "betrifft §22 ABs. 1, "
				except AttributeError:
					try:
						re.compile("wirddervorgenannteStimmrechtsanteilgem..[§]*22Abs", re.I).search(tableTextBlank).group(0).encode("utf-8") + " §22 ABs. 1"
						anteil21_22 = anteil
						#kommentar += "betrifft §22 ABs. 1, "
					except AttributeError:
						try:
							anteil21_22 = re.compile("(\d[\d,.]*%)derStimmrechtebetrug[\w().,]{0,80}DieseStimmrechtsanteilesinddemMitteilendennach[§]*22Abs\.1", re.I).search(tableTextBlank).group(1).encode("utf-8") + " §22 ABs. 1"
							#kommentar += "betrifft §22 ABs. 1, "
						except AttributeError:
							try:
								anteil21_22 = re.compile("Diese(\d[\d,.]*%)[\w().,]{0,80}werden[\w().,]{0,170}(gem..|gem\.)[§]*22", re.I|re.U).search(tableTextBlank).group(1).encode("utf-8") + " §22 ABs. 1"
								#kommentar += "betrifft §22 ABs. 1, "
								#print anteil21_22
							except AttributeError:
								try: # jetzt Abs. 21
									re.compile("hatuns(nach|gem..)[§]*21Abs\.1WpHG", re.I).search(tableTextBlank).group(1).encode("utf-8")
									anteil21_22 = anteil
									#print anteil21_22
								except AttributeError:
									try:
										anteil21_22 = re.compile("entfallen([\d,.]*%)[\w().,]{0,50}aufStimmrechtsanteilenach[§]*21", re.I).search(tableTextBlank).group(1).encode("utf-8")
									except AttributeError: 
										anteil21_22 = "???"
										kommentar += "§21,22 unklar, "
										#print anteil21_22  + "- anteil21_2"
										#print tableTextBlank


	try:
		if bool(re.search(".berschr(eiten|eitung|itt)|Erwerb[^/]", tableTextBlank, re.I)): art = ">"
		if bool(re.search("Unterschr(eiten|eitung|itt)|Ver.u.erung", tableTextBlank, re.I)): art = "<"
		if bool(re.search("Unterschr(eiten|eitung|itt)|Ver.u.erung", tableTextBlank, re.I)) and bool(re.search(".berschr(eiten|eitung|itt)|Erwerb[^/]", tableTextBlank, re.I)):
			art = "<>"
			kommentar += "2 in 1er Meldung, "

		return {'name': name, 'datum': datum, 'art': art, 'schwelle': schwelle, 'anteil': anteil, 'anteil21_22': anteil21_22, 'kommentar': kommentar}
	except:
		
		art = "???"
		kommentar += "art unklar, "
		return {'name': name, 'datum': datum, 'art': art, 'schwelle': schwelle, 'anteil': anteil, 'anteil21_22': anteil21_22, 'kommentar': kommentar}




##################
### CSV-EXPORT ###
##################
def parse_all():
	output = open("data.csv", 'wt')
	writer = csv.writer(output)
	writer.writerow(('Name', 'Datum', 'Art', 'Schwelle', 'Anteil', 'Anteil 21_22', 'id', 'Kommentar'))
	for f in os.listdir("Sites/"):
		if f[:2] == 'id':
	
			doc = open("Sites/" + f, "r")
			result = parse_document(doc.read(), f)
			if result == False:
				os.rename("Sites/" + f, "Sites/manuell/" + f)
			elif result == "selber_emittent":
				os.rename("Sites/" + f, "Sites/" + config.suchbegriff + "/" + f)
			# zweiter Durchlauf

			else:
				writer.writerow((result['name'], result['datum'],result['art'],result['schwelle'], result['anteil'], result['anteil21_22'], f, result['kommentar']))
			doc.close()

parse_all()