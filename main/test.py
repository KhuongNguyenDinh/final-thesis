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
from bson import ObjectId
import fingerprints
import datetime

def flatten(lst):
    list_final = []
    for sublist in lst:
        if isinstance(sublist,list):
            for i in sublist:
                list_final.append(i)
        else:
            list_final.append(sublist)
    return list_final
begin_time = datetime.datetime.now()
with open('airlines_final.csv') as f:
    data = pd.read_csv(f) # load all data in to list "data"
    shape = data.shape
    describe = data.describe()
    idx = data.index
    headings = data.columns.tolist() # list of all headings
    values = data.values.tolist() # list of all values 
    group_list = []
    for i in range(0,len(headings)-1):
        group_list.append(data[headings[i]].unique().tolist())
    print(group_list[5])
    # lev_obj = knn(group_list[5], 3)
    # print(lev_obj.levenshtein())
    print(datetime.datetime.now() - begin_time)
    # dame_obj = knn(group_list[5], 3)
    # print(dame_obj.damerau())
    a = Fingerprinter("æ")
    print(a.get_fingerprint())
    finger_obj = fingerprint("æ")
    print(finger_obj)
    # jaro = similarity(group_list[5], 1)
    # jaro_obj = jaro.jaro()
    # print(jaro_obj)
    

#### TO SELECT SPECIFIC COLUMN ####
    # spec = data[data[headings[2]] == "Friday"]
    # subset = [headings[2],headings[3],headings[4]]
    # multi = data[subset]
    # print(spec)


    # a = knn(group_list[5],int(input("radius: ")))
    # print(levenshtein("ly thuong kiet","Lý Thường Kiệt"))
    # print(group_list[5])
    # print(a.levenshtein())
    # print(b.fingerprint())
    # print(data['dest_size'].value_counts())
    # del a
# f = Fingerprinter('ly thuong kiet')
# f1 = Fingerprinter('Lý Thường Kiệt')
# f3 = fingerprints.generate("duong 3 tháng 2")
# f4 = fingerprints.generate("3 thang 2")
# f5 = fingerprints.generate("ba thang hai")
# text = "Vị trí nhà cách 20m ra mặt ngõ lớn 279 Đội Cấn, đường ô tô tránh, cả ngõ có 5-6 nhà. Tương lai mở rộng ngõ 279 nhà cách ngõ vài mét ( sau này ngõ 279 thành phố Đại Yên) giá trị nhà tăng chóng mặt. Diện tích 38m2, xây 05 tầng, mặt tiền rộng 4,1m, nhà còn rất mới, phù hợp cho việc vừa ở vừa kinh doanh, hoặc cho thuê văn phòng.Nhà chủ nhà tự xây, khung BTCT chắc chắn, thiết kế hiện đại+Tầng 1: 1 Phòng rộng + bếp + vs.+ Tầng 2: P khách + 1 ngủ + vs.+ Tầng 3+4: Mỗi tầng 2 ngủ + vs.+ Tầng 5: P. Thờ + sân phơi.Sổ đỏ chính chủ, pháp lý rõ ràng, sẵn sang giao dịchGiá: 4.7 tỷ có thương lượng cho khách có thiện trí.Liên Hệ: Thanh Tùng: 0912142902. Quý khách gọi ngay để được tư vấn nhiệt tình và xem nhà miễn phí. Nhà mới, ở ngay, ngõ nông, kinh doanh, cho thuê của hàng, văn phòng, Đội Cấn, Ba Đình "
# f6 = fingerprints.generate(text.encode("utf-8","strict"))
# print(f.get_fingerprint())
# print(f1.get_fingerprint())
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

# with open('airlines_final.json',encoding="utf8") as f:
#     data = pd.read_json(f) # load all data in to list "data"
#     # pd.DataFrame.from_dict(data["detail"])
#     # values= pd.json_normalize(data['detail'])
#     # headings = data.columns.tolist()
#     # df = pd.json_normalize(data, 'detail', ['homepage','address'] , record_prefix='detail_')
#     # a = pd.json_normalize(data)
#     # a = data['detail'].T
#     html = data.to_html()
#     text_file = open("test.html", "w")
#     text_file.write(html)
#     text_file.close()   
    # group = []
    # for i in range(1,len(headings)-1):
    #     group.append(data[headings[i]].unique().tolist())
    # for x in data['detail']:
    #     print(data['detail'].columns.tolist())
    # print(data["detail"].from_dict())
# arr = ["east Us", "EAST US", "east us", "Midwest US", "WEST US"]

# lst = []
# rad = int(input("Radius:"))
# a = Levenshtein()
# for x in range(0,len(arr)):
#     for y in range(x,len(arr)):
#         if rad == a.distance(arr[x].lower(),arr[y].lower()):
#             lst.append(arr[y])
# print(lst)