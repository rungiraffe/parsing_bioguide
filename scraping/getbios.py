##ONE BIG SCRIPT TO GET AND PARSE BIOGUIDE##

import requests
from bs4 import BeautifulSoup
import re
from urlparse import urlparse
import os
import urllib2
import datetime

##------CREATE THE DIRECTORIES------##
biodirectory = "" #Insert your directory path here
if not os.path.exists(biodirectory):
    os.makedirs(biodirectory, 0777)

url = "http://bioguide.congress.gov/biosearch/biosearch1.asp"

for i in range(41, 42):
	i = str(i)
	
	##------SCRAPE SEARCHES BY CONGRESS IN BIOGUIDE-----##
	print "Scraping Congress " + i + "..."
	
	congress = {'congress': i}
	r = requests.post(url, data=congress)
	
	#Append search results into a list
	BioSearch = []
	BioSearch.append(r.content)
	
	print "Congress " + i + " scraped."
	
	##-----GETTING MEMINDEX NUMBERS-----#
	print "Getting MemIndex Numbers for Congress " + i + "..."
	
	for line in BioSearch:
		soup = BeautifulSoup (''.join(line))
	
		#getting rid of the random link in text
		final_link = soup.p.a
		final_link.decompose()
	
		#creating a list for the urls
		CleanList = []
		links = soup.find_all('a')
	
		#for each link, isolating it, getting the query section, putting in in clean_list
		for link in links:
			single_link = link['href']
			url_part = urlparse(single_link)
			query = url_part.query
			memindex = re.sub(".[a-z,=]", "", query)
			entry = "%s" % memindex
			CleanList.append(entry)
	
	print "MemIndex Numbers saved for Congress " + i + "."
			
	##------LOOKING UP BIOS, EXTRACTING TEXT, WRITING TO TEXT FILE------###
	
	print "Looking up Bios for Congress " + i + "..."
	
	AllBio = []
	ErrorList = []
	errorf = open("bio_errors.txt", 'a')
	biourl = 'http://bioguide.congress.gov/scripts/biodisplay.pl?index='
	
	for item in CleanList:
		response = urllib2.urlopen(biourl + item)
		webcontent = response.read()
		try:
			newsoup = BeautifulSoup(''.join(webcontent))
			
			#Getting rid of names in bio paragraphs
			strike_name = newsoup.p.font
			strike_name.decompose()
			
			#Getting rid of bio tags and extracting bio text
			bio_tags = newsoup.p
			bio = bio_tags.get_text()
			biochar = bio.encode('ascii' , 'ignore')
			
			biof = open("bios/" + item + ".txt", 'w')
			print "Writing " + item + " in " + i + " Congress"
			biof.write(biochar)
			
		except:
			print item + " did not write."
			ErrorList.append(item)
			for error in ErrorList:
				errorf.write(error + " did not write.\n")
				
number = str(len(ErrorList))
timestamp = str(datetime.datetime.now())
errorf.write(number + " files did not write (" + timestamp + ")\n")
			
biof.close
errorf.close
		


		
