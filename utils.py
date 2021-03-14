def list_of_keys(collection):
# type: list of list
# parameter: collection
    key_lst = []
    for x in collection: 
        count = key_lst.count(list(x.keys()))
        if count == 0:
            key_lst.append(list(x.keys()))
        else:
            continue
    return key_lst

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