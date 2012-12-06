import csv
import simplekml
 
inputfile = csv.reader(open("20thbaicforkml.csv","rU"))
kml=simplekml.Kml()

for row in inputfile:
	if row[5] == "":
		desc_text = "<![CDATA[" + row[1] + "<br/>" + row[2] + "<br/>" + row[3] + "<br/>" + row[4] + "]]>"
	else:
		desc_text = "<![CDATA[" + row[1] + "<br/>" + row[2] + "<br/>" + row[3] + "<br/>" + row[4] + "<br/>" + row[5]"]]>"
	point = kml.newpoint(name=row[0], description= desc_text, coords=[(row[9],row[8])])
	point.timespan.begin = row[6]
	point.timespan.end = row[7]
	
kml.save("baic71-95.kml")