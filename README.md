
Version: 0.0.1

# Description
* If sucesseful returns a json containing the geocoding and/or the place id info results, with **'status': 'OK'**. If not, returns json with **'status': 'UNABLE'**.
* If no services are available, then an _OutOfServices_ exception will be throwed
* In case of incorrect usage (e.g.: incorrect arguments) or some other catastrophic event, a _RuntimeError_ or a _Exception_ will be throwed


# Requirements
* Python 3.7.x
* geopy
* certifi

# Fields
* geocoding:
	* formatted_address
	* latitude
	* longitude
	* accuracy
	* place_id
	* type
	* postcode
	* input_string
	* number_of_results
	* status
	* response
	* localidade
	* distrito
	* concelho
	* freguesia	
	* service
* place:
	* status_place
	* formatted_address_place
	* vicinity
	* formatted_phone_number
	* plus_code
	* lat
	* lon
	* postcode_place
	* street_number
	* route
	* locality
	* city
	* country
	* id
	* international_phone_number
	* name
	* rating
	* types
	* website
	* url
	* permanently_closed
	* open_now
	* periods
	* weekday_text
		

# Example

```python
import geocode
	
try:
	geo = Geogoogle('xxxxxxxxxxxxx')

	# only geocode
	result = geo.geocode(addr = 'santa francecinha', local= 'porto', country = "Portugal", saveraw = True)
	
	# only place
	result = geo.place('asdFewf3DSfs34fsd34rSDFSDfs')

	# geocode + place
	result = geo.getGeoPlaceInfo(addr_name = 'santa francecinha', local= 'porto', country = "Portugal") 
					
except Exception as e:
	print (str(e))
```

# Notes: 
* Only uses **Google** services.
* Each step (geocoding, place) requires one API call.
* _getGeoPlaceInfo()_ -- 2 API calls
* _geocode()_ -- 1 API call
* _place()_ -- 1 API call
