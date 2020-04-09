
import geogoogle


print (geogoogle.__version__)
#print (geogoogle.__doc__)

try:
	geo = geogoogle.Geogoogle('xxxxxxxxxxxxxxxxxxxx')
		
	# geocode + place
	result = geo.getGeoPlaceInfo(addr_name = 'santa francecinha', local= 'porto', country = "Portugal") 
	print (result)
	
except Exception as e:
	print (str(e))


