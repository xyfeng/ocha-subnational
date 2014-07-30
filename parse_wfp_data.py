import sqlite3, json, ijson, csv
import os, sys, shutil, getopt, urllib2, time
import string, decimal

# FUNCTIONS

# load regional code
# regional_code = json.load(open('data/regional.json'))
fao_countries = json.load(open('FAO/fao_country.json'))

# decimal bug
def decimal_default(obj):
  if isinstance(obj, decimal.Decimal):
    return float(obj)
  raise TypeError

def get_fao_country_code(a3):
  for country in fao_countries:
    if country['alpha-3'] == a3:
      return country['code']

def get_fao_country_alpha_3(code):
  for country in fao_countries:
    if country['code'] == code:
      return country['alpha-3']

def create_folder(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)
  return

# parse
result = []

# get download list
download_list = []
with open('WFP/value.csv', 'rb') as f:
  reader = csv.reader(f)
  skiptitle = True
  curr_node = None

  for row in reader:
    if skiptitle:
      skiptitle = False
    else:
      region = row[0]
      if region not in download_list:
        download_list.append(region)
print download_list

# convert to fao codes
code_list = []
for d in download_list:
  code_list.append(get_fao_country_code(d))
print code_list

result = []

# save state list
# f = open('WFP/g2014_2013_1_mid/G2014_2013_1_mid.geojson')
# objects = ijson.items(f, 'features.item.properties')
# for o in objects:
#   admin_name = o['ADM1_NAME']
#   print 'Processing: ' + admin_name
#   for c in code_list:
#     if o['ADM0_CODE'] == c:
#       result.append({
#         'code': o['ADM1_CODE'],
#         'name': admin_name
#         })
# with open('FAO/fao_state.json', 'w') as outfile:
#   json.dump(result, outfile, default=decimal_default)

# save city list
# f = open('FAO/source/g2014_2013_2_mid/G2014_2013_2_mid.geojson')
# objects = ijson.items(f, 'features.item.properties')
# for o in objects:
#     admin_name = o['ADM2_NAME']
#     print 'Processing: ' + admin_name
#     for c in code_list:
#       if o['ADM0_CODE'] == c:
#         result.append({
#           'code': o['ADM2_CODE'],
#           'name': admin_name
#           })
#         with open('FAO/fao_city.json', 'w') as outfile:
#           json.dump(result, outfile, default=decimal_default)

# save country feature
f = open('FAO/source/g2014_2013_0_mid/G2014_2013_0_mid.geojson')
objects = ijson.items(f, 'features.item')
create_folder('FAO/country')
for o in objects:
  country_name = o['properties']['ADM0_NAME']
  print 'Processing: ' + country_name
  for c in code_list:
    if o['properties']['ADM0_CODE'] == c:
      country_alpha_3 = get_fao_country_alpha_3(c)
      o['properties']['alpha-3'] = country_alpha_3
      with open('FAO/country/'+country_alpha_3+'.json', 'w') as outfile:
        json.dump(o, outfile, default=decimal_default)


# save state feature
# f = open('FAO/source/g2014_2013_1_mid/G2014_2013_1_mid.geojson')
# objects = ijson.items(f, 'features.item')
# for o in objects:
#   admin_name = o['properties']['ADM1_NAME']
#   admin_code = o['properties']['ADM1_CODE']
#   print 'Processing: ' + admin_name
#   for c in code_list:
#     if o['properties']['ADM0_CODE'] == c:
#       country_alpha_3 = get_fao_country_alpha_3(c)
#       folder_path = 'FAO/country/' + country_alpha_3
#       create_folder(folder_path)
#       with open(folder_path+'/'+str(admin_code)+'.json', 'w') as outfile:
#         json.dump(o, outfile, default=decimal_default)


# save city feature
# f = open('FAO/source/g2014_2013_2_mid/G2014_2013_2_mid.geojson')
# objects = ijson.items(f, 'features.item')
# for o in objects:
#   admin_name = o['properties']['ADM2_NAME']
#   admin_code = o['properties']['ADM2_CODE']
#   print 'Processing: ' + admin_name
#   for c in code_list:
#     if o['properties']['ADM0_CODE'] == c:
#       country_alpha_3 = get_fao_country_alpha_3(c)
#       state_code = o['properties']['ADM1_CODE']
#       folder_path = 'FAO/country/' + country_alpha_3 + '/' + str(state_code)
#       create_folder(folder_path)
#       with open(folder_path+'/'+str(admin_code)+'.json', 'w') as outfile:
#         json.dump(o, outfile, default=decimal_default)

