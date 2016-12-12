# Database Preparation

To use the database used for the app, first you need to install `Postgresql` and `PostGIS`.
To do this on a mac:

```bash
  brew install postgresql, postgis
```

After you have installed these two, please create a GIS database template:

```bash
  createdb template_postgis
  psql template_postgis
  >>> create extension postgis;
  >>> create extension postgis_topology;
```

Then you can actually populate the database with the csv and shapefiles in this folder:

```bash
  python database_populate.py
```
