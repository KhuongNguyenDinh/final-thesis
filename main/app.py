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
from strsimpy import *
from main.clustering import *
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Testing" 
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'csv', 'tsv', 'json'}
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER



##GLOBAL VARIABLES###
cluster_lst = []
cosmos_lst = []
method = ""
req_col = ""
req_rad = "0"
headings = []
values = []
group_list = []
#################


def csv2json(data):
	reader = csv.DictReader
	reader = csv.DictReader(data)
	out = json.dumps([ row for row in reader ])  
	print("JSON parsed!")  
	return out
	print("JSON saved!")

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

def method_using(name,column,radius):
    cluster = []
    if name == "levenshtein":
        obj = knn(column, radius)
        cluster = obj.levenshtein()
    elif name == "damerau":
        obj =  knn(column, radius)
        cluster = obj.damerau()
    elif name == "hamming":
        obj =  knn(column, radius)
        cluster = obj.hamming()   
    elif name == "jaro":
        obj =  similarity(column, radius)
        cluster = obj.jaro_sim()   
    elif name == "jaro_winkler":
        obj =  similarity(column, radius)
        cluster = obj.jaro_sim()   
    elif name == "levenshtein_sim":
        obj =  similarity(column, radius)
        cluster = obj.levenshtein_sim()   
    elif name == "damerau_sim":
        obj =  similarity(column, radius)
        cluster = obj.damerau_sim()
    elif name == "num_sim":    
        obj =  similarity(column, radius)
        cluster = obj.num_sim()    
    elif name == "fingerprint":
        cluster = fingerprint(column)    
    elif name == "n_gram":
        cluster = fingerprint_ngram(column,radius) 
    return cluster      

########### C R U D ###############
@app.route("/users",  methods=["POST"])
def create_user():
    try:
        user = {}
        dbResponse = collection.insert_one(user)
        return Response(
            response= json.dumps({"message":"Successfully created", "id":f"{dbResponse.inserted_id}"}),
            status = 200,
            mimetype = "application/json"
        )
    except Exception as ex:
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
        query = "SELECT * FROM c OFFSET 0 LIMIT " + str(request.form.get('number'))
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
        headings.clear()
        values.clear()
        group_list.clear()
        headings_cosmos = data.columns.tolist() # list of all headings
        headings.extend(headings_cosmos)
        values_cosmos = data.values.tolist() # list of all values
        values.extend(values_cosmos)
        group_list_data = [] # list of all unique values in group
        group_list.extend(group_list_data)
        for i in range(1,len(headings_cosmos)-1):
            group_list.append(data[headings_cosmos[i]].unique().tolist())
        return render_template('retrieve.html',data = data, headings = headings_cosmos, values = values_cosmos, group_list = group_list)
    return render_template('upload.html')


@app.route('/data', methods = ['POST','GET'])
def data():
    if request.method == "POST":
        f = request.form['file']
        with open(f,encoding='utf-8') as file:
            if f.endswith('.csv'): # if the open file is csv
                data = pd.read_csv(file) # load all data in to list "data"
            elif f.endswith('.json'): #else if the open file is json
                data = pd.read_json(file)
            elif f.endswith('.tsv'): #else if the open file is tsv
                data = pd.read_csv(file, sep = '\t') 
            elif f.endswith('.xlsx'): #else if the open file is xlsx
                data = pd.xlsx(file, sep='|', encoding='latin-1')
            headings.clear()
            values.clear()
            group_list.clear()
            headings_data = data.columns.tolist() # list of all headings
            headings.extend(headings_data)
            values_data = data.values.tolist() # list of all values
            values.extend(values_data)
            group_list_data = [] # list of all unique values in group
            group_list.extend(group_list_data)
            for i in range(0,len(headings_data)-1):
                group_list.append(data[headings_data[i]].unique().tolist())
        return render_template('data.html', data = data, headings = headings_data, values = values_data, group_list = group_list_data)

@app.route('/cluster', methods = ['GET' , 'POST'])
def cluster():
    head = []
    head.extend(headings)
    if request.method == "POST":
        method = request.form.get("methods")
        req_col = request.form.get("headings")
        req_rad = request.form["radius"]
        print(method)
        print(req_col)
        print(req_rad)
        column = []
        ele = []
        group_lst= []
        column.extend(headings)
        ele.extend(values)
        group_lst.extend(group_list)
        for i in range(0,len(column)):
            if column[i] == req_col:
                para2 = group_lst[i]
        if method is not "n_gram":
            cluster = method_using(method,para2,float(req_rad))
        else:
            cluster = method_using(method,para2,int(req_rad))
        return render_template('clustered.html', col = column, ele = ele, group_lst = group_lst, cluster = cluster)
    return render_template('cluster.html', head = head)

@app.route('/clustered', methods=["POST","GET"])
def clustered():
    return render_template("clustered.html")


@app.route('/csv2json', methods=["POST"])
def c2j():
	f = request.files['data_file']
	if not f:
		return "No file"
	file_contents = io.StringIO(f.stream.read().decode('utf-8'))
	result = csv2json(file_contents)
	response = make_response(result)
	response.headers["Content-Disposition"] = "attachment; filename=Converted.json"
	return response

@app.route('/convert', methods= ["POST", "GET"])
def convert():
	return render_template('convert.html')

@app.route('/project', methods = ['POST','GET'])
def project():
    return render_template("project.html")

# @app.errorhandler(Exception)
# def all_exception_handler(error):
#     return "Error: " + str(error.code)

mongo = PyMongo(app)
if __name__  == "__main__" :
    app.run(port = 5000)