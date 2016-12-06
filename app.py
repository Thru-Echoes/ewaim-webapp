# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash
from flask import abort
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os
from static.py.bibUtil import *
from ewaim import calculate
import csv
import errno
import json

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

def get_csv():
    csv_path = "./static/csv/la-riots-deaths.csv"
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    return list(csv_obj)

sample_data = [{
  "name": "bootstrap-table",
  "commits": "10",
  "attention": "122",
  "uneven": "An extended Bootstrap table"
},
 {
  "name": "multiple-select",
  "commits": "288",
  "attention": "20",
  "uneven": "A jQuery plugin"
}, {
  "name": "Testing",
  "commits": "340",
  "attention": "20",
  "uneven": "For test"
}]


############################################################
############################################################
############################################################

## Setup Middleware / routes to each web page

@app.route("/")
def index():
    obj_list = get_csv()
    return render_template("index.html", obj_list = obj_list, sample_data = sample_data)

@app.route("/<row_id>/")
def detail(row_id):
    obj_list = get_csv()
    for row in obj_list:
        if row['id'] == row_id:
            return render_template("detail.html", obj_row = row)

    abort(404)

@app.route("/showcalc", methods = ["GET", "POST"])
def showcalc():
    return render_template("showcalc.html")

@app.route("/calc", methods = ["GET", "POST"])
def calc():

    if request.method == "POST":
        if ((request.form['query_string'] is None) or (len(request.form['query_string']) == 0)):
            flash("Bad query - could not interpret.")
            return redirect(request.url)

        if request.form['query_string']:

            try:
                simple_math = request.form['query_string']
                calc_result = calculate(simple_math)
                return render_template("showcalc.html", simple_math = simple_math, calc_result = calc_result)
            except:
                flash("Something went wrong...")
                return redirect(request.url)

    return render_template("calc.html")


######## Below route as reference (may use)

# Creeate route for fileupload html
@app.route("/fileupload", methods = ["GET", "POST"])
def fileupload():
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

                return render_template("showresults.html", collectName = collectName, filenamee = filename, fileUpload = bibDB[0], fileSize = len(bibDB))

        else:
            # No file uploaded
            flash("Please select a file and try again.")
            return redirect(request.url)

    return render_template("fileupload.html")

# Creeate route for showresults html
@app.route("/showresults", methods = ["GET", "POST"])
def showresults():
    return render_template("showresults.html")

if __name__ == "__main__":
    app.run(port = 8888, debug = True, use_reloader = True)
