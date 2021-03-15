import json
def flatten(lst):
    list_final = []
    for sublist in lst:
        if isinstance(sublist,list):
            for i in sublist:
                list_final.append(i)
        else:
            list_final.append(sublist)

    return list_final


def list_of_keys_mongoDB(collection):
# type: list of list
# parameter: collection
    key_lst = []
    for x in collection: 
        count = key_lst.count(list(x.keys()))
        if count == 0:
            key_lst.append(list(x.keys()))
        else:
            continue
    final = flatten(key_lst)
    return final

def list_of_keys_json(jsonfile):
# type: list of list
# parameter: collection
    key_lst = []
    for x in jsonfile: 
        count = key_lst.count(list(x.keys()))
        if count == 0:
            key_lst.append(list(x.keys()))
        else:
            continue
    final = flatten(key_lst)
    return final

def list_of_values_json(jsonfile):
    values = []
    for x in jsonfile:
        values.append(list(x.values()))
    return values

def merge_remove_dup(lst):
# type: list
# parameter: list of list
    final_lst = []
    i = 0
    for x in lst:
        while i < len(x):
            if final_lst.count(x[i]) == 0:
                final_lst.append(x[i])
            else:
                continue
            i += 1
    return [final_lst]