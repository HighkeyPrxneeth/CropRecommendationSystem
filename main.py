import pgeocode

nomi = pgeocode.Nominatim('us')
zipcode = input("Enter the zipcode: ")
lat, long = nomi.query_postal_code(zipcode)[['latitude', 'longitude']]
