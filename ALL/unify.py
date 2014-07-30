### API
###

import csv, json
import sqlite3
import os

# Functions
def clean_units(units_text):
	if units_text == 'incidents per year' or units_text.lower() == 'count' or units_text == 'persons per square km':
		return 'count'
	if '%' in units_text or units_text == 'percentage' or 'per 100' in units_text:
		return '%'
	if '$' in units_text or units_text == 'USD':
		return '$'
	if 'per 1,000' in units_text:
		return 'per 1,000'
	if '10,000' in units_text:
		return 'per 10,000'
	if '100,000' in units_text:
		return 'per 100,000'
	if units_text == 'thousands':
		return '1,000'
	if units_text == 'millions':
		return '1,000,000'
	if units_text == ',000$ USD':
		return '$1,000'
	if 'km' in units_text:
		return 'km'
	if units_text == 'years':
		return 'time'
	if units_text == 'rank':
		return 'rank'
	if units_text == 'Fraction':
		return 'fraction'
	if units_text == 'index':
		return 'index'
	if units_text == 'total':
		return 'total'
	if units_text == 'uno':
		return 'uno'
	if units_text == 'both sexes':
		return 'both sexes'
	return None

# read old database
connection = sqlite3.connect('data/denormalized_db_old.sqlite')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('SELECT indicator_name, region, period, value, units, dsID FROM dataset_denorm ORDER BY period')

# read new indicator table
csvfile = open('data/indicator.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='"')
indid_list = []
for line in creader:
	indid_list.append([line[0], line[1]])

def getIndicatorID(text):
	for one in indid_list:
		if one[1] == text:
			return one[0]
	return None

# read country name index
countries = json.load(open('../WFP/regional.json'))
def getRegionName(region):
	for one in countries:
		if one['alpha-3'] == region:
			return one['name']
	return None


# Create CSV export 
csv_export = [['indicator_name', 'region_name', 'admin1_name', 'admin2_name', 'period', 'value', 'region', 'admin1', 'admin2', 'indID', 'units', 'units_text']]

# read wfp file
wfpFile = open('../WFP/wfp_data.csv', 'rb')
wfpReader = csv.reader(wfpFile, delimiter=',', quotechar='"')
FIRST_LINE = True
for line in wfpReader:
	if FIRST_LINE:
		FIRST_LINE = False
	else:
		csv_export.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], '%', 'Percent'])

# add other indicators	
for row in cursor:
	indid_name = row[0]
	indid = getIndicatorID(indid_name)
	region = row[1]
	region_name = getRegionName(region)
	period = row[2]
	value = row[3]
	dsID = row[5]
	units_text = row[4]
	units = clean_units(units_text)
	print 'name: '+ indid_name
	print indid
	print units_text
	print units
	if region_name and indid and units:
		csv_export.append([indid_name, region_name, 'NA', 'NA', period, value, region, 'NA', 'NA', indid, units, units_text])

with open('all_data.csv', 'wb') as csvfile:
	dbwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	for one in csv_export:
		try:
			dbwriter.writerow(one)
		except:
			print 'ERROR'

csvfile.close()
connection.close()

