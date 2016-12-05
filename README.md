<img src="https://travis-ci.org/Thru-Echoes/ewaim-webapp.svg?branch=master">


# EWAIM: an Extensible Web App for Interactive Mapping

The **leaf-tut** branch follows the *Leaflet x Flask (Python) x Javascript* tutorial of building a web app to interface with the LA riot deaths.

This tutorial can be [found here.](https://first-news-app.readthedocs.io/en/latest/)

And an [example app here.](http://ireapps.github.io/first-news-app/build/index.html)

## 1 EWAIMAPP

#### 1.1 Setup

```
    $ python3 setup.py install
```

#### 1.2 Test

```
    $ python3 setup.py test
```

### Components

A web app built with:

*Backend* - **flask framework** connects to spatial SQL database

*Frontend* - **Leaflet mapping framework** with data analysis + metadata + extra visualizations - use of **D3js** etc

*Data Analysis* - **Kernel Density Estimations (KDE)**, **Gaussian Mixture Model (GMM)**, etc

### Data Analysis

##### KDE

A non-parameteric density estimator

##### GMM

A parametric probability density function represented as a weighted sum of Gaussian component densities

##### More

##### Database note

Commands for using the database I uploaded:

```bash
  createdb tweets template template_postgis
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
