from flask import Flask, redirect, url_for, render_template, Response, make_response,json, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
from pathlib import Path
import pymongo, io, csv, os, json, hashlib
import pprint as p
from clustering import *
import pandas as pd
import numpy as np
from facet import *
from bson import ObjectId
import fingerprints
def flatten(lst):
    list_final = []
    for sublist in lst:
        if isinstance(sublist,list):
            for i in sublist:
                list_final.append(i)
        else:
            list_final.append(sublist)
    return list_final
with open('airlines_final.csv') as f:
    data = pd.read_csv(f) # load all data in to list "data"
    headings = data.columns.tolist() # list of all headings
    values = data.values.tolist() # list of all values 
    group_list = []
    for i in range(0,len(headings)-1):
        group_list.append(data[headings[i]].unique().tolist())
    # a = knn(group_list[5],int(input("radius: ")))
    b = key_collision(group_list[5])
#     # print(levenshtein_distance("ly thuong kiet","Lý Thường Kiệt"))
#     # print(group_list[5])
    # print(a.levenshtein())
    print(b.fingerprint())
    # del a
# f = fingerprints.generate("coöperatieve vennootschap met onbeperkte aansprakelijkheid")
# f2 = fingerprints.generate("Công ty trách nhiệm hữu hạn")
# f3 = fingerprints.generate("duong 3 tháng 2")
# f4 = fingerprints.generate("3 thang 2")
# f5 = fingerprints.generate("ba thang hai")
# f6 = fingerprints.generate("chu Van an")
# print(f)
# print(f2)
# print(f3)
# print(f4)
# print(f5)
# print(f6)
# # print(a.partial_match())
# del f
# del f2
# del f3
# del f4
# del f5
# del f6

# with open('sample.json',encoding="utf8") as f:
#     data = json.load(f) # load all data in to list "data"
#     # headings = data.columns.tolist()
#     values= pd.json_normalize(data['detail'])
#     # group = []
#     # for i in range(1,len(headings)-1):
#     #     group.append(data[headings[i]].unique().tolist())
#     for x in data['detail']:
#         print(data['detail'][x])

# arr = ["east Us", "EAST US", "east us", "Midwest US", "WEST US"]

# lst = []
# rad = int(input("Radius:"))
# a = Levenshtein()
# for x in range(0,len(arr)):
#     for y in range(x,len(arr)):
#         if rad == a.distance(arr[x].lower(),arr[y].lower()):
#             lst.append(arr[y])
# print(lst)