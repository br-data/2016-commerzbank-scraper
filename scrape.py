# -*- coding: utf-8 -*-
from mechanize import Browser
from bs4 import BeautifulSoup as BS
from datetime import datetime
import re
import os
import csv
import config


###############
### SCRAPER ###
###############

def get_documents (s = config.suchbegriff, b = config.bereich, l = config.language, sd = config.start_day, sm = config.start_month, sy = config.start_year, ed = config.end_day, em = config.end_month, ey = config.end_year):	
	
	# Browser initialisieren
	br = Browser()
	br.set_handle_robots(False)
	br.set_handle_referer(False)
	br.set_handle_refresh(False)
	br.addheaders = [('User-agent', 'Firefox')]
	br.open('https://www.unternehmensregister.de/ureg/search1.6.html')

	# Formular der Seite mit Optionen von oben ausfuellen
	br.select_form(name="searchRegisterForm")
	br['searchRegisterForm:registerDataFullText'] = s
	br['searchRegisterForm:publicationsOfCapitalInvestmentsCategory'] = [b,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsLanguage'] = [l,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsStartDateDay'] = [sd,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsStartDateMonth'] = [sm,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsStartDateYear'] = [sy,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsEndDateDay'] = [ed,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsEndDateMonth'] = [em,]
	br['searchRegisterForm:publicationsOfCapitalInvestmentsPublicationsEndDateYear'] = [ey,]
	br.submit()

	#Dokumente in den Ordner "Sites" abspeichern
	destination = "Sites/"
	base_url = br.geturl()
	soup = BS(br.response().read(), "html.parser")

	# nDocs zählt die Dokumente
	nDocs = 1
	page_next = ""

	# klickt den weiter button am ende der Seiter, falls dieser existiert
	while page_next is not None:

		# suche den weiter-Button
		try:
			page_next = soup.find('div', attrs={'id': 'result_pagingnav'}).find(string="Weiter").parent.get('href')
		except AttributeError:
			page_next = None

		# links zu den dokumenten haben den tite. 'Stimmrechtsmitteilungen'
		doc_links = soup.find_all('a', attrs={'title': 'Mitteilung bedeutender Stimmrechtsanteile'})

		for doc in doc_links:
			br.open(base_url + doc.get('href'))
			soup = BS(br.response().read().decode('utf-8'), "html.parser")
			f = open(destination + "/" + re.search("id=([0-9]*)", doc.get('href')).group(0).replace("=","_") + ".html", 'w')
			f.write(str(soup))
			f.close()
			print nDocs
			print base_url + doc.get('href')
			
			nDocs = nDocs + 1
		
		if page_next is not None: 
			br.open(base_url + page_next)
			soup = BS(br.response().read(), "html.parser")	


get_documents()

















