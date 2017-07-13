#!/usr/bin/env python
import requests

current = requests.get("https://api.weather.gov/stations/KNTU/observations/current").json()
print "Outside: {}F, {}".format(9.0/5.0 * int(current['properties']['temperature']['value']) + 32, current['properties']['textDescription'])
print "Last Updated: {}".format(current['properties']['timestamp'])

print ""

forecast = requests.get("https://api.weather.gov/points/36.8101,-76.0936/forecast").json()
print "{}: {}".format(forecast['properties']['periods'][0]['name'], forecast['properties']['periods'][0]['shortForecast'])
#for day in forecast['properties']['periods']:
#    print "{}: {}".format(day['name'], day['shortForecast'])
    #print day
print "Last Updated: {}".format(forecast['properties']['updated'])
