__author__ = 'nguyen dinh khuong'
from flask import Flask, redirect, url_for, render_template, Response, make_response,json, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
from utils import *
import numpy as np
import pandas as pd

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Testing" 

#### test connection
try:
    mongo = pymongo.MongoClient(host = "localhost", 
    port = 27017, 
    serverSelectionTimeoutMS = 1000)
    db = mongo.Testing
    collection = db.User
except:
    print("ERROR - Unable to connect to Database")

########### C R U D ###############
@app.route("/users",  methods=["POST"])
def create_user():
    try:
        user = {"name" : "viet", "age" : "20"}
        dbResponse = collection.insert_one(user)
        return Response(
            response= json.dumps({"message":"Successfully created", "id":f"{dbResponse.inserted_id}"}),
            status = 200,
            mimetype = "application/json"
        )
    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"Can not insert", "id":f"{dbResponse.inserted_id}"}),
            status = 200,
            mimetype="application/json"
        )


@app.route("/users", methods=["GET"])
def get_users():
    try:
        data = list(collection.find())
        for x in data:
            x["_id"] = str(x["_id"])
        return Response(
            response= json.dumps(data),
            status = 500,
            mimetype="application/json"
        )

    except Exception as ex:
        print(ex)
        return Response(
            response= json.dumps({"message":"Can not read", "id":f"{dbResponse.inserted_id}"}),
            status = 500,
            mimetype="application/json"
        )
##################################################

#### upload file####
@app.route('/upload', methods = ['GET' , 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/data', methods = ['GET' , 'POST'])
def data():
    if request.method == 'POST':
        f = request.form['csvfile']
        with open(f) as file:
            data = [] # load all data in to list "data"
            if f.endswith('.csv'): # if the open file is csv
                csvfile = csv.reader(file)
                edit = csv.writer(file)
                for row in csvfile:
                    data.append(row)
                headings = data[0] # list of all headings
                values = [] # list of all values 
                for i in range(1,len(data)):
                    values.append(data[i])
                return render_template('data.html', data = data, headings = headings, values = values)
            elif f.endswith('.json'): #else if the open file is json
                data = json.load(file)
                headings = list_of_keys_json(data)
                values = list_of_values_json(data)
                return render_template('data.html', data = data, headings = headings, values = values)

@app.route("/")
def home_page():
    return render_template("index.html")

mongo = PyMongo(app)

if __name__  == "__main__":
    app.run(port = 5000, debug = True)