#! /usr/bin/env python

""" EWAIM source code: an extensible web app for interactive mapping"""

import argparse
from unittest import TestCase
import math
import csv

def check_args():
    parser = argparse.ArgumentParser(description = 'EWAIM: an extensible web app for interactive mapping')
    parser.add_argument('-sm', action = 'store', dest = 'simple_math',
                        help = 'Store a flag')
    parser.add_argument('-ff', action = 'store_true', default = False,
                        dest = 'fflag',
                        help = 'Store a flag')
    parser.add_argument('--version', action = 'version', version = '%(prog)s 1.0')

    results = parser.parse_args()
    return(results.simple_math. results.fflag)

def calculate(simple_math, f_flag = False):
    calc_return = eval(simple_math)
    return calc_return

def get_csv(csv_path = "./static/csv/carbon_sample_sm.csv"):
    #csv_path = "./static/csv/la-riots-deaths.csv"
    #csv_path = "./static/csv/carbon_sample_sm.csv"
    csv_file = open(csv_path, 'r')
    csv_obj = csv.DictReader(csv_file)
    return list(csv_obj)

def mean_lat_long(obj_csv):
    print("obj_csv: ", obj_csv)

    #return list(lat_mean)

if __name__ == '__main__':
    cli_args = check_args()
    #raw_result = calculate(cli_args[0], f_flag = cli_args[1])
    #print('\n-----------------')
    #print('The result is: ', raw_result)
    #print('-----------------\n')
    calculate(cli_args[0], f_flag = cli_args[1])
