import csv, json
import sqlite3
import os

# Create the database
connection = sqlite3.connect('wfp_data.sqlite')
connection.text_factory = str
cursor = connection.cursor()

# Create the table
# cursor.execute('DROP TABLE IF EXISTS wfp')
# cursor.execute('CREATE TABLE wfp ( region text, admin1 text, admin2 text, period text, indID text, indicator_name text, value real, units text) ')
# connection.commit()

# Load the CSV file into CSV reader
indicators = []
csvfile = open('indicator.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')
for row in creader:
	indicators.append(row)

csvfile = open('value.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')

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
		if s['name'] == name:
			return s['code']
	print 'looking for: ' + name
	for s in state_list:
		if name in s['name']:
			print 'found: ' + s['name']
			return s['code']
	for s in state_list:
		if s['name'] in name:
			print 'found: ' + s['name']
			return s['code']
	print 'NOT FOUND'
	return 0

# print find_state_list('BDI')

# Iterate through the CSV reader, inserting values into the database
skiptitle = True
for row in creader:
  if skiptitle:
    skiptitle = False
  else:
  	region = row[0]
  	admin1 = row[1]
  	if admin1 != 'NA':
  		code = find_state_code(region, admin1)
  		if code != 0:
  			admin1 = code
  	admin2 = row[2]
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
#   	cursor.execute('INSERT INTO wfp VALUES (?,?,?,?,?,?,?,?)', (region, admin1, admin2, period, indID, indicator_name, value, units))

# Close the csv file, commit changes, and close the connection
# csvfile.close()
# connection.commit()
# connection.close()
