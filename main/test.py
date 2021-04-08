from flask import Flask, redirect, url_for, render_template, Response, make_response,json, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
import pprint as p
from clustering import *
import pandas as pd
from facet import *
from bson import ObjectId
import fingerprint
with open('airlines_final.csv') as f:
    data = pd.read_csv(f) # load all data in to list "data"
    headings = data.columns.tolist() # list of all headings
    values = data.values.tolist() # list of all values 
    group_list = []
    for i in range(0,len(headings)-1):
        group_list.append(data[headings[i]].unique().tolist())
    a = knn(3,group_list[5])
    print(a.levenshtein())
    print(a.partial_match())
    print(1)



    
