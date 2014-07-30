### API
###

import csv, json, operator

Scheme = {
	".POP.": "Population",
	".ECO.": "Economic",
	".HTH.": "Health",
	".FOS.": "Food Security",
	".NUT.": "Nutrition",
	".EDU.": "Education",
	".PRO.": "Protection",
	".HLP.": "Housing, Land and Property",
	".MIN.": "Mine Action",
	".CDT.": "Coordination",
	".WSH.": "Water, Sanitation and Hygiene",
	".SHE.": "Emergency Shelter and NFI",
	".LOG.": "Logistics",
	".FUN.": "Funding",
	".HUM.": "Humanitarian Profile",
	".EAR.": "Early Recovery",
	".GEN.": "Gender-based violence",
	".CAM.": "Camp Coordination / Management",
	".TEL.": "Emergency Telecommunications",
	".OTH.": "Others"
}

result = {}

# read all data table
csvfile = open('all_data.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')
firstLine = True
for line in creader:
	if firstLine:
		firstLine = False
	else:
		indid_name = line[0]
		print indid_name
		indid = line[9]
		topic = ''
		for key in Scheme:
			if key in indid:
				topic = Scheme[key]
				break
		if topic not in result:
			result[topic] = [{
				'indid': indid,
				'name': indid_name
			}]
		else:
			FOUND = False
			for one in result[topic]:
				if one['indid'] == indid:
					FOUND = True
					break
			if not FOUND:
				result[topic].append({
					'indid': indid,
					'name': indid_name
				})
				result[topic].sort(key=operator.itemgetter('name'))

csvfile.close()

with open('topics.json', 'w') as outfile:
  json.dump(result, outfile)

