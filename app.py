# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash
from flask import abort
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os
from ewaim import calculate
import csv
import errno
import json
import psycopg2 as psy

############################################################
############################################################
############################################################

## Init the app
#connection = psy.connect('dbname = tweets1k host = localhost')
#cursor = connection.cursor()

#def query_sql():
#    sql_cmd = "select ST_AsGeoJSON(geom) from ca_census_tract where name10 = 'Orange';"
#    cursor.execute(sql_cmd)
#    return cursor.fetchall()

#def county_topo():
#    sql_cmd = "SELECT name10, ST_AsGeoJSON(geom) from ca_census_tract;"
#    cursor.execute(sql_cmd)
#    return cursor.fetchall()

UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SECRET_KEY = "stars_and_moon"
DEBUG = True
app.config.from_object(__name__)

## Utility functions
def makePathExist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

makePathExist('static/db')

def get_csv():
    #csv_path = "./static/csv/la-riots-deaths.csv"
    csv_path = "./static/csv/carbon_sample_sm.csv"
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    return list(csv_obj)

def mean_lat_long(obj_csv):
    print("obj_csv: ", obj_csv)


############################################################
############################################################
############################################################

## Setup Middleware / routes to each web page

@app.route("/")
def index():
    obj_list = get_csv()
    ## obj_latlong = mean_lat_long(obj_list)
    init_zoom = 6
    data_name = "Carbon Samples"
    show_points = "true"
    show_states = "true"
    show_popup = "true"
    pearl_sp = "abbreviata_bancrofti"
    obj_show = {
        "pearl_sp" : pearl_sp,
        "data_name" : data_name,
        "init_zoom" : init_zoom,
        "show_points" : show_points,
        "show_states" : show_states,
        "show_popup" : show_popup,
    }
    #obj_sql = query_sql()
    #county_plus = county_topo()
    return render_template("index.html", obj_list = obj_list, obj_show = obj_show)

@app.route("/ex_raster", methods = ["GET", "POST"])
def ex_raster():
    return render_template("ex_tif_raster.html")

@app.route("/<pedon_key>/")
def point_page(pedon_key):
    obj_list = get_csv()
    for row in obj_list:
        if row['pedon_key'] == pedon_key:
            return render_template("point_page.html", obj_row = row)

    abort(404)

@app.route("/show_calc", methods = ["GET", "POST"])
def show_calc():
    return render_template("show_calc.html")

@app.route("/get_calc", methods = ["GET", "POST"])
def get_calc():

    if request.method == "POST":
        if ((request.form['query_string'] is None) or (len(request.form['query_string']) == 0)):
            flash("Bad query - could not interpret.")
            return redirect(request.url)

        if request.form['query_string']:

            try:
                simple_math = request.form['query_string']
                calc_result = calculate(simple_math)
                return render_template("show_calc.html", simple_math = simple_math, calc_result = calc_result)
            except:
                flash("Something went wrong...")
                return redirect(request.url)

    return render_template("get_calc.html")


######## Below route as reference (may use)

# Creeate route for fileupload html
@app.route("/file_upload", methods = ["GET", "POST"])
def file_upload():
    if request.method == "POST":
        if len(request.files) > 0:

            flash("Successfully uploaded BibTeX file")
            fileStruct = request.files['fileInput']

            # check if the post request has the file part
            if 'fileInput' not in request.files:
                flash('No file part')
                return redirect(request.url)

            # if user does not select file, browser also
            # submit a empty part without filename
            if fileStruct.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if fileStruct.filename:
                filename = secure_filename(fileStruct.filename)
                fileStruct.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                # Add Bib file to relative path
                absPathh = os.path.abspath(UPLOAD_FOLDER + filename)
                bibDB = bib_parse(absPathh)

                if "collectName" in request.form:
                    if (request.form["collectName"] == '') or (len(request.form["collectName"]) == 0):
                        collectName = "Default"
                    else:
                        collectName = request.form["collectName"]
                else:
                    collectName = "Default"

                # Create table and pass in collection name
                create_table(collectName, bibDB)

                return render_template("show_results.html", collectName = collectName, filenamee = filename, fileUpload = bibDB[0], fileSize = len(bibDB))

        else:
            # No file uploaded
            flash("Please select a file and try again.")
            return redirect(request.url)

    return render_template("file_upload.html")

# Creeate route for show_results html
@app.route("/show_results", methods = ["GET", "POST"])
def showresults():
    return render_template("show_results.html")

if __name__ == "__main__":
    app.run(port = 5555, debug = True, use_reloader = True)
