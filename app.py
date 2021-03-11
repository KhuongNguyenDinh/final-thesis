# https://docs.python.org/3/library/tkinter.html
import tkinter as tk
import os
# import mysql.connector
from pymongo import MongoClient
from pprint import pprint 
from tkinter import * 

my_w = tk.Tk()
my_w.geometry("400x250") 

client = MongoClient('localhost', 27017)
db = client.Testing
users = db.User.find({})

#check whether the key is already in the list
key_lst = []
for x in users:
    count = key_lst.count(list(x.keys()))
    if count == 0:
        key_lst.append(list(x.keys()))
    else:
        continue

for x in key_lst:
    pprint(x)

i=0 
for student in key_lst: 
    for j in range(len(student)):
        e = Entry(my_w, width=10, fg='blue') 
        e.grid(row=i, column=j) 
        e.insert(END, student[j])
    i=i+1

my_w.mainloop()