# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug import secure_filename
from flask_bootstrap import Bootstrap
import os
from static.py.bibUtil import *

import errno

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

## Init the app

UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
SECRET_KEY = "stars_and_moon"
DEBUG = True
app.config.from_object(__name__)

############################################################
############################################################
############################################################

## Setup Middleware / routes to each web page

@app.route("/")
def index():
    return render_template("index.html")

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

# Creeate route for getquery html
@app.route("/getquery", methods = ["GET", "POST"])
def getquery():

    dataExist = True if table_check() else False

    if request.method == "POST":

        if ((request.form['queryString'] is None) or (len(request.form['queryString']) == 0)):
            flash("Bad query - could not interpret.")
            return redirect(request.url)

        if request.form['queryString']:
            qString = request.form['queryString']

            try:
                tmpReturn = query(qString)
                qReturn = []

                counter = 1
                for i in tmpReturn:
                    tmpDict = {
                        "Tag" : i[0],
                        "Authors" : i[1],
                        "Editors" : i[2],
                        "Journal" : i[3],
                        "Book" : i[4],
                        "Volume" : i[5],
                        "Pages" : i[6],
                        "Title" : i[7],
                        "Year" : i[8],
                        "Collection" : i[9],
                        "Counter" : counter
                    }
                    qReturn.append(tmpDict)
                    counter += 1

                return render_template("showquery.html", queryReturn = qReturn)
            except:
                flash("Exception raised. Please try again.")
                return redirect(request.url)

    return render_template("getquery.html", dataExist = dataExist)

# Creeate route for showresults html
@app.route("/showresults", methods = ["GET", "POST"])
def showresults():
    return render_template("showresults.html")

# Creeate route for showresults html
@app.route("/showquery", methods = ["GET", "POST"])
def showquery():
    return render_template("showquery.html")

## Note: this script is doing the equivalent of a NodeJS project
# files 'app.js' and all render middlewares in 'routes/'

# Create new pages with Middleware augment via
# '@app.route("/FOOBAR") ... def FOOBAR(): ... '

if __name__ == "__main__":
    app.run(port = 8888)
