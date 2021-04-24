import numpy as np
import string
import fingerprints
from strsimpy import *

def flatten(lst):
    list_final = []
    for sublist in lst:
        if isinstance(sublist,list):
            for i in sublist:
                list_final.append(i)
        else:
            list_final.append(sublist)
    return list_final

class knn():
    def __init__(self, group, radius):
        self.group = group
        self.radius = radius

    def levenshtein(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius >= Levenshtein.distance(self,self.group[i].lower(),self.group[j].lower()):
                # if self.radius >= Damerau.distance(self,(self.group[i]).lower(),(self.group[j]).lower()):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster

#  1:  begin
#  2:     while (not last character) do
#  3:      begin
#  4:        readSymbol()
#  5:        shorten context
#  6:        while (context not found and context length not -1) do
#  7:         begin
#  8:           output(escape sequence)
#  9:           shorten context
# 10:         end
# 11:        output(character)
# 12:        while (context length not -1) do
# 13:         begin
# 14:           increase count of character (create node if nonexistant)
# 15:           shorten context
# 16:         end
# 17:      end
# 18:  end 
    def partial_match(self):
        return NotImplemented

class key_collision():
    def __init__(self, group):
        self.group = group
        
    def fingerprint(self):
        self.cluster = []
        for i in range(0, len(self.group)):
            for j in range(i+1, len(self.group)):
                if fingerprints.generate(self.group[i]) == fingerprints.generate(self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster

    def ngram_fingerprint(self):
        return NotImplemented
