import os.path  
import osgeo.ogr
import numpy as np
import psycopg2 as psy
import pandas as pd

print('Creating database for temperature...')

database_create = 'createdb temperature -T template_postgis'
os.system(database_create )

connection = psy.connect('dbname = temperature host = localhost')  
cursor = connection.cursor()

data = pd.read_csv('./temperature.csv')

print('Creating table for temperature...')

sql_cmd = """CREATE TABLE IF NOT EXISTS temperature (P_key SERIAL PRIMARY KEY,
                                                      Pedon_key CHAR(8),
                                                      Lat REAL,
                                                      Long REAL,
                                                      Temp REAL,
                                                      Geom GEOMETRY);"""

cursor.execute(sql_cmd)

for i, row in data.iterrows():

    cursor.execute("""INSERT INTO temperature (Pedon_key, Lat, Long, Temp, Geom) VALUES 
                      (%s, %s, %s, %s, ST_GeomFromText('POINT(%s %s)', %s));""",
                   (row['pedon_key'], row['lat'], row['long'], row['temp'], row['long'], row['lat'], '4326')) 
    
print('Creating table for US states...')
    
sql_cmd = """CREATE TABLE IF NOT EXISTS us_states (gid INTEGER PRIMARY KEY,
                                                   Name VARCHAR(50),
                                                   Geom GEOMETRY);"""

cursor.execute(sql_cmd)

shapefile = osgeo.ogr.Open('./states/cb_2015_us_state_500k.shp')
layer = shapefile.GetLayer()

for i in range(layer.GetFeatureCount()):  
    feature = layer.GetFeature(i) 
    gid = feature.GetField("GEOID")
    name = feature.GetField("NAME")  
    wkt = feature.GetGeometryRef().ExportToWkt()  
    cursor.execute("""INSERT INTO us_states (gid, Name, Geom)
                      VALUES (%s, %s, ST_GeometryFromText(%s, 4326))""", (gid, name, wkt)) 
    
connection.commit()

cursor.close()
connection.close()

print('Finished!!')