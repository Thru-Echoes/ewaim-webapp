import bibtexparser
from bibtexparser.bparser import BibTexParser
from pprint import pprint
from functools import wraps
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import sqlite3
import bibtexparser.customization as cus
import re

class sql_utl:

    def __init__(self):
        self.db = None
        self.connection = None
        self.cursor = None

    def connect(self, database):
        """sql database connection"""
        self.db = database
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()

    def table_list(self):
        """show table list of current database"""
        sql_cmd = "select * from sqlite_master where type = 'table';"
        self.cursor.execute(sql_cmd)
        db_info = self.cursor.fetchall()
        for entry in db_info:
            print(entry)

    def drop(self, table):
        """drop selected table from database"""
        sql_cmd = "drop table %s" % (table)
        self.cursor.execute(sql_cmd)

    def close (self):
        """commit changes to the database and close the connection"""
        self.connection.commit()
        self.connection.close()

def callonce(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not wrapper.called:
            wrapper.called = True
            return f(*args, **kwargs)
    wrapper.called = False
    return wrapper

@callonce
def get_ADS_jrnls():

    '''
    Define a function that pulls full ADS journal names and maps them to their macros. Returns pandas DF.
    '''

    global macro

    response = urlopen('http://adsabs.harvard.edu/abs_doc/aas_macros.html')
    html = response.read()
    response.close

    soup = BeautifulSoup(html, 'html5lib')
    macro_string = str(soup.find('pre').find_all('b'))

    ADS_lines = macro_string.split('\n')[3:-1]

    macros = []
    j_names = []

    for line in ADS_lines:
        macros.append(line.split()[0])
        j_names.append(' '.join(line.split()[1:]))

    macro = pd.DataFrame({'macro':pd.Series(macros), 'j_name':pd.Series(j_names)})

def custom_callback(record):

    get_ADS_jrnls()

    # Convert to unicode
    record = cus.convert_to_unicode(record)

    # Convert jounal macro to real name
    if 'journal' in record and '\\' in record['journal']:
        record["journal"] = macro['j_name'][macro['macro'] == record["journal"].strip('\\')].values[0]

    # Convert author strings
    if 'author' in record:

        rep = {"{": "", "}": "", "~": " "}
        rep = dict((re.escape(k), v) for k, v in rep.items())
        pattern = re.compile("|".join(rep.keys()))
        record['author'] = pattern.sub(lambda m: rep[re.escape(m.group(0))], record['author'])

    return record

def bib_parse(path):

    with open(path) as bibtex_file:
        parser = BibTexParser()
        parser.customization = custom_callback
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        input_data = bib_database.entries
    return input_data

def connection(f):

    global sql
    sql = sql_utl()

    @wraps(f)
    def wrapper(*args, **kwargs):
        sql.connect('static/db/sample.db')
        result = f(*args, **kwargs)
        sql.close()
        return result

    return wrapper

@connection
def create_table(collection, input_data):

    sql.cursor.execute("""CREATE TABLE IF NOT EXISTS bib_data (tag text, authors text, editors text, journal text, book text,
                          volume int, pages int, title text, year int, collection text)""")

    for i in input_data:

        tag = i['ID'] if 'ID' in i else None

        author = i['author'] if 'author' in i else None

        editor = i['editor'] if 'editor' in i else None

        journal = i['journal'] if 'journal' in i else None

        book = i['booktitle'] if 'booktitle' in i else None

        volume = i['volume'] if 'volume' in i else None

        pages = i['pages'] if 'pages' in i else None

        title = i['title'] if 'title' in i else None

        year = i['year'] if 'year' in i else None

        sql.cursor.execute("""INSERT INTO bib_data (tag, authors, editors, journal, book, volume, pages,
                              title, year, collection) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                              (tag, author, editor, journal, book, volume, pages, title, year, collection,))

@connection
def query(input_query):
    sql.cursor.execute('SELECT * FROM bib_data WHERE %s' % (input_query))
    result = sql.cursor.fetchall()
    return result

@connection
def table_check():
    sql.cursor.execute("SELECT * FROM sqlite_master WHERE name ='bib_data' and type='table';")
    return sql.cursor.fetchall()

#parsed_data = bib_parse('../../../sample_data/sample_refs.bib')
#create_table('test_table', input_data)
#query('test_table', 'title like "%parallax%" and authors like "%Hawley%"')
