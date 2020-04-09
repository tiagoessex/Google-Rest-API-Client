#import pandas as pd
#import logging
#import time
import csv
import requests
import json


from geopy.geocoders import GoogleV3
from geopy.geocoders import TomTom
from geopy.geocoders import Nominatim
from geopy.geocoders import Bing
from geopy.geocoders import Here
from geopy.geocoders import AzureMaps

from geopy.exc import (
    GeocoderQueryError,
    GeocoderQuotaExceeded,
    ConfigurationError,
    GeocoderParseError,
    GeocoderAuthenticationFailure,
    GeocoderInsufficientPrivileges,
    GeocoderTimedOut,
    GeocoderServiceError,
    GeocoderUnavailable,
    GeocoderNotFound
)


import ssl
import certifi
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx



############ logging ############

#logger = logging.getLogger("root")
#logger.setLevel(logging.DEBUG)
# create console handler
#ch = logging.StreamHandler()
#ch.setLevel(logging.DEBUG)
#logger.addHandler(ch)


############ ERRORS ############

class UnableToGeocode(Exception): 
	# Constructor or Initializer 
	def __init__(self, value): 
		self.value = value 
  
	# __str__ is to print() the value 
	def __str__(self): 
		return(repr(self.value)) 
		
class Geogoogle():
	geolocator_google = None

	#SHOW_ERRORS = True



	def __init__(self, googlekey = None):
		if not googlekey:
			raise RuntimeError("No key!")
		self.key = googlekey



	############ SERVICES ############

	def initOutput(self):
		output={}
		output["formatted_address"] = None
		output["latitude"] = None
		output["longitude"] = None
		output["accuracy"] = None
		output["place_id"] = None
		output["type"] = None
		output["postcode"] = None
		output["input_string"] = None
		output["number_of_results"] = None
		output["status"] = None
		output["response"] = None
		output["localidade"] = None
		output["distrito"] = None
		output["concelho"] = None
		output["freguesia"] = None	
		output["service"] = 'GOOGLE'
		return output
		
	def initOutputPlace(self):
		output = {}
		output["status_place"] = None
		output["formatted_address_place"] = None
		output["vicinity"] = None
		output["formatted_phone_number"] = None
		output["plus_code"] = None
		output["lat"] = None
		output["lon"] = None
		output["postcode_place"] = None
		output["street_number"] = None
		output["route"] = None
		output["locality"] = None
		output["city"] = None
		output["country"] = None
		output["id"] = None
		output["international_phone_number"] = None
		output["name"] = None
		output["rating"] = None
		output["types"] = None
		output["website"] = None
		output["url"] = None
		output["permanently_closed"] = None
		output["open_now"] = None
		output["periods"] = None
		output["weekday_text"] = None
		return output
	
		

	def google(self, addr, local, country, saveraw):
		
		output=self.initOutput()		
		address = "" if addr is None else addr
		address = address + ("" if local is None else "," + local)
		address = address + ("" if country is None else "," + country)
		
		# init service if not init yet
		if not self.geolocator_google:		
			self.geolocator_google = GoogleV3(api_key=self.key)
		
		# geocode address
		location = self.geolocator_google.geocode(address,exactly_one=False) #, components={"country": "PT"})
		if location is not None:
			answer = location[0].raw

			output['status'] = "OK"		
			output["formatted_address"] = location[0].address
			output["latitude"] = location[0].latitude
			output["longitude"] = location[0].longitude
			output["accuracy"] = answer.get('geometry').get('location_type')
			output["place_id"] = answer.get("place_id")
			output["type"] = ",".join(answer.get('types'))
			output["postcode"] = ",".join([x['long_name'] for x in answer.get('address_components') 
									  if 'postal_code' in x.get('types')])
			output["input_string"] = address
			output["number_of_results"] = len(location)
			output["localidade"] = ",".join([x['long_name'] for x in answer.get('address_components') 
									  if 'locality' in x.get('types')]).split(',')[0]
			
			
			#output["service"] = 'GOOGLE'
			
			if saveraw:
				output["response"] = location[0].raw		
			
		else:
			#output['status'] = "ZERO_RESULTS"
			raise UnableToGeocode("Unable to geocode entity.")
		
		return output



	def geocode(self, addr = None, local = None, country = 'Portugal', saveraw = True):	
		geocode_result = None
		try:				
			geocode_result = self.google(addr, local, country, saveraw)
		except UnableToGeocode as e:
			geocode_result = self.initOutput()
			geocode_result['status'] = "UNABLE"
			geocode_result['service'] = "GOOGLE"
		except (GeocoderQueryError,GeocoderAuthenticationFailure,GeocoderInsufficientPrivileges,ConfigurationError):
			#if self.SHOW_ERRORS:
			#	logger.error ('\n--------------------------------------------------------------------')
			#	logger.error ('ERROR: something wrong with either the service or the query.')
			#	logger.error ('--------------------------------------------------------------------')
			raise RuntimeError("Check the key!")
		except GeocoderQuotaExceeded:
			#if self.SHOW_ERRORS:
			#	logger.error ('\n--------------------------------------------------------------------')
			#	logger.error ('ERROR: you have reached the end of your quota for the service.')
			#	logger.error ('--------------------------------------------------------------------')
			raise RuntimeError("Quota limit reached!")
		except GeocoderTimedOut:
			#if self.SHOW_ERRORS:
			#	logger.error ('\n--------------------------------------------------------------------')
			#	logger.error ('TIMEOUT: something went wrong with the geocoding the address: [{}].'.format(addr))
			#	logger.error ('while using the service.')
			#	logger.error ('Passing to the next service.')
			#	logger.error ('--------------------------------------------------------------------')
			raise
		except (GeocoderServiceError,GeocoderUnavailable):
			#if self.SHOW_ERRORS:
			#	logger.error ('\n--------------------------------------------------------------------')
			#	logger.error ('ERROR: service unavailable or unknown error for the service.')
			#	logger.error ('--------------------------------------------------------------------')
			raise RuntimeError("Service unavailable or unknown error for the service.")
		except GeocoderNotFound:
			#if self.SHOW_ERRORS:
			#	logger.error ('\n--------------------------------------------------------------------')
			#	logger.error ('ERROR: unknown service.')
			#	logger.error ('check if this service still exists!')
			#	logger.error ('--------------------------------------------------------------------')
				raise RuntimeError("Check if the service still exists!")
		except Exception as e:				
			#logger.error ('\n--------------------------------------------------------------------')
			#logger.error("Unknown catastrophic error while processing address: {}".format(addr))
			#logger.error("Check the error and correct it before restart the application.")
			#logger.error(str(e))
			#logger.error('--------------------------------------------------------------------')
			raise

		
		return geocode_result
		
		

	def place(self, place_id = None):
		if not place_id:
			raise RuntimeError("No place id!")
		
		url = "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}".format(place_id, self.key)
		results = requests.get(url)

		results = results.json()
		
		output = self.initOutputPlace()

		status = results['status']
		
		if status != 'OK':
			if status == 'ZERO_RESULTS':
				raise RuntimeError("No Results!")
			elif status == 'OVER_QUERY_LIMIT':
				raise RuntimeError("You have exceded your quota!")
			elif status == 'REQUEST_DENIED':
				raise RuntimeError("Invalid key!")
			elif status == 'INVALID_REQUEST':
				raise RuntimeError("Check the place id!")
			elif status == 'NOT_FOUND':
				raise RuntimeError("No place with that id founded!")
			else:
				raise RuntimeError("Unknown Error!")
	
		if len(results['result']) > 0:  
			answer = results['result']
			output["status_place"] = results.get('status')
			output["formatted_address_place"] =  answer.get('formatted_address')
			output["vicinity"] = answer.get('vicinity')		# address (no cp, loc, country
			output["formatted_phone_number"] = answer.get('formatted_phone_number')
			if answer.get('plus_code'):
				output["plus_code"] = answer.get('plus_code').get('global_code')	# open location code
			if answer.get('geometry') and answer.get('geometry').get('location'):
				output["lat"] = answer.get('geometry').get('location').get('lat')
				output["lon"] = answer.get('geometry').get('location').get('lng')
			if answer.get('address_components'):
				output["postcode_place"] =  ",".join([x['long_name'] for x in answer.get('address_components') if 'postal_code' in x.get('types')])
				output["street_number"] = ",".join([x['long_name'] for x in answer.get('address_components') if 'street_number' in x.get('types')]) # house number
				output["route"] =  ",".join([x['long_name'] for x in answer.get('address_components') if 'route' in x.get('types')])	# street name
				output["locality"] =  ",".join([x['long_name'] for x in answer.get('address_components') if 'locality' in x.get('types')])	# loc / city
				output["city"] =  ",".join([x['long_name'] for x in answer.get('address_components') if 'administrative_area_level_1' in x.get('types')])	# city
				output["country"] =  ",".join([x['long_name'] for x in answer.get('address_components') if 'country' in x.get('types')])
			output["id"] = answer.get('id')
			output["international_phone_number"] =  answer.get('international_phone_number')
			output["name"] = answer.get('name')		# e canonicalized business name
			output["rating"] = answer.get('rating')
			output["types"] = answer.get('types')			# restaurant, ...	
			output["website"] = answer.get('website')
			output["url"] = answer.get('url')				# google place to this place
			output["permanently_closed"] = answer.get('permanently_closed')	# is this place permanently closed?
			if answer.get('opening_hours'):
				output["open_now"] = answer.get('opening_hours').get('open_now')
				# an array of opening periods covering seven days, starting from Sunday, in chronological order.
				output["periods"] = answer.get('opening_hours').get('periods')
				# array of seven strings representing the formatted opening hours for each day of the week - depends on the language param
				output["weekday_text"] = answer.get('opening_hours').get('weekday_text')
			
		return output



	def getGeoPlaceInfo(self, addr_name = None, local = None, country = 'Portugal'):
		geo_result = self.geocode(addr_name, local, country)
		place_result = self.place(geo_result['place_id'])
		return {**geo_result, **place_result}




