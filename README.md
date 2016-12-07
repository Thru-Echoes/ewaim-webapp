<img src="https://travis-ci.org/Thru-Echoes/ewaim-webapp.svg?branch=master">

# EWAIM: an Extensible Web App for Interactive Mapping

The **leaf-tut** branch follows the *Leaflet x Flask (Python) x Javascript* tutorial of building a web app to interface with the LA riot deaths.

This tutorial can be [found here.](https://first-news-app.readthedocs.io/en/latest/)

And an [example app here.](http://ireapps.github.io/first-news-app/build/index.html)

## 0 To Do

#### 0.0 References

- [ ] Check out Google Earth Engine
- [ ] Check out CartoDB

#### 0.1 Oliver

- [X] Make nav_layout.html for web app skeleton
- [ ] Create Flask layout for maps
- [ ] Create Flask layout for data analysis results etc
- [ ] Pick data based on user event (local CSV Carbon vs CSV Twitter)  
- [ ] Make front page to select data (have world map background)
- [ ] From selected data, render Carbon map
- [ ] Make clickable / selectable heatmap layer - users can select different variables / layers for mapping
- [ ] ... heatmap will be directly on map (all frontend), make it able to accept backend data   

**Next stages...**

- [ ] Make data table CSV downloadable
- [ ] Allow users to upload their own data  

#### 0.2 Miao

- [ ] Assume frontend passes back 'use postgres' - make db connections
- [ ] Use Geo-Alch
- [ ] Create GIS utility functions
- [ ] Create shapefile utility functions
- [ ] Create raster utility functions

<hr>

## 1 EWAIMAPP

#### 1.1 Setup

```
    $ python3 setup.py install
```

#### 1.2 Test

```
    $ python3 setup.py test
```

#### 1.3 Usage Outline

1. On home page, select 1 of 2 databases to connect to
    * either **Tweets (geom points)** or **PEARL (polygons)**
2. After 1, home page will show a breakdown + title etc of the db
3. AddLayers to maps via checkboxes as **county, states, countries, or NA** in Javscript (*Leaflet*)
4. ...

## 2 Web App Components

A web app built with:

*Backend* - **flask framework** connects to spatial SQL database

*Frontend* - **Leaflet mapping framework** with data analysis + metadata + extra visualizations - use of **D3js** etc

*Data Analysis* - **Kernel Density Estimations (KDE)**, **Gaussian Mixture Model (GMM)**, etc

## 3 Data Analysis

##### KDE

A non-parameteric density estimator

##### GMM

A parametric probability density function represented as a weighted sum of Gaussian component densities

##### More

Coming soon...

## 4 Database Note

Commands for using the database I uploaded:

```bash
  createdb tweets -T template_postgis
  gunzip -c tweets_db.gz | psql tweets
```

If you don't have `postgis` template, please do this first:

```bash
  createdb template_postgis
  psql template_postgis
  >>> create extension postgis;
  >>> create extension postgis_topology;
```

To install `postgresql` and `postgis`:

OSX:
```bash
  brew install postgresql postgis
```


*Coming soon...*
