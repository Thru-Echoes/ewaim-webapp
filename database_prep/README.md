# Database Preparation

To use the database, first you need to install `Postgresql` and `PostGIS`.

To do this on a mac:

```bash
  brew install postgresql postgis
  brew services start postgresql
```
After you have installed these two, please create a GIS database template:

```bash
  createdb template_postgis
  psql template_postgis
  >>> create extension postgis;
  >>> create extension postgis_topology;
  >>> \q
```

Then you need to install python packages `gdal` and `psycopg2`. But the installation of python `gdal` is painful, see notes below.

Then you can actually populate the database with the csv and shapefiles in this folder:

```bash
  python database_populate.py
```

After the database is populated properly, the `db_util.py`, which has some simple GIS function from `PostGIS` can be done,
and called by the server.

# Note!!!!!!!
Still, the installation of `gdal` can be painful. If you don't want to do that, I have dumped a database file here, `temperature.gz`.

To use it, you will need to do this:

```bash
  createdb temperature -T template_postgis
  gunzip -c temperature.gz | psql temperature
```
The python package `psycopg2` and the `PostGIS` template are still needed.
