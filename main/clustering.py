import numpy as np
import string
import re, string
from strsimpy import *
import jellyfish as jf
import fingerprints 

# JARO WINKLER:
# The Jaro-Winkler functions compare two strings and return a score indicating
# how closely the strings match. The score ranges from 0 (no match) to 1
# (perfect match).

# Two null strings ('') will compare as equal. Strings should be unicode
# strings, and will be compared as given; the caller is responsible for
# capitalisations and trimming leading/trailing spaces.

# You should normally only need to use either the jaro_metric() or
# jaro_winkler_metric() functions defined here. If you want to implement your
# own, non-standard metrics, look at the comments and functions in the jaro.py
# submodule.
PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

def flatten(lst):
    list_final = []
    for sublist in lst:
        if isinstance(sublist,list):
            for i in sublist:
                list_final.append(i)
        else:
            list_final.append(sublist)
    return list_final

class similarity(object):
    def __init__(self,group,threshold):
        self.group = group
        self.threshold = threshold
    
    def jaro_sim(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.threshold <= jf.jaro_similarity(self.group[i],self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster
            
    def jaro_winkler_sim(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.threshold <= jf.jaro_winkler_similarity(self.group[i],self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster
    
    def levenshtein_sim(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius <= (1 - jf.levenshtein_distance(self.group[i],self.group[j]) / max(len(self.group[i]),len(self.group[j]))):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster

    def damerau_sim(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius <= (1 - jf.damerau_levenshtein_distance(self.group[i],self.group[j]) / max(len(self.group[i]),len(self.group[j]))):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster

class knn(object):
    def __init__(self,group,radius):
        self.group = group
        self.radius = radius

    def levenshtein(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius >= jf.levenshtein_distance(self.group[i],self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster
 
# Where levenshtein_distance('fish', 'ifsh') == 2 as it would require a deletion and an insertion
# though damerau_levenshtein_distance('fish', 'ifsh') == 1 as this counts as a transposition.
   
    def damerau(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius >= jf.damerau_levenshtein_distance(self.group[i],self.group[j]):
                    self.cluster.append([self.group[i],self.group[j]])
        return self.cluster     

# Hamming distance is the measure of the number of characters that differ between two strings.
# Typically Hamming distance is undefined when strings are of different length, 
# but this implementation considers extra characters as differing. For example hamming_distance('abc', 'abcd') == 1.
    def hamming(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius >= jf.hamming_distance(self.group[i],self.group[j]):
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



class Fingerprinter(object):
    def __init__(self, string):
        self.string = self._preprocess(string)

    def _preprocess(self, string):
        return PUNCTUATION.sub('', string.strip().lower())

    def _latinize(self, string):
        return unidecode(string.encode().decode('utf-8'))

    def _unique_preserving_order(self, seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]

    def get_fingerprint(self):
        return fingerprints.generate(self.string)

    def get_ngram_fingerprint(self, n=1):
        return self._latinize(''.join(
            self._unique_preserving_order(
                sorted([self.string[i:i + n] for i in range(len(self.string) - n + 1)]))
        ))
    
def fingerprint(group):
    cluster = []
    for i in range(0,len(group)):
        lhs = Fingerprinter(group[i])
        for j in range(i+1, len(group)):
            rhs = Fingerprinter(group[j])
            if lhs.get_fingerprint() == rhs.get_fingerprint():
                cluster.append([lhs.get_fingerprint(),rhs.get_fingerprint()])
    return cluster

def fingerprint_ngram(group):
    cluster = []
    for i in range(0,len(group)):
        lhs = Fingerprinter(group[i])
        for j in range(i+1, len(group)):
            rhs = Fingerprinter(group[j])
            if lhs.get_ngram_fingerprint() == rhs.get_ngram_fingerprint():
                cluster.append([lhs.get_ngram_fingerprint(),rhs.get_ngram_fingerprint()])
    return cluster

