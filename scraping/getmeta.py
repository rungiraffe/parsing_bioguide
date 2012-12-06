##ONE BIG SCRIPT TO GET AND PARSE BIOGUIDE##

import requests
from bs4 import BeautifulSoup
import re
import os
import datetime

##------CREATE THE DIRECTORY------##
metadirectory = "/Users/Rungiraffe/Desktop/scraped_bioguide/final/meta"
if not os.path.exists(metadirectory):
	os.makedirs(metadirectory, 0777)

##------CREATE ERROR FILE------##
metaf = open("meta_errors.txt", "a")
timestamp = str(datetime.datetime.now())
metaf.write("For " + timestamp + ":\n")

##------ENTER FIRST AND LAST CONGRESS YOU WANT TO SCRAPE-----##
firstCong = 61
lastCong = 91

##------SCRAPE SEARCHES BY CONGRESS IN BIOGUIDE-----##

url = "http://bioguide.congress.gov/biosearch/biosearch1.asp"

for i in range(firstCong, lastCong + 1):
	i = str(i)
	
	print "Scraping Congress " + i + "..."
	
	congress = {'congress': i}
	r = requests.post(url, data=congress)
	
	#Append search results into a list
	BioSearch = []
	BioSearch.append(r.content)
	
	print "Congress " + i + " scraped."
	
	##------GET METADATA FROM SEARCH PAGES------##
	
	print "Extracting MetaData from Congress " + i + "..."
	
	for item in BioSearch:
		soup = BeautifulSoup(''.join(item))
			
		#isolating the table rows
		trs = soup.find_all('tr')
		
		#Getting rid of random rows a the top of the page
		top = soup.find_all('tr')[0]
		header = soup.find_all('tr')[1]
		top.decompose()
		header.decompose()
		
		#Create the files to store the metadata
		metacsv = open("meta/" + i + "meta.csv", "w")
		
		#Getting the data out of cells
		invalid = 0
		for tr in trs:
			try:
				name = str(tr.find_all('td')[0].string)
				clean_name = re.sub("(, Jr.|, Sr.)", "", name)
				position = str(tr.find_all('td')[2].string)
				party = str(tr.find_all('td')[3].string)
				state = str(tr.find_all('td')[4].string)
				metacsv.write("%s, %s, %s, %s\n" % (clean_name, position, party, state))
			except:
				invalid += 1
	
	metaf.write(str(invalid) + " rows in Congress " + i + " are invalid.\n")	
	print str(invalid) + " rows in Congress " + i + " are invalid."	
	print "MetaData from Congress " + i + " extracted."

metacsv.close
metaf.close

		