import pyorient
import sys

client = pyorient.OrientDB("localhost", 2424)
session_id = client.connect("root", "188019")
db_name = "soufun"
db_username = "admin"
db_password = "admin"

if client.db_exists( db_name, pyorient.STORAGE_TYPE_MEMORY ):
	client.db_open( db_name, db_username, db_password )
	print db_name + " opened successfully"
else:
	print "database [" + db_name + "] does not exist! session ending..."
	sys.exit()

lat1 = 22.532498
lat2 = 22.552317

lng1 = 114.044329
lng2 = 114.076644

query = 'SELECT FROM Listing WHERE latitude BETWEEN {} AND {} AND longitude BETWEEN {} AND {}'

records = client.command(query.format(lat1, lat2, lng1, lng2))

numListings = len(records)

print 'received ' + str(numListings) + ' records'

client.db_close()

output = {"type":"FeatureCollection","features":[]}

for record in records:
    feature = {"type":"Feature","properties":{},"geometry":{"type":"Point"}}
    feature["id"] = record._rid
    feature["properties"]["name"] = record.title
    feature["properties"]["price"] = record.price
    feature["geometry"]["coordinates"] = [record.latitude, record.longitude]

    output["features"].append(feature)
    
return json.dumps(output)
