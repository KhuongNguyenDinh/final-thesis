__author__ = 'nguyen dinh khuong'
from flask import Flask, redirect, url_for, render_template, Response, make_response, json, request, send_from_directory, jsonify
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
from io import StringIO
from main.utils import *
from markupsafe import escape
import numpy as np
import pandas as pd
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Testing" 
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'csv', 'tsv', 'json'}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

cosmos_lst = []
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
############### test connection ############
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
        user = {"name" : "khuong", "age" : "22"}
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
### HOMEPAGE ###
@app.route("/")
def home_page():
    return render_template("index.html")

#### upload file####
@app.route('/upload', methods = ['GET' , 'POST'])
def upload():
    if request.method == "POST":
        endpoint = request.form.get("endpoint")
        key = request.form.get("key")
        client = CosmosClient(endpoint, key)
        database_name = request.form.get("DB_name")
        database = client.create_database_if_not_exists(id=database_name)
        container_name = request.form.get("Container_name")
        container = database.create_container_if_not_exists(
        id=container_name, 
        partition_key=PartitionKey(path=request.form.get("Partition_key")),
        offer_throughput=400
        )
        query = "SELECT * FROM c OFFSET 0 LIMIT 5"
        items = list(container.query_items(
        query=query,
        enable_cross_partition_query=True
        ))
        for i in range(0,len(items)):
            cosmos_lst.append(items[i])
        cosmos_json = json.dumps(cosmos_lst, ensure_ascii=False, sort_keys=False, indent=4)
        jsonfile = open("jsontemp.json", "w" ,encoding="utf-8")
        jsonfile.truncate(0)
        jsonfile.write(cosmos_json)
        data = pd.read_json("jsontemp.json")
        headings = data.columns.tolist() # list of all headings
        values = data.values.tolist() # list of all values
        group_list = []
        for i in range(1,len(headings)-1):
            group_list.append(data[headings[i]].unique().tolist())
        return render_template('retrieve.html',data = data, headings = headings, values = values, group_list = group_list)
    return render_template('upload.html')


@app.route('/cluster', methods = ['GET' , 'POST'])
def cluster():
    return render_template('cluster.html', lst = cosmos_lst)


@app.route('/data', methods = ['POST','GET'])
def data():
    if request.method == 'POST':
        f = request.form['file']
        with open(f,encoding = "utf8") as file:
            if f.endswith('.csv'): # if the open file is csv
                data = pd.read_csv(file) # load all data in to list "data"
                headings = data.columns.tolist() # list of all headings
                values = data.values.tolist() # list of all values
                group_list = [] # list of all unique values in group
                for i in range(0,len(headings)-1):
                    group_list.append(data[headings[i]].unique().tolist())
            elif f.endswith('.json'): #else if the open file is json
                data = pd.read_json(file)
                headings = data.columns.tolist() # list of all headings
                values = data.values.tolist() # list of all values
                group_list = []
                for i in range(1,len(headings)-1):
                    group_list.append(data[headings[i]].unique().tolist())
            return render_template('data.html', data = data, headings = headings, values = values, group_list = group_list)    

@app.route('/convert', methods = ['GET' , 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
            return redirect(url_for('uploaded_file', filename=filename))
    return render_template('convert.html')


def process_file(path, filename):
    convert(path, filename)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")

def convert(path, filename):
    input_file = open(path,'rb')
    f = request.form['file']
    with open(f,encoding = "utf8") as file:
        if f.endswith('.csv'):
            df = pd.read_csv(file)
            output = df.to_json()
        return output
            
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


mongo = PyMongo(app)
if __name__  == "__main__":
    app.run(port = 5000)