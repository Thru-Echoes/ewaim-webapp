# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash
from flask import abort
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os
from ewaim import calculate
from ewaim import get_csv
from ewaim import mean_lat_long
import csv
import errno
import json
import psycopg2 as psy
from static.py.db_util import *

############################################################
############################################################
############################################################

## Init the app

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

############################################################
############################################################
############################################################

## Setup Middleware / routes to each web page

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        print("\n------")
        print("POST request in index")
        print("------\n")

        if request.form['optionsRadios']:
            try:
                req_raw = request.form['optionsRadios']
                if req_raw == "option-pearl":
                    return render_template("pick_pearl_sp.html")

                elif req_raw == "option-temp":
                    obj_list = get_csv()

                    st_cali = get_state(state = "California")
                    st_arzn = get_state(state = "Arizona")
                    st_nvda = get_state(state = "Nevada")

                    init_lat = 36.23418283
                    init_long = -116.8341902
                    init_zoom = 6
                    data_name = "Temperature Samples"
                    show_points = "true"
                    show_states = "true"
                    show_popup = "true"
                    obj_show = {
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long,
                        "show_points" : show_points,
                        "show_states" : show_states,
                        "show_popup" : show_popup,
                    }
                    return render_template("temp_map.html", obj_list = obj_list, obj_show = obj_show, st_cali = st_cali)

                elif req_raw == "option-abba":
                    init_zoom = 3
                    init_lat = 11.252725743861603
                    init_long = -0.005242086131886481
                    data_name = "Global Parasite Distributions"
                    pearl_sp = "abbreviata_bancrofti"
                    prop_name = "Abbreviata bancrofti"
                    sub_name = ""
                    obj_show = {
                        "pearl_sp" : pearl_sp,
                        "prop_name" : prop_name,
                        "sub_name" : sub_name,
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long
                    }
                    ## Pull in PEARL metadata
                    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
                    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/ABBREVIATA_BANCROFTI.csv")
                    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)

                elif req_raw == "option-aslo":
                    init_zoom = 3
                    init_lat = 11.252725743861603
                    init_long = -0.005242086131886481
                    data_name = "Global Parasite Distributions"
                    pearl_sp = "ascocotyle_longa"
                    prop_name = "Ascocotyle longa"
                    sub_name = ""
                    obj_show = {
                        "pearl_sp" : pearl_sp,
                        "prop_name" : prop_name,
                        "sub_name" : sub_name,
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long
                    }
                    ## Pull in PEARL metadata
                    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
                    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/ASCOCOTYLE_LONGA.csv")
                    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)

                elif req_raw == "option-ctca":
                    init_zoom = 3
                    init_lat = 11.252725743861603
                    init_long = -0.005242086131886481
                    data_name = "Global Parasite Distributions"
                    pearl_sp = "ctenocephalides_canis"
                    prop_name = "Ctenocephalides canis"
                    sub_name = "Common dog flea"
                    obj_show = {
                        "pearl_sp" : pearl_sp,
                        "prop_name" : prop_name,
                        "sub_name" : sub_name,
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long
                    }
                    ## Pull in PEARL metadata
                    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
                    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/CTENOCEPHALIDES_CANIS.csv")
                    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)

                elif req_raw == "option-zylu":
                    init_zoom = 3
                    init_lat = 11.252725743861603
                    init_long = -0.005242086131886481
                    data_name = "Global Parasite Distributions"
                    pearl_sp = "zygocotyle_lunata"
                    prop_name = "Zygocotyle lunata"
                    sub_name = ""
                    obj_show = {
                        "pearl_sp" : pearl_sp,
                        "prop_name" : prop_name,
                        "sub_name" : sub_name,
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long
                    }
                    ## Pull in PEARL metadata
                    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
                    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/ZYGOCOTYLE_LUNATA.csv")
                    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)

                else:
                    flash("Something went wrong with finding that data...")
                    return redirect(request.url)
            except:
                flash("Bad query - could not interpret.")
                return redirect(request.url)

    return render_template("index.html")

@app.route("/temp_map", methods = ["GET", "POST"])
def temp_map():
    if request.method == "POST":
        print("\n------")
        print("POST request in temp_map")
        print("------\n")

    obj_list = get_csv()

    st_cali = get_state(state = "California")
    st_arzn = get_state(state = "Arizona")
    st_nvda = get_state(state = "Nevada")

    init_lat = 36.23418283
    init_long = -116.8341902
    init_zoom = 6
    data_name = "Temperature Samples"
    show_points = "true"
    show_states = "true"
    show_popup = "true"
    obj_show = {
        "data_name" : data_name,
        "init_zoom" : init_zoom,
        "init_lat" : init_lat,
        "init_long" : init_long,
        "show_points" : show_points,
        "show_states" : show_states,
        "show_popup" : show_popup,
    }
    return render_template("temp_map.html", obj_list = obj_list, obj_show = obj_show, st_cali = st_cali)

@app.route("/pick_pearl_sp", methods = ["GET", "POST"])
def pick_pearl_sp():
    if request.method == "POST":
        print("\n------")
        print("POST request in pick_pearl_sp")
        #print("request.form['query_string']: ", request.form['query_string'])
        print("------\n")

        if request.form['query_string']:
            try:
                req_raw = request.form['query_string']
                if req_raw == "abba":
                    print("It is abba time...")
                    init_zoom = 3
                    init_lat = 11.252725743861603
                    init_long = -0.005242086131886481
                    data_name = "Global Parasite Distributions"
                    pearl_sp = "abbreviata_bancrofti"
                    prop_name = "Abbreviata bancrofti"
                    obj_show = {
                        "pearl_sp" : pearl_sp,
                        "prop_name" : prop_name,
                        "data_name" : data_name,
                        "init_zoom" : init_zoom,
                        "init_lat" : init_lat,
                        "init_long" : init_long
                    }
                    ## Pull in PEARL metadata
                    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
                    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/ABBREVIATA_BANCROFTI.csv")
                    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)


                else:
                    flash("Something went wrong with finding that species...")
                    return redirect(request.url)

            except:
                flash("Bad query - could not interpret.")
                return redirect(request.url)

@app.route("/pearl_map", methods = ["GET", "POST"])
def pearl_map():

    if request.method == "POST":
        print("\n------")
        print("POST request in pearl_map")
        print("------\n")

    init_zoom = 3
    init_lat = 11.252725743861603
    init_long = -0.005242086131886481
    data_name = "Global Parasite Distributions"
    pearl_sp = "abbreviata_bancrofti"
    prop_name = "Abbreviata bancrofti"
    obj_show = {
        "pearl_sp" : pearl_sp,
        "prop_name" : prop_name,
        "data_name" : data_name,
        "init_zoom" : init_zoom,
        "init_lat" : init_lat,
        "init_long" : init_long
    }
    ## Pull in PEARL metadata
    obj_meta = get_csv(csv_path = "./static/csv/pearl_data_summary.csv")
    obj_sp = get_csv(csv_path = "./static/csv/pearl_sp/ABBREVIATA_BANCROFTI.csv")
    return render_template("pearl_map.html", obj_show = obj_show, obj_meta = obj_meta, obj_sp = obj_sp)

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

@app.route("/ex_raster", methods = ["GET", "POST"])
def ex_raster():
    return render_template("ex_tif_raster.html")

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
def show_results():
    return render_template("show_results.html")

if __name__ == "__main__":
    app.run(port = 5555, debug = True, use_reloader = True)
