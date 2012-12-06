import requests
import csv
 
inputfile = csv.reader(open("baic_address.csv","rU"))
outputfile = open("baic_geocode.csv","a")

for row in inputfile:
	url = 'http://maps.googleapis.com/maps/api/geocode/json'
	payload = {'address':row, 'sensor':'false'}
	r = requests.get(url, params=payload)
	json = r.json
	lat = json['results'][0]['geometry']['location']['lat']
	lng = json['results'][0]['geometry']['location']['lng']
	for item in row:
		street = row[0]
		city = row[1]
		state = row[2]
	print street, city, state, lat, lng
	outputfile.write("%s, %s, %s, %r, %r\n" % (street, city, state, lat, lng))
		
