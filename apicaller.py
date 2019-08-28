#!/usr/bin/env python
import json
import requests
from apikey import apikey
from location import locationCode

## Utility Description

# This utility dumps the contents of a GET request to AccuWeather for your location 
# in order to prevent using up valuable API calls. The free tier for AccuWeather dev
# tools limits you to 50 calls per day, and PiClock requires 48 of those to update
# current conditions throughout the day (24 hours * 2 calls per hour).
#
# You can use this tool to generate real data for testing purposes. Simply run
# sudo ./dummy.py to generate new data to the dummydata.txt file.

class ApiCaller:
	
	def __init__(self):
		self.currentWeather = {}
		self.forecast = {}
		self.getData()
		self.parseData()
	
	def getData(self):
		url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationCode + '?apikey=' + apikey + "&details=true"
		currentWeatherRequest = requests.get(url).json()

		if 'Message' not in currentWeatherRequest:
			print('Generating current weather data from AccuWeather...')
			with open('currentweather.json', 'w') as f:
				json.dump(currentWeatherRequest, f)
		else:
			print('Maxed out API calls to AccuWeather. Attempting to use cached current weather data...')
			
		url = 'http://dataservice.accuweather.com/currentconditions/v1/' + locationCode + '?apikey=' + apikey + "&details=true"
		forecastRequest = requests.get(url).json()

		if 'Message' not in forecastRequest:
			print('Generating forecast data from AccuWeather...')
			with open('forecast.json', 'w') as f:
				json.dump(forecastRequest, f)
		else:
			print('Maxed out API calls to AccuWeather. Attempting to use cached forecast data...')		

	def parseData(self):
		with open('data.json', 'r') as f:
			currentWeather = json.load(f)
			
		with open('forecast.json', 'r') as f:
			forecast = json.load(f)
				
		self.currentWeather = currentWeather
		self.forecast = forecast
		
	
	def getLocation(self, zipcode):
		url = 'http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=' + apikey + '&q=' + str(zipcode)
		data = requests.get(url).json()
		newLocationCode = data[0]['Key']
		
		if 'Message' not in data:
			print('Generating new AccuWeather location code...')
			with open('location.py', 'w') as f:
				f.write('locationCode = "' + newLocationCode + '"')
		else:
			print('Maxed out API calls to AccuWeather. Please try again later...')
			
