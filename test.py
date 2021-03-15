from flask import Flask, redirect, url_for, render_template, Response, make_response,json, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
import pprint as p
from utils import *

with open('User.json') as file:
    data= json.load(file)
    headings = list(list_of_keys_json(data))
    values = list_of_values_json(data)
    print(headings)
    print(values)
    