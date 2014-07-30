### API
#		1 indicator & 1 timestamp
#		comparing countries
# 	http://ocha.parseapp.com/getmapdata?period=2009&indid=CHD.B.FOS.04.T6
#
###

import csv, json
import sqlite3
import os

# Create the database
connection = sqlite3.connect('wfp_data.sqlite')
connection.text_factory = str
cursor = connection.cursor()

# Create the table
cursor.execute('DROP TABLE IF EXISTS wfp')
cursor.execute('CREATE TABLE wfp ( indicator_name text, region_name text, admin1_name text, admin2_name text, period text, value real, region text, admin1 text, admin2 text, indID text, units text) ')
connection.commit()

# Create CSV export 
csv_export = [['indicator_name', 'region_name', 'admin1_name', 'admin2_name', 'period', 'value', 'region', 'admin1', 'admin2', 'indID', 'units']]

# Load the CSV file into CSV reader
indicators = []
csvfile = open('indicator.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in creader:
	indicators.append(row)

csvfile = open('value.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')

countries = json.load(open('regional.json'))
states = json.load(open('../FAO/fao_state.json'))
cities = json.load(open('../FAO/fao_city.json'))

def find_state_list(country):
	files = [int(f) for f in os.listdir('../FAO/country/'+country) if f != '.DS_Store' and '.json' not in f]
	result = []
	for f in files:
		for s in states:
			if s['code'] == f:
				result.append(s)
				break
	return result
def find_city_list(country, state):
	files = [int(f.replace('.json','')) for f in os.listdir('../FAO/country/'+country+'/'+str(state)) if f != '.DS_Store']
	result = []
	for f in files:
		for c in cities:
			if c['code'] == f:
				result.append(c)
				break
	return result
def find_state_code(country, name):
	state_list = find_state_list(country)
	for s in state_list:
		if s['name'].encode('UTF-8') == name:
			return s['code']
	for s in state_list:
		if name in s['name'].encode('UTF-8'):
			print 'looking for: ' + name
			print 'found: ' + s['name']
			return s['code']
	# for s in state_list:
	# 	if s['name'].encode('UTF-8') in name:
	# 		print 'found: ' + s['name']
	# 		return s['code']
	return 0
def find_city_code(country, state, name):
	city_list = find_city_list(country, state)
	for c in city_list:
		if c['name'].encode('UTF-8') == name:
			return c['code']
	return 0

# print find_state_list('RWA')

# Iterate through the CSV reader, inserting values into the database
skiptitle = True
for row in creader:
  if skiptitle:
    skiptitle = False
  else:
  	region = row[0]
  	for one in countries:
  		if one['alpha-3'] == region:
  			region_name = one['name']
  	admin1 = row[1]
  	admin1_name = 'NA'
  	if admin1 != 'NA':
	  	# print admin1
  		code = find_state_code(region, admin1)
  		if code != 0:
  			admin1 = code
		  	for one in states:
		  		if one['code'] == admin1:
		  			admin1_name = one['name']
	  	else:
	  		continue
  	admin2 = row[2]
  	admin2_name = 'NA'
  	if admin2 != 'NA':
  		code = find_city_code(region, admin1, admin2)
  		if code != 0:
  			admin2 = code
		  	for one in cities:
		  		if one['code'] == admin2:
		  			admin2_name = one['name']
	  	else:
	  		continue
  	period = row[3]
  	indID = row[5]
  	value = float(row[6])
  	indicator_name = ''
  	units = ''
  	for one in indicators:
  		if one[0] == indID:
  			indicator_name = one[1]
  			units = one[2]
  			break
  	cursor.execute('INSERT INTO wfp VALUES (?,?,?,?,?,?,?,?,?,?,?)', (indicator_name, region_name, admin1_name, admin2_name, period, value, region, admin1, admin2, indID, units))
  	csv_export.append([indicator_name, region_name, admin1_name, admin2_name, period, value, region, admin1, admin2, indID, units])
# Close the csv file, commit changes, and close the connection
csvfile.close()
connection.commit()
connection.close()


with open('wfp_data.csv', 'wb') as csvfile:
    dbwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    for one in csv_export:
    	dbwriter.writerow(one)
