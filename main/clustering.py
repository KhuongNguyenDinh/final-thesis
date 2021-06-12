import numpy as np
import string
import re, string
from unidecode import unidecode
from strsimpy import *
import fingerprints

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

class knn(object):
    def __init__(self, group, radius):
        self.group = group
        self.radius = radius

    def levenshtein(self):
        self.cluster = []
        for i in range(0,len(self.group)):
            for j in range(i+1, len(self.group)):
                if self.radius >= Levenshtein.distance(self,self.group[i].lower(),self.group[j].lower()):
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
                sorted([self.string[i:i + n] for i in range(len(self.string) - n + 1)])
            )
        ))

if __name__ == '__main__':
    group = ['West US', 'East US', 'Midwest US', 'EAST US', 'Middle East', 'Europe', 'eur', 'middle east']
    a = knn(group,0)
    print(a.levenshtein())

