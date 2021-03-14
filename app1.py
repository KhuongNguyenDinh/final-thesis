# https://docs.python.org/3/library/tkinter.html
import tkinter as tk
import os
from pymongo import MongoClient
from pprint import pprint 
from tkinter import * 
from utils import *
import json

client = MongoClient('localhost', 27017)
db = client.airlines
collection = db.airinfo

final =collection.find()
key_list = list_of_keys(collection.find({}))
final = merge_remove_dup(key_list)
datalst = []

for x in collection.find():
    for y in final[0]:
        datalst.append(x[y])


values_data = datalst


class Values: 
    def __init__(self,root): 
        # code for creating table 
        a = 1
        b = -1
        for i in range(0,50):
            if b == 10 : 
                a += 1 
                b = 0
            else :
                b+=1
            self.e = Entry(root, width=20, fg='black', 
                           font=('Arial',8,'bold')) 
            self.e.grid(row=a, column=b) 
            self.e.insert(END, values_data[i])


class Keys:
    def __init__(self,root): 
        # code for creating table 
        for i in range(key_rows): 
            for j in range(key_columns):     
                self.e = Entry(root, width=20, fg='red', 
                               font=('Arial',8,'bold')) 
                self.e.grid(row=i, column=j) 
                self.e.insert(END, key_data[i][j])    


key_data = final 
key_rows = len(key_data) 
key_columns = len(key_data[0]) 

   
root = Tk() 
k = Keys(root) 
v = Values(root)

root.mainloop() 