from flask import Flask, redirect, url_for, render_template, Response, make_response,json, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
import pprint as p
from utils import *
import pandas as pd

df = pd.read_csv(
    'ride_sharing_new.csv',
)
print(df.groupby(["station_A_name","station_B_name"]).first())