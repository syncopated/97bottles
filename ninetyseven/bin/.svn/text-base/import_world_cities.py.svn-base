import csv
from django.utils.encoding import force_unicode
from BeautifulSoup import BeautifulSoup
from savoy.core.geo.models import City

CITY_DATA_FILE = "bin/data/worldcitiespop.txt"
# Format: ['Country', 'City', 'AccentCity', 'Region', 'Population', 'Latitude', 'Longitude']
city_reader = csv.reader(open(CITY_DATA_FILE, "rb"))

REGION_DATA_FILE = "bin/data/region_codes.txt"
# Format: ['US', '40', 'Oklahoma'], ['GB', 'D3', 'Derbyshire'], ['CA', '02', 'British Columbia']
region_reader = csv.reader(open(REGION_DATA_FILE, "rb"))

for row in city_reader:
  country_code = row[0]
  city = row[2]
  region_code = row[3]
  region = ''
  population = row[4]
  try:
    if population != '':
      population = int(row[4])
  except:
    population = None
    print "ERROR: Population was not a number"
  if population and population > 30000:
    for region_row in csv.reader(open(REGION_DATA_FILE, "rb")):
      this_country_code = region_row[0].lower()
      this_region_code = region_row[1]
      if country_code == this_country_code and region_code == this_region_code:
        region = region_row[2]
    try:
      if country_code == "us":
        c, created = City.objects.get_or_create(
          city = city,
          state = region_code,
          country = country_code,
        )
      else:
        c, created = City.objects.get_or_create(
          city = force_unicode(BeautifulSoup(city)),
          province = force_unicode(BeautifulSoup(region)),
          country = force_unicode(BeautifulSoup(country_code)),
        )
    except:
      print "ERROR: There was an error saving %s, %s, %s." % (city, region, country_code.upper())